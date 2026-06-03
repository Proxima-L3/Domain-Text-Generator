"""Where the main markov chain map creator function lives.

Markov chain function used to actually build the Markov chain "transition" table from the cleaned text produced from preprocess.py.

Functions:
    create_markov_chain_map: Creates the actual markov chain map trained on cleaned up corpora text from preprocess.py.
"""

# import numpy as np
from collections import defaultdict


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









