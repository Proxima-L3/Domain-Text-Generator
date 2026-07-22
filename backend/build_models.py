import couchdb
from corpora_retrieval import gutendex_api, pmc_api, mediawiki_api
from src.preprocess import process_api_retrieved_corpora_to_string, clean_up_corpora_string
from src.train import create_markov_chain_map


def create_model(corpora_api_class, user_input_topic, corpora_count):
    """Creates the corpora markov chain map model and returns it.
    
    Creates the corpora markov chain map model and outputs it so that it can be saved to the couchdb by the save_model function.
    """
    # call corpora processor and pass input topic and article count as arguments
    corpora_set_string = process_api_retrieved_corpora_to_string(corpora_api_class,user_input_topic, corpora_count)

    # cleans up corpora string, adds punctuation tokenization, and adds sentence start tag indicators to help markov chain determine when sentences should begin
    clean_corpora_string = clean_up_corpora_string(corpora_set_string)

    # user input is passed in to corpora chain map creator function
    corpora_markov_chain_map = create_markov_chain_map(clean_corpora_string)

    return corpora_markov_chain_map

def save_model_to_db(markov_chain_model):
    """
    
    
    """
    
    print('nothing for now')
    # server = couchdb.Server('http://localhost:5984/')
    # db = server['your_database_name']

    # # save a document
    # db.save({'_id': 'carpentry', 'model': serialized_model})

    # # load a document
    # doc = db['carpentry']

