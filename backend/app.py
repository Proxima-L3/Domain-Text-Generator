import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from corpora_retrieval import gutendex_api, pmc_api
from main import main


load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
CORS(app, origins=os.environ.get('CORS_ORIGINS').split(','))


@app.route('/generate', methods=['POST'])
def index():
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
    
    specialization_topic_catalyst_map = {'generic': [gutendex_api.RetrieveCorporaFromGutendexAPI, '', ''], 'medical - experimental autogen text': [pmc_api.RetrieveCorporaFromPMCAPI, 'cryonics', 'Cryogenic preservation']}

    try:
        specialization = request.json['specialization']

        input_text_length = int(request.json['word_count'])

        corpora_api_class, input_topic, input_catalyst = specialization_topic_catalyst_map[specialization]

        generated_text_output = main(corpora_api_class ,input_topic, input_catalyst, input_text_length)
    except ValueError:
        return jsonify({'error': 'invalid number format for word_count'}), 400
    except KeyError:
        return jsonify({'error': 'invalid specialization!'}), 400

    return jsonify({'generated_text': generated_text_output})


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false') == 'true')
