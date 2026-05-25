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
corpora_string = 'a string of text with multiple reoccurring words like: string string words like with'




# STEP 2: create word instance map of corpora input
def create_word_instance_map(corpora):

    corpora_list = corpora.split(' ')
    # corpora_list
    corpora_map = defaultdict(lambda: 1)

    for item in corpora_list:
        if item in corpora_map:
            corpora_map[item] += 1
        else:
            corpora_map[item]
    
    return corpora_map


corpora_dict = create_word_instance_map(corpora_string)




# STEP 3: 