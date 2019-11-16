#!/usr/bin/python3
"""#### LING 570: Homework #8 - Ryan Timbrook ############
Author: Ryan Timbrook
Date: 11/22/2018
Q3: Write create_vectors.sh
    - This python script creates training and test vectors from several directories of documents.
    - This script has the same function as "mallet import-dir"
    
Format: command line: create_vectors.sh train_vector_file test_vector_file ratio dir1 dir2 ...
        
Input: ratio dir1 dir2 ...
    -***Note: The command line should include one or more directories
    -Ratio is the portion of the training data 

Output File: train_vector_file test_vector_file
   -Format: Same format as output from Q2
       -one line with the format as:
           -instanceName targetLabel f1 v1 f2 v2 ... (standard format)
           -label f1:v1 f2:v2 ... (svmlight format)
            
From Command line, Run as: ./create_vectors.sh train.vectors.txt test.vectors.txt ratio dir1 dir2 dir3
"""

import sys, time, re, os, fnmatch
from collections import Counter
from optparse import OptionParser

#import proc_file from Q2
import proc_file

#---- GLOBALS -----------------------------------------#
isTest = False
isLocal = False
cmdArgs = []

LOCAL_PATH = "./570/"
REMOTE_PATH = "/dropbox/18-19/570/"

##------------------------------------------------------------------------
# Main Procedural Function
##------------------------------------------------------------------------
def main():
    if isTest: print("main: Entering")
    trainVectors = ""
    testVectors = ""
    ratio = 0.0
    dir1 = ""
    dir2 = ""
    dir3 = ""
    dirList = [] #format tuple (dir,classLabel)
    path = ""
    classLabel = "" #is the basename of an input directory
    
    if isLocal:
        trainVectors="train.vectors.txt"; testVectors="test.vectors.txt"; ratio=float("0.9"); dir1="hw8/20_newsgroups/talk.politics.guns"; dir2="hw8/20_newsgroups/talk.politics.mideast"; dir3="hw8/20_newsgroups/talk.politics.misc"
        dirList.append((dir1,dir1.split("/")[2])); dirList.append((dir2,dir2.split("/")[2])); dirList.append((dir3,dir3.split("/")[2]))
        path = LOCAL_PATH
    else:
        trainVectors=cmdArgs[0]; testVectors=cmdArgs[1]; ratio=float(cmdArgs[2])
        tempDirList = cmdArgs[3:]
        for d in tempDirList:
            c = d.split("/")[-1]
            dirList.append((d,c))
        path = ""
    if isTest: print("search dir list:[{0}]".format(dirList))
    if isTest: print("trainVectorFileName:[{0}] testVectorFileName:[{1}] ratio:[{2}]".format(trainVectors,testVectors,ratio))
    
    
    try:
        
        o_train = open(trainVectors,'wb')
        o_test = open(testVectors,'wb')
        
        #loop through directory's to process
        for dir in dirList:
            classLabel = dir[1]
            dataFiles = getFilesFromPath(path+dir[0])
            trainingFiles, testFiles = splitDataTrainingTest(dataFiles,ratio)
            processTrainingDataFiles(o_train,path+dir[0],trainingFiles,classLabel)
            processTestDataFiles(o_test, path+dir[0], testFiles, classLabel)
    
    except Exception as e:
        sys.stderr.write("Caught Exception in Main, Error Message:[{0}]".format(str(e)))  
        
    finally:
        o_train.flush()
        o_train.close()
        o_test.flush()
        o_test.close()
        
    
    if isTest: print("main: Exiting")
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Calls functions from proc_file.py to perform generation and printing tasks
# Generate Feature Vector
# Steps:
#    1: skip header
#    2: replace all chars that are not [a-zA-Z] with whitespace
#    3: lowercase all remaining chars
#    4: break text into token by whitespace, each token becomes a feature
#    5: calculate value of a feature; which is the number of occurrences of the token in input_file
##------------------------------------------------------------------------
def processTrainingDataFiles(o_train, path, training, classLabel):
    
    for t in training:
        instanceName, targetLabel, featureVectors = proc_file.generateFeatureVector(path+"/"+t,classLabel)
        printFeatureVector(o_train,targetLabel,featureVectors,instanceName)
    
    o_train.flush()
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Calls functions from proc_file.py to perform generation and printing tasks
# Generate Feature Vector
# Steps:
#    1: skip header
#    2: replace all chars that are not [a-zA-Z] with whitespace
#    3: lowercase all remaining chars
#    4: break text into token by whitespace, each token becomes a feature
#    5: calculate value of a feature; which is the number of occurrences of the token in input_file
##------------------------------------------------------------------------
def processTestDataFiles(o_test, path, testing, classLabel):
    
    for t in testing:
        instanceName, targetLabel, featureVectors = proc_file.generateFeatureVector(path+"/"+t,classLabel)
        printFeatureVector(o_test,targetLabel,featureVectors,instanceName)
        
    o_test.flush()   
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Print Feature Vector
# Output has only one line with format:
#     >>>instanceName targetname f1 v1 f2 v2 ...
# feature vector pairs as: (featname, value) 
##------------------------------------------------------------------------
def printFeatureVector(outputFile,targetLabel,featureVectors,instanceName=None,format="standard"):
    output = ""
    
    if format == "standard":
        outputHead = instanceName+" "+targetLabel
        outputFeat = ' '.join( ["{0} {1}".format(k,v) for k,v in featureVectors.items() ] )
        output = "{0} {1}\n".format(outputHead,outputFeat)
        outputFile.write(output.encode())
    else:
        outputFeat = ' '.join( ["{0}:{1}".format(k,v) for k,v in featureVectors ] )
        output = targetLabel+" "+outputFeat
        outputFile.write(output.encode())

##------------------------------------------------------------------------
# File IO - Helper Functions - Gets  file locations
##------------------------------------------------------------------------
def getFilesFromPath(path):
    dataFiles = []
    
    dataFiles = next(os.walk(path))[2]#get only files
    #adding sorted due to issues when fetching files on padas from dropbox. list returns out of order
    dataFiles = sorted(dataFiles)
    if isTest: print("Top 5 data files in path:[{0}]\n[{1}]".format(path,dataFiles[:5]))
    
    return dataFiles    
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Split data into training and test
##------------------------------------------------------------------------
def splitDataTrainingTest(dataFiles,ratio):
    if isTest: print("Top 5 data files: {0}".format(dataFiles[:5]))

    
    trainingFilesCnt = int(len(dataFiles)*ratio)
    trainingFiles = dataFiles[:trainingFilesCnt]
    testFiles = dataFiles[trainingFilesCnt:]
    
    if isTest: print("Top 5 Training Data Files: {0}".format(trainingFiles[:5]))
    if isTest: print("Top 5 Test Data Files: {0}".format(testFiles[:5]))
    
    return trainingFiles, testFiles
##------------------------------------------------------------------------
   
##------------------------------------------------------------------------
# Execute Main Function
##------------------------------------------------------------------------
if __name__ == "__main__":
    t0 = time.time()
    if isTest: print("Number of command line arguments:{0}".format(len(sys.argv)));
    #remove program file name from input command list
    sys.argv.remove(sys.argv[0])
    if len(sys.argv) > 0:
        for arg in sys.argv:
            if isTest: print("argument:{0}".format(arg))
            cmdArgs.append(arg.strip())
    main()
    t1 = time.time()
    duration = t1-t0
    if isTest: print("Total processing time:{0:0.10f}".format(duration))