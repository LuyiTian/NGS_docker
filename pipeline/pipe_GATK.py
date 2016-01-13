## pipe_GATK.py
import os
from param_cfg import *
from util import run_task, join_params
_version = version_cfg["GATK_VERSION"]


@run_task("GATK BQSR")
def gatk_bqsr(args, param_dict=None):
    """
    Base quality score recalibration (BQSR) is a process in which we apply machine learning
    to model these errors empirically and adjust the quality scores accordingly. This allows
    us to get more accurate base qualities, which in turn improves the accuracy of our variant
    calls. The base recalibration process involves two key steps: first the program builds a model
    of covariation based on the data and a set of known variants (which you can bootstrap if
    there is none available for your organism), then it adjusts the base quality scores
    in the data based on the model.
    """
    cmd = DOCKER_RUN + """ gatk:{_v} -T BaseRecalibrator {param} -nct {_p}\
    -R {_R} -I {dedup} -knownSites {_dbsnp_vcf} -o {table}"""
    cmd = cmd.format(
        _ref_v=version_cfg["REF_VERSION"],
        _out_d=args.out_dir,
        param=join_params(param_dict),
        _p=args.p,
        _v=_version,
        _R=ref_file_cfg[version_cfg["REF_VERSION"]]["fa"],
        _dbsnp_vcf=ref_file_cfg[version_cfg["REF_VERSION"]]["dbsnp"],
        dedup=file_cfg["dedup"](args),
        table=file_cfg["table"](args)
        )
    return cmd, file_cfg["table"](args)


@run_task("GATK printread")
def gatk_printread(args, param_dict=None):
    """
    PrintReads is a generic utility tool for manipulating sequencing data in SAM/BAM format.
    It can dynamically merge the contents of multiple input BAM files, resulting in merged output
    sorted in coordinate order.
    """
    cmd = DOCKER_RUN + """ gatk:{_v} -T PrintReads {param} -nct {_p}\
    -R {_R} -I {dedup} -BQSR {table} -o {bqsr}"""
    cmd = cmd.format(
        _ref_v=version_cfg["REF_VERSION"],
        _out_d=args.out_dir,
        param=join_params(param_dict),
        _p=args.p,
        _v=_version,
        _R=ref_file_cfg[version_cfg["REF_VERSION"]]["fa"],
        dedup=file_cfg["dedup"](args),
        table=file_cfg["table"](args),
        bqsr=file_cfg["bqsr"](args)
        )
    return cmd, file_cfg["bqsr"](args)


@run_task("GATK HaplotypeCaller")
def gatk_haplotypecaller(args, param_dict=None):
    """
    The HaplotypeCaller is capable of calling SNPs and indels simultaneously via local de-novo
    assembly of haplotypes in an active region. In other words, whenever the program encounters
    a region showing signs of variation, it discards the existing mapping information and completely
    reassembles the reads in that region.
    """
    cmd = DOCKER_RUN + """gatk:{_v} -T HaplotypeCaller {param} -nct {_p} -R {_R}\
    -I {bqsr} --emitRefConfidence GVCF --dbsnp {_dbsnp_vcf} -o {gvcf}"""
    cmd = cmd.format(
        _ref_v=version_cfg["REF_VERSION"],
        _out_d=args.out_dir,
        param=join_params(param_dict),
        _p=args.p,
        _v=_version,
        _dbsnp_vcf=ref_file_cfg[version_cfg["REF_VERSION"]]["dbsnp"],
        _R=ref_file_cfg[version_cfg["REF_VERSION"]]["fa"],
        bqsr=file_cfg["bqsr"](args),
        gvcf=file_cfg["gvcf"](args))
    return cmd, file_cfg["gvcf"](args)
