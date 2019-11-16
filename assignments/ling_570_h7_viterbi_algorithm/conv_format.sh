#!/bin/bash
#Author: Ryan Timbrook
#Date: 11/16/2018
#Q2: Write conv_format.sh
#This shell script executes a python program that:
#	-
#	-
#Format: command line: 
# - 
#Input File: 
#	-Format: 
#
#   -Format: 
#			
#From Command line, Run as: 
#   

##-- CONSTANTS --##
PY_ENV="/usr/bin/python3"
PRG_NAME="conv_format.py"

##--------------------------------------------------
## Execute python script
##--------------------------------------------------
function convFormat(){
	cat $1 | ${PY_ENV} ./${PRG_NAME}
}


### EXECUTE FUNCTIONS
convFormat

exit 0