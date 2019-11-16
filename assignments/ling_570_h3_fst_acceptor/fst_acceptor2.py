#!/usr/bin/python
"""#### LING 570: Homework #2 - Ryan Timbrook ############
    FST acceptor 
Author: Ryan Timbrook
Date: 10/18/2018

Format: fst_acceptor2.sh fst_file input_file > output_file
Ran as: 
    $ fst_acceptor2.sh hw3/examples/fst1 hw3/examples/ex2 > q3/ex2.fst1
    $ fst_acceptor2.sh hw3/examples/fst2 hw3/examples/ex2 > q3/ex2.fst2

"""

import sys, collections, re, queue

##--------------------------------------
# Class Objects
##--------------------------------------
class FST(object):

    
    def __init__(self,name):
        self.name = name
        self.initialWeight = 0
        self.finalWeight = {lambda args: None}
        self.states = set()
        self.arcs = []
        self.isymbols = set()
        self.osymbols = set()
        self.initalState = None
        self.finalState = None
        self.arcsBySourceState = {}
        self.arcsByToState = {}
   
            
    #asDIRECTION IS EITHER 'DESTINATION' or 'SOURCE'
    def addState(self,state):
        self.states.add(state)
        
    def setInitialState(self,state):
        self.initalState = state
        if state not in self.states: self.addState(state)
    
    def setFinalState(self,state):
        self.finalState = state
        if state not in self.states: self.addState(state)
    #collections.namedtuple ('Token',['token','freq'])
    def addArc(self,arcID,previousState,ilabol,olabel,weight,nextstate):
        #transition inbut label, transition output label, transtion weight, transition destination
        arc = (previousState,ilabol,olabel,weight,nextstate)
        if arc not in self.arcs: self.arcs.append(arc)
        #self.arcs[arcID] = (previousState,ilabol,olabel,weight,nextstate)
        if previousState not in self.arcsBySourceState.keys(): self.arcsBySourceState[previousState] = []
        self.arcsBySourceState[previousState].append(arc)
        if nextstate not in self.arcsByToState.keys(): self.arcsByToState[nextstate] = []
        self.arcsByToState[nextstate].append(arc)
        self.addISymbols(ilabol)
        self.addOSymbols(olabel)
        
    def addISymbols(self,ilabel):
        self.isymbols.add(ilabel)
    
    def addOSymbols(self,olabel):
        self.osymbols.add(olabel)
    
    def transitions(self,state):
        return self.arcsBySourceState[state]
    
    def d_transitions(self,state,symbol):
        nextstate = -1
        olabel = None
        weight = None
        # return nextstate
        allArcs = self.transitions(state)
        for arc in allArcs:
            nlab = arc[1]
            if symbol == nlab:
                nextstate = arc[4]
                olabel = arc[2]
                weight = arc[3]
                break
        # else return -1 for illegal/missing transition
        return nextstate, olabel, weight
    
    def getPossTransitions(self,state,label):
        key = (state, label)
        allArcs = self.transitions(state)
        possArcs = []
        for arc in allArcs:
            nlab = arc[1]
            if not nlab or nlab==label:
                possArcs.append(arc)
        return possArcs
    
    def getInitalState(self):
        return self.initalState
    
    def getFinalState(self):
        return self.finalState
        
##--------------------------------------
class State(object):
    def __init__(self, name):
        self.name = name
        self.links = {} # Dictionary indexed by symbol of arrays of states
    
    def addLink(self, state, symbol):
        # 
        if symbol not in self.links:
            self.links[symbol] = []
        # 
        if state not in self.links[symbol]:
            self.links[symbol].append(state)
    
    
##############################################


#---- GLOBALS -----#
isTest = False
isLocal = False
cmdArgs = []
keyStates = {'START':"",'FINAL':""}
#---- OUTPUT Formats ----#
OUT_SYM=" => "
OUT_NONE="*none*"
SPACE=" "
NULL_E ="*e*"
##--------------------------------------
# Main Procedural Function
##--------------------------------------
def main():
    if isTest: print("main: Entering")
    if isTest: print("main: Cmd Arg 1:[%s] Arg 2:[%s]"%(cmdArgs[0],cmdArgs[1]))
    
    if isLocal:
        fstFile = "examples/fst2"; inputFile= "examples/ex2"
    else:
        fstFile = cmdArgs[0]
        inputFile = cmdArgs[1]
    
    
    #create fst from input fst definition file
    fst = createFST(fstFile)
    
    isAccepted = False
    transduction = []
    
    #process input file
    with open(inputFile, 'r') as f:
        
        for L in f.readlines():
            L = L.strip()
            transduced = transduce(fst, L)
            #[0]-> isAccepted [1]->output transduction
            if transduced[0]:   
            #accept
                isAccepted = True
                transduction.append(transduced[1])
            else:
            #reject
                isAccepted = False
                
            #if isTest: print("line[%s] isAccepted[%s] output[%s]"%(L,str(isAccepted),transduction))
            transduct = ""
            #line = ''.join(L)
            if len(transduction) > 0: 
                for out in transduction:
                    transduct = transduct + ''.join(out)
            else:
                transduct = ""
            #print output
            fPrint(L,transduct,isAccepted)
        
    
    if isTest: print("main: Exiting")

##--------------------------------------
# Function Transduce
##--------------------------------------
def transduce(fst, tape):
    if isTest: print("transduce: Entering tape[%s]"%tape)
    isAccept = False
    index = 0
    transduction = []
    weight = []
    currentState = fst.getInitalState()
    #currentArc = fst.arcsBySourceState[currentState]
    #currentArc = fst.arcs[index]
    
    tapeQueue = queue.Queue()
    tapeElements = tape.split(" ")
    for e in tapeElements:
        tapeQueue.put(e)
    
    #if index <= len(tapeElements):
    while not tapeQueue.empty():
        e = tapeQueue.get()
        out = acceptState(fst,currentState,e)
        #out[0]->isAccepted, out[1]->nextstate, out[2]->output string
        index += 1
        
        if out[0]:
            currentState = out[1]#next state
            if not out[2] == NULL_E:    
                transduction.append(out[2])
            weight.append(out[3])
            if currentState == keyStates['FINAL'] and tapeQueue.empty():
                isAccept = True
                break
            #need to get arc path
        else:
            isAccept = False 
            break
        
        if isTest: print(out)
        
    return isAccept, transduction
    
    if isTest: print("transduce: Exiting isAccept[%s] output[%s]"%(str(isAccept),str(transduction)))
##--------------------------------------

##--------------------------------------
# Accept State - returns true or false
##--------------------------------------
def acceptState(fst,searchState,symbol):
    if isTest: print("acceptState: Entering searchState[%s] symbol[%s]"%(searchState,symbol))
    isAccept = False
    nextState = -1
    acceptNullInput = "*e*"
    output = None
    weight = None
    
    if not symbol == acceptNullInput:
        nextstate_t = fst.d_transitions(searchState,symbol)
        if not nextstate_t[0] == -1:
            nextState = nextstate_t[0] 
            isAccept = True
            output = nextstate_t[1]
            weight = nextstate_t[2]
    else:
        if isTest: print("acceptState symbol is empty string, NDFST - reject [%s]"%symbol)
        sys.stderr.write("The input FST is ambiguous; symbol[%s]"%symbol)
    
    if isTest: print("acceptState: Exiting isAccept[%s] nextState[%s] output[%s] weight[%s]"%(str(isAccept),nextState,output,weight))
    return isAccept, nextState, output, weight
##--------------------------------------

##--------------------------------------
# Create FST
##--------------------------------------
def createFST(fstFile):
    if isTest: print("fstFile: Entering")
    fst = FST(fstFile.split("/")[1])
    lineCount = 1
    arcID = 0
    weight = -1
    with open(fstFile, 'r') as f:
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
                fst.setFinalState(State(line[0]).name)
            #second line is initial-state to next-state; 
            #i0=initial-state, i1=to-state, i2=input-symbol, i3=output-symbol, i4=weight
            elif lineCount == 2:
                keyStates['START'] = line[0]
                fst.setInitialState(State(line[0]).name)
                if len(line)==5: 
                    weight=line[4]
                fst.addArc(arcID,line[0],line[2],line[3],weight,line[1])
            #i0=from-state
            else:
                fst.addState(State(line[0]).name)
                if len(line)==5: 
                    weight=line[4]
                fst.addArc(arcID,line[0],line[2],line[3],weight,line[1])
            
            lineCount += 1
            arcID += 1
    
    if isTest: print("fstFile: Exiting")
    return fst
##--------------------------------------
## Format Output Function
##--------------------------------------
def fPrint(line,result,isAccepted=False):
    if isAccepted: 
        print(line+OUT_SYM+SPACE+result+SPACE+str(1))
    else: 
        print(line+OUT_SYM+OUT_NONE+SPACE+str(0))

##--------------------------------------
# Execute Main Function
##--------------------------------------
if __name__ == "__main__": 
    if isTest: print(len(sys.argv));
    #remove program file name from input command list
    sys.argv.remove(sys.argv[0])
    if len(sys.argv) > 0:
        for arg in sys.argv:
            if isTest: print(arg)
            cmdArgs.append(arg.strip())
    main()
    


