Author: Ryan Timbrook 
UW Net ID: timbrr 
Project: Ling 570 HW 11
Date: Dec 13, 2018

##---- Q1 ----##
Q1: Write word_analogy.sh that finds D given A, B, and D
Format: command line: word_analogy.sh vector_file input_dir output_dir flag1 flag2

Handling of OOV words from input data needed special handling. If any of the A/B/C words didn't appear in the vector.txt file
we were to use the first word of the vector.txt file, 'the', as the output of our analogy task. And treat this condition as a non-matched word for our accuracy metric output.
OOV words had the following impacts to our accuracy metrics:
***Vocabular Metrics: Observed OOV Instance Cnt:[1840] Observed OOV Unique Cnt:[27] Gold Standards OOV Cnt:[11] (this is the count of Gold Standard words not found in the vector.txt file)

Processing time was initially an issue. When using standard python modules the processing time for cosine_similarity and euclidian_distance took on average 30 minutes to process one input file. (code is still in word_analogy.py for reference)
After experimenting with different python packages such as numpy, pandas, and sklearn.metrics.pairwise, I found that  sklearn.metrics.pairwise cosine_similarity and euclidean_distances modules performed the best.
Average file processing time fell from 30min to ~16sec.
Experment Summary Metrics (highlevel)
-exp00: Total word_analogy.py processing time:221.5794191360 (3.60 min) - Total accuracy: 9.15% (1788/19544)
-exp01: Total word_analogy.py processing time:1320.186083    (22.4 min) - Total accuracy: 9.49% (1854/19544)
-exp10: Total word_analogy.py processing time:221.7926139832 (3.70 min) - Total accuracy: 9.32% (1822/19544)
-exp11: Total word_analogy.py processing time:1315.4681627750 (21.90 min) - Total accuracy: 9.32% (1822/19544)

Processing of files where similarity calculation is cosine_similarity takes 6x longer to process then euclidean_distance (see processing_metrics.xlsx included in hw.tar.gz package for more details)


##---- Q2 ----##
Run the following commands:

mkdir exp00 exp01 exp10 exp11
./word_analogy.sh /dropbox/18-19/570/hw11/examples/vectors.txt /dropbox/18-19/570/hw11/examples/question-data exp00 0 0 >exp00/eval_res
./word_analogy.sh /dropbox/18-19/570/hw11/examples/vectors.txt /dropbox/18-19/570/hw11/examples/question-data exp01 0 1 >exp01/eval_res
./word_analogy.sh /dropbox/18-19/570/hw11/examples/vectors.txt /dropbox/18-19/570/hw11/examples/question-data exp10 1 0 >exp10/eval_res
./word_analogy.sh /dropbox/18-19/570/hw11/examples/vectors.txt /dropbox/18-19/570/hw11/examples/question-data exp11 1 1 >exp11/eval_res


##---- Q3 ----##
Answer the following questions for the Skip-Gram model.
Assume the vocabulary has 100k words, and the word embeddings have 50 dimensions

3a: What is the "fake task" in order to learn word embeddings? That is, for this fake task, what are the input and the output at the test time?

-Given a specific input word, w1, in the middle of a sentence, pick a word at random, what's the probability that w2 is chosen.
-The input is a word and the output is a probability distribution of w2 being chosen.
-As well, an input parameter specifing the window size which constrains "nearby" for w2 would be included.

3b: How many layers are there in the neural network for solving the fake task? How many neurons are there in each layer?

-There are three layers. The Input Layer, Hidden Layer, and Output Layer.
-Input Layer Neurons: 1 neuron representing a single vector with 100,000 components (one for every word in our vocabulary of 100k words)
	-Each input word is represented as a one-hot vector.
-Hidden Layer Neurons: 50 neurons representing the 50 dimensions specified in our assumptions. This will give a weighted matrix of 100,000 rows (one for every word in our vocabulary) and 50 columns (one for every hidden neuron)
-Output Layer Neurons: 100,000 neurons (one per word in our 100k vocabulary)

3c: Not counting the vector for the input word and the output vector for the output layer, how many matrices are there in the network? What are the dimensions of the matricies?
	How many model parameters are there? That is, how many weights need to be estimated during the training?

-Matricies in the network: There is one weighted matrix in the Hidden Layer (if we are considering the output layer, neural network have two weight matrices–a hidden layer and output layer. )
-Dimensions of the matricies: 100,000 x 50 matrix - A weighted matrix of 100,000 rows (one for every word in our vocabulary) and 50 columns (one for every hidden neuron) (i.e., the 50 dimensions specified in our assumptions)
-Model parameters: 100,000 x 50 = 5,000,000 weights in the hidden layer (if we were considering the output vector, then another 5M weights)

3d: Why do we need to create the fake task?

-Create fake task: By building the NN to perform this task, it indirectly outputs word vectors we are after. The network tell's us the probability for 
every word in our vocabulary of being the "nearby word" that we chose. It predicts the likelyhood of a given word in a context we're after.


3e: For any supervised learning algorithm, the training data is a set of (x,y) pairs: x is the input, y is the output.
	For the Skip-Gram model discussed in class, what is x? What is y? (specify whether answer is from lecture material or from blogs)
	Given a set of sentences, how to generate (x,y) pairs?
	
-Skip-Gram model x: current word
-Skip-Gram model y: predicted neighboring word (probability that if you randomly pick a word nearby "ants", that is "car" - day20-word2vec.pdf)
-How to generate (x,y) pairs: For each sentence in the set, starting at the first word in the sentence a tuple, represented as (wi,wi+1) is created. 
The number of tuples created is dependent on the number of words in the sentence and the window size that's specified as "nearby". Usually this is between 5-10 words.
Example if window size is 2: First Word Set:(wi,wi+1),(wi,wi+2) Second Word Set:(wi,wi-1)(wi,wi+1)(wi,wi+2) Third Word Set:(wi,wi-2)(wi,wi-1)(wi,wi+1)(wi,wi+2) etc...
(from lecture material)

3f: What is one-hot representation? Which layer is that used? Why is it called one-hot?

-One-hot representation: It is the input word used when training the network on word pairs. The input is a one-hot vector representing the input word and the training output
is also a one-hot vector representing the output word. Though the output vector will actually be a probability distribution, not a one-hot vector.
The input one-hot vector will have components equal to the vocabulary, in our case 100K, were the input word is a component represented by 1, and all other components are zeros.
-Layer used in: Input Layer, and the Output Layer if you consider the output one-hot vector representation of probability distributions.
-Called one-hot: It's called one-hot based on their being only one of the components having any meaning, where the 1 represents the input word.


3g: Softmax is used in the output layer. Why do we need to use softmax?

-Use softmax: Softmax is used as a regression classifier in the output layer. Each output neuron will produce an output between 0 and 1, and the sum
of all these output values will add up to 1. The goal of softmax functions is to turn numbers into probabilities.
The softmax function takes an N-dimensional vector of arbitrary real values and produces another N-dimensional vector with real values in the range (0,1) that add up to 1.0. 
The outputs of the Softmax layer are guaranteed to sum to one because of the equation for the output values--each output value is divided by the sum of all output values. That is, the output layer is normalized.



