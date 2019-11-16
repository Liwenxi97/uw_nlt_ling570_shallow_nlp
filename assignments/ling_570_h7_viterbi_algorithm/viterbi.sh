#!/bin/bash
#Author: Ryan Timbrook
#Date: 11/16/2018
#Q1: Write viterbi.sh
#This shell script executes a python program that:
#	-Implements the Viterbi algorithm.
#	-
#Format: command line: viterbi.sh input_hmm test_file output_file
# - 
#Input File: HMM is a state-emission hmm - same format as HW6. The output is produced by the to-state
#	-Format: Assume the input hmm does not contain any emission probabilities for empty string
#			- output symbols are produced by the to-state
#			- No smoothing of the HMM
#			- *** if a line contains a probability not in the range 0 - 1, print out a wanring message to stderr
#				("warning: the prob is not in [0,1] range: $line", where $line is the line) and ignore those lines
#Test File: each line is an observation (a sequence of output symbols) - POS tagging, an observation will be a sentence
#	- the sentence may, or may not include special symbol(</s>) for EOS.
#	- Do not do anything special for BOS and EOS.
#Output File:
#   -Format: "observ => state seq lgprob"
#		-state seq is the best state sequence for the observation
#		-lgprob is lg P(observ,state seq); lg(x) is base-10 log
#			
#From Command line, Run as: ./viterbi.sh hmm1 test.word sys1
#   

##-- CONSTANTS --##
PY_ENV="/usr/bin/python3"
PRG_NAME="viterbi.py"

input_hmm=$1
test_word=$2
output_sys=$3


##--------------------------------------------------
## Execute python script
##--------------------------------------------------
function viterbi(){
	${PY_ENV} ./${PRG_NAME} ${input_hmm} ${test_word} ${output_sys}
}


### EXECUTE FUNCIONTS
viterbi

exit 0