#!/usr/bin/python
"""#### LING 570: Homework #1 - Ryan Timbrook ############
    Vocabulary Tool
Author: Ryan Timbrook
Date: 10/4/2018

First Running of VOC tool:
INPUT FILE COMMAND ARG: ex2_tok
OUTPUT FILE COMMAND ARG: ex2_tok_voc

Second Running of VOC tool:
INPUT FILE COMMAND ARG: ex2
OUTPUT FILE COMMAND ARG: ex2_voc

"""

import os, sys, re, collections

#Local Test
isTest = False
isLocal = False

exToken = collections.namedtuple('Token',['token','freq'])
outputFile = None
######################################
# Main Procedural Function
######################################
def main(argv):
    if argv is None:
        argv = sys.argv
    c = 0
    for arg in argv:
        if isTest: print("hw1_voc.main: argv%d[%s]"%(c,argv[c]))
        c+=1
    
    #Check if local test
    if isTest: print(isLocal)
    if isLocal:
        input1 = "ex2"; output1 = "ex2.voc"
    else:
        input1 = argv[1]; output1 = argv[2]
        
    tokenCount = 0
    words = []
    wordDict = collections.defaultdict()
    #Open output file for writing
    outputFile = open(output1,'a')
    #Open doc to tokenize
    tokFile = open(input1,'r')
    try:
        
        words = cleanDoc(tokFile).split(' ')
        
        #Tally number of instances of each word
        for word in words:
            if word.strip() is not '':   
                if word not in wordDict: 
                    wordDict[word] = 1
                    continue
                else:
                    wordDict[word] += 1
                tokenCount +=1
            else:
                if isTest: print("TEST")
        
        
        #Sort the words by frequency in descending order and print the result out
        wordDict = sorted(wordDict.items(),key=lambda x:x[1],reverse=True)
        for wordFreq in wordDict:
            if isTest: print("hw1_voc.main: %s \t %d"%(wordFreq[0],wordFreq[1]))
            outputFile.write(str(wordFreq[0]));outputFile.write(' ');outputFile.write(str(wordFreq[1]))
            outputFile.write('\n')
    
    except IOError as io:
        print("*****ERROR***** Caught IOError %s"%str(io))
    
    print("hw1_voc.main: #### Unique Token Count Total[%d] | Total Token Count[%d] ####"%(len(wordDict),tokenCount))
    # Fluch and close output file
    outputFile.flush()
    outputFile.close()

def cleanDoc(doc):
    if isTest: print("hw1_voc.cleanDoc: Entering... ")
    docLines = []
    for line in doc:
        if isTest: print("hw1_voc.cleanDoc: line -> %s "%line)
        line = re.sub(r'\n',' ',line)
        words = line.split(' ')
        
        for word in words:
            if word == '\n': word = ' '
            if word!='':docLines.append(word)
    
    if isTest: print("hw1_voc.cleanDoc: Exiting... ")
    return ' '.join(docLines)
    


##################################################################################################################
# Execute Main Function
##################################################################################################################
if __name__ == "__main__": main(sys.argv)
