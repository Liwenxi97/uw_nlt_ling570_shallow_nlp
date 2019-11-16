#!/bin/bash
#### Constants
HW3_EX_PATH="/dropbox/18-19/570/"
#HW3_EX_PATH="examples/"
OUT_SYM=" => "
OUT_NONE="*none*"
SPACE=" "
Q2_OUT_DIR="/q2"

#### END CONSTANTS
f_path_test="$(echo $1 | sed -n '/wfst/p')"
f_path_test_LEN=$(echo -n $f_path_test | wc -m)
if (( $(bc <<< "${f_path_test_LEN} > 0") )); then
	fstFile=${HW3_EX_PATH}$1
else
	fstFile=$1
fi

inputFile=${HW3_EX_PATH}$2


#echo "FST FILE NAME: ${fstFile}"
#echo "Input File Is: ${inputFile}"

PRJ_DIR=$(pwd)
PRJ_OUT_DIR=${PRJ_DIR}${Q2_OUT_DIR}

##---------------------------------------
## Main Carmel Execution Function
##---------------------------------------
function executeCarmel(){
	for instance in ${inputFile}
	do
		while read line
		do
			L=$line
			#echo "Text read from file: ${L}"
			#echo ${L} | carmel -k 1 -sli ${fstFile}
			#-lsibOE
			#-sri
			#-sqlib%
			#-b -sli
			RESULT="$(echo ${line} | carmel -lsibOE ${fstFile} 2>/dev/null)"
		
			#echo $RESULT
			RESULT_LEN=$(echo -n $RESULT | wc -m)
			#echo "LENGTH OF THE RESULT: $RESULT_LEN"
			
			if (( $(bc <<< "${RESULT_LEN} == 1") ))
			then
				if (( $(bc <<< "${RESULT} == 0") ))
				then
					#echo "RESULT is 0: ${RESULT}"
					OUTPUT=${L}${OUT_SYM}${OUT_NONE}${SPACE}${RESULT}
					echo ${OUTPUT}
				else
					#echo "ACCEPTED: ${RESULT}"
					OUTPUT=${L}${OUT_SYM}${SPACE}${RESULT}
					echo ${OUTPUT}
				fi
			else
				#echo "ACCEPTED: ${RESULT}"
				OUTPUT=${L}${OUT_SYM}${SPACE}${RESULT}
				echo ${OUTPUT}
			fi
			
		done < ${inputFile}
		
	done
}
##---------------------------------------------------
## Create the Output q2 directory if it doesn't exist
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