import pandas as pd
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
import joblib
import re

# Function to preprocess text data
def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'\W', ' ', text)  # Remove non-alphanumeric characters
    text = text.lower()  # Convert to lowercase
    return text

# Load the saved model
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

# Load the label encoder
try:
    label_encoder = joblib.load(label_encoder_path)
    print("Label encoder loaded successfully.")
except Exception as e:
    print(f"Error loading label encoder: {e}")

# Function to predict category of a new bookmark title
def predict_category(title):
    try:
        cleaned_title = preprocess_text(title)
        print(f"Cleaned Title: {cleaned_title}")

        inputs = tokenizer(cleaned_title, return_tensors='tf', truncation=True, padding=True, max_length=128)

        prediction = model(inputs)
        predicted_label = tf.argmax(prediction.logits, axis=1).numpy()[0]
        category = label_encoder.inverse_transform([predicted_label])[0]
        
        return category
    except Exception as e:
        print(f"Error predicting category: {e}")
        return None

# List of 100 example bookmark titles
example_titles = [
    "how to download", "best programming languages", "top 10 movies 2024", "healthy lifestyle tips",
    "python tutorial for beginners", "online education platforms", "latest technology trends",
    "best career advice", "shopping deals today", "upcoming tv shows", "how to learn data science",
    "top 10 lifestyle blogs", "best movies of all time", "java programming basics", "online learning resources",
    "healthy eating habits", "best online courses", "latest gadgets review", "job search tips",
    "top shopping websites", "best tv series", "how to code in python", "study tips for students",
    "how to stay fit", "best programming tutorials", "top career websites", "how to save money shopping",
    "movie reviews", "javascript for beginners", "free online courses", "how to meditate",
    "best shopping apps", "career development", "how to build a website", "learning management systems",
    "fitness routines", "how to get a job", "online shopping tips", "top 10 documentaries",
    "advanced python programming", "effective study techniques", "how to stay healthy",
    "best coding practices", "how to write a resume", "best online shopping sites", "top tv dramas",
    "data structures in java", "how to choose an online course", "healthy lifestyle blogs",
    "best educational websites", "latest smartphone reviews", "how to prepare for an interview",
    "how to find the best deals online", "top horror movies", "android app development",
    "how to improve study habits", "best fitness apps", "job interview tips", "best shopping deals",
    "how to learn javascript", "online education trends", "how to live a healthy lifestyle",
    "best coding tutorials", "how to advance your career", "top online shopping platforms",
    "classic movies to watch", "python data analysis", "how to study effectively",
    "how to stay motivated to workout", "best java tutorials", "how to create a professional resume",
    "best tech gadgets", "how to find a job online", "online shopping guide", "top 10 comedy shows",
    "machine learning basics", "how to stay focused while studying", "how to maintain a healthy diet",
    "best programming courses", "how to succeed in your career", "best places to shop online",
    "new movie releases", "web development for beginners", "how to manage time while studying",
    "home workout routines", "java programming advanced", "how to write a cover letter",
    "top shopping deals", "best tv comedies", "data science tutorials", "how to take online classes",
    "nutrition tips", "best online coding bootcamps", "how to get promoted", "best shopping apps",
    "movie streaming sites", "html and css basics", "how to balance work and study",
    "how to start a fitness journey", "latest technology news"
]

# Predict categories for the example bookmark titles
for new_bookmark_title in example_titles:
    predicted_category = predict_category(new_bookmark_title)
    print(f'Title: "{new_bookmark_title}" is predicted to be in category: "{predicted_category}"')
