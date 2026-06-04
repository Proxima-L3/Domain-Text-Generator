"""Cleans up raw corpora text.

Uses ..[insert method/library/tools].. to clean up corpora of all bloated/unwanted pieces of text from corpora such as: escape characters like \n, urls, citations, author names, etc. And maybe punctuation and converting non ascii characters and symbols not typically able to be typed on the standard keyboard.

Functions:
    process_api_retrieved_corpora_to_string: Processes (for now) admin/code user defined input topic and article count then creates an instance of the PMC corpora retrieval api class constructor. That object instance then uses its methods for retrieving a list of article ids and then saves the corpora text matched with their ids in corpora_dict of the object instance. Main purpose of function (for now) is to then retrieve only the string values or corpora_dict and join them into a single string which is then returned.
"""

from corpora_retrieval.pmc_api import RetrieveCorporaFromPMCAPI


# the cleaning up of the text functions/classes will come later for now)
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
