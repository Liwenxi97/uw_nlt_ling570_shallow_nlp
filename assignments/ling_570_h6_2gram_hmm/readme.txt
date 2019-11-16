Author: Ryan Timbrook 
UW Net ID: timbrr 
Project: Ling 570 HW 6
Date: Nov 8, 2018

##---- Q1 ----##
Q1: Write create_2gram_hmm.sh

This python program that:
    -takes annotated training data as input and creates an HMM for a Bigram POS tagger
    -NO SMOOTHING
Format: command line: cat training_data | create_2gram_hmm.sh output_hmm
Input File: training_data as std input
    -Format: "w1/t1 ... wn/tn" (wsj_sec0.word_pos)    
Output File: output_hmm ()
   -Format: 
        -prob and lgprob -> truncate to 10 digits past decimal (0.0000000001)
        -sort probabilities alphabetically on the 1st field (state or from_state) first
        -then, for lines with same 1st field, sort on the second field (symbol)
            
From Command line, Run as: 
    $ cat wsj_sec0.word_pos | ./create_2gram_hmm.sh q4/2g_hmm

Total processing time:0.3648056984

##---- Q2 ----##
Q2: Write create_3gram_hmm.sh

This python program that:
    -takes annotated training data as input and creates an HMM for a Trigram POS tagger
    -WITH SMOOTHING
Format: command line: cat training_data | create_3gram_hmm.sh output_hmm l1 l2 l3 unk_prob_file
Input File: training_data as std input
    -Format: "w1/t1 ... wn/tn" (wsj_sec0.word_pos)
Input File: unk_prob_file (used to smooth P(word | tag)
    -Format: "tag prob"
        -prob -> P(< unk > | tag)
l1,l2,l3 are lambda's used in interpolation
Output File: output_hmm (same format as Q1)
   -Format: 
        -prob and lgprob -> truncate to 10 digits past decimal (0.0000000001)
        -sort probabilities alphabetically on the 1st field (state or from_state) first
        -then, for lines with same 1st field, sort on the second field (symbol)
        
            
From Command line, Run as: 
    $ cat wsj_sec0.word_pos | ./create_3gram_hmm.sh q4/3g_hmm_0.1_0.1_0.8 0.1 0.1 0.8 unk_prob_sec22
    $ cat wsj_sec0.word_pos | ./create_3gram_hmm.sh q4/3g_hmm_0.2_0.3_0.5 0.2 0.3 0.5 unk_prob_sec22

Total processing time:19.1067469120

##---- Q3 ----##
Date: 11/8/2018
#Q3: Write check_hmm.sh
This shell script executes a python program that:
    -Reads in a state-emission HMM file, check's its format, and outputs a warning file
    -****Store's HMM file in an EFFICIENT DATA STRUCTURE****
Format: command line: check_hmm.sh input_hmm > warning_file
 - Check's whether the two parts of the HMM file are consistent
        -Do the number of states in the header match that in the distributions?
        -Are the three kinds of constraints for HMM met?
            -print out to warning file if either rules aren't met
Input File: input_hmm (state-emission HMM file that was output from Q2 program execution) 
Output File: warning_file ()

********** 	HMM Storage Data Structure *******************************************************************************
**	Created a base DTO object called HMM that contained the core attributes for storage
**  From day-13 page 31 lecture - Approach #2:
** - They include a
		ATTRIBUTE 		| 	DATA TYPE 				| 	DESCRIPTION
		header			|	OrderedDict				| collection object that stores the hmm input header data
  		state2Idx		|	dictionary				| maintains the state name as the key and it's value as a unique integer
  		symbol2Idx		|	dictionary				| maintains the symbol name as the key and it's value as a unique integer
  		idx2State		|	dictionary				| inverse of state2Idx key:value mapping
  		idx2Symbole		|	dictionary				| inverse of symbol2Idx key:value mapping
  		initProbs		|	dictionary				| maintains the init probs key:value mapping where the key is the unique integer representation of a state, value is it's probability sum
  		transitionProbs	|	2-dimensional array		| 2-d sparse matrix of state transition probabilities
  		emissionProbs	|	2-dimensional array		| 2-d sparse matrix of state emission probabilities
******----------------------------------------------------------------------------------------------------------------******
            
From Command line, Run as: 
    $ ./check_hmm.sh q4/2g_hmm > q4/2g_hmm.warning							##Total processing time:0.8406012058
    $ ./check_hmm.sh q4/3g_hmm_0.1_0.1_0.8 > q4/3g_hmm_0.1_0.1_0.8.warning	##Total processing time:45.6497781277
    $ ./check_hmm.sh q4/3g_hmm_0.2_0.3_0.5 > q4/3g_hmm_0.2_0.3_0.5.warning	##Total processing time:45.9123511314

##---- Q4 ----##
Ran commands as:

cat wsj_sec0.word_pos | ./create_2gram_hmm.sh q4/2g_hmm
cat wsj_sec0.word_pos | ./create_3gram_hmm.sh q4/3g_hmm_0.1_0.1_0.8 0.1 0.1 0.8 unk_prob_sec22
cat wsj_sec0.word_pos | ./create_3gram_hmm.sh q4/3g_hmm_0.2_0.3_0.5 0.2 0.3 0.5 unk_prob_sec22
./check_hmm.sh q4/2g_hmm > q4/2g_hmm.warning
./check_hmm.sh q4/3g_hmm_0.1_0.1_0.8 > q4/3g_hmm_0.1_0.1_0.8.warning
./check_hmm.sh q4/3g_hmm_0.2_0.3_0.5 > q4/3g_hmm_0.2_0.3_0.5.warning

