#!/usr/bin/python3
"""#### LING 570: Homework #6 - Ryan Timbrook ############
Author: Ryan Timbrook
Date: 11/8/2018
Q1: Write create_2gram_hmm.sh

This python program that:
    -takes annotated training data as input and creates an HMM for a Bigram POS tagger
    -NO SMOOTHING
Format: command line: cat training_data | create_2gram_hmm.sh output_hmm
Input File: training_data as std input
    -Format: "w1/t1 ... wn/tn" (wsj_sec0.word_pos)    
Output File: output_hmm ()
   -Format: 
        -prob and lgprob -> truncate to 10 digits past decimal (0.0000000001)
        -sort probabilities alphabetically on the 1st field (state or from_state) first
        -then, for lines with same 1st field, sort on the second field (symbol)
            
From Command line, Run as: 
    $ cat wsj_sec0.word_pos | ./create_2gram_hmm.sh q4/2g_hmm
"""
import sys, re, time, operator, math
from collections import defaultdict, Counter, OrderedDict

#---- GLOBALS -----------------------------------------#
isTest = True
isLocal = True
cmdArgs = []
POS_BOS_TAG = "BOS"
POS_EOS_TAG = "EOS"
BOS_SENTENCE_TAG = "<s>"
EOS_SENTENCE_TAG = "</s>"

##------------------------------------------------------------------------
# Main Procedural Function
##------------------------------------------------------------------------
def main():
    if isTest: print("main: Entering")
        
    if isLocal:
        training_data= "hw6/examples/wsj_sec0.word_pos"; output_hmm="q4/2g_hmm"
    else:
        output_hmm=cmdArgs[0]
    
    #when testing local get input from examples file, else read from stdin
    if not isLocal:
        trainingDataLines = sys.stdin.readlines()
    else:
        with open(training_data,'rt') as td:
            trainingDataLines = td.readlines()
    if isTest: print("Total Lines in Training Data Set:[{0}]".format(len(trainingDataLines)))
    
    #open output file for writing
    o_hmm = open(output_hmm,'w')
    
    header = OrderedDict()
    initProbabilities = []
    transitionProbabilities = []
    emissionProbabilities = []
    words = {} #output symbols
    POSs = {} #states
    wordsPOSs = {}
    transitions = {}
    
    try:
        initialize(header, initProbabilities)
        preProcessTrainingData(trainingDataLines,header,words,POSs,wordsPOSs,transitions)
        calcTrainingDataMetrics(words,POSs,wordsPOSs,transitions,initProbabilities,transitionProbabilities,emissionProbabilities)
        header['init_line_num'] = len(initProbabilities)
        
        outputHMMHeader(o_hmm,header)
        outputHMMInit(o_hmm,initProbabilities)
        outputHMMTransition(o_hmm,transitionProbabilities)
        outputHMMEmission(o_hmm,emissionProbabilities)
        
    finally:
        o_hmm.flush()
        o_hmm.close()
        

    if isTest: print("main: Exiting")
    
##------------------------------------------------------------------------
# initialize
##------------------------------------------------------------------------
def initialize(header, initProbabilities):
    header['state_num'] = 0
    header['sym_num'] = 0
    header['init_line_num'] = 1
    header['trans_line_num'] = 0
    header['emiss_line_num'] = 0 
    
    #state with initial probability
    prob = 1.0
    lgprob=math.log10(prob)
    initProbabilities.append(("BOS",1,lgprob))
    
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# pre-process input training data
##------------------------------------------------------------------------
def preProcessTrainingData(trainingDataLines,header,words,POSs,wordsPOSs,transitions):
    
    sentenceCount = 0
    #For bigram taggers, each state corresponds to a POS tag, BOS or EOS
    for sent in trainingDataLines:
        sentenceCount+=1
        sent = sent.replace('\n','')
        sent = sent.strip()
        #configure the BOS and EOS markers
        init = POS_BOS_TAG
        wordTags = sent.split()
        wordTags.insert(0,"{0}/{1}".format(POS_BOS_TAG,BOS_SENTENCE_TAG))
        wordTags.append("{0}/{1}".format(EOS_SENTENCE_TAG,POS_EOS_TAG))
        #print(wordTags)
        
        #initialize BOS
        thisPOS=init
        priorPOS=init
        word=BOS_SENTENCE_TAG
        wordTagPair=(thisPOS,word)
        
        updateDictCount(word,words)
        updateDictCount(thisPOS, POSs)
        updateDictCount(wordTagPair,wordsPOSs)
        
        #each word/pos in sentence
        for wt in wordTags[1:]:
            #[word,pos]
            tokens = wt.split('/')
            tok = tokens[0]
            #fix the word split if word was a fraction ex: 2/3 as a CD, write as 2\/3/CD
            for e in range(1,len(tokens)-1):
                #tok = tok + "\/" + tokens[e]
                tok += "/" + tokens[e]
            toktwo = tokens[-1]
            
            priorPOS = thisPOS
            thisPOS = toktwo
            wordTagPair=(thisPOS,tok)
            transitionPair=(priorPOS,thisPOS)#each state corresponds to a POS tag
            
            updateDictCount(tok,words)
            updateDictCount(thisPOS, POSs)
            updateDictCount(wordTagPair,wordsPOSs)
            updateDictCount(transitionPair,transitions)
        ##-- End loop over word/pos pairs in a given sentence
    
    ##-- End loop over all of the sentences of the training data set
    #update header with count data
    header['state_num'] = len(POSs)
    header['sym_num'] = len(words)
    #header['init_line_num'] = len(initProbabilities)
    header['trans_line_num'] = len(transitions)
    header['emiss_line_num'] = len(wordsPOSs)
          
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# calculate training data counts
##------------------------------------------------------------------------
def calcTrainingDataMetrics(words,POSs,wordsPOSs,transitions,initProbabilities,transitionProbabilities,emissionProbabilities):
    
    #get the counts
    posCnt = sum(Counter(POSs).values())
    wordsCnt = sum(Counter(words).values())
    wordPairCnt = sum(Counter(wordsPOSs).values())
    transCtn = sum(Counter(transitions).values())
    
    #transition index
    #TODO: Come back to this
    transIndex = {}
    for e in POSs:
        transIndex[e] = 0
        for transition in transitions:
            if transition[0] == e:
                transIndex[e] += 1
    ##-- end loop
    
    #get transition probabilities
    ## prob=P(to_state|from_state)
    for t in transitions:
        from_state = t[0]
        to_state = t[1]
        
        cntFromState_ToState = float(transitions[t])
        cntFromState = float(POSs[from_state])
        prob = float(cntFromState_ToState / cntFromState)
        lgprob = math.log10(prob)
        transitionProbabilities.append((from_state,to_state,prob,lgprob))
    
    ##state-emission HMM probabilities
    ## prob=P(symbol|state)
    for p in wordsPOSs:
        state = p[0]
        symbol = p[1]
        probB = float(wordsPOSs[p]) / float(wordPairCnt)
        probS = float(POSs[state]) / float(posCnt)
        prob = float(probB/probS)
        lgprob = math.log10(prob)
        emissionProbabilities.append((state, symbol, prob, lgprob))
    
    
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util FunctionProcess word/tag split
# returns a (wi,ti)
##------------------------------------------------------------------------
def splitWordTag(wordTag,delimiter="/"):
    wtTokens = wordTag.split(delimiter)
    w = wtTokens[0]
    for e in range(1,len(wtTokens)-1):
        w += "/" + wtTokens[e]
    t = wtTokens[-1]
    
    return w,t
##------------------------------------------------------------------------


##------------------------------------------------------------------------
# Util Function, update dictionary used for storing count values
##------------------------------------------------------------------------      
def updateDictCount(key,dict):
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 1
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# post-process output HMM Header
##------------------------------------------------------------------------
def outputHMMHeader(o_hmm,header):
    for k,v in header.items():
        o_hmm.write("{0}={1}\n".format(k,v))
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# post-process output HMM init
##------------------------------------------------------------------------
def outputHMMInit(o_hmm,init):
    o_hmm.write("\n{0}\n".format("\\init"))

    #state prob lg_prob
    sortedInit = sorted(init,key=lambda tup:(tup[0]))
    ## prob=\pi(state), lg_prob=lg(prob)
    for state in sortedInit:
        o_hmm.write("{0}    {1:0.10f}    {2:0.10f}\n".format(state[0],state[1],state[2]))
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# post-process output HMM transitions
##------------------------------------------------------------------------
def outputHMMTransition(o_hmm,transitions):
    o_hmm.write("\n{0}\n".format("\\transition"))
    
    #sort probabilities by first field (from_state) then by second field (to_state)
    sortedTransitions = sorted(transitions,key=lambda tup:(tup[0],tup[1]))
    
    #from_state to_state prob lg_prob
    ## prob=P(to_state | from_state)
    for trans in sortedTransitions:
        o_hmm.write("{0}    {1}    {2:0.10f}    {3:0.10f}\n".format(trans[0],trans[1],trans[2],trans[3]))
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# post-process output HMM emission
##------------------------------------------------------------------------
def outputHMMEmission(o_hmm,emissions):
    o_hmm.write("\n{0}\n".format("\\emission"))
    
    #sort probabilities by first field (from_state) then by second field (to_state)
    sortedEmissions = sorted(emissions,key=lambda tup:(tup[0],tup[1]))
    #state symbol prob lg_prob
    ## prob=P(symbol | state)
    for emis in sortedEmissions:
        o_hmm.write("{0}    {1}    {2:0.10f}    {3:0.10f}\n".format(emis[0],emis[1],emis[2],emis[2]))
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