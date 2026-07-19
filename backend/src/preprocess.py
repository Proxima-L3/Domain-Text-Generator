"""Cleans up raw corpora text.

Uses ..[insert method/library/tools].. to clean up corpora of all bloated/unwanted pieces of text from corpora such as: escape characters like \n, urls, citations, author names, etc. And maybe punctuation and converting non ascii characters and symbols not typically able to be typed on the standard keyboard.

Functions:
    process_api_retrieved_corpora_to_string: Processes (for now) admin/code user defined input topic and article count then creates an instance of the PMC corpora retrieval api class constructor. That object instance then uses its methods for retrieving a list of article ids and then saves the corpora text matched with their ids in corpora_dict of the object instance. Main purpose of function (for now) is to then retrieve only the string values or corpora_dict and join them into a single string which is then returned.
"""

import re
from unidecode import unidecode


# the cleaning up of the text functions/classes will come later for now)
def process_api_retrieved_corpora_to_string(corpora_api_class: object, user_input_topic: str, article_count: int):
    """Processes retrieved corpora from a corpora api class instance's corpora_dict.

    The purpose of this function is to make a corpora api class instance of desired api class constructor type then process the retrieved corpora from the instance's corpora_dict into a single string to later be passed into the create_markov_chain_map function as an argument.
    """

    # corpora with specified word or phrase is collected with instance of pmc_api.py's main retrieval class constructor and its methods
    corpora_retrieval_object = corpora_api_class(user_input_topic, article_count)
    corpora_retrieval_object.get_search_query_article_ids_list()
    corpora_retrieval_object.get_corpora_text()

    # parse through resulting corpora_dict attribute and join all dictionary values into single string
    corpora_set_string = ' '.join(corpora_retrieval_object.corpora_dict.values())

    return corpora_set_string

def add_sentence_start_tags(cleaned_corpora_string: str):
    """Adds <START> tags at beginning of sentences to indicate when a sentence should begin
    
    The purpose of this function is to replace certain end of sentence punctuation marks that also indicate a new sentence will begin with a <START> tag that will just be in the markov chain model itself as its own token but will later be cleaned before the actual generated text is output.
    """

    # put start before each sentence via end of sentence punctuation indicators
    output_text = cleaned_corpora_string.replace(' . ', ' . <START> ').replace(' ? ', ' ? <START> ').replace(' ! ', ' ! <START> ')

    return output_text

def clean_up_corpora_string(dirty_corpora_string: str):
    """Cleans an input corpora string of undesired artifacts left from processing source texts

    The purpose of this function is to use regex statements and parsing libraries to return a string that has been cleaned of all urls, citation markers, author names/references, escape characters, to replace non-ascii characters with characters that can be typed on a standard keyboard, and to remove extra whitespace.
    """

    cleaner_corpora = dirty_corpora_string

    # regex that removes urls
    cleaner_corpora = re.sub(r'http\S+|www\S+https\S', '', cleaner_corpora)
    # regex that removes citation markers
    cleaner_corpora = re.sub(r'\[\d+\]', '', cleaner_corpora)
    # regex that removes author name patters
    cleaner_corpora = re.sub(r'Author:\s*\w+\s+\w+', '', cleaner_corpora)
    # regex that removes escape characters
    cleaner_corpora = re.sub(r'\\[ntr]', '', cleaner_corpora)
    # function that replaces non-ascii char that cant be typed on standard keyboard
    cleaner_corpora = unidecode(cleaner_corpora)
    # regex that converts numbers that arent part of meaningful text ?
    #
    # regex that makes . , ! ? their own tokens/states in the markov chain (by adding space around the end of sentence/clause punctuation marks) ..(special regex check cases for , & . between numbers)
    cleaner_corpora = re.sub(r'([!?])', r' \1 ', cleaner_corpora)
    cleaner_corpora = re.sub(r'(?<!\d)\.(?!\d)', r' . ', cleaner_corpora)
    cleaner_corpora = re.sub(r'(?<!\d)\,(?!\d)', r' , ', cleaner_corpora)
    # function that adds start tokens indicating when a new sentence should begin
    cleaner_corpora = add_sentence_start_tags(cleaner_corpora)
    # regex that removes extra whitespace
    cleaner_corpora = re.sub(r'\s+', ' ', cleaner_corpora)

    cleaned_corpora_string = cleaner_corpora

    return cleaned_corpora_string
