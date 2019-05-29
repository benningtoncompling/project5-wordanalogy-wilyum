#!/usr/bin/env python3
'''
	William Bowers
	word_analogy.py
    Objective: Solves analogies such as "dog is to cat as puppy is to ___".
    To Run: ./word_analogy.py <vector_file> <input_directory> <output_directory> <eval_file> <should_normalize> <similarity_type>
    5/17/2019
'''
'''
Part 1 - Word Analogy solver
Write a script called word_analogy.py, that solves analogies such as "dog is to cat as
puppy is to ___". The script should run with the following command:
./word_analogy.py <vector_file> <input_directory> <output_directory> <eval_file>
<should_normalize> <similarity_type>

The vector file is a text file with the format:
word v1 v2 v3 v4 ... v300
v1-300 are the entries of the 300 dimensional word embedding vector

Step 1 will be to read in this vector file into a dictionary where the keys are the words
and the values are lists with 300 float entries each.

The input directory will be a path to a directory with several test files. Each test file has
an analogy problem on each line. The format is:
A B C D
A-D are words where A is related to B in the same way that C is related to D.
Some examples include:
Athens Greece Beijing China
amazing amazingly apparent apparently
falling fell knowing knew

Step 2 is to read in these analogy problems, ignoring D. Using only A, B, and C, find
the best candidate for D. This will be the word with the most similar vector to C_vec +
B_vec - A_vec, according to a given similarity metric.

Wether or not the vectors should be normalized before the analogy calculation (C + B -
A) is given by should_normalize:
0 - if <should_normalize> is 0, don't normalize, us the vectors as is
1 - if <should_normalize> is 1, normalize before the C + B - A calculation. This
means if the vector is v1, v2, v3... v300, you should use v1/mag, v2/mag, v3/mag...
v300/mag. Where mag is the magnitude of the vector, square root of (v1^2 + v2^2 +
v3^2 + ... + v300^2).

The similarity metrics are indicated by <similarity_type>:
0 - if similarity_type is 0, use Euclidean distance (the smaller, the more similar)
1 - if similarity_type is 1, use Manhattan distance (the smaller, the more similar)
2 - if similarity_type is 2, use cosine distance (the larger, the more similar)

You should generate one output file in output_directory for every input file in
input_directory. The input_file and output_file should have the same name, but be in
different directories. Each output file should be of the format:
A B C D'
A-C are the same as the input file A-C, D' is the word your code generated to solve the
analogy. This means that each file in the input_directory should have a corresponding
file in the output_directory, with the same number of lines, and the same first three
words on each line. Only the last word of each line may be different.

Step 3 is to run your analogy solver on all the input files, save the solved analogies to
output files, and calculate the accuracy for each file.

In addition to the output files in the output directory, you should write the accuracy for
each file to a separate output file (eval_file). The format of this file should be as shown
in sample_eval.txt
'''
import sys, os, numpy

vector_file = sys.argv[1]
input_directory = sys.argv[2]
#output_directory = sys.argv[3]
#eval_file = sys.argv[4]
#should_normalize = int(sys.argv[5])
#similarity_type = int(sys.argv[6])

#Step 1: read in vector file into a dictionary where the keys are the words and the values are lists with 300 float entries each
vector_dict = {}
with open(vector_file,'r') as vector_file:
    lines = vector_file.read().lower().split('\n')
    lines = [line.split(' ') for line in lines]

for word_vectors in lines:
    key = word_vectors[0]
    value = word_vectors[1:]
    vector_dict[key] = numpy.array(value).astype(float)

#Step 2: NORMALIZE (vector/magnitude)
def normalize():
    normalized_dict = {}
    for key, value in vector_dict.items():
        #finding magnitude = square root of (v1^2 + v2^2 + ... v300^2)
        magnitude = numpy.sqrt(sum(numpy.square(value)))
        normalized_list = []
        for vector in value:
            normalized_vector = vector/magnitude
            normalized_list.append(normalized_vector)
        normalized_dict[key] = normalized_list
    return normalized_dict

#Step 3: Distances/Similarity Types

#Euclidean = square root of (v1-v2)^2 
def euclidean_distance():
    e_dist = numpy.sqrt(sum(numpy.square(vec1-vec2)))
    return e_dist

#Manhattan = sum of |v1-v2|
def manhattan_distance():
    m_dist = sum(abs(vec1-vec2))
    return m_dist

#Cosine Similarity produces a value saying how related are two vectors by looking at the angle instead of magnitude
#Technically, the solution is already normalized so we output only dot-prod when normalization is selected
def cosine_distance():
    if normalized == 1:
        return numpy.dot(vec1, vec2)
    else:
        return numpy.dot(vec1, vec2) / numpy.sqrt(sum(numpy.square(vec1))) * numpy.sqrt(sum(numpy.square(vec2)))


#Read files to run program with
analogy_dict = {}
#looking at files within a directory
for filename in os.listdir(input_directory):
    #for hidden files
    if filename.startswith('.'):
        continue
    if not filename.endswith('.txt'):
        continue
    filepath = os.path.join(input_directory, filename)
    #want full filename path
    with open(filepath, 'r') as open_file: 
        for line in open_file.read().lower().splitlines(): 
            updated_file = line.split(' ')
            #remove 4th item (solution) of analogies
            updated_file.pop(3)
            analogy_dict[filename] = updated_file
            print(updated_file)
            
            break
#print(analogy_dict)

#C_vec + B_vec - A_vec 
output_dict = {}
for filename, updated_file in analogy_dict.items():
    analogies_list = []
    for words in updated_file:
        analogy_calc = vector_dict[words[2]] + vector_dict[words[1]] - vector_dict[words[0]]
        if similarity_type == 0:
            word = euclidean_distance(analogies_list)
        if similarity_type == 1:
            word = manhattan_distance(analogies_list)
        if similarity_type == 2:
            word = cosine_distance(analogies_list)
        words.append(word)
        analogies_list.append(words)
    output_dict[filename] = analogies_list


'''
Resources:
Paulina with normalize function

'''