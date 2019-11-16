#!/bin/bash
# Lexicon and morph_rules are input files; output is q4_expand_fsm to the q4 subdirectory
# lexicon file has the format "word classLeble"
# morph_rules file is an FSA (in Carmel format) - encodes the morphotactic rules
# output_fsm file is the expanded FSM (in Carmel format) - where an arc in the morph_rule FSA
# 		is replaced by multiple paths and each path is corresponds to an entry in the lexicon

## CONSTANTS
OUT_DIR="/q4"
PRJ_DIR=$(pwd)
PRJ_OUT_DIR=${PRJ_DIR}${OUT_DIR}

PY_ENV="/usr/bin/python"
PRG_NAME="expand_fsm1.py"

## Input/Output Command Line Arguments
lexicon_ex=$1
morph_rules_ex=$2
q4_expand_fsm=$3

##--------------------------------------------------
## Execute fsa python script
##--------------------------------------------------
function fsmExpand(){
	${PY_ENV} ./${PRG_NAME} ${lexicon_ex} ${morph_rules_ex} ${q4_expand_fsm}
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
fsmExpand

exit 0