#!/usr/bin/python3
"""#### LING 570: Homework #6 - Ryan Timbrook ############
Author: Ryan Timbrook
Date: 11/8/2018
Q2: Write create_3gram_hmm.sh

This python program that:
    -takes annotated training data as input and creates an HMM for a Trigram POS tagger
    -WITH SMOOTHING
Format: command line: cat training_data | create_3gram_hmm.sh output_hmm l1 l2 l3 unk_prob_file
Input File: training_data as std input
    -Format: "w1/t1 ... wn/tn" (wsj_sec0.word_pos)
Input File: unk_prob_file (used to smooth P(word | tag)
    -Format: "tag prob"
        -prob -> P(< unk > | tag)
l1,l2,l3 are lambda's used in interpolation
Output File: output_hmm (same format as Q1)
   -Format: 
        -prob and lgprob -> truncate to 10 digits past decimal (0.0000000001)
        -sort probabilities alphabetically on the 1st field (state or from_state) first
        -then, for lines with same 1st field, sort on the second field (symbol)
        
            
From Command line, Run as: 
    $ cat wsj_sec0.word_pos | ./create_3gram_hmm.sh q4/3g_hmm_0.1_0.1_0.8 0.1 0.1 0.8 unk_prob_sec22
    $ cat wsj_sec0.word_pos | ./create_3gram_hmm.sh q4/3g_hmm_0.2_0.3_0.5 0.2 0.3 0.5 unk_prob_sec22
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
BOS_STATE_MARKER = "BOS_BOS"
EOS_STATE_MARKER = "EOS_EOS"
UNK_WORD_MARKER = "<unk>"
##------------------------------------------------------------------------
# Main Procedural Function
##------------------------------------------------------------------------
def main():
    if isTest: print("main: Entering")
        
    if isLocal:
        #training_data= "hw6/examples/wsj_sec0.word_pos"; output_hmm="q4/3g_hmm_0.1_0.1_0.8"; lam_1=0.1; lam_2=0.1; lam_3=0.8; unk_prob="hw6/examples/unk_prob_sec22"
        training_data= "hw6/examples/wsj_sec0.word_pos"; output_hmm="q4/3g_hmm_0.2_0.3_0.5"; lam_1=0.2; lam_2=0.3; lam_3=0.5; unk_prob="hw6/examples/unk_prob_sec22"
    else:
        output_hmm=cmdArgs[0]; lam_1=cmdArgs[1]; lam_2=cmdArgs[2]; lam_3=cmdArgs[3]; unk_prob=cmdArgs[4]
    
    #when testing local get input from examples file, else read from stdin
    if not isLocal:
        trainingDataLines = sys.stdin.readlines()
    else:
        with open(training_data,'rt') as td:
            trainingDataLines = td.readlines()
    if isTest: print("Total Lines in Training Data Set:[{0}]".format(len(trainingDataLines)))
    
    #open output file for writing
    o_hmm = open(output_hmm,'w')
    
    #open unk_prob
    with open(unk_prob,'rt') as u:
        unks = u.readlines()
    
    header = OrderedDict()
    stateProbabilities = []
    transitionProbabilities = [] #P(Sj|Si)
    emissionProbabilities = [] #P(Wk|Si)
    unkProbs = defaultdict()
    tagCnts = {} #pos tags as key=tag:value=cnt
    wordCnts = {} #output symbols as key=word:value=cnt
    stateCnts = {} #states, contains combined tag's in form TAG1_TAG2 as key=state:value=cnt
    wordTagCnts = {} #word tag combinations key=(tag,word):value=cnt
    initialCnts = {} # 
    transitionCnts = {} # 
    emissionCnts = {} #
    sentenceCnt = 0
    lambdas = {'l1':float(lam_1),'l2':float(lam_2),'l3':float(lam_3)}
    
    try:
        initialize(header,initialCnts,unks,unkProbs)
        #analize training data and group according to trigram model
        preProcessTrainingData(trainingDataLines,header,wordCnts,tagCnts,stateCnts,wordTagCnts,transitionCnts,emissionCnts,sentenceCnt)
        header['init_line_num'] = len(initialCnts)
        #get tally's of the grouped data
        counts = calcTrainingDataCounts(wordCnts,tagCnts,stateCnts,wordTagCnts,initialCnts,transitionCnts,emissionCnts)
        #calculate base probabilities
        calcInitialsProbs(initialCnts,stateProbabilities,counts['initsCnt'])
        states = calcTransitionsProbs(transitionProbabilities,tagCnts,stateCnts,transitionCnts,header,counts['tagCnt'],lambdas)
        calcEmissionsProbs(emissionProbabilities,emissionCnts,unkProbs,tagCnts,wordTagCnts,states,header,counts['emitsCnt'])
        
        #print output HMM
        outputHMMHeader(o_hmm,header)
        outputHMMInit(o_hmm,stateProbabilities)
        outputHMMTransition(o_hmm,transitionProbabilities)
        outputHMMEmission(o_hmm,emissionProbabilities)
        
    finally:
        o_hmm.flush()
        o_hmm.close()

    if isTest: print("main: Exiting")
##------------------------------------------------------------------------

    
##------------------------------------------------------------------------
# initialize
##------------------------------------------------------------------------
def initialize(header, initialCnts,unks,unkProbs):
    header['state_num'] = 0
    header['sym_num'] = 0
    header['init_line_num'] = 1
    header['trans_line_num'] = 0
    header['emiss_line_num'] = 0 
    
    initialCnts[BOS_STATE_MARKER]=1
    
    #load unk_probs to dict
    ## format tag prob, means: P(<unk>|tag)=prob
    for line in unks:
        line = line.replace('\n','')
        line = line.strip()
        tag_prob = line.split()
        unkProbs[tag_prob[0]] = float(tag_prob[1])
    
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# pre-process input training data
##------------------------------------------------------------------------
def preProcessTrainingData(trainingDataLines,header,wordCnts,tagCnts,stateCnts,wordTagCnts,transitionsCnt,emissionCnts,sentenceCnt):    
    #For bigram taggers, each state corresponds to a POS tag, BOS or EOS
    for sent in trainingDataLines:
        sentenceCnt+=1
        sent = sent.replace('\n','')
        sent = sent.strip()
        #split sentence into tokens as word/pos
        wordTags = sent.split()
        
        ##-- Initialize BOS
        #configure the BOS and EOS markers
        wordTags.insert(0,"{0}/{1}".format(BOS_SENTENCE_TAG,POS_BOS_TAG))
        wordTags.append("{0}/{1}".format(EOS_SENTENCE_TAG,POS_EOS_TAG))
        #print(wordTags)
        
        updateDictCount(POS_BOS_TAG, tagCnts)
        updateDictCount(BOS_STATE_MARKER, stateCnts)
        
        #BOS pair <s>/BOS
        pair1 = wordTags[0]
        w1 = pair1.split("/")[0]
        updateDictCount(w1,wordCnts)
        t1 = pair1.split("/")[1]
        updateDictCount(t1, tagCnts)
        
        pair2 = wordTags[1]
        w2,t2 = splitWordTag(pair2)
        
        updateDictCount(w2,wordCnts)
        updateDictCount(t2, tagCnts)
        
        thisState = t1+"_"+t2
        updateDictCount(thisState,stateCnts)
        
        wordTagPair1 = (t1,w1)
        wordTagPair2 = (t2,w2)
        
        updateDictCount(wordTagPair1,wordTagCnts)
        updateDictCount(wordTagPair2,wordTagCnts)
        
        #update emission counts
        updateDictCount(wordTagPair2,emissionCnts)
        
        #update transition counts
        updateDictCount((BOS_STATE_MARKER,thisState),transitionsCnt)
        
        #TODO: come back to this emission
        updateDictCount((POS_BOS_TAG,BOS_SENTENCE_TAG),emissionCnts)
        
        priorState = thisState
        ##--- End Initialize BOS
        
        #each next word/pos in sentence
        for i in range(1,len(wordTags)-1):
            wt1 = wordTags[i]
            wt2 = wordTags[i+1]
            
            #first word/tag
            w1,t1 = splitWordTag(wt1)
            w2,t2 = splitWordTag(wt2)
            
            thisState = t1+"_"+t2
            updateDictCount(thisState,stateCnts)
            
            updateDictCount(w2,wordCnts)
            updateDictCount(t2, tagCnts)
            
            wordTagPair2 = (t2,w2)
            updateDictCount(wordTagPair2,wordTagCnts)
            
            #update emission counts
            updateDictCount(wordTagPair2,emissionCnts)
            
            #update transition counts
            updateDictCount((priorState,thisState),transitionsCnt)
          
            priorState = thisState
        ##-- End loop over word/pos pairs in a given sentence
        
        #end of sentence marking
        updateDictCount(POS_EOS_TAG, tagCnts)
        updateDictCount(EOS_STATE_MARKER,stateCnts)
        #update transition counts
        updateDictCount((priorState,EOS_STATE_MARKER),transitionsCnt)
    
    
    #-- End loop over all of the sentences of the training data set
    #update header with count data
    header['state_num'] = len(tagCnts)
    header['sym_num'] = len(wordCnts)
    header['trans_line_num'] = len(transitionsCnt)
    header['emiss_line_num'] = len(wordTags)
          
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# calculate training data counts, return dictionary of totalled counts
##------------------------------------------------------------------------

def calcTrainingDataCounts(wordCnts,tagCnts,stateCnts,wordTagCnts,initialCnts,transitionCnts,emissionCnts):
    counts = {'tagCnt':0,'wordsCnt':0,'wordTagCnt':0,'initsCnt':0,'transCnt':0,'statesCnt':0,'emitsCnt':0}
    #get the counts
    counts['tagCnt'] = sum(Counter(tagCnts).values())
    counts['wordsCnt'] = sum(Counter(wordCnts).values())
    counts['wordTagCnt'] = sum(Counter(wordTagCnts).values())
    counts['initsCnt'] = sum(Counter(initialCnts).values())
    counts['transCnt'] = sum(Counter(transitionCnts).values())
    counts['statesCnt'] = sum(Counter(stateCnts).values())
    counts['emitsCnt'] = sum(Counter(emissionCnts).values())
    
    if isTest: print("tagCnt:{0} wordsCnt:{1} wordTagCnt:{2} initsCnt:{3} transCnt:{4} statesCnt:{5} emitsCnt:{6}".format(
        counts['tagCnt'],counts['wordsCnt'],counts['wordTagCnt'],counts['initsCnt'],counts['transCnt'],counts['statesCnt'],counts['emitsCnt']))

    
    return counts
##------------------------------------------------------------------------
##------------------------------------------------------------------------
##         Calculate training data probabilities
##------------------------------------------------------------------------

def calcInitialsProbs(initialCnts,stateProbabilities,initsCnt):
    for init in initialCnts:
        initValue = initialCnts[init]
        prob = float(initValue) / float(initsCnt)
        lgprob = float(math.log10(prob))
        stateProbabilities.append((init,prob,lgprob))

##------------------------------------------------------------------------
# \transition
# from_state to_state prob lg_prob    #prob=P(to_state | from_state)
##------------------------------------------------------------------------
def calcTransitionsProbs(transitionProbabilities,tagCnts,stateCnts,transitionCnts,header,tagCnt,lambdas):
    states = []
    for t1 in tagCnts:
        for t2 in tagCnts:
            state = t1+"_"+t2
            states.append(state)
    
    transitions = []
    for s1 in states:
        for s2 in states:
            t2_1 = s1.split("_")[1]
            t2_2 = s2.split("_")[0]
            if t2_1 == t2_2:
                transitions.append((s1,s2))
    #update header 'trans_line_num'
    if isTest: print("header trans_line_num:[{0}] updated to:[{1}]".format(header['trans_line_num'],len(transitions)))
    header['trans_line_num'] = len(transitions)
    #update header 'state_num'
    if isTest: print("header state_num:[{0}] updated to:[{1}]".format(header['state_num'],len(states)))
    header['state_num'] = len(states)
    
    for transition in transitions:
        s1 = transition[0]
        s2 = transition[1]
        
        pos1 = s1.split("_")
        pos2 = s2.split("_")
        
        t1 = pos1[0]
        t2 = pos2[0]
        t3 = pos2[1]
        
        _3tsCnt = 0
        if transition in transitionCnts:
            _3tsCnt = transitionCnts[transition]
        
        #initialize probability distributions
        p1, p2, p3 = float(0),float(0),float(0)
        
        _2tsCnt = 0
        p3 = 1/float(len(tagCnts)+1)#+1 or -1
        if s1 in stateCnts:
            _2tsCnt = stateCnts[s1]
            p3 = float(_3tsCnt)/float(_2tsCnt)
        
        #reset p3 if tags are BOS or EOS markers
        if t3 == POS_BOS_TAG:
            p3 = float(0)
        if t1 == POS_EOS_TAG and t2 == POS_EOS_TAG and t3 == POS_EOS_TAG:
            p3 = 1/float(len(tagCnts)+1)
            
        if s2 in stateCnts:
            _2Cnt = tagCnts[t2]
            if t2 == POS_EOS_TAG:
                _2Cnt = _2Cnt / 2
            p2 = float(stateCnts[s2])/float(_2Cnt)
        
        if t3 in tagCnts:
            p1 = float(tagCnts[t3]) / float(tagCnt)
        
        #apply smoothing with interpolation
        prob = lambdas['l3']*p3 + lambdas['l2']*p2 + lambdas['l1']*p1
        lgprob = float("inf")
        if not prob == 0:
            lgprob = math.log10(prob)
        
        transitionProbabilities.append((s1,s2,prob,lgprob))
    ##-- end loop over transitions
    
    if isTest: print("Exiting calcTransitionsProbs transitionProbabilities Count:[{0}]".format(len(transitionProbabilities)))
    return states
    
##------------------------------------------------------------------------
# \emissioin
# state symbol prob lg_prob            #prob=P(symbol | state)
# output symbol is emitted by a state, emissioin prob rely's on only t2 of a state
##------------------------------------------------------------------------
def calcEmissionsProbs(emissionProbabilities,emissionCnts,unkProbs,tagCnts,wordTagCnts,states,header,emitsCnt):
    emissions = []
    #
    for state in states:
        for emit in emissionCnts:
            t2 = state.split("_")[1]
            if emit[0] == t2:
                emissions.append((state,emit[1]))
        #--end inner loop
    #--end outer loop
    
    #
    unks = []
    for state in states:
        for u in unkProbs:
            t2 = state.split("_")[1]
            if u == t2:
                unks.append((state,(u,unkProbs[u])))
    
    #update header emiss_line_num, include unk words
    header['emiss_line_num'] = len(emissions) + len(unks)
    if isTest: print("calcEmissionsProbs emiss_line_num:[{0}]".format(header['emiss_line_num']))
    
    #calc emission probs, (state,word)
    for emit in emissions:
        state = emit[0]
        word = emit[1]
        
        tags = state.split("_")
        #tag/word pairing based on to_state
        t2 = tags[1]
        wt = (t2,word)
        
        #(to_state,word)
        p = float(1)
        if wt in wordTagCnts:
            p = float(wordTagCnts[wt])/float(tagCnts[t2])
        
        if t2 == POS_EOS_TAG or t2 == POS_BOS_TAG:
            p = float(1)
        
        #smooth with unknown probabilities
        unkProb = float(0)
        
        if t2 in unkProbs:
            unkProb = float(unkProbs[t2])
        
        #P(w|t)=1-P(<unk>|t)
        prob = p*(float(1)-unkProb)
        
        lgprob = float("inf")
        if not prob == 0:
            lgprob = math.log10(prob)
        
        emissionProbabilities.append((state,word,prob,lgprob))
    ##-- end loop over emissions
    
    for unkPair in unks:
        state = unkPair[0]
        prob = float(unkPair[1][1])
        lgprob = math.log10(prob)
        emissionProbabilities.append((state,UNK_WORD_MARKER,prob,lgprob))
    ##-- end loop over unknowns
    
    header['sym_num'] += 1#to account for the unk
    header['emiss_line_num'] = len(emissionProbabilities)
    
    if isTest: print("Exiting calcEmissionsProbs emissionProbabilities Count:[{0}] header[sym_num]:[{1}]".format(len(emissionProbabilities),header['sym_num']))
    
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