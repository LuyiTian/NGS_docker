# NGS_docker
playing with docker and try making a variant calling pipeline
inspired by [Omics Pipe](http://pythonhosted.org/omics_pipe/) and [NGSeasy](https://github.com/KHP-Informatics/ngseasy)

*NGS_docker* is a dockerized NGS pipeline for variant calling. This program includes GATK, which is only free for academic and non-profit use. For details see: https://www.broadinstitute.org/gatk/about/#licensing

> TODO: build gatk from https://hub.docker.com/r/biodckrdev/gatk/~/dockerfile/ instead of using `ADD`

## design notes
* NGS_docker is designed for a readable and lightweighted variant calling pipeline. The `wgs_pipe.py` is the main entry of the pipeline. Tasks are executed and logged by `run_task` decorator,  Additional parameters can be added in `prog_cfg.py`. functions following the same format `def foo(args, param_dict): ... return cmd, output_file` where cmd are the command to be executed by the `run_task`, `output_file` are required for check existance.
* all programs like BWA, GATK and related reference data are dockerized.
* the structure of output dir is:
> rootdir/
>   samplename/
>       /samplename.vcf #final result
>       /log/{samplename}.std.txt # put all program output here
>       /log/{samplename}.err.txt # put error msg here
>       /log/{samplename}.run.txt # put pipeline running status here
>       /tmp # all intermadiate files
>       /tmp/cache_dict.pkl 
>       /report 
>           /variantanno # variant annotation result by snpEff
>           /fastqc # quality control report by fastqc
* `cache_dict.pkl` is a `pickle` dumped dictionary with key:value be the command:outputfiles and is updated after successfully finishing each task. NGS_docker checks the return status of each tasks and delete the `output_file` if task fails. So for each tasks if the outputfile exists and the command is the same with what stores in `cache_dict.pkl`, we will skip it.
* all reference data is named by its version (eg. hg19) and is stored in `/ref` and mount by tasks by `--volumes-from {name}`.
* `rootdir` is a host directory, its subdir `rootdir/samplename` will be used to store output. This directory is mounted as `/out_dir` and set as working directory for all tasks.