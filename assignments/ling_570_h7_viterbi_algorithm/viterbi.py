#!/usr/bin/python3
"""#### LING 570: Homework #7 - Ryan Timbrook ############
Author: Ryan Timbrook
Date: 11/15/2018
#Q1: Write viterbi.sh
This  a python program that:
    -Implements the Viterbi algorithm.
    -
Format: command line: viterbi.sh input_hmm test_file output_file
 - 
Input File: HMM is a state-emission hmm - same format as HW6. The output is produced by the to-state
   -Format: Assume the input hmm does not contain any emission probabilities for empty string
            - output symbols are produced by the to-state
            - No smoothing of the HMM
            - *** if a line contains a probability not in the range 0 - 1, print out a wanring message to stderr
                ("warning: the prob is not in [0,1] range: $line", where $line is the line) and ignore those lines
Test File: each line is an observation (a sequence of output symbols) - POS tagging, an observation will be a sentence
    - the sentence may, or may not include special symbol(</s>) for EOS.
    - Do not do anything special for BOS and EOS.
Output File:
   -Format: "observ => state seq lgprob"
        -state seq is the best state sequence for the observation
        -lgprob is lg P(observ,state seq); lg(x) is base-10 log
            
From Command line, Run as: 
    $ ./viterbi.sh hmm1 test.word sys1
    $ ./viterbi.sh hmm2 test.word sys2
    $ ./viterbi.sh hmm3 test.word sys3
    $ ./viterbi.sh hmm4 test.word sys4
    $ ./viterbi.sh hmm5 test.word sys5
"""
import sys, re, time, math
from collections import OrderedDict

#---- GLOBALS -----------------------------------------#
isTest = False
isLocal = False
cmdArgs = []

#-- Output Fromating -- #
#OBSERV = "observ =>"

#-- Local Test Files --#
#inputHMM = "hmm1"
inputHMM = "hmm2"
#inputHMM = "hmm3"
#inputHMM = "hmm4"
#inputHMM = "hmm5"

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
    
    
    def getInitProb(self,j):
        if j in self.initProbs:
            return self.initProbs[j]
        else:
            return 0
        
    #get list of start transitions
    def getStartTransitions(self):
        start_state_id=0
        for k in self.initProbs.keys():
            start_state_id = k; break
            
        startTransStates = self.transitionProbs[start_state_id]
        transitionStarts = [(self.idx2State[i],i) for i,s in enumerate(startTransStates) if not s == None]
     
        return transitionStarts
    
    #i=from_state_id; j=to_state_id
    def getTransitionProb(self,from_state_id,to_state_id):
        if not self.transitionProbs[from_state_id][to_state_id] == None:
            return self.transitionProbs[from_state_id][to_state_id]
        else:
            return 0
    
    #j=to_state_id; k=symbol
    def getEmissionProb(self,to_state_id,symbol):
        if symbol in self.symbol2Idx:
            symbol_id = self.symbol2Idx[symbol]
            if not self.emissionProbs[to_state_id][symbol_id] == None:
                return self.emissionProbs[to_state_id][symbol_id]
            elif not self.emissionProbs[to_state_id][self.symbol2Idx["<unk>"]] == None:
                return self.emissionProbs[to_state_id][self.symbol2Idx["<unk>"]]
            else:
                return 0
        else:
            if not self.emissionProbs[to_state_id][self.symbol2Idx["<unk>"]] == None:
                return self.emissionProbs[to_state_id][self.symbol2Idx["<unk>"]]
            else:
                return 0
    
        
##------------------------------------------------------------------------ 

##------------------------------------------------------------------------
# Main Procedural Function
##------------------------------------------------------------------------
def main():
    if isTest: print("main: Entering")
        
    if isLocal:
        inputHMMFile= "examples/"+inputHMM; inputTestFile="examples/test.word"; outputSysFile="sys"
    else:
        inputHMMFile=cmdArgs[0]; inputTestFile=cmdArgs[1]; outputSysFile=cmdArgs[2]

    #open and read in HMM file
    hmm_f = None
    with open(inputHMMFile,'rt') as h:
        hmm_f = h.readlines()
    if isTest: print("Total Lines in HMM Data File:[{0}]".format(len(hmm_f)))
    
    #open and read in test file
    test_f = None
    with open(inputTestFile, 'rt') as t:
        test_f = t.readlines()
    if isTest: print("Total Lines in Test Word File:[{0}]".format(len(test_f)))
    
    #open output file for writing
    o_sys = open(outputSysFile,'w')
    
    #initialize HMM dto object
    hmm = HMM()
    
    try:
        #construct HMM object
        headerCnts = initialize(hmm_f, hmm)
        
        #process test file: (observation is a single line)
        for observ in test_f:
            observ = observ.replace('\n','')
            observ = observ.strip()
            stateSeq, lgprob = viterbi(hmm, observ)
            #print output format: "observ => stateSeq lgprob"
            printObserv(observ,stateSeq,lgprob,o_sys)
        
    finally:
        o_sys.flush()
        o_sys.close()
        

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
        #if isTest: print("pi:[{0}] prob={1}".format(stateId,prob))
        hmm.initProbs[stateId] = prob
        initialsCnt+=1
    
    return initialsCnt
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Util Function, store trans_probs
# format:
#     - \transition
#     - from_state to_state prob lgprob
# Updated to not include any data after ## in a given line
##------------------------------------------------------------------------
def storeTransProbs(hmm_f,hmm,transitionStartIndex,emissionStartIndex):
    
    transitionsCnt = 0
    for line in hmm_f[transitionStartIndex:emissionStartIndex-1]:
        line = line.replace('\n','').strip()
        if line == "": continue
        line = line.split("##")
        tokens = re.split("\\s+", line[0].strip())
        
        fromStateId = hmm.state2Idx[tokens[0]]
        toStateId = hmm.state2Idx[tokens[1]]
        prob = float(tokens[2])
        
        #if line contains a probability that is not in the [0,1] range, print warning and skip line
        if not isProbabilityInRange(prob):
            sys.stderr.write("warning: the prob is not in [0,1] range: {0}".format(line[0]))
            continue #skip line
        
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
        line = line.replace('\n','').strip()
        if line == "": continue
        line = line.split("##")
        tokens = re.split("\\s+", line[0].strip())
        
        stateId = hmm.state2Idx[tokens[0]]
        symbolId = hmm.symbol2Idx[tokens[1]]
        prob = float(tokens[2])
        
        #if line contains a probability that is not in the [0,1] range, print warning and skip line
        if not isProbabilityInRange(prob):
            continue #skip line
        
        #if isTest: print("b_jk:[{0}][{1}] prob={2}".format(stateId,symbolId,prob))
        if hmm.emissionProbs[stateId][symbolId] == None:
            hmm.emissionProbs[stateId][symbolId]=prob
            emissionsCnt +=1
        else:
            print("Not empty! [{0}]".format(hmm.emissionProbs[stateId][symbolId]))
    
    return emissionsCnt

##------------------------------------------------------------------------

##------------------------------------------------------------------------
# viterbi function
#trellis object
#    desc: -each node corresponds to a distinct state at a given time
#          -begins and ends at the known states c0 cn
#          -to every possible state sequence C there corresponds a unique path through the trellis, and vise versa  
##------------------------------------------------------------------------
def viterbi(hmm, observ):
    O_tokens = re.split('\\s+',observ)
    O_leng = len(O_tokens)
    N_states = len(hmm.state2Idx)
    
    #get in initial start state
    for k in hmm.initProbs.keys():
        start_state_id = k; break
    
    #initialize collection objects
    #TODO: consider using None type in replace of int. int takes 24 bytes of memory, None takes 16 bytes
    delta = [{} for o in O_tokens]
    
    #---- Start Initialization Step --------------------------------#
    #if isTest: print("viterbi starting initialization ...")
    startTrans = hmm.getStartTransitions()
    for j in startTrans:
        
        #REGRADE - Add check to see if state emission can be reached for the first word in the observation
        startSym = checkUnknownWord(O_tokens[0],hmm)
        emissProb = hmm.emissionProbs[j[1]][hmm.symbol2Idx[startSym]]
    
        if not emissProb == None:
            delta[0][j[1]] = (hmm.getTransitionProb(from_state_id=start_state_id,to_state_id=j[1]) * hmm.getEmissionProb(to_state_id=j[1],symbol=checkUnknownWord(O_tokens[0],hmm)), start_state_id)
    #---- End Initialization Step -------------------------------------------------#
    #-------------------------------------------------------------------------------
    
    #Recursion Step
    t_start = time.time()
    #if isTest: print("viterbi starting recursion ...")
    notZeroDelta = []
    t=1
    while t<O_leng:
        t0 = time.time()
        prevStates = delta[t-1].keys()
        k=checkUnknownWord(O_tokens[t],hmm) #the symbol at time t (observation)
        j=1
        while j<N_states+1:
            #if isTest: print("search for symbol: [{0}] at state: [{1}] id:[{2}]".format(k,hmm.idx2State[j],j))
            if isReachable(j, k, prevStates, hmm):
                maxProb = 0.0
                maxProb,backPtr = max((delta[t-1][p][0] * hmm.getTransitionProb(from_state_id=p,to_state_id=j) ,p) for p in prevStates)
                if maxProb > 0.0:
                    delta[t][j] = (maxProb*hmm.getEmissionProb(to_state_id=j,symbol=k),backPtr)
                
            j+=1
        #-- end inner loop
        t1 = time.time()
        duration = t1-t0
        #if isTest: print("recursive step: processing time:[{0}] for observation[{1}] [{2}]".format(duration,t,k))
        t+=1
    ##-- end outer loop
    t_end = time.time()
    duration = t_end-t_start
    #if isTest: print("completed recursive step: total processing time:[{0}] for [{1}] observations".format(duration,t))
    #-------------------------------------------------------------------------------
    #-------------------------------------------------------------------------------
    
    #Termination Step
    #if isTest: print("viterbi starting termination ...")
    
    N = O_leng-1
    probArgmax,finalToState = max( (delta[N][k], k) for k in delta[N].keys() )
    finalProb = math.log10(probArgmax[0])
    
    bestPath = []
    bestPath.insert(0,hmm.idx2State[finalToState])
    while N>=1:
        s = probArgmax[1]
        bestPath.insert(0,hmm.idx2State[s])
        N-=1 #decrement N counting down
        probArgmax = delta[N][s]
    bestPath.insert(0,hmm.idx2State[start_state_id])#REGRADE - Uncommented out this line.
    ## -- end loop
    
    ##return bestPath
    return ' '.join(bestPath), finalProb
    
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# test if a state can be reached, return True or False
##------------------------------------------------------------------------
def isReachable(state,word,prevStates,hmm):
    #if isTest: print("getStateProb entering: state_id[{0}] state_name[{1}] word_id[{2}] word_name[{3}]".format(state, hmm.idx2State[state], hmm.symbol2Idx[word],word))
    emissProb = -1
    
    emissProb = hmm.emissionProbs[state][hmm.symbol2Idx[word]]
    
    if emissProb == None:
        return False

    for p in prevStates:
        #if isTest: print("getStateProb evaluating transitionProbs[{0}][{1}]; p={2} state={3}".format(p,state,hmm.idx2State[p],hmm.idx2State[state]))
        if not hmm.transitionProbs[p][state] == None:
            #if isTest: print("getStateProb returning prob=[{0}]".format(prob))
            return True
    
    return False
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# check for unknown word
##------------------------------------------------------------------------
def checkUnknownWord(sym,hmm):
    if not sym in hmm.symbol2Idx:
        #if isTest: print("checkUnknownWord *****[{0}]***** is unknown".format(sym))
        sym = "<unk>"
        
    return sym
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# check for unknown word
##------------------------------------------------------------------------
def isProbabilityInRange(prob): 

    if prob > -0.001 and prob < 1.001:
        return True
    else:
        sys.stderr.write("Warning, Probability is out of range [0,1]: prob=[{0}]".format(prob))
        return False
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Decode the File
##------------------------------------------------------------------------
def printObserv(observ,stateSeq,lgprob,o_sys):
    
    #o_sys.write("{0} => {1} {2:0.10f}\n".format(observ,stateSeq,lgprob))
    o_sys.write("{0} => {1} {2}\n".format(observ,stateSeq,lgprob))
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