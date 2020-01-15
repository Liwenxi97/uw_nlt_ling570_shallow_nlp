**Author: Ryan Timbrook** <br>
**UW Net ID: timbrr** <br>
**Project: Ling 570 HW 8** <br>
**Date: Oct 22, 2018** <br>

##---- Q1 ----##
$baseDir = /dropbox/18-19/570/
$dataDir = hw8/20_newsgroups
$exDir = hw8/examples

Run commands:
b: mallet import-dir --input /dropbox/18-19/570/hw8/20_newsgroups/talk.politics.* --skip-header --output politics.vectors
c: vectors2info --input politics.vectors --print-matrix siw > politics.vectors.txt
d: vectors2vectors --input politics.vectors --training-portion 0.9 --training-file train1.vectors --testing-file test1.vectors
e: vectors2classify --training-file train1.vectors --testing-file test1.vectors --trainer DecisionTree >dt.stdout 2>dt.stderr
f.1: vectors2classify --training-file /dropbox/18-19/570/hw8/examples/train.vectors --testing-file /dropbox/18-19/570/hw8/examples/test.vectors --trainer NaiveBayes > NaiveBayes.stdout 2>NaiveBayes.stderr
f.2: vectors2classify --training-file /dropbox/18-19/570/hw8/examples/train.vectors --testing-file /dropbox/18-19/570/hw8/examples/test.vectors --trainer MaxEnt > MaxEnt.stdout 2>MaxEnt.stderr
f.3: vectors2classify --training-file /dropbox/18-19/570/hw8/examples/train.vectors --testing-file /dropbox/18-19/570/hw8/examples/test.vectors --trainer DecisionTree > DecisionTree.stdout 2>DecisionTree.stderr
f.4: vectors2classify --training-file /dropbox/18-19/570/hw8/examples/train.vectors --testing-file /dropbox/18-19/570/hw8/examples/test.vectors --trainer Winnow > Winnow.stdout 2>Winnow.stderr
f.5: vectors2classify --training-file /dropbox/18-19/570/hw8/examples/train.vectors --testing-file /dropbox/18-19/570/hw8/examples/test.vectors --trainer BalancedWinnow > BalancedWinnow.stdout 2>BalancedWinnow.stderr
	
Table 1: Classification results for Q1(e)
				| Training accuracy | Test accuracy
NaiveBayes		| 0.952962962962963	| 0.8966666666666666
MaxEnt			| 0.9685185185185186| 0.8266666666666667
DecisionTree	| 0.6377777777777778| 0.5233333333333333
Winnow			| 0.3340740740740741| 0.3333333333333333
BalancedWinnow	| 0.88				| 0.7633333333333333



##---- Q2 ----##
Q2: Write proc_file.sh
    - This python script processes a document and prints out the feature vectors
    
Format: command line: proc_file.sh input_file targetlabel output_file
 - 
Input File: input_file is a text file (e.g., input_ex)
    -Format: 
            - 
Output File:
   -Format: One line with the format: "instanceName targetLabel f1 v1 f2 v2 ...
        -instanceName is the filename of the input_file
        -targetLabel is the second argument of the command line
            
From Command line: 
-Run as: ./proc_file.sh /dropbox/18-19/570/hw8/examples/input_ex c1 output_ex
	-Processed:
		-Instance Name:[input_ex], TargetLabel:[c1] Total lines in inputExLines file:[52] non-header lines count:[38]
		-Total processing time:0.0092248917

##---- Q3 ----##
Q3: Write create_vectors.sh
    - This python script creates training and test vectors from several directories of documents.
    - This script has the same function as "mallet import-dir"
    
Format: command line: create_vectors.sh train_vector_file test_vector_file ratio dir1 dir2 ...
        
Input: ratio dir1 dir2 ...
    -***Note: The command line should include one or more directories
    -Ratio is the portion of the training data 

Output File: train_vector_file test_vector_file
   -Format: Same format as output from Q2
       -one line with the format as:
           -instanceName targetLabel f1 v1 f2 v2 ... (standard format)
           -label f1:v1 f2:v2 ... (svmlight format)
            
From Command line: 
-Run as: ./create_vectors.sh train.vectors.txt test.vectors.txt 0.9 /dropbox/18-19/570/hw8/20_newsgroups/talk.politics.guns /dropbox/18-19/570/hw8/20_newsgroups/talk.politics.mideast /dropbox/18-19/570/hw8/20_newsgroups/talk.politics.misc
Total processing time:9.1051619053
***** Note: ran across an issue on patas when fetching the data files from the dropbox location
		-the data files were not coming back in the sorted order of the file names. This only occured on patas, and not when i tested locally
		-to fix the sorting issue I sorted the return data list by file name since the file names are indexed values
		-see function "getFilesFromPath" for details


##---- Q4 ----##
Task: Classify the documents in the talk.politics.* groups under $dataDir

Run Commands:
	$ ./create_vectors.sh train.vectors.txt test.vectors.txt 0.9 /dropbox/18-19/570/hw8/20_newsgroups/talk.politics.guns /dropbox/18-19/570/hw8/20_newsgroups/talk.politics.mideast /dropbox/18-19/570/hw8/20_newsgroups/talk.politics.misc
	
	##convert the training and test vectors from the text format to the binary format.##
	$ mallet import-file --input train.vectors.txt --output train.vectors
	$ mallet import-file --input test.vectors.txt --output test.vectors --use-pipe-from train.vectors
	
	##training (with MaxEnt trainer) and for testing##
	Tested this, did not include in submission: $ mallet train-classifier --input train.vectors --trainer MaxEnt --output-classifier me-model --report train:accuracy >me.stdout 2>me.stderr
	Tested this, did not include in submission: ## FROM CLASS day 16 Slide 13 - Testing the Building a tagger commands ## $ mallet classify-file --input test.vectors.txt --classifier me_model --output resultFile --report test:accuracy > me_dec.stdout 2>me_dec.stderr
	
	# Ran this as final command for classification results
	$ vectors2classify --training-file train.vectors --testing-file test.vectors --trainer MaxEnt --output-classifier me-model --report train:accuracy --report test:accuracy >me.stdout 2>me.stderr
	
	
	Table 2: Classification results for Q4
				| Training accuracy | Test accuracy
	MaxEnt		| 0.9685185185185186| 0.8266666666666667
	




