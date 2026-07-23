import argparse
from constants import db, specialization_map
from corpora_retrieval import gutendex_api, pmc_api, mediawiki_api
from src.preprocess import process_api_retrieved_corpora_to_string, clean_up_corpora_string
from src.train import create_markov_chain_map


def create_serialized_model(corpora_api_class, user_input_topic, corpora_count):
    """Creates the corpora markov chain map model and returns it.
    
    Creates the corpora markov chain map model and outputs it so that it can be saved to the couchdb by the save_model function.
    """
    # call corpora processor and pass input topic and article count as arguments
    corpora_set_string = process_api_retrieved_corpora_to_string(corpora_api_class,user_input_topic, corpora_count)

    # cleans up corpora string, adds punctuation tokenization, and adds sentence start tag indicators to help markov chain determine when sentences should begin
    clean_corpora_string = clean_up_corpora_string(corpora_set_string)

    # user input is passed in to corpora chain map creator function
    corpora_markov_chain_map = create_markov_chain_map(clean_corpora_string)

    # serialize it before returning it to be placed in database (have to use a dict comprehension to convert tuple|list keys to strings because couchdb does not support jsonifying tuples|lists)
    serialized_corpora_markov_chain_map = {'||'.join(key): value for key, value in corpora_markov_chain_map.items()}

    return serialized_corpora_markov_chain_map

def save_model_to_db(specialization, corpora_api_class, user_input_topic, corpora_count):
    """
    
    
    """
    
    serialized_markov_chain_model = create_serialized_model(corpora_api_class, user_input_topic, corpora_count)

    if specialization in db:
        model_in_db = db[specialization]
        model_in_db['model'] = serialized_markov_chain_model
        db.save(model_in_db)
    else:
        # save a document (or rather a markov chain model to database)
        db.save({'_id': specialization, 'model': serialized_markov_chain_model})

def load_model_from_db(specialization):
    """
    
    
    """
    
    # load a document (or rather a markov chain model from database)
    serialized_markov_chain_model = db[specialization]

    # deserialize the model before returning it
    markov_chain_model = {tuple(key.split('||')): value for key, value in serialized_markov_chain_model['model'].items()}

    return markov_chain_model


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--field', type=str)
    args = parser.parse_args()

    if args.all:
        for field, values in specialization_map.items():
            corpora_api_class, corpora_count, topic = values[0:3]
            save_model_to_db(field, corpora_api_class, topic, corpora_count)

            print(f'Successfully saved model for {field} to database')

    elif args.field:
        values = specialization_map[args.field]
        corpora_api_class, corpora_count, topic = values[0:3]
        save_model_to_db(args.field, corpora_api_class, topic, corpora_count)

        print(f'Successfully saved model for {args.field} to database')
