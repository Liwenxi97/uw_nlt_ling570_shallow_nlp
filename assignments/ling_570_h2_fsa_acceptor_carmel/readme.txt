Author: Ryan Timbrook 
UW Net ID: timbrr 
Project: Ling 570 HW 2
Date: Oct 11, 2018

##### Description #####
Problems to solve:


######################################################
## Q1 --> Learn the Carmel Package 					##
######################################################
Run the following commands:
a: $ carmel -k 1 fsa7 wfst1
> (0 -> 0 "they" : "PRO" / 1) (1 -> 1 "can" : "AUX" / 0.99) (2 -> 2 "fish" : "NOUN" / 0.7) 0.693

b: $ cat ~/dropbox/18-19/570/hw2/examples/wfst1_test | carmel -k 1 -sli wfst1
> (0 -> 0 "they" : "PRO" / 1) (1 -> 1 "can" : "AUX" / 0.99) (2 -> 2 "fish" : "NOUN" / 0.7) 0.693

Answers
Q1.a: Do they yield the same results? Yes
Q1.b: What do these commands do?
	a. This command returns a list of top n most likely tag sequences. First
			it combines a word-string FSA with the tagging WFST. It yields a WFSA that contains the tag sequences. 
			By applying the -k 1 switch to carmel, it then extracts the highest likely path from the resulting WFSA. 
	b. This command takes as input a file that lists the vocabulary, words, to be converted into an FSA by
			carmel using the switch commands -sli, then it does the same processesing steps as in a.
			-s: means, "take one of the transducers to be given on the standard input"
			-l: means, "to append this standard-input transducer to the left-hand side of the transduction sequence
			-i: means, "the standard-input object is in the string-from rather than FST-form

######################################################
## Q2 --> Manually Create FSAs 						##
######################################################
Manually create FSAs for the following regular expressions:
a: fsa1 for a*b*
b: fsa2 for (a|b)+cd*
c: fsa3 for ((a|b)+cd*|b*d*)
d: fsa4 for (ab*)?ba



######################################################
## Q3 --> Use Carmel To Build An FSA 				##
######################################################
wrote the process in shell:
file: fsa_acceptor.sh

Talk about the -sqlib% switch statements
and the unix 2>/dev/null to toss out some of the return garbage from carmel


######################################################
## Q4 --> Build fsa_acceptor2.sh					##
######################################################
execute as: $ ./fsa_acceptor2.sh q2/<fsa_file> <input_file> >q4/<ex.fsa_file>


######################################################
## Q5 --> Probability Question						##
######################################################
When you flip a coin, the probability of getting the head is 0.8. Now suppose you flip the coin five times, 
what is the probability of getting AT LEAST four heads out of the five flips? 

Not a fair coin... Binomial Distribution problem
n=5; X=4; p=.8 (probability of success); q=.2 (probability of failure)
>>> 5!/((5-4)!*4!) = 120/(1*24) = 5
>>> .8^4 = 0.4096
>>> .2^(5-4) = .2

>>> 5*0.4096*.2 = 0.4096

Answers:
Q5.formula: 5*0.4096*.2 = 0.4096
Q5.probability: 0.4096

######################################################
## Q6 --> Probability Distribution					##
######################################################
There are two random variables X and Y, and the joint probability P(X,Y) is shown below:
	 X=0  X=1
Y=0 0.50 0.25
Y=1 0.10 0.15

a: What is the probability distribution for P(X)?
b: What is the probability distribution for P(Y)?
c: What is the probability distribution for P(Y|X)?
d: Are X and Y independent? Why or why not?

Answers:
Q6.a: P(X=0)=.6; P(X=1)=.4
Q6.b: P(Y=0)=.75; P(Y=1)=.25
Q6.c:
>>> P(Y=0|X=0) = (.75*.6)/.6=.75 
>>> P(Y=1|X=1) = (.25*.4)/.4=.25
>>> P(Y=1|X=0) = (.25*.6)/.6=.25
>>> P(Y=0|X=1) = (.75*.4)/.4=.75
Q6.d: No, they are dependent. P(X,Y) != P(X)P(Y)

######################################################
## Q7 -->  Probability Questions					##
######################################################
There are three coins: c1, c2, and c3. When tossing a coin once, the
probabilities of getting a head for c1, c2, and c3 are 0.1, 0.4, and 0.7, respectively. Now
suppose that you first pick one of the coins, with the probability 0.2 of being c1, 0.5 of
being c2, 0.3 of being c3, and then toss the coin.

a) If you toss this selected coin once, what is the probability of getting ahead?
b) If you toss this selected coin once and get a head, what is the probability that c1 was the coin selected in the first step?

Answers:
Q7.a: (.2*.1)(.5*.4)(.3*.7)/3 = .143
Q7.b: .02

######################################################
