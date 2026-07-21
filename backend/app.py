import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from corpora_retrieval import gutendex_api, pmc_api, mediawiki_api
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
    
    # data entry, event management, executive assistance, financial analysis, rf cable design technician, vet tech,  needs better corpora
    specialization_topic_catalyst_map = {'generic': [gutendex_api.RetrieveCorporaFromGutendexAPI, 100, '', ''], 
                                         'accounting': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Accounting'], ''], 
                                         'architecture': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Architecture', 'Architectural_design'], ''], 
                                         'auto mechanics': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Automobile_maintenance', 'Auto_mechanics'], ''], 
                                         'business law': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Business_law'], ''], 
                                         'carpentry': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Carpentry', 'Woodworking', 'Wood-related terminology'], ''], 
                                         'computer science': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Computer_science'], ''], 
                                         'data entry': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Data_management'], ''], 
                                         'ems': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Emergency_medical_services', 'First_aid'], ''], 
                                         'event planning': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Event_management'], ''], 
                                         'executive assistance': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Office_administration'], ''], 
                                         'financial analysis': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Corporate_finance', 'Financial_data_analysis', 'Financial_analysts'], ''], 
                                         'graphic design': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Graphic_design'], ''], 
                                         'marketing': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Marketing', 'Promotional_and_marketing_communications'], ''], 
                                         'medical transcription': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Medical_terminology'], ''], 
                                         'phlebotomy': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Phlebotomy', 'Blood_tests'], ''], 
                                         'psychology': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Psychology'], ''], 
                                         'rf cable design technician': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Radio_spectrum', 'Radio_technology', 'Cables', 'Signal_cables'], ''], 
                                         'social work': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Social_work'], ''], 
                                         'vet tech': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Veterinary_medicine', 'Paraveterinary_workers'], ''], 
                                         'web design': [mediawiki_api.RetrieveCorporaFromMediaWikiAPI, 500, ['Web_design'], '']
                                        #  'medical - experimental autogen text': [pmc_api.RetrieveCorporaFromPMCAPI, 100, 'cryonics', 'Cryogenic preservation']
                                         }

    try:
        specialization = request.json['specialization']

        input_text_length = int(request.json['word_count'])

        corpora_api_class, article_count, input_topic, input_catalyst = specialization_topic_catalyst_map[specialization]

        generated_text_output = main(corpora_api_class , article_count,input_topic, input_catalyst, input_text_length)
    except ValueError:
        return jsonify({'error': 'invalid number format for word_count'}), 400
    except KeyError:
        return jsonify({'error': 'invalid specialization!'}), 400

    return jsonify({'generated_text': generated_text_output})


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false') == 'true')
