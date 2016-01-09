#!/bin/bash
wget -O $2 ftp://ftp-trace.ncbi.nih.gov/sra/sra-instant/reads/ByRun/sra/${1:0:3}/${1:0:6}/$1/$1.sra 