## util.py
import datetime
import functools
import os
import sys
import cPickle as pkl
import subprocess
from param_cfg import *
__TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
__RUN_LOG_FORMAT = \
    """
Task: {_n}
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


def init_datadir(args):
    """
    doc
    """
    prep_dir(args.rootdir, args.samplename)
    prep_dir(os.path.join(args.rootdir, args.samplename), "tmp")
    prep_dir(os.path.join(args.rootdir, args.samplename), "log")
    prep_dir(os.path.join(args.rootdir, args.samplename), "report")

    with open(file_cfg["run_log"](args), 'w') as f:
        f.write("#Pipeline Started\n")
        f.write("#Root dir: {}\n".format(args.rootdir))
        f.write("#Sample Name: {}\n".format(args.samplename))
    with open(file_cfg["std_log"](args), 'w') as f:
        f.write("#Root dir: {}\n".format(args.rootdir))
        f.write("#Sample Name: {}\n".format(args.samplename))
    with open(file_cfg["err_log"](args), 'w') as f:
        f.write("#Root dir: {}\n".format(args.rootdir))
        f.write("#Sample Name: {}\n".format(args.samplename))
    cache_dict = {"_samplename": args.samplename}
    pkl.dump(cache_dict, open(file_cfg["cache"](args), 'wb'))


def _check_exists(cmd, cache_dict):
    """
    """
    if cmd not in cache_dict:
        return False
    if isinstance(cache_dict[cmd], list):
        # if out_file is a list
        for f in cache_dict[cmd]:
            if not os.path.isfile(f):
                return False
    else:
        # if out_file is a string
        if not os.path.isfile(cache_dict[cmd]):
            return False
    return True


def _del_files(out_f):
    """
    """
    if isinstance(out_f, list):
        # if out_f is a list
        for f in out_f:
            os.remove(f)
    else:
        # if out_f is a string
        os.remove(f)


def run_task(task_name):
    """
    a decorator to run command, add time tag and run info to output logs
    """
    def actualDecorator(func):
        @functools.wraps(func)
        def wrapper(args, **kwargs):
            ## start logging
            run_log = open(file_cfg["run_log"](args), 'a')
            ## load cache_dict
            cache_dict = pkl.load(open(file_cfg["cache"](args), 'b'))

            start_time = datetime.datetime.now().strftime(__TIME_FORMAT)
            cmd, out_f = func(args, **kwargs)
            ## check if output file already exist
            if out_f and args.usecache:
                if _check_exists(cmd, out_f, cache_dict):
                    status = "Exists, skip this task"
                    run_log.write(__RUN_LOG_FORMAT.format(
                        _n=task_name, _st=start_time, _et=start_time, _o=out_f, _s=status))
                    run_log.close()
                    return cmd, out_f, status
            ## run command
            p = subprocess.Popen(
                cmd, shell=True, stdout=open(file_cfg["std_log"](args), 'a'), stderr=open(file_cfg["err_log"](args), 'a'))
            returncode = p.wait()
            end_time = datetime.datetime.now().strftime(__TIME_FORMAT)
            ## check return code
            if returncode == 0:
                run_log.write(__RUN_LOG_FORMAT.format(
                    _n=task_name, _st=start_time, _et=end_time, _o=out_f, _s="Success"))
                cache_dict[cmd] = out_f
                pkl.dump(cache_dict, open(file_cfg["cache"](args), 'wb'))
            else:
                run_log.write(__RUN_LOG_FORMAT.format(
                    _n=task_name, _st=start_time, _et=end_time, _o=out_f, _s="Failed"))
                print "{} fails with return code ({})\nsee:{}\nfor more info".format(
                    task_name, returncode, file_cfg["err_log"](args))
                _del_files(out_f)
                sys.exit(returncode)
            run_log.close()
            return cmd, out_f, status
        return wrapper

    return actualDecorator