##
#
import argparse
from pipeline import pipe_bwa
import subprocess
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
        help="will be created to deposite all results in rootdir, use absolute path",
        type=str,
        required=True
        )
    parser.add_argument(
        "--buildindex",
        help="whether to build bwa index before the pipeline (default %(default)s)",
        type=bool,
        default=True
        )
    parser.add_argument(
        "--usecache",
        help="whether to use cache to skip finished tasks (default %(default)s)",
        type=bool,
        default=True
        )
    args = parser.parse_args()
    return args

def main(args):
    cmd, _ = pipe_bwa.bwa_index(args)


if __name__ == '__main__':
    args = get_args()
    main(args)
