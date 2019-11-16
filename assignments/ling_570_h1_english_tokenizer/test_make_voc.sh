#!/bin/bash

PRJ_DIR=$(pwd)
PY_ENV="/usr/bin/python"
PRG_NAME="test_hw1_voc.py"

##--------------------------------------------------
## Execute make vocabulary list
##--------------------------------------------------
function makeVoc(){
	${PY_ENV} ./${PRG_NAME}
}
makeVoc

exit=0