#!/bin/bash
#Author: Ryan Timbrook
#Date: 11/1/2018
#Q1: Write ngram_count
#This shell script executes a python program to:
# collects unigrams, bigrams, and trigrams
#Format: command line: ngram_count.sh training_data ngram_count_file
#Input File: training_data
#Output File: ngram_count_file
#    
#Ran as: 
#    $ ./ngram_count.sh training_data ngram_count_file

##-- CONSTANTS --##
PY_ENV="/usr/bin/python3"
PRG_NAME="ngram_count.py"

#### END CONSTANTS
training_data=$1
ngram_count_file=$2


##--------------------------------------------------
## Execute fsa python script
##--------------------------------------------------
function ngramCount(){
	${PY_ENV} ./${PRG_NAME} ${training_data} ${ngram_count_file}
}

ngramCount

exit 0