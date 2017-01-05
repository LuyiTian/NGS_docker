################################################################
## NGSdocker Makefile
## Version 0.1
## Author: LuyiTian (tlytiger@hotmail.com)
################################################################
## Usage
################################################################
#
#    make buildimage
#
# ...or...
#
#    
#
################################################################

################################################################
## Edit this to reflect version
VERSION=0.1
BWA_VERSION=0.7.12
SAMTOOLS_VERSION=1.3.1
PICARD_VERSION=2.0.1
SRA_VERSION=2.5.7
GATK_VERSION=3.5

################################################################
## Current working dir
DIR=$(shell pwd)

################################################################
## f**k GFW
GFW=1


################################################################
# build images...
buildimage: ubuntubase bwaimage samtoolsimage picardimage gatkimage sraimage hg19image

ubuntubase:
ifeq ($(docker images -q ubuntu:14.04),"")
ifeq ($(GFW),1) 
	echo 'DOCKER_OPTS="--insecure-registry dl.dockerpool.com:5000"' >>  /etc/default/docker
	docker pull dl.dockerpool.com:5000/ubuntu:14.04
	docker tag dl.dockerpool.com:5000/ubuntu:14.04 ubuntu:14.04
else 
	docker pull ubuntu:14.04
endif
endif

bwaimage:
	cd $(DIR)/dockerfiles && \
	docker build -t bwa:$(BWA_VERSION) -f bwa_Dockerfile . 

samtoolsimage:
	cd $(DIR)/dockerfiles && \
	docker build -t samtools:$(SAMTOOLS_VERSION) -f samtools_Dockerfile . 

picardimage:
	cd $(DIR)/dockerfiles && \
	docker build -t picard:$(PICARD_VERSION) -f picard_Dockerfile .

sraimage:
	cd $(DIR)/dockerfiles && \
	docker build -t sratoolkit:$(SRA_VERSION) -f sra_Dockerfile . 

gatkimage:
	cd $(DIR)/dockerfiles && \
	docker build -t gatk:$(GATK_VERSION) -f gatk_Dockerfile . 

#####
# build data images...
hg19image:
	cd $(DIR)/dockerfiles && \
	docker build -t reference:hg19 -f hg19_Dockerfile .


################################################################
# clean up untagged images
cleanuntagged:
	docker rmi $(docker images | grep "^<none>" | awk "{print $3}")


