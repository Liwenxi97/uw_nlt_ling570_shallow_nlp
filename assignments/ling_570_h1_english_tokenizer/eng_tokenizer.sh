#!/bin/bash

PRJ_DIR=$(pwd)
#PRJ_OUT_DIR=${PRJ_DIR}${Q4_OUT_DIR}
PY_ENV="/usr/bin/python"
PRG_NAME="hw1_tok.py"
abbrev_list=$1

##--------------------------------------------------
## Execute fsa python script
##--------------------------------------------------
function tokenizer(){
	${PY_ENV} ./${PRG_NAME} ${abbrev_list}
}
tokenizer

exit=0