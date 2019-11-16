#!/usr/bin/python3
"""#### LING 570: Homework #6 - Ryan Timbrook ############
Author: Ryan Timbrook
Date: 11/8/2018
#Q3: Write check_hmm.sh
This shell script executes a python program that:
    -Reads in a state-emission HMM file, check's its format, and outputs a warning file
    -****Store's HMM file in an EFFICIENT DATA STRUCTURE****
Format: command line: check_hmm.sh input_hmm > warning_file
 - Check's whether the two parts of the HMM file are consistent
        -Do the number of states in the header match that in the distributions?
        -Are the three kinds of constraints for HMM met?
            -print out to warning file if either rules aren't met
Input File: input_hmm (state-emission HMM file that was output from Q2 program execution)
    -Format: 
Output File: warning_file ()
   -Format: 
        -
            
From Command line, Run as: 
    $ ./check_hmm.sh q4/2g_hmm > q4/2g_hmm.warning
    $ ./check_hmm.sh q4/3g_hmm_0.1_0.1_0.8 > q4/3g_hmm_0.1_0.1_0.8.warning
    $ ./check_hmm.sh q4/3g_hmm_0.2_0.3_0.5 > q4/3g_hmm_0.2_0.3_0.5.warning
"""
import sys, re, time, math
from collections import OrderedDict

##------------------------------------------------------------------------
# DTO - Data Transport Object, HMM
##------------------------------------------------------------------------
class HMM(object):
    
    def __init__(self):
        self.header = OrderedDict()
        self.state2Idx = {}
        self.symbol2Idx = {}
        self.idx2State = {}
        self.idx2Symbol = {}
        self.initProbs = {}
        self.transitionProbs = [[]]
        self.emissionProbs = [[]]
##------------------------------------------------------------------------        

#---- GLOBALS -----------------------------------------#
isTest = True
isLocal = True
cmdArgs = []
STATE_NUM = "state_num"
SYM_NUM = "sym_num"
INIT_LINE_NUM = "init_line_num"
TRANS_lINE_NUM = "trans_line_num"
EMISSION_LINE_NUM = "emission_line_num"
WARN_INIT_PROB_SUM = "the init_prob_sum for state"
WARN_TRANS_PROB_SUM = "the trans_prob_sum for state"
WARN_EMISS_PROB_SUM = "the emiss_prob_sum for state"
WARNING = "warning"
WARNING_HEADER = "different numbers of"
CLAIMED = "claimed"
REAL = "real"


#-- Test Files --#
hmmTestFile = "q4/2g_hmm"
#hmmTestFile = "q4/3g_hmm_0.1_0.1_0.8"
#hmmTestFile = "q4/3g_hmm_0.2_0.3_0.5"
##------------------------------------------------------------------------
# Main Procedural Function
##------------------------------------------------------------------------
def main():
    if isTest: print("main: Entering")
        
    if isLocal:
        hmmFile= hmmTestFile
    else:
        hmmFile=cmdArgs[0]

    #open and read in HMM file
    with open(hmmFile,'rt') as td:
        hmm_f = td.readlines()
    if isTest: print("Total Lines in HMM Data File:[{0}]".format(len(hmm_f)))
    
    #initialize HMM dto object
    hmm = HMM()
    
    try:
       
        headerCnts = initialize(hmm_f, hmm)
        validateHeaderData(hmm,headerCnts)
        validateHMMInitConstraint(hmm)
        validateHMMTransConstraint(hmm)
        validateHMMEmissConstraint(hmm)
        
    finally:
        pass
        

    if isTest: print("main: Exiting")

##------------------------------------------------------------------------
# initialize
##------------------------------------------------------------------------
def initialize(hmm_f, hmm):
    hmm.header['state_num'] = 0
    hmm.header['sym_num'] = 0
    hmm.header['init_line_num'] = 1
    hmm.header['trans_line_num'] = 0
    hmm.header['emiss_line_num'] = 0 
    sentenceCnt = 0
    initStartIndex = 0
    transitionStartIndex = 0
    emissionStartIndex = 0
    
    for sent in hmm_f:
        sentenceCnt += 1
        sent = sent.replace('\n','')
        sent = sent.strip()
        #skip empty lines
        if sent == "": continue
        ## -- get header data --##
        if re.search(r'state_num',sent):
            hmm.header['state_num'] = int(sent.split("=")[1])
            continue
        if re.search(r'sym_num',sent):
            hmm.header['sym_num'] = int(sent.split("=")[1])
            continue
        #get header data
        if re.search(r'init_line_num',sent):
            hmm.header['init_line_num'] = int(sent.split("=")[1])
            continue
        #get header data
        if re.search(r'trans_line_num',sent):
            hmm.header['trans_line_num'] = int(sent.split("=")[1])
            continue
        #get header data
        if re.search(r'emiss_line_num',sent):
            hmm.header['emiss_line_num'] = int(sent.split("=")[1])
            continue
        ##-- End header data --##
        
        #find start of initializations
        if re.search(r'\\init',sent):
            initStartIndex = sentenceCnt
            continue
        
        #find start of transitions
        if re.search(r'\\transition',sent):
            transitionStartIndex = sentenceCnt
            continue
        
        #find start of emissions
        if re.search(r'\\emission',sent):
            emissionStartIndex = sentenceCnt      
            continue
    
    if isTest: print("initialize transitionStartIndex:[{0}] emissionStartIndex:[{1}]".format(transitionStartIndex,emissionStartIndex))
    
    
    #map state id to state 
    stateCnt = mapState2Idx(hmm_f,hmm,transitionStartIndex,emissionStartIndex)
    hmm.transitionProbs = [[None for i in range(stateCnt+1)] for j in range(stateCnt+1)]
    
    symbolCnt = mapSymbol2Idx(hmm_f,hmm,emissionStartIndex)
    hmm.emissionProbs = [[None for i in range(symbolCnt+1)] for j in range(stateCnt+1)]
    
    initialsCnt = storeInitProbs(hmm_f,hmm,initStartIndex,transitionStartIndex)
    transitionsCnt = storeTransProbs(hmm_f,hmm,transitionStartIndex,emissionStartIndex)
    emissionsCnt = storeEmissProbs(hmm_f,hmm,emissionStartIndex)
    
    if isTest: print("Exiting initialize: stateCnt:[{0}], symbolCnt:[{1}], initialsCnt:[{2}], transitionsCnt:[{3}], emissionsCnt:[{4}]".format(stateCnt, symbolCnt, initialsCnt, transitionsCnt, emissionsCnt))
    return stateCnt, symbolCnt, initialsCnt, transitionsCnt, emissionsCnt
##------------------------------------------------------------------------
##------------------------------------------------------------------------
# Util Function, map state 2 id
##------------------------------------------------------------------------
def mapState2Idx(hmm_f,hmm,transitionStartIndex,emissionStartIndex):
    
    stateId = 1
    for line in hmm_f[transitionStartIndex:emissionStartIndex-2]:
        line = line.replace('\n','')
        line = line.strip()
        if line == "": continue
        tokens = re.split("\\s+", line)
       
        #map state to ids
        s1 = tokens[0]
        if not s1 in hmm.state2Idx:
            #i = stateId
            hmm.state2Idx[s1] = stateId
            hmm.idx2State[stateId] = s1
            stateId += 1
        s2 = tokens[1]
        if not s2 in hmm.state2Idx:
            #j = stateId
            hmm.state2Idx[s2] = stateId
            hmm.idx2State[stateId] = s2
            stateId += 1
        
    return stateId-1
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util Function, map symbol 2 id
##------------------------------------------------------------------------
def mapSymbol2Idx(hmm_f,hmm,emissionStartIndex): 
    symbolId = 1
    for line in hmm_f[emissionStartIndex:]:
        line = line.replace('\n','')
        line = line.strip()
        if line == "": continue
        tokens = re.split("\\s+", line)
        
        symbol = tokens[1]
        if not symbol in hmm.symbol2Idx:
            hmm.symbol2Idx[symbol] = symbolId
            hmm.idx2Symbol[symbolId] = symbol
            symbolId += 1
    
    return symbolId-1
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util Function, store init_probs
# format:
#     - \init
#     - state prob lgprob
##------------------------------------------------------------------------
def storeInitProbs(hmm_f,hmm,initStartIndex,transitionStartIndex):
    initialsCnt = 0
    
    for line in hmm_f[initStartIndex:transitionStartIndex-1]:
        line = line.replace('\n','')
        line = line.strip()
        if line == "": continue
        tokens = re.split("\\s+", line)
        
        stateId = hmm.state2Idx[tokens[0]]
        prob = float(tokens[1])
        if isTest: print("pi:[{0}] prob={1}".format(stateId,prob))
        hmm.initProbs[stateId] = prob
        initialsCnt+=1
    
    return initialsCnt
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util Function, store trans_probs
# format:
#     - \transition
#     - from_state to_state prob lgprob
##------------------------------------------------------------------------
def storeTransProbs(hmm_f,hmm,transitionStartIndex,emissionStartIndex):
    
    transitionsCnt = 0
    for line in hmm_f[transitionStartIndex:emissionStartIndex-1]:
        line = line.replace('\n','')
        line = line.strip()
        if line == "": continue
        tokens = re.split("\\s+", line)
        
        fromStateId = hmm.state2Idx[tokens[0]]
        toStateId = hmm.state2Idx[tokens[1]]
        prob = float(tokens[2])
        #if isTest: print("a_ij:[{0}][{1}] prob={2}".format(fromStateId,toStateId,prob))
        if hmm.transitionProbs[fromStateId][toStateId] == None:
            hmm.transitionProbs[fromStateId][toStateId]=prob
            transitionsCnt += 1
        else:
            if isTest: print("Not empty! [{0}]".format(hmm.transitionProbs[fromStateId][toStateId]))
    
    return transitionsCnt
        
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util Function, store emiss_probs
# format:
#     - \emission
#     - state prob lgprob ##state here represents the to_state
##------------------------------------------------------------------------
def storeEmissProbs(hmm_f,hmm,emissionStartIndex):   
    emissionsCnt = 0
    for line in hmm_f[emissionStartIndex:]:
        line = line.replace('\n','')
        line = line.strip()
        if line == "": continue
        tokens = re.split("\\s+", line)
        
        stateId = hmm.state2Idx[tokens[0]]
        symbolId = hmm.symbol2Idx[tokens[1]]
        prob = float(tokens[2])
        if isTest: print("b_jk:[{0}][{1}] prob={2}".format(stateId,symbolId,prob))
        if hmm.emissionProbs[stateId][symbolId] == None:
            hmm.emissionProbs[stateId][symbolId]=prob
            emissionsCnt +=1
        else:
            print("Not empty! [{0}]".format(hmm.emissionProbs[stateId][symbolId]))
    
    return emissionsCnt

##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util Function, validate header data
##------------------------------------------------------------------------
def validateHeaderData(hmm,headerCnts):
    stateCnt, symbolCnt, initialsCnt, transitionsCnt, emissionsCnt = headerCnts
    
    for k,v in hmm.header.items():
        if k == 'state_num':
            if v == stateCnt:
                print("{0}={1}".format(k,v))
            else:
                #print warning
                print("{0}: {1} {2}: {3}={4}, {5}={6}".format(WARNING,WARNING_HEADER,STATE_NUM,CLAIMED,v,REAL,stateCnt))
        if k == 'sym_num':
            if v == symbolCnt:
                print("{0}={1}".format(k,v))
            else:
                #print warning
                print("{0}: {1} {2}: {3}={4}, {5}={6}".format(WARNING,WARNING_HEADER,SYM_NUM,CLAIMED,v,REAL,symbolCnt))
        if k == 'init_line_num':
            if v == initialsCnt:
                print("{0}={1}".format(k,v))
            else:
                #print warning
                print("{0}: {1} {2}: {3}={4}, {5}={6}".format(WARNING,WARNING_HEADER,INIT_LINE_NUM,CLAIMED,v,REAL,initialsCnt))
        if k == 'trans_line_num':
            if v == transitionsCnt:
                print("{0}={1}".format(k,v))
            else:
                #print warning
                print("{0}: {1} {2}: {3}={4}, {5}={6}".format(WARNING,WARNING_HEADER,TRANS_lINE_NUM,CLAIMED,v,REAL,transitionsCnt))
        if k == 'emiss_line_num':
            if v == emissionsCnt:
                print("{0}={1}".format(k,v))
            else:
                #print warning
                print("{0}: {1} {2}: {3}={4}, {5}={6}".format(WARNING,WARNING_HEADER,EMISSION_LINE_NUM,CLAIMED,v,REAL,emissionsCnt))

##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util Function, validate hmm_f Constraints
# init_prob_sum = 1
# example warning: "warning: the init_prob_sum for state BOC is 0.9"
##------------------------------------------------------------------------
def validateHMMInitConstraint(hmm):
    init_prob_sum = 0
    state = None
    
    for k,v in hmm.initProbs.items():
        if isTest: print("State:[{0}] StateId:[{1}] prob:[{2}]".format(hmm.idx2State[k],k,v))
        init_prob_sum += v
        state = hmm.idx2State[k]
    
    if math.fabs((1.0 - init_prob_sum)) > 0.001:
        print("{0}: {1} {2} is {3}".format(WARNING,WARN_INIT_PROB_SUM,state,init_prob_sum))
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util Function, validate hmm_f Constraints
# trans_prob_sum: trans_prob_sum[i] is sum_j a[i][j] where size is N
# example warning: "warning: the trans_prob_sum for state N is 0.9"
##------------------------------------------------------------------------
def validateHMMTransConstraint(hmm):
    transProbSums = {}
    
    for i in range(1,len(hmm.idx2State)+1):
        trans_prob_sum = 0
        state = hmm.idx2State[i]
        for j in range(1,len(hmm.idx2State)+1):
            prob = hmm.transitionProbs[i][j]
            if not prob == None:
                trans_prob_sum += prob
        #-- end column loop
        transProbSums[state] = trans_prob_sum
    #-- end row loop
    
    
    for trans in transProbSums:
        if isTest: print("state:[{0}] abs:[{1}]".format(trans,(float(1.0) - transProbSums[trans])))
        if math.fabs((1.0 - transProbSums[trans])) > 0.001:
            print("{0}: {1} {2} is {3:0.10f}".format(WARNING,WARN_TRANS_PROB_SUM,trans,transProbSums[trans]))

##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util Function, validate hmm_f Constraint
# emiss_prob_sum: emiss_prob_sum[i] is sum_k b[i][k] where size is N
# example warning: "warning: the emiss_prob_sum for state V is 0.85"
##------------------------------------------------------------------------
def validateHMMEmissConstraint(hmm):
    emissProbSums = {}
    emiss_prob_sum = 0
    
    for i in range(1,len(hmm.idx2State)+1):
        emiss_prob_sum = 0
        state = hmm.idx2State[i]
        for j in range(1,len(hmm.idx2Symbol)+1):
            prob = hmm.emissionProbs[i][j]
            if not prob == None:
                emiss_prob_sum += prob
        #-- end column loop
        emissProbSums[state] = emiss_prob_sum
    #-- end row loop
    
    
    for emit in emissProbSums:
        if isTest: print("state:[{0}] abs:[{1}]".format(emit,(float(1.0) - emissProbSums[emit])))
        if not emit in emissProbSums:
            print("{0}: {1} {2} is {3}".format(WARNING,WARN_EMISS_PROB_SUM,emit,float(0)))
        elif math.fabs((1.0 - emissProbSums[emit])) > 0.001:
            print("{0}: {1} {2} is {3}".format(WARNING,WARN_EMISS_PROB_SUM,emit,emissProbSums[emit]))
    
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