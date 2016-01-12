## pipe_picard.py
import os
from param_cfg import *
from util import run_task


@run_task("picard sort sam")
def picard_sort(args):
    """
    doc
    """
    cmd = \
        """docker run \
    --rm \
    -v {_out_d}:/out_dir \
    -w /out_dir \
    picard:2.0.1 \
    SortSam I={aligned} O={sort} TMP_DIR=/out_dir""".format(
        aligned=file_cfg["aligned"](args),
        sort=file_cfg["sorted"](args),
        _out_d=args.out_dir)

    return cmd, os.path.join(args.out_dir, file_cfg["sorted"](args))


@run_task("picard mark duplicate")
def picard_dedup(args):
    """
    doc
    """
    cmd = \
        """docker run \
    --rm \
    -v {_out_d}:/out_dir \
    -w /out_dir \
    picard:2.0.1 \
    MarkDuplicates I={sort} O={dedup} METRICS_FILE={matrics}\
    CREATE_INDEX=true""".format(
        sort=file_cfg["sorted"](args),
        _out_d=args.out_dir,
        dedup=file_cfg["dedup"](args),
        matrics=file_cfg["matrics"](args))
    return cmd, [file_cfg["dedup"](args), file_cfg["matrics"](args)]
