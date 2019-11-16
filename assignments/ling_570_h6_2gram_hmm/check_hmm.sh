#!/bin/bash
#Author: Ryan Timbrook
#Date: 11/8/2018
#Q3: Write check_hmm.sh
#This shell script executes a python program that:
#	-Reads in a state-emission HMM file, check's its format, and outputs a warning file
#	-****Store's HMM file in an EFFICIENT DATA STRUCTURE****
#Format: command line: check_hmm.sh input_hmm > warning_file
# - Check's whether the two parts of the HMM file are consistent
#		-Do the number of states in the header match that in the distributions?
#		-Are the three kinds of constraints for HMM met?
#			-print out to warning file if either rules aren't met
#Input File: input_hmm (state-emission HMM file that was output from Q2 program execution)
#	-Format: 
#Output File: warning_file ()
#   -Format: 
#		-
#			
#From Command line, Run as: 
#   $ ./check_hmm.sh q4/2g_hmm > q4/2g_hmm.warning
#	$ ./check_hmm.sh q4/3g_hmm_0.1_0.1_0.8 > q4/3g_hmm_0.1_0.1_0.8.warning
#	$ ./check_hmm.sh q4/3g_hmm_0.2_0.3_0.5 > q4/3g_hmm_0.2_0.3_0.5.warning

##-- CONSTANTS --##
PY_ENV="/usr/bin/python3"
PRG_NAME="check_hmm.py"

OUT_DIR="/q4"
PRJ_DIR=$(pwd)
PRJ_OUT_DIR=${PRJ_DIR}${OUT_DIR}


input_hmm=$1
#echo ${output_hmm}


##--------------------------------------------------
## Execute python script
##--------------------------------------------------
function checkHmm(){
	cat $1 | ${PY_ENV} ./${PRG_NAME} ${input_hmm}
}

##---------------------------------------------------
## Create the Output q4 directory if it doesn't exist
##---------------------------------------------------
createDirectory(){
	if [ ! -d $1 ]
		then
		mkdir -p $1
	fi
}

### EXECUTE FUNCIONTS
createDirectory ${PRJ_OUT_DIR}
checkHmm

exit 0