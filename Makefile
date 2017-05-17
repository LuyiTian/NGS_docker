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
VERSION=1.0
BWA_VERSION=0.7.12
SAMTOOLS_VERSION=1.3.1
PICARD_VERSION=2.0.1
SRA_VERSION=2.8.2.1
GATK_VERSION=3.5
ISAAC3_VERSION=03.16.12.05
MANTA_VERSION=1.0.3
STRELKA_VERSION=2.7.1
################################################################
## Current working dir
DIR=$(shell pwd)

################################################################
## f**k GFW
GFW=1


################################################################
# build images...
buildimage: ubuntubase isaac3image samtoolsimage mantaimage strelkaimage

ubuntubase:
ifeq ($(docker images -q ubuntu:14.04),"")
ifeq ($(GFW),1) 
	echo 'DOCKER_OPTS="--registry-mirror=http://aad0405c.m.daocloud.io"' >>  /etc/default/docker
	docker pull aad0405c.m.daocloud.io/ubuntu:14.04
	docker tag aad0405c.m.daocloud.io/ubuntu:14.04 ubuntu:14.04
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

isaac3image:
	cd $(DIR)/dockerfiles && \
	docker build -t isaac3:$(ISAAC3_VERSION) -f Isaac3_Dockerfile . 

mantaimage:
	cd $(DIR)/dockerfiles && \
	docker build -t manta:$(MANTA_VERSION) -f manta_Dockerfile . 

strelkaimage:
	cd $(DIR)/dockerfiles && \
	docker build -t strelka:$(STRELKA_VERSION) -f manta_Dockerfile . 

#####
# build data images... disabled due to the terrible GWF in China
#hg19image:
#	cd $(DIR)/dockerfiles && \
#	docker build -t reference:hg19 -f hg19_Dockerfile .


################################################################
# clean up untagged images
cleanuntagged:
	docker rmi $(docker images | grep "^<none>" | awk "{print $3}")


