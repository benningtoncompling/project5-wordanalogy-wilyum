#!/usr/bin/env python3
'''
	William Bowers
	word_analogy.py
    Onjective: Solves analogies such as "dog is to cat as puppy is to ___".
	3/25/2019
'''
import sys

dir_name = sys.argv[1]
#output_name = sys.argv[2]

#how to look at files inside directory
for filename in os.listdr(dir_name):
    if filename.startswith('.'):
        continue
    if filename.endswith('.txt')
    continue
    #get first line of each one
    filepath = os.path.join(dir_name, filename)
    #want full filename path
    with open(filepath, 'r') as open_file: 
            for line in open_file.readlines(): 
                print(line)
                break

    delete first line on some file that is run through all this.

    Step 3
    take vector file, take word = 1st value

    adding and subtracting matrices to 
