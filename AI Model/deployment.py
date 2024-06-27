from flask import Flask, request, jsonify
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
import numpy as np
import json
from flask_cors import CORS
import re
import joblib

# Load the model
model_path = 'C:/Users/muhai/Documents/Code/Extension/AI Model/bert_bookmark_categorizer'
tokenizer_path = 'C:/Users/muhai/Documents/Code/Extension/AI Model/bert_tokenizer'
label_encoder_path = 'C:/Users/muhai/Documents/Code/Extension/AI Model/label_encoder.pkl'

try:
    tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
    print("Tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading tokenizer: {e}")

try:
    model = TFBertForSequenceClassification.from_pretrained(model_path)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

# Initialize the Flask app
app = Flask(__name__)
# Enable CORS with specific settings for the /categorize route
cors = CORS(app, resources={r"/categorize": {"origins": "*"}})

# Load the label encoder
try:
    label_encoder = joblib.load(label_encoder_path)
    print("Label encoder loaded successfully.")
except Exception as e:
    print(f"Error loading label encoder: {e}")

# Function to preprocess text data
def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'\W', ' ', text)  # Remove non-alphanumeric characters
    text = text.lower()  # Convert to lowercase
    return text

@app.route('/categorize', methods=['POST'])
def categorize():
    data = request.json
    title = data.get('title', '')

    # Debugging: Print the title being processed
    print(f"Processing title: {title}")
    
    if not title:
        return jsonify({'error': 'No title provided.'}), 400

    try:
        # Preprocess the title
        cleaned_title = preprocess_text(title)
        print(f"Cleaned Title: {cleaned_title}")  # Debug statement

        # Tokenize the title
        inputs = tokenizer(cleaned_title, return_tensors='tf', truncation=True, padding=True, max_length=128)
        print(f"Tokenized Inputs: {inputs}")  # Debug statement

        # Predict the category
        prediction = model(inputs)
        print(f"Prediction: {prediction.logits}")  # Debug statement

        predicted_label = tf.argmax(prediction.logits, axis=1).numpy()[0]
        print(f"Predicted Label: {predicted_label}")  # Debug statement

        category = label_encoder.inverse_transform([predicted_label])[0]
        return jsonify({'category': category})
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
