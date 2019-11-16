#!/usr/bin/python
"""#### LING 570: Homework #2 - Ryan Timbrook ############
    FSA acceptor 
Author: Ryan Timbrook
Date: 10/11/2018

Format: fsa_acceptor.sh fsa_file input_file > output_file

"""

import sys, collections

isTest = False
isLocal = True
##############################################
# Class Objects
##############################################
class Node(object):
    
    def __init__(self,name):
        self.name = name
        self.connections = {}
        self.isFinal = False
        self.isStart = False
        self.inputs = []
            
    #asDIRECTION IS EITHER 'DESTINATION' or 'SOURCE'
    def addConnection(self, node, symbol, asDirection=False):
        if symbol not in self.connections: self.connections[symbol] = []
        if node not in self.connections[symbol]: self.connections[symbol].append(node)
        
    def setIsFinal(self):
        self.isFinal = True
        
    def setIsStart(self):
        self.isStart = True
    
    def addInput(self, inputLabel):
        self.inputs.append(inputLabel)
##############################################


cmdArgs = []
fsaNodes = {}
keyStates = {'START':"",'FINAL':""}
######################################
# Main Procedural Function
######################################
def main():
    if isTest: print("main: Entering")
    if isTest: print("main: Cmd Arg 1:[%s] Arg 2:[%s]"%(cmdArgs[0],cmdArgs[1]))
    count = 1
    accepted = False
    #testRec("Test main",1)
    try:
        #create FSA Nodes from FSA file
        createFSANodes()
        with open(cmdArgs[1]) as f:
            for line in f.readlines():
                symbols = line.strip().split(" ")
                startState = fsaNodes[keyStates['START']]
                if isAccepted(startState,symbols):
                    accepted = True
                
                #print stdout in format specified
                if accepted:
                    print(line.strip()+" => yes")
                else:
                    print(line.strip()+" => no")
                count+=1
    except:
        print_err("Error parsing symbols File Line[%d] line[%s]"%(count,line))
        pass

##############################################
# Transition STATE
##############################################
def isAccepted(state, symbols):
    if isTest: print("isAccepted: Entering, ThisState[%s]  Symbol[%s]"%(state.name,symbols))
    accepted = False
    nullSymbol = "*e*"
    nextSymbols = []
    #put symbols to eval in queue
    if len(symbols) == 0:
        if state == keyStates['FINAL']:
            if isTest: print("reached final state [%s]"%keyStates['FINAL'])
            accepted = True
            return True
    else:
        nextSymbols.append(nullSymbol)
        nextSymbols.append(symbols[0])

    for symbol in nextSymbols:
        if isTest: print("isAccepted: symbol to evaluate[%s]"%symbol)
        if symbol in state.connections:
            for st in state.connections[symbol]:
                if symbol == nullSymbol:
                    remSymbols = symbols
                else:
                    remSymbols = symbols[1:]
                    
                if isAccepted(st, remSymbols):
                    accepted = True
                    return True
                    
    if isTest: print("acceptingState: Exiting, ThisState[%s] isAccepted[%s]"%(state,str(accepted)))
    return False

##############################################
# Create FSA Nodes
# **** DO NOT ALLOW NFAs send to stderr *****
##############################################
def createFSANodes():
    if isTest: print("createFSANodes: Entering with fsa file name[%s]"%cmdArgs[0])
    #Open FSA Input File
    #FSA format to parse (source-state (destination-state label))
    with open(cmdArgs[0]) as f:
        count = 1
        finalStateName = ""
        startStateName = ""
        for line in f.readlines():
            try:
                line = line.replace("(",'').replace(")",'')
                if isTest: print("%d %s"%(count,line))
                if count == 1:
                    finalStateName = line.strip()
                    fsaNodes[finalStateName] = Node(finalStateName)
                else:
                    seq = line.split()
                    if isTest: print(seq)
                    if count == 2:
                        #second line, first symbol represents the start state
                        #source-state
                        startStateName = seq[0]
                        n1 = Node(seq[0])
                        n1.setIsStart()
                        if seq[0] not in fsaNodes:
                            fsaNodes[seq[0]] = n1
                        
                        #destination-state
                        n2 = Node(seq[1])
                        n2.addInput(seq[2])
                        if seq[1] not in fsaNodes:
                            fsaNodes[seq[1]] = n2
                        
                        #add connections
                        fsaNodes[seq[0]].addConnection(fsaNodes[seq[1]],seq[2])
                          
                    else:
                        #the rest of the fsa file
                        #source-state
                        ss = Node(seq[0])
                        if seq[0] == startStateName: ss.setIsStart()
                        elif seq[0] == finalStateName: ss.setIsFinal()
                        if seq[0] not in fsaNodes:
                            fsaNodes[seq[0]] = ss
                        
                        #destination-state
                        ds = Node(seq[1])
                        ds.addInput(seq[2])
                        if seq[1] == startStateName: ds.setIsStart()
                        elif seq[1] == finalStateName: ds.setIsFinal()
                        if seq[1] not in fsaNodes:
                            fsaNodes[seq[1]] = ds
                        
                        #add connections
                        fsaNodes[seq[0]].addConnection(fsaNodes[seq[1]],seq[2])
                        
                count+=1
            except:
                print_err("Error parsing FSA File Line[%d] line[%s]"%(count,line))
                count+=1
                raise
        keyStates['FINAL']=finalStateName; keyStates['START']=startStateName
        ## End Looping over FSA File and creating Node connections
        if isTest: print("createFSANodes: Exiting")
    
##############################################
# Format Output
##############################################
def formatOutput():
    if isTest: print("formatOutput: Entering")


##############################################
# Print to stderr
##############################################            
def print_err(args):
    #print(args, file=sys.stderr)
    sys.stderr.write("fatal errlr [%s] \n"%args)
    
##############################################
# Execute Main Function
##############################################
if __name__ == "__main__": 
    if isTest: print(len(sys.argv));
    #remove program file name from input command list
    sys.argv.remove(sys.argv[0])
    if len(sys.argv) > 0:
        for arg in sys.argv:
            if isTest: print(arg)
            cmdArgs.append(arg.strip())
    main()
    

        
        
        
    
        


    
