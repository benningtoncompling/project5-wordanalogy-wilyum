#!/usr/bin/env python3
'''
	William Bowers
	word_analogy.py
    Objective: Solves analogies such as "dog is to cat as puppy is to ___".
    To Run: ./word_analogy.py <vector_file> <input_directory> <output_directory> <eval_file> <should_normalize> <similarity_type>
    5/17/2019
'''
import sys, os, numpy, time

#Inputs and Outputs
vector_file = sys.argv[1]
input_directory = sys.argv[2]
output_directory = sys.argv[3]
eval_file = sys.argv[4]
should_normalize = int(sys.argv[5])
similarity_type = int(sys.argv[6])

begin = time.time()

#STEP 1: read file
#Read in vector file into a list 
with open(vector_file,'r') as vector_file:
    lines = vector_file.read().lower().split('\n')
    lines = [line.split(' ') for line in lines]

#use list to create global dictionary where the keys are the words and the values are arrays with 300 float entries each
global_vector_dict = {}
for word_vectors in lines:
    key = word_vectors[0]
    value = word_vectors[1:]
    global_vector_dict[key] = numpy.array(value).astype(float)

#STEP 2:
#Scan through analogy problems
global_text_dict = {}
for filename in os.listdir(input_directory):
    #For hidden and non .txt files
    if filename.startswith('.'):
        continue
    if not filename.endswith('.txt'):
        continue

    #Want full filename path to open
    in_filepath = os.path.join(input_directory, filename)
    #fill global_text_dict
    with open(in_filepath, 'r') as text_file:
        text = []
        for line in text_file.read().lower().split('\n'):
                list = line.split()
                text.append(list)
        global_text_dict[filename] = text

#original ineffective method
    '''
    #Open each file and edit contents
    with open(in_filepath, 'r') as open_filepath: 
        for line in open_filepath.read().split('\n'): 
            #make list with space delim.
            updated_file = line.lower().split(' ')
            key = updated_file.pop(3)
            #add to dictionary
            global_text_dict[key] = updated_file
    '''

#in the case there exists a word in the text for which no vector exists an empty vector will be filled
 #[0]*300 doesnt work to create a list of. These vectors can't be normalized

#STEP 3: Define functions       
#Normalize (vector/magnitude): replaces global dictionary with normalized data
def normalize():
    normalized_dict = {}
    for key, value in global_vector_dict.items():
        #finding magnitude = square root of (v1^2 + v2^2 + ... v300^2)
        magnitude = numpy.sqrt(sum(numpy.square(value)))
        normalize_vector_list = [vector/magnitude for vector in value]
        normalized_dict[key] = numpy.array(normalize_vector_list).astype(float)
    return normalized_dict

if should_normalize == 1:
    global_vector_dict = normalize()

#Calculates distance given similarity type
#input entire list of vectors
def similarity(similarity_type, vec_1, vec_2):
    #euclidean (the smaller, the more similar)
    most_similar_word_list = []
    word_list = []
    
    if similarity_type == 0:
        for key, values in global_vector_dict.items():
            most_similar_word = numpy.sqrt(sum(numpy.square(vec_1 - values)))
            most_similar_word_list.append(most_similar_word)
            word_list.append(key)
        index = most_similar_word_list.index(min(most_similar_word_list))
        selected_word = word_list[index]

    #manhattan (the smaller, the more similar)
    if similarity_type == 1:
        for key, values in global_vector_dict.items():
            most_similar_word = sum(abs(vec_1 - values))
            most_similar_word_list.append(most_similar_word)
            word_list.append(key)
        index = most_similar_word_list.index(min(most_similar_word_list))
        selected_word = word_list[index]

    #cosine (the larger, the more similar)
    if similarity_type == 2:
        if should_normalize == 1:
            for key, values in global_vector_dict.items():
                most_similar_word = numpy.dot(vec_1, values)
                most_similar_word_list.append(most_similar_word)
                word_list.append(key)
            index = most_similar_word_list.index(max(most_similar_word_list))
            selected_word = word_list[index]
        else:
            for key, values in global_vector_dict.items():
                most_similar_word = numpy.dot(vec_1, values) / (numpy.sqrt(sum(numpy.square(vec_1))) * numpy.sqrt(sum(numpy.square(values))))
                most_similar_word_list.append(most_similar_word)
                word_list.append(key)
            index = most_similar_word_list.index(max(most_similar_word_list))
            selected_word = word_list[index]

    #return selected word for a given analogy
    return selected_word

#STEP 4: define solution
#C_vec + B_vec - A_vec = word with most similar vector distance to the actual D_vec, given certain similarity metric
out_filepath = os.path.join(output_directory, filename)
with open(out_filepath, "w") as output:
    with open(eval_file, "w") as eval_output:
        for file, text in global_text_dict.items():
            d_calc_list = []
            my_output_list = {}
            matches_list = {}
            my_output_list.setdefault(file,[])
            matches_list.setdefault(file,[])
            for unfinished_analogy in text:     
                #check if a, b, and c exists in dictionary, then find associated 'd' value
                if unfinished_analogy[0] in global_vector_dict.keys() and unfinished_analogy[1] in global_vector_dict.keys() and  unfinished_analogy[2] in global_vector_dict.keys(): 
                    #creating dictionary of calculated d's usign the original d as what that vector should represent
                    d_calc = global_vector_dict[unfinished_analogy[2]] + global_vector_dict[unfinished_analogy[1]] - global_vector_dict[unfinished_analogy[0]]
                    word = similarity(similarity_type, d_calc, global_vector_dict)
                    #print(str(unfinished_analogy) + ": " + word)
                    my_output_list[file].append([unfinished_analogy[0], unfinished_analogy[1], unfinished_analogy[2], word])
                    if word == unfinished_analogy[3]:
                        #print("matchy match")
                        matches_list[file].append(word)

            '''#put file output here
            for file, line in my_output_list.items():
                print(file)
                print(line)
                for analogy in line:
                    output.write(str(analogy))'''
                
            #accuracy output    
            accuracy = (len(matches_list[file])/len(text))*100
            eval_output.write(file + '\n' + 'ACCURACY TOP: ' + str(accuracy) + '%' + '(' + str(len(matches_list[file])) + '/' + str(len(text)) + ')' + '\n')
        eval_output.close()

'''for filename, file in my_output_list.items():
    filepath = os.path.join(output_directory, filename)
    with open(filepath, "w", encoding='UTF-8') as output:
        for lines in file:
            output.write(lines[0] + " " + lines[1] + " " + lines[2] + " " + lines[3] + "\n")'''

#write to output directory

out_filepath = os.path.join(output_directory, filename)
with open(out_filepath, "w") as output:
    for filename, text in global_text_dict.items():
        for filename2, analogies in my_output_list.items():
            if filename == filename2:
                for analogy in analogies:
                    output.write(analogy[0] + " " + analogy[1] + " " + analogy[2] + " " + analogy[3] + "\n")
        #output.close()

print('time: ', time.time()-begin)



