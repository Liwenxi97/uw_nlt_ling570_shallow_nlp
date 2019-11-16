#!/usr/bin/python
"""#### LING 570: Homework #2 - Ryan Timbrook ############
    NFA to DFA -> Converts an input NFA to an equivalent DFA 
Author: Ryan Timbrook
Date: 10/18/2018

Format: nfa_to_dfa.sh input_file > output_file
Ran as: 
    $ nfa_to_dfa.sh hw3/examples/nfa1 > q4/ex2.fst1
    $ nfa_to_dfa.sh hw3/examples/nfa2 > q4/ex2.fst2

"""

import sys, collections
from collections import OrderedDict
from functools import reduce

##--------------------------------------
# Class Objects
##--------------------------------------
class NFA(object):
    def __init__(self,name):
        self.name = name
        self.numberOfStates = 0
        #'state': [(symbol, new_state)]
        self.states = {}
        self.isymbols = []
        self.numberOfAcceptingStates = 0
        self.initalState = None
        self.finalState = set()
        self.moveNFA = {}
        self.stack = []
        self.eClosureSets = []
        
    def addState(self,state,symbol,newState):
        #add new state
        if state not in self.states.keys():
            self.states[state]=[]
        self.states[state].append((symbol,newState))
       
    def setInitalState(self,stateName):
        self.initalState = stateName
        #if state not in self.states: self.addState(state)
    
    def setFinalState(self,stateName):
        self.finalState = stateName
    
    def getVocSymbols(self):
        voc = set()
        for state in self.states:
            for c, q in self.states[state]:
                voc.add(c)
        if -1 in voc:
            voc.remove(-1)
        self.isymbols.append(list(voc))
        return list(voc)
    
    def eClosure(self,states,consumable,eSet):
        
        for state in states:
            
            if consumable == -1:
                eSet.add(state)
            
            if state in self.stack:
                self.stack.remove(state)
            
            #check for final state
            try:   
                if state == "": 
                    if isTest: print("reached final state {0}".format(state));continue
                nfaState = self.states[state]
                for c,q in nfaState:
                    if c == consumable:
                        eSet.add(q)
                        self.stack.append(q)
                        
                        self.eClosure(self.stack,consumable,eSet)
            except KeyError:
                print("Caught KeyError on state[{0}]".format(state))
                pass
        return eSet
    
    def setTransitionFunctionDeltaMoveNFA(self,unmarkedState,symbol):
        #everywhere you could possibly get to on the symbol for the given state
        T_set = set()
        if type(unmarkedState) == str:
            paths = self.states[unmarkedState]
        else:
            for s in unmarkedState:
                paths = self.states[s]
                
        if len(paths) > 1:
            for p in paths:
                if p[0] == symbol:
                    T_set.add(p[1])
        
        
        return T_set
        
    def subTransFun(self,state,voc):
        states = set([state])
        for e in voc:
            newStates = set([])
            for state in states:
                try:
                    newStates = self.moveNFA[state][e]
                except KeyError:
                    if isTest: print("caught KeyError in nfa.subTransFun state[%s] symbol[%s]"%(state,e))
                    pass
            states = newStates
        return states      
    
##------------------------------------
class DFA(object):

    def __init__(self,name):
        self.name = name
        self.numberOfStates = 0
        #'state': [(symbol, new_state)]
        self.states = {}
        self.initalState = None
        self.finalState = set()
        self.moveDFA = {}
    
    def setInitalState(self,stateName):
        self.initalState = stateName
    
    def setFinalState(self,stateName):
        self.finalState = stateName
       
    def subTransFun(self,state,voc):
        for e in voc:
            state = self.moveDFA[state][e]
        return state
    
    def inVoc(self,voc):
        return self.subTransFun(self.initalState,voc) in self.finalStates
    
    def setTransitionFunctionMoveDFA(self,delta):
        if delta not in self.moveDFA.keys():
            self.moveDFA[delta]=[]
        self.moveDFA[delta].append(delta)
    
    def addState(self,state,nfaStates):
        #add new state
        if state not in self.states.keys():
            self.states[state]=[]
        self.states[state].append(nfaStates)          
##------------------------------------    
        
    
    

#---- GLOBALS -----#
isTest = True
isLocal = True
cmdArgs = []
keyStates = {'START':"",'FINAL':""}
NULL_E ="*e*"
abecedary = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
S_DFA = set()
##------------------------------------
# Main Procedural Function
##------------------------------------
def main():
    if isTest: print("main: Entering")
    if isTest: print("main: Cmd Arg 1:[%s]"%(cmdArgs[0]))

    if isLocal:
        inputFile= "hw3/examples/nfa1"
    else:
        inputFile = cmdArgs[0]
        
    nfa = createNFA(inputFile)
    
    vocab = nfa.getVocSymbols()
    if isTest: print(vocab)
    
    
    nfa.eClosureSets.append(nfa.eClosure([nfa.initalState], -1, set()))
    for eSet in nfa.eClosureSets:
        for symbl in vocab:
            symblSet = nfa.eClosure(eSet, symbl, set())
            resSet = nfa.eClosure(symblSet, -1, set())
            if resSet not in nfa.eClosureSets:
                nfa.eClosureSets.append(resSet)
        
        #set MoveDFA to S
        #S_DFA.add((frozenset(eSet),symbl))
            
        
    #final set
    S_dfa = dict(zip(abecedary[:len(nfa.eClosureSets)],nfa.eClosureSets))             
    if isTest: print(S_dfa)
    
    dfaFinalState = None
    dfa = []
    #Set MoveDFA to S
    for s in S_dfa:
        for e in S_dfa[s]:
            if e == nfa.finalState:
                dfaFinalState = e
            state = nfa.states[e]
            if e == nfa.initalState:
                #dfa.append([m_fromState,"("+ss_a_toState, '"'+a+'"',EMPTY_STRING,"))"])
                print(e)
    

        
    
  
    #convert NFA to DFA
    #TODO: INCOMPLETE - Issues with DFA conversions
    #convertNFAtoDFA(nfa)
    
    if isTest: print("main: Exiting")

##--------------------------------------
##Convert NFA to DFA
##--------------------------------------
def convertNFAtoDFA(nfa):
    if isTest: print("convertNFAtoDFA: Entering")
    
    initialState = frozenset([nfa.initalState])
    stateSet = set([initialState])
    unmarkedQ = stateSet.copy()
    delta = {}
    finalStates = []
    language = nfa.isymbols
    
    
    
    #loop over state queue
    while len(unmarkedQ) > 0:
        qSet = unmarkedQ.pop()
                      
        ##TODO: ISSUE HERE*****
        #for each symbol in the sigma(alphabet)
        
        for symbol in language[0]: 
            S = nfa.setTransitionFunctionDeltaMoveNFA(qSet,symbol)
            if len(S) == 0: continue
            #nStates = reduce(lambda x,y: x|y, [nfa.subTransFun(q,symbol) for q in qSet])
            nStates = frozenset(S)
            
            if not nStates in stateSet:
                stateSet.add(nStates)
                unmarkedQ.add(nStates)
        ##---------------------------------------------------------------------------
    
    for qSet in stateSet:
        if len(qSet & nfa.finalStates) > 0:
            finalStates.append(qSet)
    dfa = DFA(nfa.name+"_"+'dfa')
    dfa.setTransitionFunctionMoveDFA(delta)
    dfa.setInitalState(initialState)
    dfa.setFinalState(finalStates)
    
    return dfa
    
    if isTest: print("convertNFAtoDFA: Exiting")
##--------------------------------------

##--------------------------------------
# Create NFA
##--------------------------------------
def createNFA(nfaFile):
    if isTest: print("createNFA: Entering")
        
    nfa = NFA(nfaFile.split("/")[1])
    lineCount = 1
    arcID = 0
    
    with open(nfaFile, 'r') as f:
        for line in f.readlines():
            if line == '\n': continue
            line = line.strip()
            line = line.replace("(",'').replace(")",'')
            line = line.split(" ")
            if '' in line: 
                line.remove('')
            if isTest: print("fstFile: line[%s]"%line)
            #first line is final state
            if lineCount == 1:
                keyStates['FINAL'] = line[0]
                nfa.setFinalState(line[0])
                nfa.addState(line[0],NULL_E,"")
            #second line is initial-state to next-state; 
            #i0=initial-state, i1=to-state, i2=input-symbol
            elif lineCount == 2:
                keyStates['START'] = line[0]
                nfa.setInitalState(line[0])
                nfa.addState(line[0],line[2],line[1])
            #i0=from-state
            else:
                nfa.addState(line[0],line[2],line[1])
               
            lineCount += 1
         
        
    nfa.numberOfStates = lineCount
        
        #--------------------------------------------------------
    
    if isTest: print("createNFA: Exiting")
    return nfa
##--------------------------------------
   
##--------------------------------------
## Format Output Function
##--------------------------------------
  
        
##------------------------------------
# Execute Main Function
##------------------------------------
if __name__ == "__main__": 
    if isTest: print(len(sys.argv));
    #remove program file name from input command list
    sys.argv.remove(sys.argv[0])
    if len(sys.argv) > 0:
        for arg in sys.argv:
            if isTest: print(arg)
            cmdArgs.append(arg.strip())
    main()
    