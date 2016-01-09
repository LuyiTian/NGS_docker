## param_cfg.py
import os

version_cfg = {
    "REF_VERSION": "hg19",
    "BWA_VERSION": "0.7.12"
}

file_dict = {
    "aligned": lambda n: "/tmp/{}.aln.sam".format(n),
    "sorted": lambda n: "/tmp/{}.view.bam".format(n)
}