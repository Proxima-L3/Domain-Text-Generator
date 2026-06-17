"""Where the main markov chain text generator algorithm lives.

Markov chain function used to actually produce the random unique text using the markov chain map created in train.py.

Functions:
    markov_chain_text_gen: Processes the markov chain map to produce random unique text based on markov chain statistical mathematical model.
"""

import random


def markov_chain_text_gen(corpora_chain_map, input_starter_word, output_word_count):
    """Uses the markov chain mathematical/statistical model to return unique output text.
    
    This function takes in a corpora chain map of keys (possible words in corpora) and values (nested dictionaries with keys representing next possible words and their values representing how frequently a key word follows the parent key word), a starter word to catalyze the markov chain process, and a word count integer all as arguments. The function's algorithm starts by assigning some important variables to empty strings and a list. It checks if the catalyst word is in the corpora map and if not the catalyst word starts with 'The'. It then appends the word to the output text string. The while loop checks if a dictionary of possible next words exists for the current word (markov state), then determines which word should come next in output text based on a weighted randomizer, and then that word is appended to the ongoing output_text_list. Finally, after the while loop has generated a list matching the number specified by the output word count argument, it joins the list of words into a string, and that string of all the corpora is returned.
    """

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
    while len(output_text_list) < output_word_count:

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

