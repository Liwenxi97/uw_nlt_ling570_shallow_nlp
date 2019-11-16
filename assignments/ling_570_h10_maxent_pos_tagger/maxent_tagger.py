#!/usr/bin/python3
"""#### LING 570: Homework #8 - Ryan Timbrook ############
Author: Ryan Timbrook
Date: 12/06/2018
HW: 10
Q1: Write maxent_tagger.sh
    - Create a MaxEnt POS tagger
    
Format: command line: maxent_tagger.sh train_file test_file rare_thres feat_thres output_dir
        
Input: (e.g., test.word_pos)
    -train_file: Format: w1/t1 w2/t2 ... wn/tn
    -test_file: Format: w1/t1 w2/t2 ... wn/tn
    -rare_thres: type=Integer
        -> any words in training and test that appear less than this value are treated as rear words
        -> features such as pref=xx and suf=xx should be used for rare_words
    -feat_thres: type=Integer
        -> all CurrentWord=xx features, regardless of their frequency, should be kept. For all other
            types of features, if a feature appears less than this value in the train_file, that feature
            should be removed from the feature vectors
Output File: (output_dir is a directory that stores the output files from the tagger)
        Create and store the following files under this directory
        -train_voc
        -init_feats
        -kept_feats
        -final_train.vectors.txt
        -final_test.vectors.txt
            
From Command line, Run as: ./maxent_tagger.sh wsj_sec0.word_pos test.word_pos 1 1 res_1_1
   
"""

import sys, time, re, os
from collections import Counter, OrderedDict, namedtuple
from operator import attrgetter


#---- GLOBALS -----------------------------------------#
isTest = True
isLocal = True
cmdArgs = []
TRAIN_VOC = "train_voc"
INIT_FEATS = "init_feats"
KEPT_FEATS = "kept_feats"
FINAL_TRAIN_VECTORS = "final_train.vectors.txt"
FINAL_TEST_VECTORS = "final_test.vectors.txt"
BI_BOS = "BOS/BOS BOS/BOS "
BI_EOS = " EOS/EOS EOS/EOS"
FEAT_CUR_W = "curW="
FEAT_PREV_W = "prevW="
FEAT_PREV_2_W = "prev2W="
FEAT_NEXT_W = 'nextW='
FEAT_NEXT_2_W = 'next2W='
FEAT_PREV_T = "prevT="
FEAT_PREV_TWO_TAGS = "prevTwoTags="
FEAT_PREF = "pref="
FEAT_SUF = "suf="
FEAT_CONTAIN_NUM = "containNum"
FEAT_CONTAIN_UC = "containUC"
FEAT_CONTAIN_HYP = "containHyp"


#---- LOCAL TEST ATTRIBUTES ---------------------------#
TEST_TRAIN_FILE="examples/wsj_sec0.word_pos"
TEST_TEST_FILE="examples/test.word_pos"
TEST_RARE_THRES=5 #1; 1; 2; 3; 5
TEST_FEAT_THRES=10 #1; 3; 3; 5; 10
TEST_OUTPUT_DIR="res_5_10" #res_1_1; res_1_3; res_2_3; res_3_5; res_5_10


##------------------------------------------------------------------------
# DTO object for simpler reference to data elements
##------------------------------------------------------------------------
class MaxEnt(object):
    
    def __init__(self,rareThres,featThres):
        self._trainWordCnt = 0
        self._trainTagCnt = 0
        self._trainSentCnt = 0
        self._trainRareWordCnt = 0
        self._trainInitFeatCnt = 0
        self._trainKeptFeatCnt = 0
        self._testWordCnt = 0
        self._testSentCnt = 0
        self._testUnkWordCnt = 0
        self._rareThres = rareThres
        self._featThres = featThres
        self._trainVOC = {}
        self._trainTags = set()
        self._trainRareWords = {}
        self._initialFeatures = {}
        self._keptFeatures = {}
    
    def setTrainVOC(self,voc):
        self._trainVOC = voc
        self._trainWordCnt = sum(self._trainVOC.values())
    
    def setTrainRareWords(self,rareWords):
        self._trainRareWords = rareWords
        self._trainRareWordCnt = sum(self._trainRareWords.values())
    
    def setTrainInitFeatures(self,feats):
        self._initialFeatures = feats
        self._trainInitFeatCnt = sum(self._initialFeatures.values())
        
    def setTrainKeptFeatures(self,feats):
        self._keptFeatures = feats
        self._trainKeptFeatCnt = sum(self._keptFeatures.values())
    
    #-- Utility Functions; Feature Condition Rules (Ratnaparkhi, 1996(
    def isRareWord(self,word):
        if word in self._trainRareWords:
            return True
        else:
            return False
    
    ##-- Conditions applied to rare words --##
    def containsNumbers(self,word):
        return bool(re.search(r'\d',word))
    
    def isAllUpperCaseCharacters(self,word):
        p = re.compile(r'^[A-Z]+$')
        return bool(p.match(word))
    
    def isAllLowerCase(self,word):
        p = re.compile(r'^[a-z]+$')
        return bool(p.match(word))
    
    def containsMixedCase(self,word):
        uppers = re.findall(r'[A-Z]',word)
        if len(uppers) > 0:
            return True
        else:
            return False
        
    def containsHyphen(self,word):
        hyp = re.findall(r'\w+(?:-\w+)+',word)
        if len(hyp) > 0:
            return True
        else:
            return False
    
    def wordPrefix(self,word):
        pMax = 4
        pref = ""
        prefs = []
        for i,c in enumerate(word,1):
            if not i <= pMax: break
            pref += c
            prefs.append(pref)
        return prefs
    
    def wordSuffix(self,word):
        sMax = 4
        suf = ""
        sufs = []
        for i,c in enumerate(word[::-1],1):
            if not i <= sMax: break
            suf += c
            sufs.append(suf[::-1])
        return sufs
    
    ##-- End rare word conditions --##
    
    #-- End Feature Condition Util Functions
        
    

##------------------------------------------------------------------------
# Main Procedural Function
##------------------------------------------------------------------------
def main():
    if isTest: print("main: Entering")
    trainFile = ""
    testFile = ""
    rareThres = 0
    featThres = 0
    outputDir = ""
    
    if isLocal:
        trainFile=TEST_TRAIN_FILE; testFile=TEST_TEST_FILE; rareThres=TEST_RARE_THRES; featThres=TEST_FEAT_THRES; outputDir=TEST_OUTPUT_DIR
    else:
        trainFile=cmdArgs[0]; testFile=cmdArgs[1]; rareThres=int(cmdArgs[2]); featThres=int(cmdArgs[3]); outputDir=cmdArgs[4]
      
  
    if isTest: print("trainFile:[{0}] testFile:[{1}] rareThres:[{2}] featThres:[{3}] outputDir:[{4}]".format(trainFile,testFile,rareThres,featThres,outputDir))
    
    
    #create output directories
    try:
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
    except FileExistsError:
        pass
    
    me = MaxEnt(rareThres,featThres)
    #
    try:
        
        createTrainVOC(trainFile,TRAIN_VOC,me,outputDir)
        createInitFeats(trainFile,INIT_FEATS,me,outputDir)
        createKeptFeats(KEPT_FEATS,me,outputDir)
        createTrainFeatureVectors(trainFile,FINAL_TRAIN_VECTORS,me,outputDir)
        createTestFeatureVectors(testFile,FINAL_TEST_VECTORS,me,outputDir)
        
        sys.stdout.write("# of feats:[{0}] # of kept feats:[{1}]\n".format(me._trainInitFeatCnt,me._trainKeptFeatCnt))
                
    finally:
        pass
        
    
    if isTest: print("main: Exiting")
##------------------------------------------------------------------------


##------------------------------------------------------------------------
# Process Step:1
# Create train_voc from train_file, and use the word frequency in train_voc
# and rare_thres to determine whether a word should be treated as a rare word
# the feature vectors for rare words and non-rare words are different
##------------------------------------------------------------------------
def createTrainVOC(trainFile,trainVOCFile,me,outDir):
    rareWords = []
    trainVOC = Counter()
    trainTags = set()
    
    #open training file for reading
    with open(trainFile,'r') as f:
        train = f.readlines()
    
    sentCnt = 0
    #line format: w1/t1 w2/t2 ... wn/tn
    for i,line in enumerate(train):
        if len(line) <= 1: continue
        sentCnt += 1
        line = line.replace('\n','')
        line = line.strip()
        
        wordTags = re.split('\\s+',line)
        
        lineWords = []
        #each word/pos in sentence
        for wt in wordTags:
            #[word,pos]
            w,t = splitWordTag(wt)
            lineWords.append(w)
            me._trainTags.add(t)
        
        #count frequency of words
        trainVOC.update(Counter(lineWords))    
    #--end for loop over lines
    me._trainSentCnt = sentCnt
    me._trainTagCnt = len(me._trainTags)
    
    #sort by freq in descending order. for words with same frequency, sort the lines alphabetically
    WordFreq = namedtuple('WordFreq','word,freq')
    wordFrequencies = [WordFreq._make([k,v]) for k,v in trainVOC.items()]
    wordFrequencies = sorted(sorted(wordFrequencies, key=attrgetter('word')), key=attrgetter('freq'), reverse=True)
    
    me.setTrainVOC(OrderedDict(wordFrequencies))
    
    #get rareWords list
    #TODO: is rare words calculated by Less Than threshold or Less Than Equal to threshold?
    me.setTrainRareWords(OrderedDict([(wf.word,wf.freq) for wf in wordFrequencies if wf.freq < me._rareThres]))
    
    #print train_voc
    with open(outDir+"/"+trainVOCFile,'w') as o_voc:
        
        for wf in wordFrequencies:
            o_voc.write("{0} {1}\n".format(wf.word,wf.freq))
        
        o_voc.flush()
    
    o_voc.close()
    

##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Process Step:2
# Form feature vectors for the words in train_file, and store the features 
# and frequencies in the training data in init_feats
# 
##------------------------------------------------------------------------
def createInitFeats(trainFile,trainInitFeatsFile,me,outDir):
    words = []
    tags = []
    initFeats = Counter()
    
    #open training file for reading
    with open(trainFile,'r') as f:
        train = f.readlines()
    
    #line format: w1/t1 w2/t2 ... wn/tn
    for line in train:
        if len(line) <= 1: continue
        line = line.replace('\n','')
        line = BI_BOS+replaceCommas(line.strip())+BI_EOS #Insert BOS/BOS and EOS/EOS POS Tagging scheme
        
        wordTags = re.split('\\s+',line)
        
        lineWords = []
        lineTags = []
        #each word/pos in sentence
        for wt in wordTags:
            #[word,pos]
            w,t = splitWordTag(wt)
            lineWords.append(w)
            lineTags.append(t)
        
        #start at 3rd word in list, i=2
        i=2
        lineFeats = []
        while i<len(lineWords)-2:
            curW = lineWords[i]
            #check if curW is a rare word
            if not me.isRareWord(curW):
                #word is not rare word
                lineFeats.append(FEAT_CUR_W+curW)
            else:
                #word is rare word
                #does the word contain numbers?
                if me.containsNumbers(curW):
                    lineFeats.append(FEAT_CONTAIN_NUM)
                
                #does the word contain uppercase characters?
                if me.containsMixedCase(curW):
                    lineFeats.append(FEAT_CONTAIN_UC)
                
                #does the word contain hyphens
                if me.containsHyphen(curW):
                    lineFeats.append(FEAT_CONTAIN_HYP)
                
                #what is the words prefix?
                pre = me.wordPrefix(curW)
                for p in pre:
                    lineFeats.append(FEAT_PREF+p)
                
                #what is the words suffix?
                suf = me.wordSuffix(curW)
                for s in suf:
                    lineFeats.append(FEAT_SUF+s)
            #--End Rare Word Conditions
            #Feature Conditions applied to all wi words (Ratnaparkhi, 1996)
            lineFeats.append(FEAT_PREV_W + lineWords[i-1])
            lineFeats.append(FEAT_PREV_2_W + lineWords[i-2])
            lineFeats.append(FEAT_PREV_T + lineTags[i-1])
            lineFeats.append(FEAT_PREV_TWO_TAGS + lineTags[i-2]+"+"+lineTags[i-1])
            lineFeats.append(FEAT_NEXT_W + lineWords[i+1])
            lineFeats.append(FEAT_NEXT_2_W + lineWords[i+2])
            
            #update counter
            i+=1
        #--End loop over words
        #update feature counter
        initFeats.update(Counter(lineFeats))
    #--end for loop over lines
    
    #sort by freq in descending order. for features with same frequency, sort the lines alphabetically
    FeatureFreq = namedtuple('FeatureFreq','feat,freq')
    featureFrequencies = [FeatureFreq._make([k,v]) for k,v in initFeats.items()]
    featureFrequencies = sorted(sorted(featureFrequencies, key=attrgetter('feat')), key=attrgetter('freq'), reverse=True)
    
    me.setTrainInitFeatures(OrderedDict(featureFrequencies))
    
    #print init_feats
    with open(outDir+"/"+trainInitFeatsFile,'w') as o_init_feats:
        
        for ff in featureFrequencies:
            o_init_feats.write("{0} {1}\n".format(ff.feat,ff.freq))
        
        o_init_feats.flush()
    
    o_init_feats.close()
    

##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Process Step:3
# Create kept_feats by using feat_thres to filter out low frequency features in init_feats
# ****wi features are NOT subject to filtering with feat_thres. Every wi feature
# in init_feats should be kept in kept_feats
##------------------------------------------------------------------------
def createKeptFeats(trainKeptFeatFile,me,outDir):
    keptFeats = []
    
    #Output filtered list for debugging analysis
    filteredFile = open(outDir+"/"+"filtered_features.txt",'w')
    
    #Open kept_feat file for writing
    o_keptFeatures = open(outDir+"/"+trainKeptFeatFile,'w')
        
    for feat,freq in me._initialFeatures.items():
        if freq < me._featThres and not bool(re.search(r'curW',feat)):
            #filter out low frequency features
            filteredFile.write("Filtered Features: feat:[{0}] freq:[{1}]\n".format(feat,freq))
        else:
            #keep feature
            o_keptFeatures.write("{0} {1}\n".format(feat,freq))
            keptFeats.append((feat,freq))
    #--End loop over initial features
    me.setTrainKeptFeatures(OrderedDict(keptFeats))
    
    filteredFile.flush()
    filteredFile.close()
    o_keptFeatures.flush()
    o_keptFeatures.close()

##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Process Step:4
# Of the feature vector file for train_file, removes all of the features that are not in kept_feats
# Output File Format: <lineNum>"-"<TokenIndex>"-"<Word> <Tag> <f1> <f1Cnt> <f2> <f2Cnt> ... <fn> <fnCnt>
# Output File Name: final_train.vectors.txt
##------------------------------------------------------------------------
def createTrainFeatureVectors(inputFile,outputFile,me,outDir):
    
    #open output file for writing
    o_final_train_vectors = open(outDir+"/"+outputFile,'w')
    
    #open input training file for reading
    with open(inputFile,'r') as f:
        train = f.readlines()
    
    #line format: w1/t1 w2/t2 ... wn/tn
    lineIndex = 1
    for line in train:
        if len(line) <= 1: continue
        line = line.replace('\n','')
        line = BI_BOS+replaceCommas(line.strip())+BI_EOS #Insert BOS/BOS and EOS/EOS POS Tagging scheme
        
        wordTags = re.split('\\s+',line)
        
        lineWords = []
        lineTags = []
        #each word/pos in sentence
        for wt in wordTags:
            #[word,pos]
            w,t = splitWordTag(wt)
            lineWords.append(w)
            lineTags.append(t)
        #--End loop over word tag pairs
        #start at 3rd word in list, i=2
        i=2
        while i<len(lineWords)-2:
            curW = lineWords[i]
            wordFeats = []
            wordFeatsCntr = Counter()
            #check if curW is a rare word
            if not me.isRareWord(curW):
                #word is not rare word
                wordFeats.append(FEAT_CUR_W+curW)
            else:
                #word is rare word
                #does the word contain numbers?
                if me.containsNumbers(curW):
                    wordFeats.append(FEAT_CONTAIN_NUM)
                
                #does the word contain uppercase characters?
                if me.containsMixedCase(curW):
                    wordFeats.append(FEAT_CONTAIN_UC)
                
                #does the word contain hyphens
                if me.containsHyphen(curW):
                    wordFeats.append(FEAT_CONTAIN_HYP)
                
                #what is the words prefix?
                pre = me.wordPrefix(curW)
                for p in pre:
                    wordFeats.append(FEAT_PREF+p)
                
                #what is the words suffix?
                suf = me.wordSuffix(curW)
                for s in suf:
                    wordFeats.append(FEAT_SUF+s)
            #--End Rare Word Conditions
            #Feature Conditions applied to all wi words (Ratnaparkhi, 1996)
            wordFeats.append(FEAT_PREV_W + lineWords[i-1])
            wordFeats.append(FEAT_PREV_2_W + lineWords[i-2])
            wordFeats.append(FEAT_PREV_T + lineTags[i-1])
            wordFeats.append(FEAT_PREV_TWO_TAGS + lineTags[i-2]+"+"+lineTags[i-1])
            wordFeats.append(FEAT_NEXT_W + lineWords[i+1])
            wordFeats.append(FEAT_NEXT_2_W + lineWords[i+2])
            
            
            wordFeatsCntr.update(Counter(wordFeats))
            ##--This section creates the final_train.vectors.txt file --##
            # -- Format: <lineNum>"-"<TokenIndex>"-"<Word> <Tag> --#
            o_final_train_vectors.write("{0}-{1}-{2} {3}".format(str(lineIndex),str(i-2),lineWords[i],lineTags[i]))
            #print("{0}-{1}-{2} {3} ".format(str(lineIndex),str(i-2),lineWords[i],lineTags[i]))
            
            # -- Format: <f1> <f1Cnt> <f2> <f2Cnt> ... <fn> <fnCnt> --#
            # -- Remove all features that are not in kept_feats --#
            #sort by freq in descending order. for features with same frequency, sort the lines alphabetically
            FeatureFreq = namedtuple('FeatureFreq','feat,freq')
            featureFrequencies = [FeatureFreq._make([k,v]) for k,v in wordFeatsCntr.items()]
            featureFrequencies = sorted(sorted(featureFrequencies, key=attrgetter('feat')), key=attrgetter('freq'), reverse=True)
            
            for ff in featureFrequencies:
                if ff.feat in me._keptFeatures:
                    o_final_train_vectors.write(" {0} {1}".format(ff.feat,ff.freq))
                    #print("{0} {1}".format(ff.feat,ff.freq))
            
            # -- Add Newline --#
            o_final_train_vectors.write("\n")
            
            #increment line word counter
            i+=1
        
        #increment line index counter
        lineIndex +=1
    #--End loop over lines in training file
    
    
    o_final_train_vectors.flush()
    o_final_train_vectors.close()
    
    
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Process Step:5
# Create feature vectors for test_file. Use only the features in kept_feats.
# If a word in the test_file appears Less Than rare_thres or does not appear
# at all in the training_file, the word should be treated as a rare word
# even if it appears many times in the test_file
##------------------------------------------------------------------------
def createTestFeatureVectors(inputFile,outputFile,me,outDir):
    testVOC = Counter()
    #open output file for writing
    o_final_test_vectors = open(outDir+"/"+outputFile,'w')
    
    #open input training file for reading
    with open(inputFile,'r') as f:
        test = f.readlines()
    
    #line format: w1/t1 w2/t2 ... wn/tn
    lineIndex = 1
    for line in test:
        if len(line) <= 1: continue
        line = line.replace('\n','')
        line = BI_BOS+replaceCommas(line.strip())+BI_EOS #Insert BOS/BOS and EOS/EOS POS Tagging scheme
        
        wordTags = re.split('\\s+',line)
        
        lineWords = []
        lineTags = []
        #each word/pos in sentence
        for wt in wordTags:
            #[word,pos]
            w,t = splitWordTag(wt)
            lineWords.append(w)
            lineTags.append(t)
        #--End loop over word tag pairs
        testVOC.update(Counter(lineWords))
        
        #start at 3rd word in list, i=2
        i=2
        while i<len(lineWords)-2:
            curW = lineWords[i]
            wordFeats = []
            wordFeatsCntr = Counter()
            #check if curW is a rare word
            if not me.isRareWord(curW):
                #word is not rare word
                wordFeats.append(FEAT_CUR_W+curW)
            else:
                #word is rare word
                #does the word contain numbers?
                if me.containsNumbers(curW):
                    wordFeats.append(FEAT_CONTAIN_NUM)
                
                #does the word contain uppercase characters?
                if me.containsMixedCase(curW):
                    wordFeats.append(FEAT_CONTAIN_UC)
                
                #does the word contain hyphens
                if me.containsHyphen(curW):
                    wordFeats.append(FEAT_CONTAIN_HYP)
                
                #what is the words prefix?
                pre = me.wordPrefix(curW)
                for p in pre:
                    wordFeats.append(FEAT_PREF+p)
                
                #what is the words suffix?
                suf = me.wordSuffix(curW)
                for s in suf:
                    wordFeats.append(FEAT_SUF+s)
            #--End Rare Word Conditions
            #Feature Conditions applied to all wi words (Ratnaparkhi, 1996)
            wordFeats.append(FEAT_PREV_W + lineWords[i-1])
            wordFeats.append(FEAT_PREV_2_W + lineWords[i-2])
            wordFeats.append(FEAT_PREV_T + lineTags[i-1])
            wordFeats.append(FEAT_PREV_TWO_TAGS + lineTags[i-2]+"+"+lineTags[i-1])
            wordFeats.append(FEAT_NEXT_W + lineWords[i+1])
            wordFeats.append(FEAT_NEXT_2_W + lineWords[i+2])
            
            
            wordFeatsCntr.update(Counter(wordFeats))
            ##--This section creates the final_train.vectors.txt file --##
            # -- Format: <lineNum>"-"<TokenIndex>"-"<Word> <Tag> --#
            o_final_test_vectors.write("{0}-{1}-{2} {3}".format(str(lineIndex),str(i-2),lineWords[i],lineTags[i]))
            #print("{0}-{1}-{2} {3} ".format(str(lineIndex),str(i-2),lineWords[i],lineTags[i]))
            
            # -- Format: <f1> <f1Cnt> <f2> <f2Cnt> ... <fn> <fnCnt> --#
            # -- Remove all features that are not in kept_feats --#
            #sort by freq in descending order. for features with same frequency, sort the lines alphabetically
            FeatureFreq = namedtuple('FeatureFreq','feat,freq')
            featureFrequencies = [FeatureFreq._make([k,v]) for k,v in wordFeatsCntr.items()]
            featureFrequencies = sorted(sorted(featureFrequencies, key=attrgetter('feat')), key=attrgetter('freq'), reverse=True)
            
            for ff in featureFrequencies:
                if ff.feat in me._keptFeatures:
                    o_final_test_vectors.write(" {0} {1}".format(ff.feat,ff.freq))
                    #print("{0} {1}".format(ff.feat,ff.freq))
            
            # -- Add Newline --#
            o_final_test_vectors.write("\n")
            
            #increment line word counter
            i+=1
        
        #increment line index counter
        lineIndex +=1
    #--End loop over lines in training file
    me._testSentCnt = lineIndex-1
    me._testWordCnt = sum(testVOC.values())
    
    o_final_test_vectors.flush()
    o_final_test_vectors.close()
    

##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Process Step:6
# For feature vector files, replace all the occurances of "," with 'comma'
##------------------------------------------------------------------------
def replaceCommas(sent):
    newSent = ""
    
    newSent = sent.replace(',','comma')
    
    return newSent

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
    sys.stdout.write("Total maxent_tagger.py processing time:{0:0.10f}\n".format(duration))
    