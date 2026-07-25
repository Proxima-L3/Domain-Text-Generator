"""Contains two post routes/functions that return requested generated output.

This module holds the all necessary imports for: initializing the backend flask environment, the index function which is a route for the svelte front end of Domain Text Generator to request generated text from a saved markov chain model given certain user inputs, and the api_generate function which is a route for the typing practice backend to also request generated text from saved markov chain models in couchdb.

Functions:
    index: The program's route used by the svelte frontend of Domain Text Generator site to accept several params which are used to generate text by calling the main function from main.py.
    api_generate: The program's route used by the typing site backend and frontend to request generated text given a word count desired and a specialization name corresponding to a model saved in the couchdb database. It also calls main function form main.py.
"""


import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from corpora_retrieval import gutendex_api, pmc_api, mediawiki_api
from constants import specialization_map
from main import main


load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
CORS(app, origins=os.environ.get('CORS_ORIGINS').split(','))


@app.route('/generate', methods=['POST'])
def index():
    """Expects 4 user inputs to generate user's desired text output for svelte frontend site.
    
    This index function/route is used by the svelte frontend of the Domain Text Generator site to save the user's choices on corpora api to use, topic/specialization they wish the text output to be about, an input catalyst that defines what words the text should begin with, and the user's desired output text length in words. Those saved https post params are then used when calling the main function to generate the desired text. If no errors occur, the generated text is returned back to the frontend to be displayed in the generated text output box.
    """

    try:
        user_input_corpora = request.json['corpora']
        user_input_topic = request.json['topic']
        user_input_catalyst = request.json['catalyst']
        user_input_text_length = int(request.json['textLength'])

        generated_text_output = main(user_input_corpora, user_input_topic, user_input_catalyst, user_input_text_length)
    except ValueError:
        return jsonify({'error': 'invalid number format for text length!'}), 400
    except KeyError:
        return jsonify({'error': 'invalid topic and/or catalyst!'}), 400

    return jsonify({'generated_text': generated_text_output})


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """Expects two inputs from typing site post request: a specialization name and desired word count to return desired generated text back to typing site frontend.
    
    This api_generate function/route is used by the typing site as an api endpoint to request desired generated text. It first uses the specialization map import to get the predefined input catalyst from a constants dictionary map, then defines what the specialization and desired word count of output text should be using the http's post request params. Then it uses the main function from main.py to load markov chain model defined by specialization name and generate desired output text. If the model is not found it returns an error back to the typing site (which notifies the user then navigates back a page). And if the model is found, then the desired generated text is returned back in a jsonified form.
    """

    specialization_topic_catalyst_map = specialization_map

    try:
        specialization = request.json['specialization']

        input_text_length = int(request.json['word_count'])

        input_catalyst = specialization_topic_catalyst_map[specialization][3]

        generated_text_output = main(specialization, input_catalyst, input_text_length)
        if generated_text_output == 'Text generator model not found in database for this specialization':
            return jsonify({'error': generated_text_output}), 404
    except ValueError:
        return jsonify({'error': 'invalid number format for word_count'}), 400
    except KeyError:
        return jsonify({'error': 'invalid specialization!'}), 400

    return jsonify({'generated_text': generated_text_output})


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false') == 'true')
