# NGS_docker
playing with docker and try making a variant calling pipeline
inspired by [Omics Pipe](http://pythonhosted.org/omics_pipe/) and [NGSeasy](https://github.com/KHP-Informatics/ngseasy)

*NGS_docker* is a dockerized NGS pipeline for variant calling. This program includes GATK, which is only free for academic and non-profit use. For details see: https://www.broadinstitute.org/gatk/about/#licensing

## design notes
* NGS_docker is designed for a readable and lightweighted variant calling pipeline.
* all programs like BWA, GATK and related reference data are dockerized.
* the structure of output dir is:
> rootdir/
>   samplename/
>       /samplename.vcf #final result
>       /log/std.txt # put all program output here
>       /log/err.txt # put error msg here
>       /log/run.txt # put pipeline running status here
>       /tmp # all intermadiate files
>       /tmp/cache_dict.pkl 
>       /report 
>           /variantanno # variant annotation result by snpEff
>           /fastqc # quality control report by fastqc
* `cache_dict.pkl` is a `pickle` dumped dictionary with key:value be the command:outputfiles and is updated after finishing each task. NGS_docker checks the return status of each tasks and delete the output files if task fails. So for each tasks if the outputfile exists and the command is the same with what stores in `cache_dict.pkl`, we will skip this one.