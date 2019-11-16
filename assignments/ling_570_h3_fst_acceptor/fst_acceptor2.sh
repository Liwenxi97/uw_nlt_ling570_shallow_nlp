#!/bin/bash

Q3_OUT_DIR="/q3"
HW3_EX_PATH="/dropbox/18-19/570/"

PRJ_DIR=$(pwd)
PRJ_OUT_DIR=${PRJ_DIR}${Q3_OUT_DIR}
PY_ENV="/usr/bin/python"
PRG_NAME="fst_acceptor2.py"
fstFile=${HW3_EX_PATH}$1
inputFile=${HW3_EX_PATH}$2

##--------------------------------------------------
## Execute fsa python script
##--------------------------------------------------
function fstAcceptor(){
	${PY_ENV} ./${PRG_NAME} ${fstFile} ${inputFile}
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
fstAcceptor

exit 0