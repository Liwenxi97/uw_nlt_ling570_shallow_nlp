#!/bin/bash
#Author: Ryan Timbrook
#Date: 11/22/2018
#HW: 8
#Q2: Write proc_file.sh
#This shell script executes a python program that:
#	- Processes a document and prints out the feature vectors
#	
#Format: command line: proc_file.sh input_file targetlabel output_file
# - 
#Input File: input_file is a text file (e.g., input_ex)
#	-Format: 
#			- 
#Output File:
#   -Format: One line with the format: "instanceName targetLabel f1 v1 f2 v2 ...
#		-instanceName is the filename of the input_file
#		-targetLabel is the second argument of the command line
#			
#From Command line, Run as: ./proc_file.sh $exDir/input_ex c1 output_ex
#   

##-- CONSTANTS --##
PY_ENV="/usr/bin/python3"
PRG_NAME="proc_file.py"
exDir="hw8/examples/"

input_ex=$1
targetLabel=$2
output_ex=$3


##--------------------------------------------------
## Execute python script
##--------------------------------------------------
function procFile(){
	${PY_ENV} ./${PRG_NAME} ${input_ex} ${targetLabel} ${output_ex}
}


### EXECUTE FUNCIONTS
procFile

exit 0