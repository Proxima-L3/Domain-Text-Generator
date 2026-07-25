"""Contains three functions: one for creating markov chain models, one for saving new models to couchdb database, and another for loading previously saved models from the database.

This module is the part of the pipeline responsible for creating, saving, and loading markov chain models from couchdb database. It can also be ran as a cli command tool by entering "python build_models.py --all" while in the backend directory's virtual environment to build all saved specialized fields in the specialization_map in constants.py or if only one new field needs to be saved, "python build_models.py --field "specialization model name"".

Functions:
    create_serialized_model: This function actually creates the markov chain model by accepting an api class, user_input_topic, and corpora_count as parameters and using those to run majority of the pipeline that retrieves the corpora, sets it to a string, processes/cleans it, trains the markov chain model on the corpora, and serializes it before returning the newly made corpora markov chain model.
    save_model_to_db: This function is responsible for updating or saving newly serialized markov chain models to the environment's defined couchdb database url.
    load_model_from_db: This function looks up markov chain models in the database before deserializing them and returning them as an output.
"""


import argparse
from constants import db, specialization_map
# from corpora_retrieval import gutendex_api, pmc_api, mediawiki_api
from src.preprocess import process_api_retrieved_corpora_to_string, clean_up_corpora_string
from src.train import create_markov_chain_map


def create_serialized_model(corpora_api_class, user_input_topic, corpora_count):
    """Creates the corpora markov chain map model and returns it.
    
    Creates the corpora markov chain map model and outputs it so that it can be saved to the couchdb by the save_model function.
    """
    # call corpora processor and pass input topic and article count as arguments
    corpora_set_string = process_api_retrieved_corpora_to_string(corpora_api_class, user_input_topic, corpora_count)

    # cleans up corpora string, adds punctuation tokenization, and adds sentence start tag indicators to help markov chain determine when sentences should begin
    clean_corpora_string = clean_up_corpora_string(corpora_set_string)

    # user input is passed in to corpora chain map creator function
    corpora_markov_chain_map = create_markov_chain_map(clean_corpora_string)

    # serialize it before returning it to be placed in database (have to use a dict comprehension to convert tuple|list keys to strings because couchdb does not support jsonifying tuples|lists)
    serialized_corpora_markov_chain_map = {'||'.join(key): value for key, value in corpora_markov_chain_map.items()}

    return serialized_corpora_markov_chain_map

def save_model_to_db(specialization, corpora_api_class, user_input_topic, corpora_count):
    """Calls the function that creates the markov chain model and saves it to couchdb database.
    
    This function expects parameters: specialization, a corpora api class to pull corpora from, a user input topic which is conditionally used by corpora classes in different ways, and the corpora count which defines how many articles/corpora source text to use to train model. It then runs the create_serialized_model function to create the markov chain model and if the specialization/model name exists in the database, it updates it with the newer version of the trained model. If it doesn't exist yet, it makes a new entry with the specialization name as the _id and the serialized markov chain model as the model key's value.
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
    """Uses the specialization argument to load a serialized model from couchdb, then deserializes it, and returns the model.
    
    This function expects only one parameter: specialization field. This single parameter is used to look up and retrieve the corresponding serialized markov chain model. It then deserializes it (because couchdb doesn't support saving tuples), then returns the deserialized markov chain model.
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

    if db is None:
        print('couchDB is not available. Please make sure couchDB is running.')
        exit(1)
    else:
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
