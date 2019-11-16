#!/bin/bash
#Author: Ryan Timbrook
#Date: 11/1/2018
#Q2: Write build_lm
#This shell script executes a python program that builds an LM using ngram counts:
#Format: command line: build_lm.sh ngram_count_file lm_file
#Input File: ngram_count_file (produced as output from Q1, ngram_count.py)
#Output File: lm_file (follows ARPA format)
#    
#Ran as: 
#    $ ./build_lm.sh ngram_count_file lm_file

##-- CONSTANTS --##
PY_ENV="/usr/bin/python3"
PRG_NAME="build_lm.py"

#### END CONSTANTS
ngram_count_file=$1
lm_file=$2


##--------------------------------------------------
## Execute fsa python script
##--------------------------------------------------
function buildLM(){
	${PY_ENV} ./${PRG_NAME} ${ngram_count_file} ${lm_file}
}

buildLM

exit 0