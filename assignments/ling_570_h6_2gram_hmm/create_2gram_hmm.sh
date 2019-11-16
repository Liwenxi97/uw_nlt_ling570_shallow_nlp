#!/bin/bash
#Author: Ryan Timbrook
#Date: 11/8/2018
#Q1: Write create_2gram_hmm.sh
#This shell script executes a python program that:
#	-takes annotated training data as input and creates an HMM for a Bigram POS tagger
#	-NO SMOOTHING
#Format: command line: cat training_data | create_2gram_hmm.sh output_hmm
#Input File: training_data as std input
#	-Format: "w1/t1 ... wn/tn" (wsj_sec0.word_pos)	
#Output File: output_hmm (follows ARPA format)
#   -Format: 
#		-prob and lgprob -> truncate to 10 digits past decimal (0.0000000001)
#		-sort probabilities alphabetically on the 1st field (state or from_state) first
#		-then, for lines with same 1st field, sort on the second field (symbol)
#			
#From Command line, Run as: 
#    $ cat wsj_sec0.word_pos | ./create_2gram_hmm.sh q4/2g_hmm

##-- CONSTANTS --##
PY_ENV="/usr/bin/python3"
PRG_NAME="create_2gram_hmm.py"

OUT_DIR="/q4"
PRJ_DIR=$(pwd)
PRJ_OUT_DIR=${PRJ_DIR}${OUT_DIR}


output_hmm=$1
#echo ${output_hmm}


##--------------------------------------------------
## Execute python script
##--------------------------------------------------
function create2Gram(){
	cat $1 | ${PY_ENV} ./${PRG_NAME} ${output_hmm}
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
create2Gram

exit 0