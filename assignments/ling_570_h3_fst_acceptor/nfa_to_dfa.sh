#!/bin/bash

Q4_OUT_DIR="/q4"
HW3_EX_PATH="/dropbox/18-19/570/"

PRJ_DIR=$(pwd)
PRJ_OUT_DIR=${PRJ_DIR}${Q4_OUT_DIR}
PY_ENV="/usr/bin/python"
PRG_NAME="nfa_to_dfa.py"
nfaFile=${HW3_EX_PATH}$1

##--------------------------------------------------
## Execute fsa python script
##--------------------------------------------------
function nfaToDFA(){
	${PY_ENV} ./${PRG_NAME} ${nfaFile}
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
nfaToDFA

exit 0