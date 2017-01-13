## run_illumina_wgs_pipe.py
#
import argparse
import os
from pipeline import pipe_issac3
from pipeline import util
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
# This program includes Issac3, Strelka and Manta. They are developed
# by Illumina (https://github.com/Illumina)
# NOTE: they will use A LOT memorys so make sure you have enough available RAM
################################################################"""\
.format(__PROG, __VERSION, __AUTHOR)


def get_args():
    parser = argparse.ArgumentParser(
        prog=__PROG,
        description=__MAN,
        version=__VERSION,
        epilog="NOTE: all input fastq file should locate in the same dir",
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
        help="unique samplename, will be used as the prefix for all files",
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
        "--refdir", "-r",
        help="the folder that contains all reference data. if --buildindex=True then the issac3 index will be built in this folder under ./issac3_index",
        type=str,
        required=True
        )
    parser.add_argument(
        "--buildindex",
        help="whether to build issac3 index before the pipeline (default %(default)s)",
        action='store_true',
        default=False
        )
    parser.add_argument(
        "--usecache",
        help="whether to use cache to skip finished tasks (default %(default)s)",
        action='store_true',
        default=False
        )
    parser.add_argument(
        "-R1",
        help="read 1 files for paired-ended reads if single-ended reads just use R1",
        type=str,
        required=True
        )
    parser.add_argument(
        "-R2",
        help="read 2 for paired-ended reads, if single-ended reads ignore this arg",
        type=str,
        default=None
        )
    parser.add_argument(
        "-aux",
        help="additional argument that passed to the program (e.g. -aux '-w 5')",
        type=str,
        default=None
        )
    args = parser.parse_args()
    return args


def main(args):
    args.out_dir = os.path.join(args.rootdir, args.samplename)
    print args
    util.init_datadir(args)
    if args.buildindex:
        print pipe_issac3.issac3_index(args, param_dict=args.aux)
    print pipe_issac3.issac3_align(args, param_dict=args.aux)

if __name__ == '__main__':
    args = get_args()
    main(args)
