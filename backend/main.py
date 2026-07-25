"""Contains two functions that run Domain Specific Text Generator using loaded couchdb models and the full pipeline for the main_cli_test version of the main function.

This module holds the main function which functions as a critical part of the full pipeline, loading saved markov chain models from couchdb and returning generated text. It also holds a cli test main function that can be run as a script from the cli to test the full pipeline. It imports the relevant modules needed for both functions.

Functions:
    main: The program's critical entry point function which takes in arguments needed to catalyze the text generation process and determine how many words should be output as well as an argument to look up if a markov chain model is in the couchdb database. If it is, it uses src.generate's markov_chain_text_gen function to return the desired generated text. If the model does not exist in the database, it returns a string telling the user "Text generator model not found in database for this specialization".
    main_cli: The program's secondary cli based entry point function which requests user input which is passed into functions pieced together from modules of the project's corpora retrieval package and its src package: preprocess, train, and generate. It then returns a print statement with the desired output in the terminal (for admin/development purposes).
"""

from constants import db
from build_models import load_model_from_db
from corpora_retrieval import gutendex_api, pmc_api, mediawiki_api
from src.preprocess import process_api_retrieved_corpora_to_string, clean_up_corpora_string
from src.train import create_markov_chain_map
from src.generate import markov_chain_text_gen


def main(specialization, user_input_catalyst, user_input_text_length) -> str:
    """Accepts frontend user input to output unique text using a couple modules.
    
    This function is the main function that accepts a specialization, an input catalyst, and desired text length as parameters. It checks if the specialization's markov chain model is in the couchdb database and if so, loads it from db. It then uses the loaded model, the input catalyst, and desired text length when calling the generate text function from generate.py. If the specialization model is in the database the generated output text is returned and if not, a message telling the user that the model for the chosen specialization is not present in the database is returned.
    """

    # conditional that checks if a model is in db yet by _id = specialization
    if specialization in db:
        # load model from database into a local variable
        corpora_markov_chain_map = load_model_from_db(specialization)
        # user input and created corpora markov chain map is passed in to markov chain text generator algorithm
        generated_text_output = markov_chain_text_gen(corpora_markov_chain_map, user_input_catalyst, user_input_text_length)
        return generated_text_output
    else:
        return 'Text generator model not found in database for this specialization'

def main_cli_test() -> None:
    """Requests relevant user input to output unique text using various modules.
    
    This function is a version of the main function but for testing the full pipeline from the cli without having to load or save models to couchdb. It can be run as a script/cli tool and it's main purpose is for admin/dev testing. It requests user input required for all the various modules used in project. It pieces together all the modules that retrieve corpora from an api endpoint using a class constructor, processes that text in a function, what is returned is then passed into another function that creates a markov chain based corpora map, and then that map is passed into the markov chain text generator function itself, which returns unique text of a specified topic and word count.
    """

    # temp code that: requests user enter a word and a word limit to kickstart the markov chain
    corpora_class_map = {
        'gutendex': gutendex_api.RetrieveCorporaFromGutendexAPI,
        'mediawiki': mediawiki_api.RetrieveCorporaFromMediaWikiAPI,
        'pmc': pmc_api.RetrieveCorporaFromPMCAPI
    }
    corpora_api_class = corpora_class_map[input('Enter corpora api class you would like to use to generate text (gutendex, mediawiki, pmc): ')]
    corpora_count = int(input('Enter number of articles/corpora you would like the markov chain text generator to be trained on: '))

    if corpora_api_class == corpora_class_map['mediawiki']:
        user_input_topic = input('Enter a word or multiple words separated by spaces that the generated text should be about: ').split()
    else:
        user_input_topic = input('Enter a word or phrase that the generated text should be about: ')
    user_input_catalyst = input('Enter two words to catalyze text generation: ')
    user_input_text_length = int(input('Enter the number of words you would like in your generated text: '))

    # call corpora processor and pass input topic and article count as arguments
    corpora_set_string = process_api_retrieved_corpora_to_string(corpora_api_class,user_input_topic, corpora_count)

    # cleans up corpora string, adds punctuation tokenization, and adds sentence start tag indicators to help markov chain determine when sentences should begin
    clean_corpora_string = clean_up_corpora_string(corpora_set_string)

    # user input is passed in to corpora chain map creator function
    corpora_markov_chain_map = create_markov_chain_map(clean_corpora_string)

    # user input and created corpora markov chain map is passed in to markov chain text generator algorithm
    generated_text_output = markov_chain_text_gen(corpora_markov_chain_map, user_input_catalyst, user_input_text_length)

    # temp save to a text file line below
    # with open('sample3_gen_text_output.txt', mode='w', encoding='utf-8') as f:
        # f.write(generated_text_output)
        
    # call main function to follow DRY
    return print(generated_text_output)




if __name__ == '__main__':
    main_cli_test()
