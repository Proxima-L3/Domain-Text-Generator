"""Where the main markov chain text generator algorithm lives.

Markov chain function used to actually produce the random unique text using the markov chain map created in train.py.

Functions:
    markov_chain_text_gen: Processes the markov chain map to produce random unique text based on markov chain statistical mathematical model.
"""

import random


# STEP 3: create output text using populated corpora_chain_map and some user input

# this function will be moved to generate.py and that module will import the create_markov_chain_map function to create a corpora_chain_map variable for first function parameter. input starter word and output text length will be values using with below input console requests for now

def markov_chain_text_gen(corpora_chain_map, input_starter_word, output_text_length):

    next_word = ''
    output_text_list = []
    output_text = ''

    if input_starter_word in corpora_chain_map:
        inner_dict = corpora_chain_map[input_starter_word]
        output_text_list.append(input_starter_word)
    else:
        inner_dict = corpora_chain_map['The']
        output_text_list.append('The')

    print(f'starter word found: {input_starter_word in corpora_chain_map}')
    print(f"'The' found: {'The' in corpora_chain_map}")
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

