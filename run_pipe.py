##
#
import argparse
from pipeline import pipe_bwa
import param_cfg
__PROG = "NGS_docker"
__AUTHOR = "Luyi Tian"
__VERSION = "0.1"
__MAN = \
    """
################################################################
# Program: {}
# Version {}
# Authors: {}
#
# NGS_docker is a dockerized NGS pipeline for variant calling
# This program includes GATK, which is only
# free for academic and non-profit use
# for details see:
# https://www.broadinstitute.org/gatk/about/#licensing
################################################################"""\
.format(__PROG, __VERSION, __AUTHOR)


def get_args():
    parser = argparse.ArgumentParser(
        prog=__PROG,
        description=__MAN,
        version=__VERSION,
        epilog="to change parameters used in ",
        formatter_class=argparse.RawDescriptionHelpFormatter
        )
    parser.add_argument(
        "-p",
        help="the number of precessors used (default %(default)s)",
        type=int,
        default=4
        )
    parser.add_argument(
        "--samplename", "-n",
        help="unique samplename, will be used as a prefix for all files",
        type=str,
        required=True
        )
    parser.add_argument(
        "--rootdir", "-o",
        help="a subdir /samplename will be created to deposite all results",
        type=str,
        required=True
        )
    parser.add_argument(
        "--buildindex",
        help="whether to build bwa index before the pipeline",
        type=bool,
        default=True
        )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    pipe_bwa.bwa_index("ucsc.hg19.fasta.gz", param_cfg.version_cfg)
