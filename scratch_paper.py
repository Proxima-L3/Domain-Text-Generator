"""This module holds the initial mvp version of the markov chain program.

Because I don't exactly know how the end product will be organized and this is all new to me, I figured it'd be best if I just get a starter algorithm going along with the more complicated scaffolding of the end product to expedite my progression with the application.
"""

import numpy as np
from collections import defaultdict


# ALGORITHM:


# STEP 1: find resources for corpora of specialized field AND import it to string form

corpora_string = 'a string of text with multiple reoccurring words like: string string words like with'
corpora_list = corpora_string.split(' ')


# STEP 2: using defaultdict create map that will automatically add instances of each word of corpora list as keys and then populate each keys inner dictionary with instances of each possible word that follows as keys and the number of times it happens as values

def create_markov_chain_map(corpora_list):

    corpora_map = defaultdict(lambda: defaultdict(lambda: 1))
    index = 0

    for item in corpora_list:
        if len(corpora_list) - 1 != index:
            next_word = corpora_list[index+1]
            corpora_map[item][next_word] += 1
            index += 1

    return corpora_map

corpora_markov_chain_map = create_markov_chain_map(corpora_list)


# STEP 3: create output text using populated corpora_chain_map and some user input

def markov_chain_text_gen(corpora_chain_map, input_starter_word, output_text_length):

    inner_dict = corpora_chain_map[input_starter_word]
    next_word = 'The'
    output_text_list = []
    output_text = ''

    while len(output_text_list) < output_text_length:

        # come up with next word in output text by finding the word that follows most frequently
        word_instances = 0
        for possible_word in inner_dict:
            if inner_dict[possible_word] > word_instances:
                next_word = possible_word
                word_instances = inner_dict[possible_word]
        
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

print(markov_chain_text_gen(corpora_markov_chain_map, user_input_catalyst, user_input_text_length))