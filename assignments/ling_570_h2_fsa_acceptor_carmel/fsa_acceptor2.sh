#!/bin/bash

Q4_OUT_DIR="/q4"

PRJ_DIR=$(pwd)
PRJ_OUT_DIR=${PRJ_DIR}${Q4_OUT_DIR}
PY_ENV="/usr/bin/python"
PRG_NAME="fsa_acceptor2.py"
fsaFile=$1
inputFile=$2

##--------------------------------------------------
## Execute fsa python script
##--------------------------------------------------
function fsaAcceptor(){
	${PY_ENV} ./${PRG_NAME} ${fsaFile} ${inputFile}
}

##---------------------------------------------------
## Create the Output q3 directory if it doesn't exist
##---------------------------------------------------
createDirectory(){
	if [ ! -d $1 ]
		then
		mkdir -p $1
	fi
}


### EXECUTE FUNCIONTS
createDirectory ${PRJ_OUT_DIR}
fsaAcceptor

exit 0