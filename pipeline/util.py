## util.py
import datetime
import functools
import os
import sys
import cPickle as pkl
import subprocess
from collections import OrderedDict
from param_cfg import *
__TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
__RUN_LOG_FORMAT = \
    """
Task: {_n}
    Command: {_cmd}
    Start Time: {_st}
    Output: {_o}
    End Time: {_et}
    Status: {_s}
"""


def prep_dir(result_dir, sub_dir):
    """
    create sub folder, also create root folder if it does not exist
    """
    if not os.path.isdir(result_dir):
        os.mkdir(result_dir)
    sub_path = os.path.join(result_dir, sub_dir)
    if not os.path.isdir(sub_path):
        os.mkdir(sub_path)
    return sub_path


def join_params(cfg_dict):
    res = []
    for key, val in cfg_dict.items():
        res.append(key)
        res.append(val)
    return " ".join(res)


def init_datadir(args):
    """
    doc
    """
    out_dir = prep_dir(args.rootdir, args.samplename)
    prep_dir(out_dir, "tmp")
    prep_dir(out_dir, "log")
    prep_dir(out_dir, "report")
    if os.path.isfile(os.path.join(out_dir, file_cfg["run_log"](args))):
        mode = "w"
        cache_dict = OrderedDict()
        cache_dict["_samplename"] = args.samplename
        pkl.dump(cache_dict, open(os.path.join(out_dir, file_cfg["cache"](args)), 'wb'))
    else:
        mode = "a"
    with open(os.path.join(out_dir, file_cfg["run_log"](args)), mode) as f:
        f.write("#Pipeline Started at: {}\n".format(datetime.datetime.now().strftime(__TIME_FORMAT)))
        f.write("#Args:\n")
        f.write("".join(["#  {}\n    {}\n".format(k, v) for k, v in vars(args).iteritems()]))
    with open(os.path.join(out_dir, file_cfg["std_log"](args)), mode) as f:
        f.write("#Pipeline Started at: {}\n".format(datetime.datetime.now().strftime(__TIME_FORMAT)))
        f.write("#Root dir: {}\n".format(args.rootdir))
        f.write("#Sample Name: {}\n".format(args.samplename))
    with open(os.path.join(out_dir, file_cfg["err_log"](args)), mode) as f:
        f.write("#Pipeline Started at: {}\n".format(datetime.datetime.now().strftime(__TIME_FORMAT)))
        f.write("#Root dir: {}\n".format(args.rootdir))
        f.write("#Sample Name: {}\n".format(args.samplename))


def _check_exists(cmd, cache_dict):
    """
    """
    if cmd not in cache_dict:
        return False
    if not cache_dict[cmd]:
        return False
    if isinstance(cache_dict[cmd], list):
        # if out_file is a list
        for f in cache_dict[cmd]:
            if not os.path.isfile(os.path.join(args.out_dir, f)):
                return False
    else:
        # if out_file is a string
        if not os.path.isfile(os.path.join(args.out_dir, cache_dict[cmd])):
            return False
    return True


def _del_files(out_f):
    """
    clean up if task fails
    """
    if not out_f:
        return
    if isinstance(out_f, list):
        # if out_f is a list
        for f in out_f:
            if os.path.isfile(os.path.join(args.out_dir, f)):
                os.remove(os.path.join(args.out_dir, f))
    else:
        # if out_f is a string
        if os.path.isfile(os.path.join(args.out_dir, out_f)):
            os.remove(os.path.join(args.out_dir, out_f))


def run_task(task_name):
    """
    a decorator to run command, add time tag and run info to output logs
    """
    def actualDecorator(func):
        @functools.wraps(func)
        def wrapper(args, **kwargs):
            ## start logging
            run_log = open(os.path.join(args.out_dir, file_cfg["run_log"](args)), 'a')
            ## load cache_dict
            cache_dict = pkl.load(open(os.path.join(args.out_dir, file_cfg["cache"](args)), 'rb'))

            start_time = datetime.datetime.now().strftime(__TIME_FORMAT)
            cmd, out_f = func(args, **kwargs)
            print cmd
            ## check if output file already exist
            if args.usecache and out_f and _check_exists(args, cmd, cache_dict):
                status = "Exists, skip this task"
                end_time = datetime.datetime.now().strftime(__TIME_FORMAT)
                returncode = 0
            else:
                ## if not exists run command
                p = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=open(os.path.join(args.out_dir, file_cfg["std_log"](args)), 'a'),
                    stderr=open(os.path.join(args.out_dir, file_cfg["err_log"](args)), 'a'))
                returncode = p.wait()
                end_time = datetime.datetime.now().strftime(__TIME_FORMAT)
                ## check return code
                if returncode == 0:
                    status = "Success"
                    ## save successful result to cache
                    cache_dict[cmd] = out_f
                    pkl.dump(
                        cache_dict,
                        open(os.path.join(args.out_dir, file_cfg["cache"](args)), 'wb'))
                else:
                    status = "Failed"
                    print "{} fails with return code ({})\nsee:{}\nfor more info".format(
                        task_name,
                        returncode,
                        os.path.join(args.out_dir, file_cfg["err_log"](args)))
                    ## delete out_f if task fails
                    _del_files(out_f)
            ## write to run log, if task fails, exit with return code
            run_log.write(__RUN_LOG_FORMAT.format(
                _n=task_name,
                _st=start_time,
                _et=end_time,
                _o=out_f,
                _s=status,
                _cmd=cmd))
            run_log.close()
            if returncode != 0:
                sys.exit(returncode)
            return cmd, out_f, status
        return wrapper

    return actualDecorator