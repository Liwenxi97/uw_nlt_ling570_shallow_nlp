#!/bin/bash
#Author: Ryan Timbrook
#Date: 12/06/2018
#HW: 10
#Q1: Write maxent_tagger.sh
#    - Create a MaxEnt POS tagger
#    
#Format: command line: maxent_tagger.sh train_file test_file rare_thres feat_thres output_dir
#        
#Input: (e.g., test.word_pos)
#	-train_file: Format: w1/t1 w2/t2 ... wn/tn
#	-test_file: Format: w1/t1 w2/t2 ... wn/tn
#	-rare_thres: type=Integer
#		-> any words in training and test that appear less than this value are treated as rear words
#		-> features such as pref=xx and suf=xx should be used for rare_words
#	-feat_thres: type=Integer
#		-> all CurrentWord=xx features, regardless of their frequency, should be kept. For all other
#			types of features, if a feature appears less than this value in the train_file, that feature
#			should be removed from the feature vectors
#Output File: (output_dir is a directory that stores the output files from the tagger)
#		Create and store the following files under this directory
#		-train_voc
#		-init_feats
#		-kept_feats
#		-final_train.vectors.txt
#		-final_test.vectors.txt
#            
#From Command line, Run as: ./maxent_tagger.sh wsj_sec0.word_pos test.word_pos 1 1 res_1_1
#   

##-- CONSTANTS --##
PY_ENV="/usr/bin/python3"
PRG_NAME="maxent_tagger.py"

##-- Command Line Arguments --##
trainFile=$1
testFile=$2
rareThres=$3
featThres=$4
outputDir=$5

FINAL_TRAIN_VECTORS="final_train.vectors.txt"
FINAL_TEST_VECTORS="final_test.vectors.txt"

PRJ_DIR=$(pwd)
PRJ_OUT_DIR=${outputDir}

##--------------------------------------------------
## Execute python script
##--------------------------------------------------
function createMaxEntTagger(){
	${PY_ENV} ./${PRG_NAME} ${trainFile} ${testFile} ${rareThres} ${featThres} ${outputDir}
}

##--------------------------------------------------
## Execute Mallet to convert the training and testing vectors to binary format
##--------------------------------------------------
function malletImport(){
	mallet import-file --token-regex "[^\s]+" --preserve-case --input ${outputDir}/${FINAL_TRAIN_VECTORS} --output ${outputDir}/"final_train.vectors"
	mallet import-file --token-regex "[^\s]+" --preserve-case --input ${outputDir}/${FINAL_TEST_VECTORS} --output ${outputDir}/"final_test.vectors" --use-pipe-from ${outputDir}/"final_train.vectors"
}


##--------------------------------------------------
## Execute Mallet vectors2classify on training and test vectors
##--------------------------------------------------
function malletVec2Classify(){
	vectors2classify --training-file ${outputDir}/"final_train.vectors" --testing-file ${outputDir}/"final_test.vectors" --trainer MaxEnt --output-classifier ${outputDir}/"me_model" --report train:accuracy train:confusion test:accuracy test:confusion >${outputDir}/me_model.stdout 2>${outputDir}/me_model.stderr

}

##--------------------------------------------------
## Execute Mallet classify-file
##--------------------------------------------------
function malletClassify(){
	mallet classify-file --input ${outputDir}/${FINAL_TEST_VECTORS} --classifier ${outputDir}/"me_model" --output ${outputDir}/"sys_out"

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
createMaxEntTagger
malletImport
malletVec2Classify
malletClassify
end=$SECONDS
echo "Total Execution Time: $((end-start)) seconds"
exit 0