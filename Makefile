################################################################
## NGSdocker Makefile
## Version 0.1
## Author: LuyiTian (tlytiger@hotmail.com)
################################################################
## Usage
################################################################
#
#    make all && sudo make install
#
# ...or...
#
#    make INSTALLDIR="/CUSTOM/PATH" all && sudo make install
#
################################################################

################################################################
## Edit this to reflect version
VERSION=0.1


################################################################
## This is where we will make ngs_projects and download metadata to etc etc
## Edit this if you want to install all somewhere else
# eg:
# make INSTALLDIR="/aa/bb" all
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
# Intsalling all or parts...
################################################################

ubuntubase:
	@ifeq(GFW,1) \
		echo "pull ubuntu 14.04 from dockerpool" \
	#	echo "DOCKER_OPTS=\"--insecure-registry dl.dockerpool.com:5000\"" > /etc/default/docker \
	#	service docker restart \
	#	docker pull dl.dockerpool.com:5000/ubuntu:14.04 \
	#	docker tag dl.dockerpool.com:5000/ubuntu:14.04 ubuntu:14.04 \
	else \
		echo "pull ubuntu 14.04 from docker.io, if doesnot work try make GFW=1" \
	#	docker pull ubuntu:14.04 \


