from flask import Flask, request, jsonify
from flask_cors import CORS
from main import main


app = Flask(__name__)
CORS(app, origins=['http://localhost:5174', 'https://proxima-l3.github.io'])

@app.route('/generate', methods=['POST'])
def index():
    user_input_topic = request.json['topic']
    user_input_catalyst = request.json['catalyst']
    user_input_text_length = int(request.json['textLength'])

    generated_text_output = main(user_input_topic, user_input_catalyst, user_input_text_length)

    return jsonify({'generated_text': generated_text_output})

if __name__ == '__main__':
    app.run(debug=True)
