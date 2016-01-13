##
#
import argparse
import os
from pipeline import pipe_bwa, pipe_picard, pipe_GATK
from pipeline import util
from prog_cfg import bwa_mem_cfg, gatk_bqsr_cfg
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
        "--buildindex",
        help="whether to build bwa index before the pipeline (default %(default)s)",
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
        help="read 1 files for paired-ended reads, separated by space, if single-ended reads just use R1",
        nargs='+',
        type=str,
        required=True
        )
    parser.add_argument(
        "-R2",
        help="read 2 for paired-ended reads, if single-ended reads ignore this arg",
        nargs='+',
        type=str,
        default=""
        )
    args = parser.parse_args()
    return args


def main(args):
    args.out_dir = os.path.join(args.rootdir, args.samplename)
    print args
    util.init_datadir(args)
    if args.buildindex:
        print pipe_bwa.bwa_index(args)
    #print pipe_bwa.bwa_mem(args, bwa_mem_cfg)
    #print pipe_picard.picard_sort(args)
    #print pipe_picard.picard_dedup(args)
    print pipe_GATK.gatk_bqsr(args)
    print pipe_GATK.gatk_printread(args)

if __name__ == '__main__':
    args = get_args()
    main(args)
