"""Run Domain Specific Text Generator from program entry point.

This module holds the main function which acts as the program's entry point. It imports the relevant modules needed for the main function.

Functions:
    main: The program's entry point function which (for now) requests user input which are passed into functions pieced together from modules of the project's src package: preprocess, train, and generate. It then (for now) returns a print statement with the desired output in the terminal (for development purposes).
"""

from src.preprocess import process_api_retrieved_corpora_to_string, clean_up_corpora_string
from src.train import create_markov_chain_map
from src.generate import markov_chain_text_gen


def main() -> None:
    """Requests relevant user input output unique text using various modules.
    Create instance of .... and call its run()? method.
    
    For now — the function is the main function that requests user input required for all the various modules used in project. It pieces together all the modules that retrieve corpora from an api endpoint using a class constructor, processes that text in a function, what is returned is then passed into another function that creates a markov chain based corpora map, and then that map is then passed into the markov chain text generator function itself, which returns unique text of a specified topic and word count.
    """

    # temp code that: requests user enter a word and a word limit to kickstart the markov chain
    user_input_topic = input('Enter a word or phrase that the generated text should be about: ')
    user_input_catalyst = input('Enter a word to catalyze text generation: ')
    user_input_text_length = int(input('Enter the number of words you would like in your generated text: '))

    # number of articles to pull for corpora
    article_count = 5

    # call corpora processor and pass input topic and article count as arguments
    corpora_set_string = process_api_retrieved_corpora_to_string(user_input_topic, article_count)

    # cleans up corpora string
    clean_corpora_string = clean_up_corpora_string(corpora_set_string)

    # user input is passed in to corpora chain map creator function
    corpora_markov_chain_map = create_markov_chain_map(clean_corpora_string)

    # user input and created corpora markov chain map is passed in to markov chain text generator algorithm
    generated_text_output = markov_chain_text_gen(corpora_markov_chain_map, user_input_catalyst, user_input_text_length)

    # temp save to a text file line below
    # with open('sample_gen_text_output.txt', mode='w', encoding='utf-8') as f:
        # f.write(generated_text_output)
        
    return print(generated_text_output)




if __name__ == '__main__':
    main()
