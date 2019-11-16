#!/bin/bash
#### Constants
CARMEL_PATH="/NLP_TOOLS/ml_tools/FST/carmel/latest/bin/carmel"

#### END CONSTANTS
fsaFile=$1
inputFile=$2
OUT_SYM=" => "
YES="yes"
NO="no"
Q3_OUT_DIR="/q3"

#echo "FSA FILE NAME: ${fsaFile}"
#echo "Input File Is: ${inputFile}"

PRJ_DIR=$(pwd)
PRJ_OUT_DIR=${PRJ_DIR}${Q3_OUT_DIR}

##---------------------------------------
## Main Carmel Execution Function
##---------------------------------------
function executeCarmel(){
	while read line
	do
		L=$line
		#echo "Text read from file: ${L}"
		RESULT="$(echo ${L} | eval ${CARMEL_PATH} -k 1 -sqlib% ${fsaFile} 2>/dev/null)"
		
		#echo $RESULT
		#RESULT_LEN=$(echo -n $RESULT | wc -m)
		#echo "LENGTH OF THE RESULT: $RESULT_LEN"
		if [ ${RESULT} -eq 1 ]
		then
			#echo "RESULT is equal to 1: ${RESULT}"
			OUTPUT=${L}${OUT_SYM}${YES}
			echo ${OUTPUT}
		else
			#echo "RESULT is NOT equal to 1: ${RESULT}"
			OUTPUT=${L}${OUT_SYM}${NO}
			echo ${OUTPUT}
		fi
		
	done < ${inputFile}
	
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
executeCarmel

exit 0