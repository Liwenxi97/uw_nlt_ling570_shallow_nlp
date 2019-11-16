#!/bin/bash
#Author: Ryan Timbrook
#Date: 11/8/2018
#Q2: Write create_3gram_hmm.sh
#
#This shell script executes a python program that:
#    -takes annotated training data as input and creates an HMM for a Trigram POS tagger
#    -WITH SMOOTHING
#Format: command line: cat training_data | create_3gram_hmm.sh output_hmm l1 l2 l3 unk_prob_file
#Input File: training_data as std input
#    -Format: "w1/t1 ... wn/tn" (wsj_sec0.word_pos)
#Input File: unk_prob_file (used to smooth P(word | tag)
#    -Format: "tag prob"
#        -prob -> P(< unk > | tag)
#l1,l2,l3 are lambda's used in interpolation
#Output File: output_hmm (same format as Q1)
#   -Format: 
#        -prob and lgprob -> truncate to 10 digits past decimal (0.0000000001)
#        -sort probabilities alphabetically on the 1st field (state or from_state) first
#        -then, for lines with same 1st field, sort on the second field (symbol)
#        
#            
#From Command line, Run as: 
#    $ cat wsj_sec0.word_pos | ./create_3gram_hmm.sh q4/3g_hmm_0.1_0.1_0.8 0.1 0.1 0.8 unk_prob_sec22
#    $ cat wsj_sec0.word_pos | ./create_3gram_hmm.sh q4/3g_hmm_0.2_0.3_0.5 0.2 0.3 0.5 unk_prob_sec22

##-- CONSTANTS --##
PY_ENV="/usr/bin/python3"
PRG_NAME="create_3gram_hmm.py"

OUT_DIR="/q4"
PRJ_DIR=$(pwd)
PRJ_OUT_DIR=${PRJ_DIR}${OUT_DIR}

out_hmm=$1
in_l1=$2
in_l2=$3
in_l3=$4
in_unk_prob=$5


##--------------------------------------------------
## Execute python script
##--------------------------------------------------
function create3Gram(){
	cat $1 | ${PY_ENV} ./${PRG_NAME} ${out_hmm} ${in_l1} ${in_l2} ${in_l3} ${in_unk_prob}
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
create3Gram

exit 0