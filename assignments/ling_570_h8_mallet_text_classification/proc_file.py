#!/usr/bin/python3
"""#### LING 570: Homework #8 - Ryan Timbrook ############
Author: Ryan Timbrook
Date: 11/22/2018
Q2: Write proc_file.sh
    - This python script processes a document and prints out the feature vectors
    
Format: command line: proc_file.sh input_file targetlabel output_file
 - 
Input File: input_file is a text file (e.g., input_ex)
    -Format: 
            - 
Output File:
   -Format: One line with the format: "instanceName targetLabel f1 v1 f2 v2 ...
        -instanceName is the filename of the input_file
        -targetLabel is the second argument of the command line
            
From Command line, Run as: ./proc_file.sh $exDir/input_ex c1 output_ex
"""

import sys, time, re, os, fnmatch
from collections import Counter, OrderedDict

#---- GLOBALS -----------------------------------------#
isTest = False
isLocal = False
cmdArgs = []

LOCAL_PATH = "./570/"
REMOTE_PATH = "../opt/dropbox/17-18/570/"

##------------------------------------------------------------------------
# Main Procedural Function
##------------------------------------------------------------------------
def main():
    if isTest: print("main: Entering")
        
    if isLocal:
        input_ex="hw8/examples/input_ex"; targetLabel="c1"; output_ex="output_ex"
    else:
        input_ex=cmdArgs[0]; targetLabel=cmdArgs[1]; output_ex=cmdArgs[2]
    
    outputFile = None
    
    try:
        #open output file for writing
        outputFile = open(output_ex,'wb')
        
        instanceName, targetLabel, featVec = generateFeatureVector(input_ex, targetLabel)
        printFeatureVector(outputFile,targetLabel,featVec,instanceName)
        
    finally:
        outputFile.flush()
        outputFile.close()
        
    if isTest: print("main: Exiting") 
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Generate Feature Vector
# Steps:
#    1: skip header
#    2: replace all chars that are not [a-zA-Z] with whitespace
#    3: lowercase all remaining chars
#    4: break text into token by whitespace, each token becomes a feature
#    5: calculate value of a feature; which is the number of occurrences of the token in input_file
# return tuple (instanceName targetLabel featureVector)
##------------------------------------------------------------------------
def generateFeatureVector(input_ex, classLabel):
    outFeatureVector = Counter()
    instanceName = input_ex.split("/")[-1]
    targetLabel = classLabel
    
    
    #open and readin input file
    with open(input_ex,'rb') as in_f:
        inputExLines = in_f.readlines()
    if isTest: print("Instance Name:[{0}], TargetLabel:[{1}] Total lines in inputExLines file:[{2}]".format(instanceName,classLabel,len(inputExLines)))
    
    #get index, skip header
    lineIndex = 0
    for line in inputExLines:
        if not line == b'\n':
            lineIndex += 1
            continue
        else:
            break
        
    lines = inputExLines[lineIndex+1:] #skip header
    if isTest: print("non-header lines count:[{0}]".format(len(lines)))
    
    #replace all characters that are not [a-zA-Z] with whitespace
    lines = [ re.sub(b'[^a-zA-Z]',b' ',l) for l in lines]
    #lowercase all remaining char
    lines = [l.lower() for l in lines]
    #break text into token by whitespace - each token is a feature
    tokLines = [ re.split(b'\\s+',l) for l in lines]
    for t in tokLines:
        tokens = [e.decode() for e in t]
        while True:
            if '' in tokens:
                tokens.remove('')
            else:
                break
            
        #calculate feature value - frequency of occurances
        outFeatureVector.update(Counter(tokens))
        
    fv = OrderedDict(sorted(outFeatureVector.items()))
    
    return instanceName, targetLabel, fv
    
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