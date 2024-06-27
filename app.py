from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification
import joblib
import re
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI app
app = FastAPI()

# Load the model
model_path = 'AI Model/bert_bookmark_categorizer'
tokenizer_path = 'AI Model/bert_tokenizer'
label_encoder_path = 'AI Model/label_encoder.pkl'

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

# Enable CORS with specific settings for the /categorize route
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to preprocess text data
def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'\W', ' ', text)  # Remove non-alphanumeric characters
    text = text.lower()  # Convert to lowercase
    return text

# Define a Pydantic model for the request body
class CategorizeRequest(BaseModel):
    title: str

@app.post('/categorize')
async def categorize(request: CategorizeRequest):
    title = request.title

    # Debugging: Print the title being processed
    print(f"Processing title: {title}")

    if not title:
        raise HTTPException(status_code=400, detail="No title provided.")

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
        return {"category": category}
    except Exception as e:
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
