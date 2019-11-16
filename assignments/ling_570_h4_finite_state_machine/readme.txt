Author: Ryan Timbrook 
UW Net ID: timbrr 
Project: Ling 570 HW 4
Date: Oct 25, 2018


##---- Q1 ----##
Q1: Write expand_fsm1
Logic was implemented using python, file name: expand_fsm1.py python script

This python script builds an expanded FSM given a lexicon 
and morphotactic rules expressed by an FSA

Format: command line: expand_fsm1_old.sh lexicon morph_rules output_fsm
Ran as: 
    $ ./expand_fsm1.sh lexicon_ex morph_rules_ex q4/q4_expand_fsm
The output_fsm file is the expanded FSM (in the Carmel format) where an arc in the morph_rule FSA is replaced by
multiple paths and each path correspond to an entry in the lexicon - (i.e. the input symbol in the expanded FSM
should be a character or an empty string e, not a word)

##---- Q2 ----##
Q2: Write morph_acceptor1.sh, which checks whether the input words are accepted by the FSM created in Q1
This logic was written in a Bash Shell script that acts as a wrapper to the carmel tool
File Name: morph_acceptor1.sh
- Has 3 command line arguments, 1&2 are input files, 3 is output file; 1:fsm, 2:word_lis, 3:output
- Input 1: q4/q4_expand_fsm 
- Input 2: worldlist_ex
- Output 3: q4/q4_result
- Output Format: word => answer(yes or no)


##---- Q3 ----##
Q3: Part1: Write expand_fsm2
Part 1: Logic was implemented using python
File name: expand_fsm2.py python script

This python script builds an expanded FSM given a lexicon 
and morphotactic rules expressed by an FSA

Format: command line: expand_fsm2.sh lexicon morph_rules output_fsm
Ran as: 
    $ ./expand_fsm2.sh lexicon_ex morph_rules_ex q5/q5_expand_fsm

The output_fsm file is the expanded FSM (in the Carmel format) where an arc in the morph_rule FSA is replaced by
multiple paths and each path correspond to an entry in the lexicon - (i.e. the input symbol in the expanded FSM
should be a character or an empty string e, not a word)

Q3: Part 2: Write a morph_acceptor.sh
This logic was written in a Bash Shell script that acts as a wrapper to the carmel tool
File Name: morph_acceptor2.sh
Has 3 command line arguments, 1&2 are input files, 3 is output file; 1:expanded fsm, 2:word_list, 3:output

- Input 1: q5/q5_expand_fsm 
- Input 2: worldlist_ex
- Output 3: q5/q5_result
- Output Format: "word => answer" 
- 		... where "answer" is "morph1/label1 morph2/label2 ..." if the word is accepted by morph acceptor
-		... or "*NONE*" otherwise

This second morph acceptor differs from the first in that the first was used only as an acceptor
and did not generate output. The second is an FST where each transition has both an input and a corresponding output.
Each character's input has the same character as output, but at the ends of each morpheme their is the empty string character "*e*" as input.
; and it's output is written as, "morph1/label1" which is specified as the Output format requirement shown above. If an input word is accepted
this is the returned output that is written out to file.


##---- Q4 ----##
Executed from the command line as: 
./expand_fsm1.sh lexicon_ex morph_rules_ex q4/q4_expand_fsm
./morph_acceptor1.sh q4/q4_expand_fsm wordlist_ex q4/q4_result

##---- Q5 ----##
Executed from the command line as:
./expand_fsm2.sh lexicon_ex morph_rules_ex q5/q5_expand_fsm
./morph_acceptor2.sh q5/q5_expand_fsm wordlist_ex q5/q5_result
