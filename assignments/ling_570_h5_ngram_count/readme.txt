Author: Ryan Timbrook 
UW Net ID: timbrr 
Project: Ling 570 HW 5
Date: Nov 1, 2018

##---- Q1 ----##
Q1: Write ngram_count

This python script collects unigrams, bigrams, and trigrams:

Format: command line: ngram_count.sh training_data ngram_count_file
Input File: training_data
Output File: ngram_count_file

-Format of the training data:
    w1 w2 ... w_n; one sentence per line
-Format of the ngram_count file is: 
    count word1 ... word_k
    -As output order matters:
        1st: unigrams
        2nd: bigrams
        3rd: trigrams
    -As output, n-gram chunks are sorted by frequency in descending order.
        -if frequency's are the same, sort by ngrams alphabetically
    -BOS as <s>
    -EOS as </s>
    
Ran as: 
    $ ./ngram_count.sh training_data ngram_count_file


**** There are performance issues when running the program against the wsj_sec0_19.word training data.
The size of the data file cause the secondary sort algorithm to take to much time to process. When applying the function
to sort the n-gram output file alphategically when the frequencies are the same. 
When the program is ran against the sample training data file, 'training_data_ex' the process time is:
Total processing time:22.9651584625

There are two methods in the main function that sort and print the output. 

sortPrint(ngram,o_file) -> This method sorts only at the frequency level, this is what was ran against the real training data file due to performance issues with the complete sorting method 
printSortSubDictChunks(sgram,o_file) -> This method sorts on both frequency and then on alphabetic when the n-grams have the same frequency. It runs fine against the sample training data file, but takes 20+ minutes against the real training data file.


##---- Q2 ----##
Q2: Write build_lm

This shell script executes a python program that builds an LM using ngram counts:

Format: command line: build_lm.sh ngram_count_file lm_file
Input File: ngram_count_file (produced as output from Q1, ngram_count.py)
Output File: lm_file (follows ARPA format)

**Special Instructions: 
    -For prob and lgprob numbers on each line, truncate to ten places after the decimal
    -DO NOT USE SMOOTHING for the probability distributions

Ran as: 
    $ ./build_lm.sh ngram_count_file lm_file


##---- Q3 ----##
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



##---- Q4 ----##
./ngram_count.sh hw5/examples/wsj_sec0_19.word wsj_sec0_19.ngram_count

ngram_count.sh
This program runs fine when sorting the n-gram lines by frequency, but when applying logic to sort
the line alphabetically when two or more n-grams have the same frequency, this application performs
poorly on the large training data set. The test_data set was fine and sorting these sub chunks of the
data set wasn't an issue.

This is the processing time for the program when only applying sorting at the n-gram frequency level
The additional sorting method applied if the frequencies are the same is commented out in the main function of the ngram_count.py program
**ngram_count.sh: Total processing time:8.2060225010

./build_lm.sh wsj_sec0_19.ngram_count wsj_sec0_19.lm
build_lm.sh: 	Total processing time:37.0849130154

./ppl.sh wsj_sec0_19.lm 0.05 0.15 0.8 570/hw5/examples/wsj_sec22.word ppl_0.05_0.15_0.8
./ppl.sh wsj_sec0_19.lm 0.1 0.1 0.8 570/hw5/examples/wsj_sec22.word ppl_0.1_0.1_0.8
./ppl.sh wsj_sec0_19.lm 0.2 0.3 0.5 570/hw5/examples/wsj_sec22.word ppl_0.2_0.3_0.5
./ppl.sh wsj_sec0_19.lm 0.2 0.5 0.3 570/hw5/examples/wsj_sec22.word ppl_0.2_0.5_0.3
./ppl.sh wsj_sec0_19.lm 0.2 0.7 0.1 570/hw5/examples/wsj_sec22.word ppl_0.2_0.7_0.1
./ppl.sh wsj_sec0_19.lm 0.2 0.8 0 570/hw5/examples/wsj_sec22.word ppl_0.2_0.8_0
./ppl.sh wsj_sec0_19.lm 1.0 0 0 570/hw5/examples/wsj_sec22.word ppl_1.0_0_0

ppl.sh: 		Total processing time:25.626607179

lambda_1	lambda_2	lambda_3	Perplexity
0.05			0.15	0.8			399.7492045413
0.1				0.1		0.8			378.6184198758
0.2				0.3		0.5			237.2555441229	
0.2				0.5		0.3			213.7026970508
0.2				0.7		0.1			212.3350581220
0.2				0.8		0			236.5229223156
1.0				0		0			998.6719067522

