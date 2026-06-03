"""Cleans up raw corpora text.

Uses ..[insert method/library/tools].. to clean up corpora of all bloated/unwanted pieces of text from corpora such as: escape characters like \n, urls, citations, author names, etc. And maybe punctuation and converting non ascii characters and symbols not typically able to be typed on the standard keyboard.
"""

from corpora_retrieval.pmc_api import RetrieveCorporaFromPMCAPI


# the turning of the resulting corpora retrieval object instance's corpora_dict will be here in preprocess (it will make a call to pmc_api to make an object instance then join all the values of corpora_dict attribute into a single string.. the cleaning up of the text functions/classes will come later for now)
def process_api_retrieved_corpora_to_string(user_input_topic: str, article_count: int):
    """Processes retrieved corpora from a corpora api class instance's corpora_dict.

    The purpose of this function is to make a corpora api class instance of desired api class constructor type then process the retrieved corpora from the instance's corpora_dict into a single string to later be passed into the create_markov_chain_map function as an argument.
    """

    # corpora with specified word or phrase is collected with instance of pmc_api.py's main retrieval class constructor and its methods
    corpora_retrieval_object = RetrieveCorporaFromPMCAPI(user_input_topic, article_count)
    corpora_retrieval_object.get_search_query_article_ids_list()
    corpora_retrieval_object.get_corpora_text()

    # parse through resulting corpora_dict attribute and join all dictionary values into single string
    corpora_set_string = ' '.join(corpora_retrieval_object.corpora_dict.values())

    return corpora_set_string
