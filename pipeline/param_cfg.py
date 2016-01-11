## param_cfg.py
import os
version_cfg = {
    "REF_VERSION": "hg19",
    "BWA_VERSION": "0.7.12"
}

ref_file_cfg = {
    "hg19": {
        "fa": "/ref/ucsc.hg19.fasta.gz"
    }
}

file_cfg = {
    "std_log": lambda args: "log/{}.std.txt".format(args.samplename),
    "run_log": lambda args: "log/{}.run.txt".format(args.samplename),
    "err_log": lambda args: "log/{}.err.txt".format(args.samplename),
    "cache": lambda args: "tmp/cache_dict.pkl",
    "aligned": lambda args: "tmp/{}.aln.sam".format(args.samplename),
    "sorted": lambda args: "tmp/{}.sort.bam".format(args.samplename)
}

bwa_mem_cfg = {
    "-R": r"'@RG\tID:group1\tSM:sample1\tLB:lib1\tPL:illumina\tPU:unit1'",
    "-M": ""
}
