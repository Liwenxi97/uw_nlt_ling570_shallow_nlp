#!/usr/bin/python3
"""#### LING 570: Homework #5 - Ryan Timbrook ############
Author: Ryan Timbrook
Date: 11/1/2018
Q1: Write ngram_count

This python script collects unigrams, bigrams, and trigrams:

Format: command line: ngram_count.sh training_data ngram_count_file
Input File: training_data
Output File: ngram_count_file

-Format of the training data:
    w1 w2 ... w_n; one sentence per line
-Format of the ngram_count file is: 
    count word1 ... word_k
    -As output order matters:
        1st: unigrams
        2nd: bigrams
        3rd: trigrams
    -As output, n-gram chunks are sorted by frequency in descending order.
        -if frequency's are the same, sort by ngrams alphabetically
    -BOS as <s>
    -EOS as </s>
    
Ran as: 
    $ ./ngram_count.sh training_data ngram_count_file


"""

import sys, re, time, operator
from collections import defaultdict, Counter, OrderedDict


#---- GLOBALS -----------------------------------------#
isTest = True
isLocal = True
cmdArgs = []

##------------------------------------------------------------------------
# Main Procedural Function
##------------------------------------------------------------------------
def main():
    if isTest: print("main: Entering")
        
    if isLocal:
        #training_data= "hw5/examples/wsj_sec0_19.word"; ngram_count_file="wsj_sec0_19.ngram_count"
        training_data= "hw5/examples/training_data_ex"; ngram_count_file="wsj_sec0_19.ngram_count"
    else:
        training_data=cmdArgs[0]; ngram_count_file=cmdArgs[1]
    
    #open output ngram count file for writing
    f_ngram = open(ngram_count_file,'w')
    
    #readin training data
    trainingDataFile = open(training_data, 'rt')
    
    try:
        unigrams = defaultdict()
        bigrams = defaultdict()
        trigrams = defaultdict()
        
        countNGrams(trainingDataFile,unigrams,bigrams,trigrams)
        
        #sortPrint(unigrams,f_ngram)
        printSortSubDictChunks(unigrams,f_ngram)
        #sortPrint(bigrams,f_ngram)
        printSortSubDictChunks(bigrams,f_ngram)
        #sortPrint(trigrams,f_ngram)
        printSortSubDictChunks(trigrams,f_ngram)
        
    finally:
        trainingDataFile.close()
        f_ngram.close()
        
    if isTest: print("main: Exiting")
    
##------------------------------------------------------------------------
# Count ngrams
##------------------------------------------------------------------------        
def countNGrams(trainingDataFile, unigrams, bigrams, trigrams):
    
    for line in trainingDataFile.readlines():
        line = line.strip('\n')
        line = "<s> "+line+" </s>"
        tokens = re.split("\\s+", line)
        
        #unigrams
        for tok in tokens:
            updateDict(tok,unigrams)
        #-- end unigram count--#
        
        #bigrams
        i = 1
        while i < len(tokens):
            token = ""
            j = i-1
            while j <= i:
                token += tokens[j] + " "
                j+=1
            updateDict(token.strip(),bigrams)  
            i+=1   
        #-- end bigrams count --#
        
        #trigrams
        i = 2
        while i < len(tokens):
            token = ""
            j = i-2
            while j <= i:
                token += tokens[j] + " "
                j+=1
            updateDict(token.strip(),trigrams)
            i+=1
        #-- end trigrams count --#
        
##------------------------------------------------------------------------
# Util Function, Add elements to output dictionary
##------------------------------------------------------------------------      
def updateDict(token,ngram):
    if token in ngram:
        ngram[token] += 1
    else:
        ngram[token] = 1
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# sort and print ngrams
##------------------------------------------------------------------------ 
def sortPrint(ngram,o_file):
    #sort by frequency in descending order
    #if frequency's are equal, sort ngrams alphabetically
   
    
    #sort by value returns a sorted listed of tuples (token, frequency)
    ngram = sortDictByValue(ngram, reverse=True)
    
    for e in ngram:
        o_file.write("{0} {1}\n".format(e[1],e[0]))
            
            
        
    
##------------------------------------------------------------------------   
    
##------------------------------------------------------------------------
# Util Function, Sort Dictionary by Value, return sorted tuple (token, frequency)
##------------------------------------------------------------------------
def sortDictByValue(ngram,reverse=False):
    return sorted(ngram.items(), key=lambda x: x[1], reverse=reverse)
    #return OrderedDict(sorted(ngram.items(), key=lambda x: x[1],reverse=reverse))
         
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util Function, Sort Dictionary by key, return sorted dictionary object
##------------------------------------------------------------------------
def sortDictByKey(ngram,reverse=False):
    return {k:v for k,v in sorted(ngram.items(),reverse=reverse)}
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util Function, Sort ngram chunks by value
##------------------------------------------------------------------------
def printSortSubDictChunks(sgram,o_file):
    #sort by value returns a sorted listed of tuples (token, frequency)
    sgram = sortDictByValue(sgram, reverse=True)
    
    
    i = 0
    while i<len(sgram)-1:
        tup1 = sgram[i]
        tup2 = sgram[i+1]
        if tup1[1] == tup2[1]: 
            subNgram = []
            match = True
            freqMatch = tup1[1]
            j=i
            while match and j<=len(sgram)-2:
                tup1 = sgram[j]
                tup2 = sgram[j+1]
                #if isTest: print("sub-chunch-match: freq:{0} token1:{1} token2:{2} index:{3}-{4}".format(freqMatch,tup1[0],tup2[0],i,j))
                if tup1[1] == tup2[1]:
                    if not tup1 in subNgram:
                        subNgram.append(tup1)
                    if not tup2 in subNgram:
                        subNgram.append(tup2)
                else:
                    #sub grouping complete, sort sublist and update master dictionary, i=start range, j=end range
                    #sgram= updateNGram(sgram,subNgram,(i,j))
                    subNgram = sorted(subNgram, key=operator.itemgetter(0))
                    #
                    for s in subNgram:
                        o_file.write("{0} {1}\n".format(s[1],s[0]))
                    subNgram = []
                    match = False
                j+=1
            if len(subNgram) > 0:
                #sgram= updateNGram(sgram,subNgram,(i,j))
                subNgram = sorted(subNgram, key=operator.itemgetter(0))
                for s in subNgram:
                        o_file.write("{0} {1}\n".format(s[1],s[0]))
            i=j
        else:
            o_file.write("{0} {1}\n".format(tup1[1],tup1[0]))  
            i+=1
    
    

##------------------------------------------------------------------------
# Util Function, Sort ngram chunks by value
##------------------------------------------------------------------------
def sortSubDictChunks(sgram):
    i = 0
    while i<len(sgram)-1:
        tup1 = sgram[i]
        tup2 = sgram[i+1]
        if tup1[1] == tup2[1]: 
            subNgram = []
            match = True
            freqMatch = tup1[1]
            j=i
            while match and j<=len(sgram)-2:
                tup1 = sgram[j]
                tup2 = sgram[j+1]
                #if isTest: print("sub-chunch-match: freq:{0} token1:{1} token2:{2} index:{3}-{4}".format(freqMatch,tup1[0],tup2[0],i,j))
                if tup1[1] == tup2[1]:
                    if not tup1 in subNgram:
                        subNgram.append(tup1)
                    if not tup2 in subNgram:
                        subNgram.append(tup2)
                else:
                    #sub grouping complete, sort sublist and update master dictionary, i=start range, j=end range
                    sgram= updateNGram(sgram,subNgram,(i,j))
                    subNgram = []
                    match = False
                j+=1
            if len(subNgram) > 0:
                sgram= updateNGram(sgram,subNgram,(i,j))
            i=j
        else:    
            i+=1
    
    return sgram

##------------------------------------------------------------------------
# Util Function, update ngram by replacing chunks in sorted order
##------------------------------------------------------------------------
def updateNGram(ngram, subNgram, indexRange):
    subNgram = sorted(subNgram)
    i = indexRange[0]
    for sub in subNgram:
        ngram[i] = sub
        i+=1
    
    return ngram
##------------------------------------------------------------------------


##------------------------------------
# Execute Main Function
##------------------------------------
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