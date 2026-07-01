"""Where the main markov chain text generator algorithm lives.

Markov chain function used to actually produce the random unique text using the markov chain map created in train.py.

Functions:
    markov_chain_text_gen: Processes the markov chain map to produce random unique text based on markov chain statistical mathematical model.
"""

import random


def markov_chain_text_gen(corpora_chain_map, input_starter_words, output_word_count):
    """Uses the markov chain mathematical/statistical model to return unique output text.
    
    This function takes in a corpora chain map of keys (possible words in corpora) and values (nested dictionaries with keys representing next possible words and their values representing how frequently a key word follows the parent key word), a starter word to catalyze the markov chain process, and a word count integer all as arguments. The function's algorithm starts by assigning some important variables to empty strings and a list. It checks if the catalyst word is in the corpora map and if not the catalyst word starts with 'The'. It then appends the word to the output text string. The while loop checks if a dictionary of possible next words exists for the current word (markov state), then determines which word should come next in output text based on a weighted randomizer, and then that word is appended to the ongoing output_text_list. Finally, after the while loop has generated a list matching the number specified by the output word count argument, it joins the list of words into a string, and that string of all the corpora is returned.
    """

    input_starter_tuple = tuple(input_starter_words.split())
    next_word = ''
    output_text_list = []
    output_text = ''
    punc_counter = 0

    if input_starter_tuple in corpora_chain_map:
        inner_dict = corpora_chain_map[input_starter_tuple]
        output_text_list.extend(input_starter_words.split())
    else:
        inner_dict = corpora_chain_map[('<START>', 'The')]
        output_text_list.extend(['<START>', 'The'])

    print(f'starter words found: {input_starter_tuple in corpora_chain_map}')
    print(f"'<START> The' found: {('<START>', 'The') in corpora_chain_map}")
    while len(output_text_list) - punc_counter < output_word_count:

        # if next word inner dictionary is not empty, come up with next word in output text via randomizer weighted by which options follow most frequently
        if inner_dict:
            key_list = list(inner_dict.keys())
            value_list = list(inner_dict.values())
            next_word = str(random.choices(key_list, value_list, k=1)[0])
        else:
            inner_dict =  corpora_chain_map[random.choice(list(corpora_chain_map.keys()))]
            key_list = list(inner_dict.keys())
            value_list = list(inner_dict.values())
            next_word = str(random.choices(key_list, value_list, k=1)[0])
        
        # add word to output text list
        output_text_list.append(str(next_word))

        # focus next code loop to second word in previous tuple and decided upon next word as next loop's tuple markov state
        inner_dict = corpora_chain_map[(output_text_list[-2], next_word)]

        # increment punc_counter if next_word is in punctuation list (do this to ensure punctuation marks dont count towards output_word_count)
        if next_word in ['!', '?', ',', '.', '<START>']:
            punc_counter += 1
    
    output_text = ' '.join(output_text_list)

    # remove start tags that indicate the start of a sentence
    output_text = output_text.replace(' <START> ', ' ').replace('<START> ', '')
    # remove space in front of punctuation marks that indicate end of sentence or clause from output text
    output_text = output_text.replace(' .', '.').replace(' ,', ',').replace(' ?', '?').replace(' !', '!')

    return output_text

