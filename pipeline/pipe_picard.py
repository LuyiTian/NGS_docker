## pipe_picard.py
import os
from param_cfg import *
from util import run_task, join_params
_version = version_cfg["PICARD_VERSION"]


@run_task("picard sort sam")
def picard_sort(args, param_dict=None):
    """
    doc
    """
    cmd = DOCKER_RUN + \
        """ picard:{_v} \
    SortSam {param} I={aligned} O={sort} TMP_DIR=/out_dir SORT_ORDER=coordinate"""
    cmd = cmd.format(
        _ref_v=version_cfg["REF_VERSION"],
        _out_d=args.out_dir,
        _v=_version,
        aligned=file_cfg["aligned"](args),
        sort=file_cfg["sorted"](args),
        param=join_params(param_dict))

    return cmd, os.path.join(args.out_dir, file_cfg["sorted"](args))


@run_task("picard mark duplicate")
def picard_dedup(args, param_dict=None):
    """
    doc
    """
    cmd = DOCKER_RUN + \
        """ picard:{_v} \
    MarkDuplicates {param} I={sort} O={dedup} METRICS_FILE={matrics} CREATE_INDEX=true"""
    cmd = cmd.format(
        _v=_version,
        _ref_v=version_cfg["REF_VERSION"],
        _out_d=args.out_dir,
        sort=file_cfg["sorted"](args),
        param=join_params(param_dict),
        dedup=file_cfg["dedup"](args),
        matrics=file_cfg["matrics"](args))
    return cmd, [file_cfg["dedup"](args), file_cfg["matrics"](args)]
