################################################################
## NGSdocker Makefile
## Version 0.1
## Author: LuyiTian (tlytiger@hotmail.com)
################################################################
## Usage
################################################################
#
#    
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
SAMTOOLS_VERSION=1.3
PICARD_VERSION=1.119

################################################################
## This is where we will make ngs_projects and download metadata to etc etc
## Edit this if you want to install all somewhere else
# eg:
# make INSTALLDIR="/your/path" all
#
INSTALLDIR=/root/NGS_docker

################################################################
## Current working dir
DIR=$(shell pwd)

################################################################
## Install bin path - edit at will
## TARGET_BIN=/usr/local/bin
## changed to move bin to user folder. no need for sudo with install
TARGET_BIN=$(INSTALLDIR)

################################################################
## f**k GFW
GFW=1


################################################################
# build images...
buildimage: ubuntubase bwaimage samtoolsimage picardimage hg19image

ubuntubase:
ifeq ($(GFW),1) 
	@echo "pull ubuntu 14.04 from dockerpool" 
	sed -i 'DOCKER_OPTS="--insecure-registry dl.dockerpool.com:5000"' /etc/default/docker
	docker pull dl.dockerpool.com:5000/ubuntu:14.04
	docker tag dl.dockerpool.com:5000/ubuntu:14.04 ubuntu:14.04
else 
	@echo "pull ubuntu 14.04 from docker.io, if doesnot work try 'GFW=1'" 
	docker pull ubuntu:14.04
endif

bwaimage:
	@echo "build bwa image from dockerfile"
	cd dockerfiles && \
	docker build -t bwa:$(BWA_VERSION) -f bwa_Dockerfile . && \
	cd ..

samtoolsimage:
	@echo "build samtools image from dockerfile"
	cd dockerfiles && \
	docker build -t samtools:$(SAMTOOLS_VERSION) -f samtools_Dockerfile . && \
	cd ..

picardimage:
	@echo "build picard image from dockerfile"
	cd dockerfiles && \
	docker build -t picard:$(PICARD_VERSION) -f picard_Dockerfile . && \
	cd ..

#####
# build data images...
hg19image:
	@echo "build hg19 reference image from dockerfile"
	cd dockerfiles && \
	docker build -t reference:hg19 -f hg19_Dockerfile . && \
	cd ..


