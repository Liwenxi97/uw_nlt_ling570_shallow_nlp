#!/bin/bash
#Author: Ryan Timbrook
#Date: 11/1/2018
#Q3: Write ppl
#This shell script executes a python program that calculates the perplexity of a test data given an LM:
#	For smoothing, it uses interpolation
#Format: command line: ppl.sh lm_file l1 l2 l3 test_date output_file
#Input File: lm_file (Is the output file generated from Q2)
#Input File: test_data (same format as the training_data from Q1)
#Output File: output_file
#	-all real numbers are truncated to 10 places after the decimal points
#    
#Ran as: 
#    $ ./ppl.sh lm_file l1 l2 l3 test_date output_file

##-- CONSTANTS --##
PY_ENV="/usr/bin/python3"
PRG_NAME="ppl.py"

#### END CONSTANTS
lm_file=$1
l1=$2
l2=$3
l3=$4
test_data=$5
output_file=$6



##--------------------------------------------------
## Execute fsa python script
##--------------------------------------------------
function buildLM(){
	${PY_ENV} ./${PRG_NAME} ${lm_file} ${l1} ${l2} ${l3} ${test_data} ${output_file}
}

buildLM

exit 0