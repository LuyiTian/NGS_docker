## bwa.py
import os
from param_cfg import *
from util import run_task, join_params, abs_path


@run_task("build bwa index")
def bwa_index(args):
    """
    """
    _ref_version = version_cfg["REF_VERSION"]
    _bwa_version = version_cfg["BWA_VERSION"]
    _in_fa = ref_file_cfg[_ref_version]["fa"]
    cmd1 = \
        """docker create \
    -v /ref \
    --name {_ref_v} reference:{_ref_v}""".format(_ref_v=_ref_version)

    cmd2 = \
        """docker run \
    --rm \
    --volumes-from {_ref_v} \
    -w /ref \
    bwa:{_bwa_v} \
    bwa index {in_f} """.format(
        in_f=_in_fa,
        _ref_v=_ref_version,
        _bwa_v=_bwa_version)

    return " && ".join([cmd1, cmd2]), None


def bwa_mem(args):
    """
    """
    def parse_in(args):
        """
        to deal with following issues:
            - there may be multiple fastq files
            - fastq files may be gzipped
            - fastq file may not locate in the `--rootdir`
        """
        data_dir, _ = os.path.split(abs_path(args.R1[0]))
        in_f = []
        if len(args.R1) == 1:
            in_f.append(os.path.split(abs_path(args.R1[0]))[1])
        else:
            if args.R1[0].split('.')[-1] == "gz":
                in_f.append("'<zcat {}'".format(" ".join([os.path.split(it)[1] for it in args.R1])))
            else:
                in_f.append("'<cat {}'".format(" ".join([os.path.split(it)[1] for it in args.R1])))
        if args.R2 is not None:
            if len(args.R2) == 1:
                in_f.append(os.path.split(abs_path(args.R1[0]))[1])
            else:
                if args.R1[0].split('.')[-1] == "gz":
                    in_f.append("'<zcat {}'".format(" ".join([os.path.split(it)[1] for it in args.R2])))
                else:
                    in_f.append("'<cat {}'".format(" ".join([os.path.split(it)[1] for it in args.R2])))
        return data_dir, " ".join(in_f)

    data_dir, in_fq = parse_in(args)
    _ref_version = version_cfg["REF_VERSION"]
    _bwa_version = version_cfg["BWA_VERSION"]
    _in_fa = ref_file_cfg[_ref_version]["fa"]
    _out_sam = "> /out_dir/{}".format(os.path.join("/out_dir", file_cfg["aligned"](args)))

    bwa_cmd = " ".join(
        ["bwa mem -p {_p}".format(_p=args.p), join_params(bwa_mem_cfg), _in_fa, in_fq, _out_sam])
    cmd = \
        r"""docker run \
    --rm \
    --volumes-from {_ref_v} \
    -v {_out_d}:/out_dir \
    -v {_data_d}:/data\
    -w /data \
    bwa:{_bwa_v} bash -c "{_bwa_c}" """.format(
        _ref_v=_ref_version,
        _bwa_v=_bwa_version,
        _out_d=args.out_dir,
        _data_d=data_dir,
        _bwa_c=bwa_cmd)
    return cmd, os.path.join(args.out_dir, file_cfg["aligned"](args))
