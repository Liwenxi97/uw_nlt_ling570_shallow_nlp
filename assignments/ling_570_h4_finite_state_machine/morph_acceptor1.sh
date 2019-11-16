#!/bin/bash
# Has 3 command line arguments, 1&2 are input files, 3 is output file; 1:fsm, 2:word_lis, 3:output
# Input 1: q4/q4_expand_fsm 
# Input 2: worldlist_ex
# Output 3: q4/q4_result
# Output Format: word => answer(yes or no)

#### Constants
#CARMEL_PATH="/NLP_TOOLS/ml_tools/FST/carmel/latest/bin/carmel"

#### END CONSTANTS
expand_fsm=$1
wordlist_ex=$2
q4_result=$3
OUT_SYM=" => "
YES="yes"
NO="no"
OUT_DIR="/q4"
PRJ_DIR=$(pwd)
PRJ_OUT_DIR=${PRJ_DIR}${OUT_DIR}

##---------------------------------------------------
## Create the Output q4 directory if it doesn't exist
##---------------------------------------------------
createDirectory(){
	if [ ! -d $1 ]
		then
		mkdir -p $1
	fi
}

### EXECUTE FUNCTIONS
createDirectory ${PRJ_OUT_DIR}


##---------------------------------------------------
## Breakdown words into their individual characters
##---------------------------------------------------

while read line
do
echo $line | sed 's/.\{1\}/"&" /g'
done <${wordlist_ex} >inputCharacters

##---------------------------------------------------

##---------------------------------------
## Main Carmel Execution
##---------------------------------------

carmel -lsibOE ${expand_fsm} < inputCharacters > stdout_log.txt 2> stderr_log.txt

##---------------------------------------


##---------------------------------------------------
## Print the output
## Output Format: word => answer(yes or no)
##---------------------------------------------------

while IFS= read -r line_1 && IFS= read -r line_2 <&3 
do
	
	if [[ ${line_2} == "0" ]]
	then
		#echo "RESULT is equal to 1: ${RESULT}"
		OUTPUT=${line_1}${OUT_SYM}${NO}
		echo ${OUTPUT}
	else
		#echo "RESULT is NOT equal to 1: ${RESULT}"
		OUTPUT=${line_1}${OUT_SYM}${YES}
		echo ${OUTPUT}
	fi
	
done <${wordlist_ex} 3<stdout_log.txt >${q4_result}

exit 0