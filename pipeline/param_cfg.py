## param_cfg.py

version_cfg = {
    "REF_VERSION": "GRCh37",
    "BWA_VERSION": "0.7.12",
    "PICARD_VERSION": "2.0.1",
    "GATK_VERSION": "3.5",
    "ISSAC3_VERSION": "03.16.12.05",
    "MANTA_VERSION": "1.0.3",
    "STRELKA_VERSION": "2.7.1"
}

ref_file_cfg = {
    "hg19": {
        "fa": "/ref/ucsc.hg19.fasta",
        "dbsnp": "/ref/dbsnp_138.hg19.vcf"
    },
    "GRCh37": {
        "fa": "/ref/human_g1k_v37.fasta",
        "dbsnp": "/ref/dbsnp_138.b37.vcf"
    }
}

DOCKER_RUN = "docker run --rm --volumes-from {_ref_v} -v {_out_d}:/out_dir -w /out_dir "

## all values in file_cfg are relative paths
file_cfg = {
    "std_log": lambda args: "log/{}.std.txt".format(args.samplename),
    "run_log": lambda args: "log/{}.run.txt".format(args.samplename),
    "err_log": lambda args: "log/{}.err.txt".format(args.samplename),
    "cache": lambda args: "tmp/cache_dict.pkl",
    "aligned": lambda args: "tmp/{}.aln.sam".format(args.samplename),
    "sorted": lambda args: "tmp/{}.sort.bam".format(args.samplename),
    "dedup": lambda args: "tmp/{}.dedup.bam".format(args.samplename),
    "matrics": lambda args: "tmp/{}.matrics".format(args.samplename),
    "table": lambda args: "tmp/{}.table".format(args.samplename),
    "bqsr": lambda args: "tmp/{}.bqsr.bam".format(args.samplename),
    "gvcf": lambda args: "{}.raw.g.vcf".format(args.samplename),
}
