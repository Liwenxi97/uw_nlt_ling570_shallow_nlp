Author: Ryan Timbrook 
UW Net ID: timbrr 
Project: Ling 570 HW 3
Date: Oct 18, 2018

##---- Description ----##
Goal: Become familiar with FST

 
##---- Q1 ----##
Task is to create FSTs for the following regular relations
and save them in Carmel format as files 'fst1', 'fst2', 'fst3'
>>> fst1 for {(a^2n,b^n)|n>=0}
>>> fst2 for {(a^n,b^2nc)|n>=0}
>>> fst3 for {(a^nd*,(bc)^ng)|n>=0}



##---- Q2 ----##
Task is to use Carmel to build an FST acceptor
Build this in fst_acceptor.sh wrapping carmel package in bash shell script commands
Found this carmel switch command to work well for this exercise
echo ${line} | carmel -lsibOE ${fstFile} 2>/dev/null

##---- Q3 ----##
Task is to build an FST acceptor without using Carmel
Format: fst_acceptor2.sh fst_file input_file > output_file
Ran as: 
    $ fst_acceptor2.sh hw3/examples/fst1 hw3/examples/ex2 > q3/ex2.fst1
    $ fst_acceptor2.sh hw3/examples/fst2 hw3/examples/ex2 > q3/ex2.fst2

##---- Q4 ----##
Task is to build an NFA to DFA converter
Format: nfa_to_dfa.sh input_file > output_file
Ran as: 
    $ nfa_to_dfa.sh hw3/examples/nfa1 > q4/ex2.fst1
    $ nfa_to_dfa.sh hw3/examples/nfa2 > q4/ex2.fst2

Unable to complete this task in the given timeframe. extremely stumped on following the documentation
lecture slides.
