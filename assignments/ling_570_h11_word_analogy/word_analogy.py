#!/usr/bin/python3
"""#### LING 570: Homework #8 - Ryan Timbrook ############
Author: Ryan Timbrook
Date: 12/06/2018
HW: 11
#Q1: Write word_analogy.sh that finds D given A, B, and D
       
Format: command line: word_analogy.sh vector_file input_dir output_dir flag1 flag2
       
Input: 
 - vector_file: has format "w v1 v2 ... vn" where <v1,v2, ..., vn> is word embedding of the word w
 - input_dir: is a directory that contains a list of test files. Test file lines have the format "A B C D", the four words of the word anology task
 - output_dir: is the directory to store the output
             - for each file under input_dir, this script creates a file with the same name under the output_dir
            - the two files have the exactly the same number of lines and the same content, except that the word
            D in the files under output_dir is the word selected by the algorithm
 - flag1: an integer flag indicating if the word embeddings should be normalized first
        - Non-Zero triggers the normalization
        - Zero indicates to just use original vectors as is
 - flag2: an integer flag indicating which similarity function to use for calculating sim(x,y)
        - Non-Zero triggers the use of cosine similarity
        - Zero triggers the use of Euclidean distance
Output File: stdout redirected to output_dir/eval_result
         - Prints accuracy metrics
        - Format:
            fileName1
            ACCURACY TOP1: acc% (cor/nuum)
            fileName2
            ACCURACY TOP1: acc% (cor/num)
            ...
            Total accuracy: accTotal% (corSum/numSum)            
From Command line, Run as: 
   ./word_analogy.sh /dropbox/18-19/570/hw11/examples/vectors.txt /dropbox/18-19/570/hw11/examples/question-data exp00 0 0 > exp00/eval_res
    ./word_analogy.sh /dropbox/18-19/570/hw11/examples/vectors.txt /dropbox/18-19/570/hw11/examples/question-data exp01 0 1 > exp01/eval_res
    ./word_analogy.sh /dropbox/18-19/570/hw11/examples/vectors.txt /dropbox/18-19/570/hw11/examples/question-data exp10 1 0 > exp10/eval_res
    ./word_analogy.sh /dropbox/18-19/570/hw11/examples/vectors.txt /dropbox/18-19/570/hw11/examples/question-data exp11 1 1 > exp11/eval_res
  
"""

import sys, time, re, os
from collections import OrderedDict
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances


#---- GLOBALS -----------------------------------------#
isTest = True
isLocal = True
cmdArgs = []

#---- LOCAL TEST ATTRIBUTES ---------------------------#
VECTOR_FILE="examples/vectors.txt"
INPUT_DIR="examples/question-data"
OUTPUT_DIR="exp00" # exp01; exp10; exp11
NORMALIZE_FLAG=0 #1=Normalize; 0=NONE
SIMILARITY_FLAG=0 #1=Cosine_similarity; 0=Euclidean_distance 

##------------------------------------------------------------------------
# DTO object for simpler reference to data elements
##------------------------------------------------------------------------
class WordAnalogy(object):
    
    def __init__(self,normFlg,simFlg):
        self.normalizationFlag = normFlg
        self.similarityFlag = simFlg
        self.wordVectors = OrderedDict()
        self.word2Idx = {}
        self.idx2Word = {}
        self.resultFileData = []
        self.pdVecDataFrame = None
        
        #accuracy metrics
        self.corCntSum = 0
        self.numCntSum = 0
        self.file_accuracys = {} #key=fileName, value is a tuple(<cor>,<num>)
        self.OOVCnt = 0
        self.OOVSet = set()
        self.OOVGoldSet = set()
  
    #calculation for normalization of word embedding vectors
    def normalize(self,v):
        norm = np.sqrt(np.sum(np.square(v)))
        return v/norm
        
    #calculate cosine similarity
    def cosineSimilarity(self,x,y):
        if self.normalizationFlag == 1: 
            y = self.normalize(y)
        return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))
        
    #calculate Euclidean distance
    def euclideanDistance(self,x,y):
        if self.normalizationFlag == 1: 
            y = self.normalize(y)
        return np.sqrt(np.sum((x - y) ** 2))
    

##------------------------------------------------------------------------
# Main Procedural Function
##------------------------------------------------------------------------
def main():
    if isTest: print("main: Entering")
    vectorFile = ""
    inputDir = ""
    outputDir = ""
    normalizationFlag = 0
    similarityFlag = 0
    
    if isLocal:
        vectorFile=VECTOR_FILE; inputDir=INPUT_DIR; outputDir=OUTPUT_DIR; normalizationFlag=NORMALIZE_FLAG; similarityFlag=SIMILARITY_FLAG
    else:
        vectorFile=cmdArgs[0]; inputDir=cmdArgs[1]; outputDir=cmdArgs[2]; normalizationFlag=int(cmdArgs[3]); similarityFlag=int(cmdArgs[4])
      
  
    if isTest: print("vectorFile:[{0}] inputDir:[{1}] outputDir:[{2}] normalizationFlag:[{3}] similarityFlag:[{4}]".format(vectorFile,inputDir,outputDir,normalizationFlag,similarityFlag))
    
    
    #create output directories
    try:
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
    except FileExistsError:
        pass
    
    wa = WordAnalogy(normalizationFlag,similarityFlag)
    #
    try:
        questionDataFiles = getFilesFromPath(inputDir)
        wordIdxIndex = loadVectors(vectorFile,wa)
        preProcessTestData(inputDir,questionDataFiles,wa,wordIdxIndex)
        wordAnalogyTask(outputDir,inputDir,questionDataFiles,wa)
        printAccuracy(wa)
        
        if isTest: print("Vocabular Metrics: OOV Instance Cnt:[{0}] OOV Unique Cnt:[{1}] Gold Standards OOV Cnt:[{2}]".format(wa.OOVCnt,len(wa.OOVSet),len(wa.OOVGoldSet)))
        
    finally:
        pass
        
    
    if isTest: print("main: Exiting")
##------------------------------------------------------------------------


##------------------------------------------------------------------------
# Utility Function 
##------------------------------------------------------------------------
def wordAnalogyTask(outDir,inputDir,testFiles,wa):
    #first word in word embedding file - used for D when A B or C are not found in training data file
    t0 = time.time()
    if isTest: print("Starting wordAnalogyTasks")
    
    firstWord = 0
    for w in wa.wordVectors:
        firstWord = w
        break
    
    #loop over test files
    for file in testFiles:
        t1 = time.time()
        #resultDataList = []
        #resultData = OrderedDict()
        fileCorCnt = 0
        fileNumCnt = 0
        o_file = open(outDir+"/"+file,'w') #open file for writing
        t_file = open(inputDir+"/"+file,'r') #open test file for reading
        testFileLines = t_file.readlines()
        
        for line in testFileLines:
            line = line.replace('\n','')
            line = line.strip()
            words = re.split("\\s+",line)
            analogy = 0
            
            #go over all words in vector file and find one that is most similar to y=xB-xA+xC
            A = wa.word2Idx[words[0]]
            B = wa.word2Idx[words[1]]
            C = wa.word2Idx[words[2]]
            D = wa.word2Idx[words[3]]
            
            useFirstWord = False
            if A in wa.wordVectors:
                vA = np.array(wa.wordVectors[A])
            else:
                #if isTest: print("***WARNING*** File:[{0}] word:[{1}] NOT FOUND IN vectors file".format(file,wa.idx2Word[A]))
                useFirstWord = True
                wa.OOVCnt +=1
                wa.OOVSet.add(wa.idx2Word[A])
            
            if B in wa.wordVectors:
                vB = np.array(wa.wordVectors[B])
            else:
                #if isTest: print("***WARNING*** File:[{0}] word:[{1}] NOT FOUND IN vectors file".format(file,wa.idx2Word[B]))
                useFirstWord = True
                wa.OOVCnt +=1
                wa.OOVSet.add(wa.idx2Word[B])
            
            if C in wa.wordVectors:
                vC = np.array(wa.wordVectors[C])
            else:
                #if isTest: print("***WARNING*** File:[{0}] word:[{1}] NOT FOUND IN vectors file".format(file,wa.idx2Word[C]))
                useFirstWord = True
                wa.OOVCnt +=1
                wa.OOVSet.add(wa.idx2Word[C])
            
            #look to see if gold standard word is in vocabulary
            if not D in wa.wordVectors:
                wa.OOVCnt +=1
                wa.OOVSet.add(wa.idx2Word[D])
                wa.OOVGoldSet.add(wa.idx2Word[D])
            
            if not useFirstWord:
                vY = vB-vA+vC
                #get similarity sim(x,y)
                if wa.similarityFlag != 0:
                    analogy = findMostSimWord_Cosine(vY,wa)
                else:
                    analogy = findMostSimWord_Euclidean(vY,wa)
            else:
                analogy = firstWord
            
            #check if analogy is equal to test word D
            wa.numCntSum +=1
            fileNumCnt +=1
            if analogy == wa.word2Idx[words[3]]:
                wa.corCntSum +=1
                fileCorCnt +=1
            else:
                #if isTest: print("***INFO*** File:[{0}] Analogy Word:[{1}] NOT EQUAL TO Test Word:[{2}]".format(file,wa.idx2Word[analogy],words[3]))
                pass
            #write output
            o_file.write("{0} {1} {2} {3}\n".format(words[0],words[1],words[2],wa.idx2Word[analogy]))
            
            #wa.resultFileData.append(OrderedDict({file:[words[0],words[1],words[2],wa.idx2Word[analogy]]}))
            
            ##--end loop over line
            #resultDataList.append([words[0],words[1],words[2],wa.idx2Word[analogy]])
            
        #--End of For Loop over file - store file accuracy metrics
        #resultData[file] = resultDataList
        wa.file_accuracys[file] = (fileCorCnt,fileNumCnt)
        #flush and close output file
        o_file.flush()
        o_file.close()
        t_file.close()
        t2 = time.time()
        
        if isTest: print("Completed Processing file:[{0}] elapsed time:[{1}]".format(file,t2-t1))
    
    t3 = time.time()
    if isTest: print("Completed Processing all files, elapsed time:[{0}]".format(file,t3-t0))
##------------------------------------------------------------------------

##------------------------------------------------------------------------
## Find most similar w
##------------------------------------------------------------------------
def findMostSimWord_Cosine(y,wa):
    #maxSim = -1.0
    #maxSimWord = ""
    cosSimsMaxIndex = 0
    #comprehension enhances process time
    #maxSim,maxSimWord = max((wa.cosineSimilarity(np.array(v),y),w) for w,v in wa.wordVectors.items())
     
    #testing packages for faster processing time -> performs 20x faster than comprehension statement above
    try:
        dfTrans = wa.pdVecDataFrame.T #transpose dataframe
        cosSims = cosine_similarity(dfTrans, y.reshape(1,-1))
        cosSimsMaxIndex = np.argmax(cosSims)
        cosSimsMaxValue = cosSims[cosSimsMaxIndex]
        #if isTest: print("Cosine Similarity: Max Similar Value for vector:[{0}]\cosSimsMaxValue:[{1}] word:[{2}]".format(y,cosSimsMaxValue,wa.idx2Word[cosSimsMaxIndex]))

    except ValueError:
        sys.stderr.write("ERROR: Caught ValueError performing cosine_similarity on vector:[{0}]".format(y))
    
    #return maxSimWord
    return cosSimsMaxIndex+1

##------------------------------------------------------------------------

##------------------------------------------------------------------------
## Find most similar w ->smaller the distance is, the more similar the two words are
## *Note: Using sklearn.metrics.pairwise.euclidean_distance package due to processing time issues with custom code
##------------------------------------------------------------------------
def findMostSimWord_Euclidean(y,wa):
    #minSim = 100.0
    #minSimWord = ""
    eucDistSimMinIndex = 0
    #comprehension enhances process time
    #minSim,minSimWord = min((wa.euclideanDistance(np.array(v),y),w) for w,v in wa.wordVectors.items())
    #if isTest: print("Euclidean Distance: Minimum Similar Value, minSim:[{0}] word:[{1}]".format(minSim,wa.idx2Word[minSimWord]))
    #testing packages for faster processing time -> performs 20x faster than comprehension statement above
    try:
        dfTrans = wa.pdVecDataFrame.T #transpose dataframe
        eucDists = euclidean_distances(dfTrans,y.reshape(1,-1))
        eucDistSimMinIndex = np.argmin(eucDists)
        eucDistSimMinValue = eucDists[eucDistSimMinIndex]
        #if isTest: print("Euclidean Distance: Minimum Similar Value for vector:[{0}]\neucDistSimMinValue:[{1}] word:[{2}]".format(y,eucDistSimMinValue,wa.idx2Word[eucDistSimMinIndex+1]))
    except ValueError:
        sys.stderr.write("ERROR: Caught ValueError performing euclidean_distances on vector:[{0}]".format(y))
        
    #return minSimWord
    return eucDistSimMinIndex+1

##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Utility Function to normalize vectors
# has format "w v1 v2 ... vn" where <v1,v2, ..., vn> is word embedding of the word w
##------------------------------------------------------------------------
def loadVectors(vecFile,wa):
  
    with open(vecFile,'r') as v:
        vectors = v.readlines()
    
    wordIndex = 1
    #pdCols = []
    #pdVecs = []
    for line in vectors:
        if len(line) <= 1: continue
        
        line = line.replace('\n','')
        line = line.strip()
        
        tokens = re.split('\\s+',line)
        
        if not tokens[0] in wa.word2Idx:
            wa.word2Idx[tokens[0]] = wordIndex
            wa.idx2Word[wordIndex] = tokens[0]
            wa.wordVectors[wordIndex] = [float(i) for i in tokens[1:]]
            wordIndex += 1
    
    #test numpy n-dim array
    #wordvecs = np.array([[vec]for vec in wa.wordVectors.values()])
    
    #normalize if flag is == 1
    if wa.normalizationFlag == 1:
        wa.wordVectors = {w:wa.normalize(v) for w,v in wa.wordVectors.items()}
        
    #tests pandas dataframe
    #pdData = np.array([[cols]for cols in pdCols],[[vecs]for vecs in pdVecs])
    wa.pdVecDataFrame = pd.DataFrame(wa.wordVectors)
    #print(wa.pdVecDataFrame.head(5))
    return wordIndex
    
##------------------------------------------------------------------------

##------------------------------------------------------------------------
# Pre-Process question-data test files
##------------------------------------------------------------------------
def preProcessTestData(inputDir,testFiles,wa,wordidx):
    wordIndex = wordidx+1
    
    for file in testFiles:
        t_file = open(inputDir+"/"+file,'r')
        testFileLines = t_file.readlines()
        
        for line in testFileLines:
            line = line.replace('\n','')
            line = line.strip()
            words = re.split("\\s+",line)
            
            for w in words:
                if not w in wa.word2Idx:
                    wa.word2Idx[w] = wordIndex
                    wa.idx2Word[wordIndex] = w
                    wordIndex +=1
            ##--end loop over line words
        ##--end loop over test file lines
        t_file.close()
    ##--end loop over all test files
    

##------------------------------------------------------------------------

##------------------------------------------------------------------------
# File IO - Helper Functions - Gets  file locations
##------------------------------------------------------------------------
def getFilesFromPath(path):
    dataFiles = []
    
    dataFiles = next(os.walk(path))[2]#get only files
    #if isTest: print("Top 5 data files in path:[{0}]\n[{1}]".format(path,dataFiles[:5]))
    
    return dataFiles    
##------------------------------------------------------------------------


##------------------------------------------------------------------------
# Utility Function to print accuracy metrics
##------------------------------------------------------------------------
def printAccuracy(wa):
    
    for file,acc in wa.file_accuracys.items():
        sys.stdout.write("{0}:\n".format(file))
        sys.stdout.write("ACCURACY TOP1: {0}% ({1}/{2})\n".format(round((acc[0]/acc[1])*100,2),acc[0],acc[1]))
    
    sys.stdout.write("\n")
    sys.stdout.write("Total accuracy: {0}% ({1}/{2})\n".format(round((wa.corCntSum/wa.numCntSum)*100,2),wa.corCntSum,wa.numCntSum))


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
    if isTest: print("Total word_analogy.py processing time:{0:0.10f}\n".format(duration))
    