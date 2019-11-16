#!/bin/bash
# Has 3 command line arguments, 1&2 are input files, 3 is output file; 1:expanded fsm, 2:word_lis, 3:output
# Q3 Write morph_acceptor2.sh
# Input 1: q5/q5_expand_fsm 
# Input 2: worldlist_ex
# Output 3: q5/q5_result
# Output Format: "word => answer" 
# 		... where "answer" is "morph1/label1 morph2/label2 ..." if the word is accepted by morph acceptor
#		... or "*NONE*" otherwise

#### Constants
#CARMEL_PATH="/NLP_TOOLS/ml_tools/FST/carmel/latest/bin/carmel"

#### END CONSTANTS
expand_fsm=$1
wordlist_ex=$2
q5_result=$3
OUT_SYM=" => "
OUT_NONE="*NONE*"

OUT_DIR="/q5"
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
		OUTPUT=${line_1}${OUT_SYM}${OUT_NONE}
		echo ${OUTPUT}
	else
		#echo "RESULT is NOT equal to 1: ${RESULT}"
		OUTPUT="${line_1}${OUT_SYM}${line_2%1}"
		echo ${OUTPUT}
	fi
	
done <${wordlist_ex} 3<stdout_log.txt >${q5_result}

exit 0