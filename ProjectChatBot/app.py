import flask
from flask import Flask, render_template, request, jsonify
import json
import random

def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading data: {e}")
        return None

def get_response_by_keywords(user_input, intents_data):
    if not intents_data or 'intents' not in intents_data:
        return "I'm sorry, my knowledge base is not available."

    user_input = user_input.lower()
    for intent in intents_data['intents']:
        for pattern in intent['patterns']:
            pattern_words = pattern.lower().split()
            if any(word in user_input for word in pattern_words):
                return random.choice(intent['responses'])
    return "I'm sorry, I don't have an answer for that."


app = Flask(__name__)
intents_data = load_data('intents.json')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_message = request.json.get('message')
    response = get_response_by_keywords(user_message, intents_data)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)