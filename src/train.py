"""Where the main markov chain map creator function lives.

Markov chain function used to actually build the Markov chain "transition" table from the cleaned text produced from preprocess.py.

Functions:
    create_markov_chain_map: Creates the actual markov chain map trained on cleaned up corpora text from preprocess.py.
"""

import numpy as np
import random
from collections import defaultdict


# ALGORITHM:


# STEP 1: find resources for corpora of specialized field AND import it to string form

# the finding of resources algo is in pmc_api
# the turning of the resulting corpora retrieval object instance's corpora_dict will be put in preprocess (it will make a call to pmc_api to make an object instance then join all the values of corpora_dict attribute into a single string.. the cleaning up of the text functions/classes will come later for now)


# STEP 2: using defaultdict create map that will automatically add instances of each word of corpora list as keys and then populate each keys inner dictionary with instances of each possible word that follows as keys and the number of times it happens as values

# the corpora_text argument will be imported from preprocess

def create_markov_chain_map(corpora_text: str):

    corpora_list = corpora_text.split(' ')

    corpora_map = defaultdict(lambda: defaultdict(lambda: 1))
    index = 0

    for item in corpora_list:
        if len(corpora_list) - 1 != index:
            next_word = corpora_list[index+1]
            corpora_map[item][next_word] += 1
            index += 1

    return corpora_map

# corpora_markov_chain_map = create_markov_chain_map(corpora_list)







# STEP 3: create output text using populated corpora_chain_map and some user input

# this function will be moved to generate.py and that module will import the create_markov_chain_map function to create a corpora_chain_map variable for first function parameter. input starter word and output text length will be values using with below input console requests for now

def markov_chain_text_gen(corpora_chain_map, input_starter_word, output_text_length):

    next_word = ''
    output_text_list = []
    output_text = ''

    if input_starter_word in corpora_chain_map:
        inner_dict = corpora_chain_map[input_starter_word]
    else:
        inner_dict = corpora_chain_map['The']

    while len(output_text_list) < output_text_length:

        # if next word inner dictionary is not empty, come up with next word in output text via randomizer weighted by which options follow most frequently
        if inner_dict:
            key_list = list(inner_dict.keys())
            value_list = list(inner_dict.values())
            next_word = str(random.choices(key_list, value_list, k=1)[0])
        
        # focus next code loop to decided upon next word
        inner_dict = corpora_chain_map[next_word]

        # add word to output text list
        output_text_list.append(str(next_word))
    
    output_text = ' '.join(output_text_list)

    return output_text




# STEP 4: (temp) request user enter a word and a word limit to kickstart the markov chain

user_input_catalyst = input('Enter a word to catalyze text generation: ')
user_input_text_length = int(input('Enter a the number of words you would like in your generated text: '))




# STEP 5: user input is passed in to markov chain algorithm

# print(markov_chain_text_gen(corpora_markov_chain_map, user_input_catalyst, user_input_text_length))