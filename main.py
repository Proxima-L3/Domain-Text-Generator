"""Run Domain Specific Text Generator from program entry point.

This module imports the .... class and calls its .run()? method from which
the program begins.
"""

# insert imports
from corpora_retrieval.pmc_api import RetrieveCorporaFromPMCAPI
from src.train import create_markov_chain_map
from src.generate import markov_chain_text_gen


def main() -> None:
    """Create instance of .... and call its run()? method."""

    # temp code that: requests user enter a word and a word limit to kickstart the markov chain
    user_input_topic = input('Enter a word or phrase that the generated text should be about: ')
    user_input_catalyst = input('Enter a word to catalyze text generation: ')
    user_input_text_length = int(input('Enter the number of words you would like in your generated text: '))

    # number of articles to pull for corpora
    article_count = 5

    # corpora with specified word or phrase is collected with instance of pmc_api.py's main retrieval class constructor and its methods (move this to preprocess later)
    corpora_retrieval_object = RetrieveCorporaFromPMCAPI(user_input_topic, article_count)
    corpora_retrieval_object.get_search_query_article_ids_list()
    corpora_retrieval_object.get_corpora_text()

    # parse through resulting corpora_dict attribute and join all dictionary values into single string (change this so it calls a function or class method to do the below action from preprocess module)
    corpora_set_string = ' '.join(corpora_retrieval_object.corpora_dict.values())

    # user input is passed in to corpora chain map creator function
    corpora_markov_chain_map = create_markov_chain_map(corpora_set_string)

    # user input and created corpora markov chain map is passed in to markov chain text generator algorithm
    generated_text_output = markov_chain_text_gen(corpora_chain_map=corpora_markov_chain_map, input_starter_word=user_input_catalyst, output_text_length=user_input_text_length)

    print(generated_text_output)



if __name__ == '__main__':
    main()
