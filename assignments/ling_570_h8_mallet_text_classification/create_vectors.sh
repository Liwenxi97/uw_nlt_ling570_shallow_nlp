#!/bin/bash
#Author: Ryan Timbrook
#Date: 11/22/2018
#HW: 8
#Q3: Write create_vectors.sh
#    - This python script creates training and test vectors from several directories of documents.
#    - This script has the same function as "mallet import-dir"
#    
#Format: command line: create_vectors.sh train_vector_file test_vector_file ratio dir1 dir2 ...
#        
#Input: ratio dir1 dir2 ...
#    -***Note: The command line should include one or more directories
#    -Ratio is the portion of the training data 
#
#Output File: train_vector_file test_vector_file
#   -Format: Same format as output from Q2
#       -one line with the format as:
#           -instanceName targetLabel f1 v1 f2 v2 ... (standard format)
#           -label f1:v1 f2:v2 ... (svmlight format)
#            
#From Command line, Run as: ./create_vectors.sh train.vectors.txt test.vectors.txt dir1 dir2 dir3
#   

##-- CONSTANTS --##
PY_ENV="/usr/bin/python3"
PRG_NAME="create_vectors.py"
exDir="../opt/dropbox/17-18/570/"


##--------------------------------------------------
## Execute python script
##--------------------------------------------------
function createVectors(){
	${PY_ENV} ./${PRG_NAME} $@
}


### EXECUTE FUNCIONTS
createVectors

exit 0