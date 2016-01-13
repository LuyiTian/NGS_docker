###################
## stores program prarmeters, except in/out
bwa_mem_cfg = {
    "-R": r"'@RG\tID:group1\tSM:sample1\tLB:lib1\tPL:illumina\tPU:unit1'"
}

gatk_bqsr_cfg = {
    "--fix_misencoded_quality_scores": "",
    "-fixMisencodedQuals": ""
}
