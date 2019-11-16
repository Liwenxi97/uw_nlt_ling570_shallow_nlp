#!/usr/bin/python
"""#### LING 570: Homework #4 - Ryan Timbrook ############
Author: Ryan Timbrook
Date: 10/25/2018
Q1: Write expand_fsm1

This python script builds an expanded FSM given a lexicon 
and morphotactic rules expressed by an FSA

Format: command line: expand_fsm1_old.sh lexicon morph_rules output_fsm
Ran as: 
    $ ./expand_fsm1.sh lexicon_ex morph_rules_ex q4/q4_expand_fsm

Lexicon and morph_rules are input files; output_fsm is output file to write to
The lexicon file has the format "word classLable", where word and classLabel can be any string
that does not contain whitespace

The morph_rules file is an FSA (in Carmel format) that encodes the morphotactic rules

The output_fsm file is the expanded FSM (in the Carmel format) where an arc in the morph_rule FSA is replaced by
multiple paths and each path correspond to an entry in the lexicon - (i.e. the input symbol in the expanded FSM
should be a character or an empty string e, not a word)

"""

import sys, re


#---- GLOBALS -----#
isTest = False
isLocal = False
cmdArgs = []
EMPTY_STRING = "*e*"
#------------------
##------------------------------------
# Main Procedural Function
##------------------------------------
def main():
    if isTest: print("main: Entering")
    #if isTest: print("main: Cmd Arg 1:[%s] 2:[%s] 3:[%s]"%(cmdArgs[0],cmdArgs[1],cmdArgs[2]))

    if isLocal:
        lexicon_ex= "examples/lexicon_ex"; morph_rules_ex="examples/morph_rules_ex"; q4_expand_fsm="q4/q4_expand_fsm"
    else:
        lexicon_ex=cmdArgs[0]; morph_rules_ex=cmdArgs[1]; q4_expand_fsm=cmdArgs[2]
    
    
    #lexicon
    with open(lexicon_ex, 'r') as l:
        lexicon = l.read().splitlines()
    #unpack lexicon ex file
    lexicons = lexHelper(lexicon)

    #morph rules
    with open(morph_rules_ex, 'r') as m:
        morph_rules = m.read().splitlines()
    #unpack morph rules
    morph_rules = morphRules(morph_rules)
    
    #open expand fsm file for output
    o_expan_fsm = open(q4_expand_fsm, 'w')
    #expand the FSM
    expandedFSM = expandFSM(morph_rules,lexicons,o_expan_fsm)
    
    #write expanded fsm to output file
    printExpandedFSM(expandedFSM,morph_rules,o_expan_fsm)
    
    o_expan_fsm.close

##------------------------------------
# Expand FSM Function
##------------------------------------
def expandFSM(morphRules,lexicons,o_expan_fsm):
    expandedFSM = []
    stateIndex = 100
    
    #start with first rule
    for rule in morphRules[1:]:
        #look for epsillons
        m_fromState = rule[0]
        m_toState = rule[1]
        m_pos = rule[2].strip(")")
        if m_pos == EMPTY_STRING:
            expandedFSM.append([m_fromState,m_toState,EMPTY_STRING,"))"])
        #iterate over lexicons
        for lex in lexicons:
            l_word = lex[0]
            l_pos = lex[1].strip(")")
            if l_pos == m_pos:
                #rules match
                if len(l_word) == 1:
                    stateIndex += 1
                    expandedFSM.append([m_fromState,m_toState,'"'+l_word+'"',"))"])
                else:
                    for a in l_word[0]:
                        stateIndex += 1
                        #substate naming convention: 
                        ss_a_toState = m_fromState.strip("(")+"."+str(stateIndex)
                        if isTest: print("{0} -> new sub-from-state name:{1}".format(m_fromState.strip("("),ss_a_toState))
                        expandedFSM.append([m_fromState,"("+ss_a_toState, '"'+a+'"',"))"])
                    #substates
                    for b in l_word[1:-1]:
                        stateIndex +=1
                        ss_b_fromState = m_fromState.strip("(")+"."+str(stateIndex-1)
                        ss_b_toState = m_fromState.strip("(")+"."+str(stateIndex)
                        if isTest: print("{0} -> new sub-from-state name:{1}".format(m_fromState.strip("("),ss_b_fromState))
                        if isTest: print("{0} -> new sub-to-state name:{1}".format(m_fromState.strip("("),ss_b_toState))
                        expandedFSM.append(["("+ss_b_fromState,"("+ss_b_toState,'"'+b+'"',"))"])
                    #final rule/state
                    for c in l_word[-1]:
                        ss_c_fromState = m_fromState.strip("(")+"."+str(stateIndex)
                        if isTest: print("{0} -> new sub-from-state name:{1}".format(m_fromState.strip("("),ss_c_fromState))
                        expandedFSM.append(["("+ss_c_fromState, m_toState, '"'+c+'"',"))"])
            

    return expandedFSM
##------------------------------------
##------------------------------------
# Lexicon Function
##------------------------------------
def lexHelper(lexicon):
    #format: [word, classLable]
    lexicons=[]
    lexMap = {}
    for lex in lexicon:
        lexicons += [re.split("\s+",lex)]
    
    if [""] in lexicons:
        while [""] in lexicons:
            lexicons.remove([""])
    
    #create dict map where key is the classLable and their lexicon words are the values   
    #ex: {'reg_verb_stem':['walk','talk','impeach']}
    for l in lexicons:
        if l[1] not in lexMap.keys(): lexMap[l[1]]=[]
        lexMap[l[1]].append(l[0])
    
    lexMap = lexMap
    
    return lexicons
##------------------------------------

##------------------------------------
# Morph Rule Function
##------------------------------------
def morphRules(morphRules):
    morph_rules = []
    
    for rule in morphRules:
        morph_rules += [re.split("\s+", rule)]

    if [""] in morph_rules:
        while [""] in morph_rules:
            morph_rules.remove([""])
    
    return morph_rules
##------------------------------------

##------------------------------------
# Print Expanded FSM Function
##------------------------------------
def printExpandedFSM(exFSM,morphRules,output_file):
    acceptState = morphRules[0][0]
    if isTest: print(acceptState)
    output_file.write(acceptState+'\n')
    
    for ex in exFSM:
        o_line = ""
        for element in ex[:-2]:
            o_line += element +" "
        for element in ex[-2:]:
            o_line += element
        if isTest: print(o_line)
        output_file.write(o_line+'\n')
    
##------------------------------------

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