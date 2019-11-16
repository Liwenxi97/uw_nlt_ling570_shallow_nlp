#!/usr/bin/python3
"""#### LING 570: Homework #5 - Ryan Timbrook ############
Author: Ryan Timbrook
Date: 11/1/2018
Q3: Write ppl
This shell script executes a python program that calculates the perplexity of a test data given an LM:
    For smoothing, it uses interpolation
Format: command line: ppl.sh lm_file l1 l2 l3 test_date output_file
Input File: lm_file (Is the output file generated from Q2)
Input File: test_data (same format as the training_data from Q1)
Output File: output_file
    -all real numbers are truncated to 10 places after the decimal points
    
Ran as: 
    $ ./ppl.sh lm_file l1 l2 l3 test_date output_file

"""

import sys, re, time, string, math
from collections import defaultdict


#---- GLOBALS -----#
isTest = False
isLocal = False
cmdArgs = []

##------------------------------------------------------------------------
# Main Procedural Function
##------------------------------------------------------------------------
def main():
    isTest = False
    if isTest: print("main: Entering")
        
    if isLocal:
        lm_file= "wsj_sec0_19.lm"; lam_1=0.05; lam_2=0.15; lam_3=0.8; test_date='hw5/examples/wsj_sec22.word'; out_ppl_file='ppl_0.05_0.15_0.8'
    else:
        lm_file=cmdArgs[0]; lam_1=cmdArgs[1]; lam_2=cmdArgs[2]; lam_3=cmdArgs[3]; test_date=cmdArgs[4]; out_ppl_file=cmdArgs[5]
    
    #open output ppl file for writing
    o_ppl = open(out_ppl_file,'w')
    
    #readin lm file output from Q2, build_lm program
    lmFile = open(lm_file, 'rt')
    
    #readin testdata file
    testDataFile = open(test_date, 'rt')
    
    try:
        unigrams = defaultdict()
        bigrams = defaultdict()
        trigrams = defaultdict()
        
        #process LM input data
        processLMFInput(lmFile, unigrams, bigrams, trigrams)
        
        lambdas = {'lam_1':float(lam_1),'lam_2':float(lam_2),'lam_3':float(lam_3)}
        
        processTestDataInput(testDataFile,o_ppl,unigrams,bigrams,trigrams,lambdas)
        
        
    finally:
        o_ppl.flush()
        o_ppl.close()
        lmFile.close()
        testDataFile.close()
    
    if isTest: print("main: Exiting")


##------------------------------------------------------------------------
# Process LM Input File
##------------------------------------------------------------------------
def processLMFInput(lmFile, unigrams, bigrams, trigrams):
    isTest = False
    ngram = defaultdict()
    
    for line in lmFile.readlines():
        line = line.strip('\n')
        
        #skip the line if it's a non-data line
        if re.match(r'\\data\\',line) or re.match(r'ngram',line) or re.match(r'\\end\\',line) or len(line) == 0:
            if isTest: print("non-data line:[{0}]".format(line))
            continue
        #starts with \\1-grams:
        elif re.match(r'\\1-grams:',line):
            if isTest: print("unigram: line:[{0}]".format(line))
            ngram = unigrams
            continue
        #starts with \\2-grams:
        elif re.match(r'\\2-grams:',line):
            if isTest: print("bigrams line:[{0}]".format(line))
            ngram = bigrams
            
        #starts with \\3-grams:
        elif re.match(r'\\3-grams:',line):
            if isTest: print("trigrams line:[{0}]".format(line))
            ngram = trigrams
            
        else:
            if isTest: print("data-line: [{0}]".format(line))
            ngramStats = re.split("\\s+", line)
            if len(ngramStats) == 4: #unigram
                ngram[ngramStats[3]] = (int(ngramStats[0]), float(ngramStats[1]), float(ngramStats[2]))
            elif len(ngramStats) == 5: #bigram
                token = ngramStats[3]+" "+ngramStats[4]
                ngram[token] = (int(ngramStats[0]), float(ngramStats[1]), float(ngramStats[2]))
            elif len(ngramStats) == 6: #trigram
                token = ngramStats[3]+" "+ngramStats[4]+" "+ngramStats[5]
                ngram[token] = (int(ngramStats[0]), float(ngramStats[1]), float(ngramStats[2]))
            else:
                if isTest: print("ERROR: Unknown lm data line length: line:[{0}]".format(line))
                raise ValueError
    
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Process Test Data Input File
##------------------------------------------------------------------------
def processTestDataInput(testDataFile,o_ppl,unigrams,bigrams,trigrams,lambdas):
    #isTest = True
    sentence_count = 1
    g_loov = 0
    g_word_count = 0
    g_prob_sum = 0
    g_ppl = 0
    UNSEEN_NGRAMS = "(unseen ngrams)"
    UNKNOWN_WORD = "(unknown word)"
    NEG_INF = "-inf"
    
    for line in testDataFile.readlines():
        #line specific metrics
        oov_count = 0
        ukw_count = 0
        prob_sum = 0
        
        line = line.strip('\n')
        #output format requirement, wrap sentence in standard tags
        line = "<s> " + line + " </s>"
        if isTest: print("Sent #{0}: {1}".format(sentence_count, line))
        #write the sentencing being processed
        o_ppl.write("\nSent #{0}: {1}\n".format(sentence_count, line))
        #tokenize the sentence for analysis
        tokens = re.split("\\s+", line)
        sentence_count += 1
        i=1
        while i < len(tokens):
            wi = tokens[i]
            wi1 = tokens[i-1].strip()
            wi2 = ""
            if i-2 >= 0: 
                wi2 = tokens[i-2].strip()
            
            #ngram data structure, dictionaries as: key=token, values=(tokenCount,prob,logprob); token is a string, tokenCount is an int, prob and logprob are floats
            #TODO: look for case sensitivity
            if wi in unigrams: #known word
                if isTest: print("known word: [{0}]".format(wi))
                p1 = unigrams[wi][1] #P(wi)
                p2 = 0              #P(wi | wi1)
                p3 = 0              #P(wi | wi2 wi1)
                isUnseenNgram = False
                
                #get prob 2
                #wi1_wi = wi1+" "+wi
                if isTest: print("get prob 2: [{0}]".format(wi1+" "+wi))
                if wi1+" "+wi in bigrams and wi1 in unigrams:
                    p2 = bigrams[wi1+" "+wi][1]
                else:
                    isUnseenNgram = True
                
                #get prob 3
                #wi2_wi1_wi = wi2+" "+wi1+" "+wi
                #wi2_wi1 = wi2+" "+wi1
                if not wi2 == "" and wi2+" "+wi1+" "+wi in trigrams and wi2+" "+wi1 in bigrams:
                        p3 = trigrams[wi2+" "+wi1+" "+wi][1]
                else:
                    if not wi2 == "": 
                        isUnseenNgram = True
            
                #calculate the interpolated probability from input lambda's
                interp_prob = (lambdas['lam_1']*p1)+(lambdas['lam_2']*p2)+(lambdas['lam_3']*p3)
                
                prob_sum += float(math.log10(interp_prob))
                ukw_count += 1
                unseenNgrams = ""
                if isUnseenNgram: 
                    unseenNgrams = UNSEEN_NGRAMS
                wi2_wi1 = wi2+" "+wi1
                o_ppl.write("{0}: lg P({1} | {2}) = {3:0.10f} {4}\n".format(i, wi, wi2_wi1.strip(),float(math.log10(interp_prob)),unseenNgrams))
                
            else: #unknown word
                oov_count += 1
                wi2_wi1 = wi2+" "+wi1
                o_ppl.write("{0}: lg P({1} | {2}) = {3} {4}\n".format(i, wi, wi2_wi1.strip(),NEG_INF,UNKNOWN_WORD))
            
            ##--END IF Word in Unigram
            i +=1
        ##--END WHILE LOOP on Sentence
        #output sentence level metrics
        ppl = math.pow(10,-1*(prob_sum/(ukw_count*1.0)))
        o_ppl.write("1 sentence, {0} words, {1} OOVs\n".format(len(tokens)-2,oov_count))#exclude BOS and EOS from word count
        o_ppl.write("lgprob={0} ppl={1}\n".format(prob_sum,ppl))
        o_ppl.write("\n")
        g_prob_sum += prob_sum
        g_loov += oov_count
        g_word_count += len(tokens)-2
    ##--END FOR LOOP on TEST DATA FILE
    #output test data file metrics
    sentence_count -= 1
    N = g_word_count + sentence_count - g_loov
    avg_lgprob = float(g_prob_sum/N)
    g_ppl = math.pow(10,(-1*g_prob_sum)/(N*1.0))
    
    o_ppl.write("\n{0}\n".format("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"))
    o_ppl.write("sent_num={0} word_num={1} oov_num={2}\n".format(sentence_count,g_word_count,g_loov))
    o_ppl.write("lgprob={0:0.10f} ave_lgprob={1:0.10f} ppl={2:0.10f}\n".format(g_prob_sum,avg_lgprob,g_ppl))

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