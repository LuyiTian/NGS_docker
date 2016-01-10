## param_cfg.py
import os
version_cfg = {
    "REF_VERSION": "hg19",
    "BWA_VERSION": "0.7.12"
}

ref_file_cfg = {
    "hg19": {
        "fa": "ucsc.hg19.fasta.gz"
    }
}

file_cfg = {
    "std_log": lambda args: os.path.join(args.rootdir, args.samplename, "/log/{}.std.txt".format(args.samplename)),
    "run_log": lambda args: os.path.join(args.rootdir, args.samplename, "/log/{}.run.txt".format(args.samplename)),
    "err_log": lambda args: os.path.join(args.rootdir, args.samplename, "/log/{}.err.txt".format(args.samplename)),
    "cache": lambda args: os.path.join(args.rootdir, args.samplename, "/tmp/cache_dict.pkl"),
    "aligned": lambda args: os.path.join(args.rootdir, args.samplename, "/tmp/{}.aln.sam".format(args.samplename)),
    "sorted": lambda args: os.path.join(args.rootdir, args.samplename, "/tmp/{}.sort.bam".format(args.samplename))
}
