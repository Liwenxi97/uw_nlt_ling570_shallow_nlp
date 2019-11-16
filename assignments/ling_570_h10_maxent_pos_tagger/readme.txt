Author: Ryan Timbrook 
UW Net ID: timbrr 
Project: Ling 570 HW 10
Date: Dec 6, 2018

##---- Q1 ----##
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

##---- Q2 ----##
*Run below 5 command lines on maxent_tagger to complete table 1:

#Creates feature vectors for train_file and test_file
# Command Format: shell_script train_file test_file rare_thres feat_thres output_dir
CMD 1: $ ./maxent_tagger.sh wsj_sec0.word_pos test.word_pos 1 1 res_1_1
CMD 2: $ ./maxent_tagger.sh wsj_sec0.word_pos test.word_pos 1 3 res_1_3
CMD 3: $ ./maxent_tagger.sh wsj_sec0.word_pos test.word_pos 2 3 res_2_3
CMD 4: $ ./maxent_tagger.sh wsj_sec0.word_pos test.word_pos 3 5 res_3_5
CMD 5: $ ./maxent_tagger.sh wsj_sec0.word_pos test.word_pos 5 10 res_5_10


maxent_tagger.sh performs the following steps:
	1: Executes maxent_tagger.py which creates final_train.vectors.txt and final_test.vectors.txt along with init_feats, kept_feats and train_voc output files 
	2: Executes mallet import-file commands to convert final_train.vectors.txt and final_test.vectors.txt into binary vector files, final_train.vectors and final_test.vectors
	3: Executes vector2classify on final_train.vectors and final_test.vectors outputs are the me_model, me_model.stderr and me_model.stdout files

## Mallet Commands used in maxent_tagger.sh
##convert the training and test vectors from the text format to the binary format.##
	$ mallet import-file --token-regex "[^\s]+" --preserve-case --input final_train.vectors.txt --output final_train.vectors
	$ mallet import-file --token-regex "[^\s]+" --preserve-case --input final_test.vectors.txt --output final_test.vectors --use-pipe-from final_train.vectors

## MaxEnt Classifier Command used in maxent_tagger.sh
##training (with MaxEnt trainer) and for testing##
	$ vectors2classify --training-file final_train.vectors --testing-file final_test.vectors --trainer MaxEnt --output-classifier me_model --report train:accuracy --report test:accuracy >me_model.stdout 2>me_model.stderr
	$ vectors2classify --training-file res_1_1/final_train.vectors --testing-file res_1_1/final_test.vectors --trainer MaxEnt --output-classifier me_model --report train:accuracy train:confusion test:raw test:accuracy test:confusion >me_model.stdout 2>me_model.stderr

#Get sys_out from classifier
**Note: Note Implemented. Classification is completed during the vectors2classify command ####mallet train-classifier --input res_1_1/final_train.vectors --trainer MaxEnt --output-classifier res_1_1/me_model --report train:accuracy train:confusion >res_1_1/me_model.stdout 2>res_1_1/me_model.stderr
$ mallet classify-file --input final_test.vectors.txt --classifier "me_model" --output "sys_out"
 


Table 1: Tagging accuracy with different thresholds
	| Expt Id |	rare thres | feat thres | training accuracy | test accuracy 	| # of feats | # of kept feats | running time(min) |
	| 1_1	  | 1		   | 1			| 0.9575036059503563| 0.8280930992241732|	325157	 |		325157	   |    3.90 (234 sec) | 
	| 1_3	  | 1		   | 3	        | 0.970075994058255 | 0.8366680277664352|	325157	 |		298784	   |	5.98 (349 sec) |
	| 2_3     | 2          | 3          | 0.9586661212891003| 0.8293180890159249|	356312	 |		321519	   |	2.78 (167 sec) |
	| 3_5     | 3          | 5          | 0.9420464575574261| 0.8248264597795019|	373390	 |		319095	   |	3.48 (209 sec) |
	| 5_10    | 5          | 10         | 0.9737572926309445| 0.8558595345038791|	398230	 |      313552     |	4.28 (257 sec) |
	


********************** THE BELOW INFORMATION IS NOT FOR GRADING *************************************************************************************************
***** FOR REFERENCE ONLY! This table represents Tagging accuracy output values prior to including an additional command to mallet that preserves case sensitivity
# mallet import-file --token-regex "[^\s]+" --preserve-case
# From the mallet documentation:
--preserve-case. MALLET by default converts all word features to lowercase.
--token-regex. MALLET divides documents into tokens using a regular expression. As of version 2.0.8, the default token expression is '\p{L}[\p{L}\p{P}]+\p{L}', which is valid for all Unicode letters, 
and supports typical English non-letter patterns such as hyphens, apostrophes, and acronyms. Note that this expression also implicitly drops one- and two-letter words.

Table 1.a: Tagging accuracy with different thresholds
	| Expt Id |	rare thres | feat thres | training accuracy | test accuracy 	| # of feats | # of kept feats | running time(min) |
	| 1_1	  | 1		   | 1			| 0.7476695873070548| 0.5349122090649244|	325157	 |		325157	   |    232 sec        | 
	| 1_3	  | 1		   | 3	        | 0.7115239714968461| 0.5700285830951409|	325157	 |		298784	   |	204 sec		   |
	| 2_3     | 2          | 3          | 0.7513293578179157| 0.5912617394855043|	356312	 |		321519	   |	256 sec	       |
	| 3_5     | 3          | 5          | 0.7643107791005576| 0.6194365046957943|	373390	 |		319095	   |	178 sec	       |
	| 5_10    | 5          | 10         | 0.7781963789800004| 0.6382196815026542|	398230	 |      313552     |	91 sec		   |




***Further Data Investigation
$ vectors2info --input res_1_1/final_train.vectors --print-matrix sic > info_res_1_1/final_train.vectors_info.txt
$ vectors2info --input res_1_1/final_train.vectors --print-labels TRUE > info_res_1_1/final_train.vectors_info.txt
$ classifier2info --classifier res_1_1/me_model > info_res_1_1/me_model_info.txt
$ vectors2classify --training-file res_1_1/final_train.vectors --testing-file res_1_1/final_test.vectors --trainer MaxEnt --output-classifier me_model --report train:accuracy train:confusion test:raw test:accuracy test:confusion >me_model.stdout 2>me_model.stderr


