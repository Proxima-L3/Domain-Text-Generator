"""Where the main markov chain map creator function lives.

Markov chain function used to actually build the Markov chain "transition" table from the cleaned text produced from preprocess.py.

Functions:
    create_markov_chain_map: Creates the actual markov chain map trained on cleaned up corpora text from preprocess.py.
"""

from collections import defaultdict


def create_markov_chain_map(corpora_text: str):
    """Creates and returns a markov chain map.
    
    Takes in corpora text string as an input which is split at spaces (for now) into a list. That list is then iterated through, adding every possible word as a key to a nested dictionary. The values for the word keys are nested dictionaries. The nested dictionaries hold next possible words as keys along with integer values indicating how frequently that possible word follows the main parent key word.
    """

    corpora_list = corpora_text.split(' ')

    corpora_map = defaultdict(lambda: defaultdict(lambda: 1))
    index = 0

    for item in corpora_list:
        if len(corpora_list) - 2 != index:
            state = (item, corpora_list[index+1])
            next_word = corpora_list[index+2]
            corpora_map[state][next_word] += 1
            index += 1

    return corpora_map

