import nltk, json, random
from flask import Flask, request, jsonify, render_template
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def load_data(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word not in stop_words]
    return tokens

def get_response_by_keywords(user_input, intents_data):
    user_tokens = preprocess(user_input)

    best_intent = None
    best_score = 0

    for intent in intents_data['intents']:
        for pattern in intent['patterns']:
            pattern_tokens = preprocess(pattern.lower()) 
            score = len(set(user_tokens) & set(pattern_tokens)) 
            
            if score > best_score:
                best_score = score
                best_intent = intent

    if best_intent:
        return random.choice(best_intent['responses'])
    else:
        return "I'm sorry, I don't have an answer for that."

app = Flask(__name__)
intents_data = load_data("intents.json")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_bot_response():
    user_message = request.json.get("message")
    response = get_response_by_keywords(user_message, intents_data)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
