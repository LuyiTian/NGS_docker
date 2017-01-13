# pipe_issac3.py
import os
from param_cfg import *
from util import run_task, join_params
_version = version_cfg["ISSAC3_VERSION"]


@run_task("build issac3 index")
def issac3_index(args, param_dict=None):
    """
    """
    cmd1 = \
        """ mkdir -p {_issac_index_dir} """.format(
            _issac_index_dir=os.path.join(args.refdir, "issac3_index"))
    cmd2 = \
        """docker run --rm \
        -v {_out_d}:/out_dir \
        -v {_ref_dir}:/ref \
        -w /out_dir \
        isaac3:{_v} isaac-sort-reference \
        {param} \
        -g {_ref_fa} \
        -j {_p} \
        -o /out_dir """.format(
        _p=args.p,
        _ref_dir=args.refdir,
        _ref_fa=ref_file_cfg[version_cfg["REF_VERSION"]]["fa"],
        _out_d=os.path.join(args.refdir, "issac3_index"),
        param=join_params(param_dict),
        _v=_version)

    return " && ".join([cmd1, cmd2]), None


@run_task("issac3 alignment")
def issac3_align(args, param_dict=None):
    """
    """
    fq_dir = os.path.dirname(args.R1)  # assume R1 and R2 in the same dir
    if args.R2 is None:
        cmd1 = \
            """ ln -sf {_R1} {_dest}""".format(
                _R1=args.R1,
                _dest=os.path.join(fq_dir, "lane1_read1.fastq.gz"))
    else:
        cmd1 = \
            """ ln -sf {_R1} {_dest} && ln -sf {_R2} {_dest2}""".format(
                _R1=args.R1,
                _dest=os.path.join(fq_dir, "lane1_read1.fastq.gz"),
                _R2=args.R2,
                _dest2=os.path.join(fq_dir, "lane1_read2.fastq.gz"))
    cmd2 = \
        """docker run --rm \
        -v {_out_d}:/out_dir \
        -v {_ref_index}:/ref \
        -v {_datadir}:/datadir \
        -w /out_dir \
        isaac3:{_v} isaac-align \
        -b /datadir \
        -m 40 \
        --base-calls-format fastq-gz \
        {param} \
        -r /ref \
        --enable-numa \
        -j {_p} \
        -o /out_dir """.format(
        _p=args.p,
        _datadir=fq_dir,
        _ref_index=os.path.join(args.refdir, "issac3_index"),
        _out_d=args.out_dir,
        param=join_params(param_dict),
        _v=_version)

    return " && ".join([cmd1, cmd2]), None
