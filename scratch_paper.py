"""This module holds the initial mvp version of the markov chain program.

Because I don't exactly know how the end product will be organized and this is all new to me, I figured it'd be best if I just get a starter algorithm going along with the more complicated scaffolding of the end product to expedite my progression with the application.
"""

import numpy as np
from collections import defaultdict


# ALGORITHM:

# - retrieve/import (multiple) corpora text for a specific field


# markov chain algo:

# turn corpora into string
# turn string into list split at ' '
# turn list into a dictionary using defaultdict with a conditional as an argument
#   the conditional says defaultdict will assign the new key entry a value of 1 unless it already exists in which case it is assigned a value of dictionaryname[item] += 1








# STEP 1: find resources for corpora of specialized field AND import it to string form

# - import corpora to string form
# corpora_string = 'a string of text with multiple reoccurring words like: string string words like with'




# # STEP 2: create word instance map of corpora input
# def create_word_instance_map(corpora):

#     corpora_list = corpora.split(' ')
#     # corpora_list
#     corpora_map = defaultdict(lambda: 1)

#     for item in corpora_list:
#         if item in corpora_map:
#             corpora_map[item] += 1
#         else:
#             corpora_map[item]
    
#     return corpora_map


# corpora_dict = create_word_instance_map(corpora_string)




# STEP 3: how frequently a word shows up after a specified word.. to do that we need a hash map with keys representing each possible word and values representing a list of the next most likely words to come next............... so a dictionary with each possible word filled with keyless dictionaries as values with each dictionary having keys representing a word that was found to follow the input word (insert: we need an algorithm that takes the current state aka input word ) and values representing how many times that series of pairs occurred.


# we need these data structures:
#   - list1 = a list converted from a string of the corpus text
#   - dict1 = a dictionary with key values representing each word of the above list with values that are dictionaries (dict2)
#       - values that are dictionaries have: 1 key (frequency?) with int value representing how frequently a word appears in corpus text, 1 key (markov_state) with list value of index location numbers where current markov state word appears in list1
#   - a function that creates dict3
#   - dict3 = a dictionary with keys representing each word of corpus list and values that are lists of
#   - 
#   -? dict? = a dictionary with all possible words and how frequently they appear
#   - 
#   - 
#   - ultimately we need a dictionary with keys representing each possible word and their values are dictionaries of keys representing words that follow parent key with values representing number of times that happens
#   - 
#   - 
#   - 
#   - 
#   - 
#   - 
#   - 
#   - so make a dictionary (dict1) of keys of all possible words with empty default dictionary type values
#   - then a function that loops through corpus list (keep track of current index and list value)
#       - grab count corresponding to corpus list index
#       - grab default dict value of dict1's key that corresponds to current corpus list item being iterated through
#       - grab next index value of corpus list using count + 1 and save word value
#       - add word as key to default dict with value = 1
#       - if word as key to default dict already exists += 1 its value
corpora_string = 'a string of text with multiple reoccurring words like: string string words like with'
corpora_list = corpora_string.split(' ')

def create_corpora_map(corpora_list):
    
    corpora_map = defaultdict(lambda: defaultdict(lambda: 1))

    for item in corpora_list:
        corpora_map[item]

    return corpora_map

corpora_dict = create_corpora_map(corpora_list)

def create_markov_chain_map(corpora_list, corpora_map):

    index = 0

    for item in corpora_list:
        if len(corpora_list) - 1 != index:
            next_word = corpora_list[index+1]
            corpora_map[item][next_word] += 1
            index += 1

    return corpora_map

corpora_markov_chain_map = create_markov_chain_map(corpora_list, corpora_dict)


def markov_chain_text_gen(corpora_chain_map, input_starter_word, output_text_length):

    inner_dict = corpora_chain_map[input_starter_word]
    next_word = 'The'
    output_text_list = []
    output_text = ''

    while len(output_text_list) < output_text_length:

        # come up with next word in output text
        word_instances = 0
        for possible_word in inner_dict:
            if inner_dict[possible_word] > word_instances:
                next_word = possible_word
                word_instances = inner_dict[possible_word]
        
        inner_dict = corpora_chain_map[next_word]

        output_text_list.append(str(next_word))
    
    output_text = ' '.join(output_text_list)




# STEP 4: (temp) request user enter a word and a word limit to kickstart the markov chain

user_input_catalyst = input('Enter a word to catalyze text generation: ')
user_input_text_length = int(input('Enter a the number of words you would like in your generated text: '))




# STEP 5: user input is passed in to markov chain algorithm

print(markov_chain_text_gen(corpora_markov_chain_map, user_input_catalyst, user_input_text_length))