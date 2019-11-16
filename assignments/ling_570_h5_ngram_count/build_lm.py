#!/usr/bin/python3
"""#### LING 570: Homework #5 - Ryan Timbrook ############
Author: Ryan Timbrook
Date: 11/1/2018
Q2: Write build_lm

This shell script executes a python program that builds an LM using ngram counts:

Format: command line: build_lm.sh ngram_count_file lm_file
Input File: ngram_count_file (produced as output from Q1, ngram_count.py)
Output File: lm_file (follows ARPA format)

**Special Instructions: 
    -For prob and lgprob numbers on each line, truncate to ten places after the decimal
    -DO NOT USE SMOOTHING for the probability distributions

Ran as: 
    $ ./build_lm.sh ngram_count_file lm_file

"""

import sys, re, math, time
from collections import defaultdict
from collections import OrderedDict


#---- GLOBALS -----#
isTest = True
isLocal = False
cmdArgs = []

##------------------------------------
# Main Procedural Function
##------------------------------------
def main():
    if isTest: print("main: Entering")
    
    if isLocal:
        ngram_count_file= "wsj_sec0_19.ngram_count"; lm_file="wsj_sec0_19.lm"
        #ngram_count_file= "hw5/examples/ngram_count_ex"; lm_file="wsj_sec0_19.lm"
    else:
        ngram_count_file=cmdArgs[0]; lm_file=cmdArgs[1]
    
    #open output lm file for writing
    o_lm = open(lm_file,'w')
    
    #readin ngram count file produced from Q1 ngram_count program
    ngramCountFile = open(ngram_count_file, 'rt')
    
    try:
        unigrams = defaultdict()
        bigrams = defaultdict()
        trigrams = defaultdict()
        
        tallies = tallyNGrams(ngramCountFile,unigrams,bigrams,trigrams,o_lm)
        
        unigrams = sortDictByValue(unigrams, reverse=True)
        bigrams = sortDictByValue(bigrams, reverse=True)
        trigrams = sortDictByValue(trigrams, reverse=True)
        
        calcProbabilities(tallies,unigrams,bigrams,trigrams,o_lm)
        
        
    finally:
        ngramCountFile.close()
        o_lm.close()
        
    if isTest: print("main: Exiting")

##------------------------------------------------------------------------
# Util Function: gets totals for each of the ngrams
##------------------------------------------------------------------------
def tallyNGrams(ngramCountFile,unigrams,bigrams,trigrams,o_lm):
    u_tokens = 0
    u_total = 0
    b_tokens = 0
    b_total = 0
    t_tokens = 0
    t_total = 0
    tallyDict = {'unigrams':(),'bigrams':(),'trigrams':()}
   
    for line in ngramCountFile.readlines():
        line = line.strip('\n')
        tokens = re.split("\\s+", line)
        
        #unigrams
        if len(tokens) == 2:
            u_tokens += 1
            u_total += int(tokens[0])
            updateDict(tokens,unigrams)
            tallyDict['unigrams'] = (u_tokens,u_total)
        #bigrams
        if len(tokens) == 3:
            b_tokens += 1
            b_total += int(tokens[0])
            updateDict(tokens, bigrams)
            tallyDict['bigrams'] = (b_tokens,b_total)
        #trigrams
        if len(tokens) == 4:
            t_tokens += 1
            t_total += int(tokens[0])
            updateDict(tokens, trigrams)
            tallyDict['trigrams'] = (t_tokens,t_total)
    
    
    o_lm.write("\\data\\\n")
    o_lm.write("ngram 1: type={0} token={1}\n".format(u_tokens,u_total))
    o_lm.write("ngram 2: type={0} token={1}\n".format(b_tokens,b_total))
    o_lm.write("ngram 3: type={0} token={1}\n".format(t_tokens,t_total))
    o_lm.flush()
   
    return tallyDict
##------------------------------------------------------------------------
# Util Function: calculate the probability's and log probabilites for ngrams
##------------------------------------------------------------------------
def calcProbabilities(tallies, unigrams, bigrams, trigrams, o_lm):
    
    #unigrams
    o_lm.write("\n\\1-grams:\n")
    uni_tallies = tallies['unigrams']
    for token in unigrams:
        try:
            cnt = unigrams[token]
            prob = float(cnt/uni_tallies[1])
            lgprob = math.log10(prob)
        
            if not probZero(prob):
                o_lm.write("{0} {1:0.10f} {2:0.10f} {3}\n".format(cnt, prob, lgprob, token))
        except ValueError:
            pass
    #bigrams
    o_lm.write("\n\\2-grams:\n")
    bi_tallies = tallies['bigrams']
    for token in bigrams:
        token = token.strip()
        tokens = re.split("\\s+", token)
        uniCnt = unigrams[tokens[0]] 
        try:
            cnt = bigrams[token]
            prob = float(cnt/uniCnt)
            lgprob = math.log10(prob)
            
            if not probZero(prob):
                o_lm.write("{0} {1:0.10f} {2:0.10f} {3}\n".format(cnt, prob, lgprob, token))
        except ValueError:
            pass
    #trigrams
    o_lm.write("\n\\3-grams:\n")
    tr_tallies = tallies['trigrams']
    for token in trigrams:
        token = token.strip()
        tokens = re.split("\\s+", token)
        biCnt = bigrams[tokens[0]+" "+tokens[1]]
        try:
            cnt = trigrams[token]
            prob = float(cnt/biCnt)
            lgprob = math.log10(prob)
            
            if not probZero(prob):
                o_lm.write("{0} {1:0.10f} {2:0.10f} {3}\n".format(cnt, prob, lgprob, token))
        except ValueError:
            pass
    
    o_lm.write("\n\\end\\")
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util Function, Add elements to ngram dictionaries
##------------------------------------------------------------------------      
def updateDict(token,ngram):
    
    freq = token[0]
    newToken = ""
    for e in token[1:]:
        newToken += ''.join(e)+" "
    #print(newToken)
    newToken = newToken.strip()
    ngram[newToken] = int(freq)

##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util Function, Sort Dictionary by Value, return sorted tuple (token, frequency)
##------------------------------------------------------------------------
def sortDictByValue(ngram,reverse=False):
    newDict = OrderedDict()
    
    sortedByValue = sorted(ngram.items(), key=lambda x: x[1], reverse=reverse)
    
    for e in sortedByValue:
        newDict[e[0]] = e[1]
    
    return newDict
         
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util Function, Sort Dictionary by Value, return sorted tuple (token, frequency)
##------------------------------------------------------------------------
def probZero(prob):
    if prob < float(0.0000000001):
        if isTest: print("probZero True: {0}".format(prob))
        return True
    else:
        return False

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