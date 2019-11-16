#!/bin/bash
#Author: Ryan Timbrook
#Date: 12/13/2018
#HW: 11
#Q1: Write word_analogy.sh that finds D given A, B, and D
#    
#    
#Format: command line: word_analogy.sh vector_file input_dir output_dir flag1 flag2
#        
#Input: 
# - vector_file: has format "w v1 v2 ... vn" where <v1,v2, ..., vn> is word embedding of the word w
# - input_dir: is a directory that contains a list of test files. Test file lines have the format "A B C D", the four words of the word anology task
# - output_dir: is the directory to store the output
# 			- for each file under input_dir, this script creates a file with the same name under the output_dir
#			- the two files have the exactly the same number of lines and the same content, except that the word
#			D in the files under output_dir is the word selected by the algorithm
# - flag1: an integer flag indicating if the word embeddings should be normalized first
#		- Non-Zero triggers the normalization
#		- Zero indicates to just use original vectors as is
# - flag2: an integer flag indicating which similarity function to use for calculating sim(x,y)
#		- Non-Zero triggers the use of cosine similarity
#		- Zero triggers the use of Euclidean distance
#Output File: stdout redirected to output_dir/eval_result
# 		- Prints accuracy metrics
#		- Format:
#			fileName1
#			ACCURACY TOP1: acc% (cor/nuum)
#			fileName2
#			ACCURACY TOP1: acc% (cor/num)
#			...
#			Total accuracy: accTotal% (corSum/numSum)            
#From Command line, Run as: 
#   ./word_analogy.sh /dropbox/18-19/570/hw11/examples/vectors.txt /dropbox/18-19/570/hw11/examples/question-data exp00 0 0 > exp00/eval_res
#	./word_analogy.sh /dropbox/18-19/570/hw11/examples/vectors.txt /dropbox/18-19/570/hw11/examples/question-data exp01 0 1 > exp01/eval_res
#	./word_analogy.sh /dropbox/18-19/570/hw11/examples/vectors.txt /dropbox/18-19/570/hw11/examples/question-data exp10 1 0 > exp10/eval_res
#	./word_analogy.sh /dropbox/18-19/570/hw11/examples/vectors.txt /dropbox/18-19/570/hw11/examples/question-data exp11 1 1 > exp11/eval_res


##-- CONSTANTS --##
PY_ENV="/usr/bin/python3"
PRG_NAME="word_analogy.py"

##-- Command Line Arguments --##
vectorFile=$1
inputDir=$2
outputDir=$3
flag1=$4
flag2=$5


PRJ_DIR=$(pwd)
PRJ_OUT_DIR=${PRJ_DIR}${outputDir}

##--------------------------------------------------
## Execute python script
##--------------------------------------------------
function runWordAnalogy(){
	${PY_ENV} ./${PRG_NAME} ${vectorFile} ${inputDir} ${outputDir} ${flag1} ${flag2}
}

##---------------------------------------------------
## Create the Output directory if it doesn't exist
##---------------------------------------------------
createDirectory(){
	if [ ! -d $1 ]
		then
		mkdir -p $1
	fi
}


### EXECUTE FUNCIONTS
start=$SECONDS
createDirectory ${PRJ_OUT_DIR}
runWordAnalogy
end=$SECONDS
#echo "Total Execution Time: $((end-start)) seconds"
exit 0