Author: Ryan Timbrook 
UW Net ID: timbrr 
Project: Ling 570 HW 1
Date: Oct 4, 2018

Description:
Problems to solve:
1: Implemented an English tokenizer
2: Implement a tool that take's the tokenizer's output as input to create a vocabulary from

*** Many different challenges presents it's self when you using just regular expressions for tokenization the
	a combination of expressions, combined with rule based inclusion of the abbreviation's list along with a
	contractions function proved to yield the best results. I could have spent another week tweeking all of the
	different combination of these techniques and still be far from capturing all of the possible use cases.

Execution Consolidated steps:
>>> ./eng_tokenizer.sh
>>> ./make_voc.sh
>>> ./make_ex_voc.sh

########## Step 1:
Execute Details: English Tokenization Program
Source Code Files:
Program Name: hw1_tok.py
    Invoked as: ./eng_tokenizer.sh
    	within sh file: /usr/bin/python hw1_tok.py ex2 abbrev_list ex2_tok
    <source_code_filename> <input_doc_filename> <input_abbrev_list_filename> <output_filename>
    where,
    	<source_code_filename> python source code file
        <input_doc_filename> is the name of the file holding the sentences to tokenize
        <input_abbrev_list_filename> is the name of the file holding the abbreviation list
        <output_filename> is the name of the file to write the results out to

Execution Totals:
---> Sentence Count Total[2713]

########## Step 2:
Execute Details: Vocabulary Tool Program
Source Code Files:
Program Name: hw1_voc.py
    Invoked as: ./make_voc.sh
    	within sh file: /usr/bin/python hw1_voc.py ex2_tok ex2_tok_voc
    <source_code_filename> <input_tok_filename> <output_filename>
    where,
    	<source_code_filename> python source code file
        <input_tok_filename> is the name of the file that was output from step 1 tokenizer execution
        <output_filename> is the name of the file to write the results out to

Execution Totals:
---> Unique Token Count Total[7689] | Total Token Count[39213]


########## Step 3:
Execute Details: Vocabulary Tool Program
Source Code Files:
Program Name: hw1_voc.py
    Invoked as: ./make_ex_voc.sh
    	within sh file: /usr/bin/python hw1_voc.py ex2 ex2_voc
    <source_code_filename> <input_doc_filename> <output_filename>
    where,
    	<source_code_filename> python source code file; **simple tokenization program by white space only
        <input_doc_filename> is the name of the file that was output from step 1 tokenizer execution
        <output_filename> is the name of the file to write the results out to

Execution Totals:
---> Unique Token Count Total[10425] | Total Token Count[29399]


########## Output Counts:
Number of tokens:
	-ex2: 
		Unique Token Count Total[10425]
		Total Token Count[29399]
	-ex2.tok:
		Unique Token Count Total[7689]
		Total Token Count[86115]
	
Number of lines:
	-ex2.voc: 10424
	-ex2.tok.voc: 7689