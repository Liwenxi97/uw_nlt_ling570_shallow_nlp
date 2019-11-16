#!/usr/bin/python
"""#### LING 570: Homework #1 - Ryan Timbrook ############
    English Tokenizer
Author: Ryan Timbrook
Date: 10/4/2018

INPUT FILE COMMAND ARG: ex2
INPUT FILE COMMAND ARG: abbrev_list
OUTPUT FILE COMMAND ARG: ex2.tok

"""

import os, sys, re, collections


#Local Test
isTest = False
isLocal = False

exToken = collections.namedtuple('Token',['type','value'])
abbreviationList = []

######################################
# Main Procedural Function
######################################
def main(argv):
    if argv is None:
        argv = sys.argv
    c = 0
    for arg in argv:
        if isTest: print("hw1_tok.main: argv%d[%s]"%(c,argv[c]))
        c+=1
    #Check if local test
    if isTest: print(isLocal)
    if isLocal:
        input1 = "ex2"; input2= "abbrev-list"
    else:
        #input1 = argv[1]; input2 = argv[2]
        input1 = argv[1]
    
    #Load Abbreviations List
    abbrevListFile = open(input1,'r')
     
    for abbrev in abbrevListFile.readlines():
        abbreviationList.append(abbrev.replace('\n',''))
    if isTest: print(abbreviationList)
    
    #Format Abbreviation List
    abbrevStr = formatApprevList()
    
    #Load input file to tokenize
    sentCount=0
    try:
        #for tokSent in tokFile.readlines():
        for tokSent in sys.stdin.readlines():
            newLine = ""
            sentCount += 1
            for t in iterTok(sentCount,tokSent,abbrevStr):
                if isTest: print(t.value)
                toks = splitApostrophe(t)
                
                if len(toks)!= 0:
                    newLine += toks[0].value
                    newLine += ' '
                    newLine += toks[1].value
                    newLine += ' '
                else:                    
                    newLine += t.value
                    newLine += ' '
            print(newLine)
        
    except IOError as io:
        sys.stderr.write("*****ERROR***** Caught IOError %s"%str(io))
    
    #print("hw1_tok.main: #### Sentence Count Total[%d] ####"%sentCount)

##############################################
# Iterator Token Function
##############################################
def iterTok(lineNum, sent, abbrevExc):
    if isTest: print("hw1_tok.iterTok: Entering -> Line#[%d] | Sentence[%s]" %(lineNum,sent))
    if isTest: print("hw1_tok.iterTok: abbrevStr: %s"%abbrevExc)
    
    exTokenSpecification = [
    ('ABBREV',r'([A-Za-z]\.[A-Za-z]\.)'), #Abbreviation
    ('ABBREV_LIST',r'('+abbrevExc+')'),#
    ('EMAIL',r'(\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b)'), #
    ('TIME',r'([0-9]+:[0-9]+)'), #
    ('PATH',r'\b[a-z]:\\(?:[^\\/:*?"<>|\x00-\x1F]+\\)*[^\\/:*?"<>|\x00-\x1F]*'), #
    ('PUNCT',r'(,|"|;|\?|[@]+?| -- |: )'), #
    ('DOLLAR_SIGN',r'[$]'), #
    ('SINGLE_PERCENT',r'(\d+%)'), #
    ('NUM_INT_DEC',r'(-?[0-9]+\.[0-9]+%?)'), #an integer or decimal number
    ('NUM_THOUSANDS',r'([0-9]{1,3},[0-9]{3})'), #a large number in the thousands
    ('NUM_HUND_THOUSANDS',r'([0-9]{1,3},[0-9]{3},[0-9]{3})'), #a large number in the thousands
    ('APOSTROPHE_A',r"([a-zA-Z]+'? )"), #
    ('APOSTROPHE_B',r"([a-zA-Z]+?'[a-zA-Z]+?)"), #
    ('ALPHA_NUM',r'[A-Za-z0-9]+'), #Alpha word identifier
    ('ARITH_OP',r'( [+\-*/] )'), #
    ('TILDE',r'( [~] )'), #
    ('NEW_LINE',r'\n'), #
    ('SKIP',r'[ \t]+'),#
    ('OTHER',r'\.'), #
    ]
    
    exTokRE = '|'.join('(?P<%s>%s)' % pair for pair in exTokenSpecification)
    
    for rePair in re.finditer(exTokRE, sent):
        typ = rePair.lastgroup
        value = rePair.group(typ)
        if typ == 'NEW_LINE':
            rePair.end()
        elif typ == 'SKIP':
            pass
        else:
            yield exToken(typ,value)
    

##############################################
# Format Abbreviation List
##############################################
def formatApprevList():
    if isTest: print("hw1_tok.formatApprevList: Entering -> Abbreviation List:[%s] " %abbreviationList)
   
    abbrevStr = '|'.join(abbreviationList)
    abbrevStr = re.sub(r'\.','\.',abbrevStr)
    
    if isTest: print("hw1_tok.formatApprevList: Exiting -> abbrevStr:[%s] " %abbrevStr)
    return abbrevStr

##############################################
# Split Contractions
##############################################
def splitApostrophe(tok):
    contractions = {"n't","'d","'re","'s","'ll","'ve","'clock","'er"}
    toks = []
    if tok.type == 'APOSTROPHE_B':
        for c in contractions:
            if tok.value.find(c) != -1:
                if isTest: print("FOUND CONTRACTION: %s for value: %s"%(c,tok.value))
                s = tok.value.split(c)
                s[1] = c
                if isTest: print("FOUND CONTRACTION: split: %s"%s)
                toks.append(exToken(tok.type,s[0]))
                toks.append(exToken(tok.type,s[1]))
    return toks

##############################################
# Execute Main Function
##############################################
if __name__ == "__main__": main(sys.argv)