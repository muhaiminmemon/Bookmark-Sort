import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification, BertConfig
from transformers import InputExample, InputFeatures
import joblib
import re
import numpy as np

# Function to preprocess text data
def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'\W', ' ', text)  # Remove non-alphanumeric characters
    text = text.lower()  # Convert to lowercase
    return text

# Load the dataset
file_path = 'C:/Users/muhai/Documents/Code/Extension/AI Model/cleaned_combined_dataset.csv'
try:
    data = pd.read_csv(file_path)
except Exception as e:
    print(f"Error loading dataset: {e}")
    raise

# Preprocess the 'text' column
data['Cleaned_Text'] = data['text'].apply(preprocess_text)

# Encode labels
label_encoder = LabelEncoder()
data['Category'] = label_encoder.fit_transform(data['label'])

# Compute class weights
class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(data['Category']), y=data['Category'])
class_weights_dict = dict(enumerate(class_weights))

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(data['Cleaned_Text'], data['Category'], test_size=0.2, random_state=42)

# Load the BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize the text
train_encodings = tokenizer(X_train.tolist(), truncation=True, padding=True, max_length=128)
test_encodings = tokenizer(X_test.tolist(), truncation=True, padding=True, max_length=128)

# Convert to TensorFlow dataset
train_dataset = tf.data.Dataset.from_tensor_slices((
    dict(train_encodings),
    y_train
)).shuffle(len(X_train)).batch(16)

test_dataset = tf.data.Dataset.from_tensor_slices((
    dict(test_encodings),
    y_test
)).batch(16)

# Load the BERT model
model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(label_encoder.classes_))

# Compile the model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=2e-5),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Train the model with class weights
try:
    model.fit(train_dataset, epochs=5, validation_data=test_dataset, class_weight=class_weights_dict)
except Exception as e:
    print(f"Error during model training: {e}")
    raise

# Save the model
try:
    model.save_pretrained('C:/Users/muhai/Documents/Code/Extension/AI Model/bert_bookmark_categorizer')
    tokenizer.save_pretrained('C:/Users/muhai/Documents/Code/Extension/AI Model/bert_tokenizer')
except Exception as e:
    print(f"Error saving model: {e}")
    raise

# Save the label encoder
try:
    joblib.dump(label_encoder, 'C:/Users/muhai/Documents/Code/Extension/AI Model/label_encoder.pkl')
except Exception as e:
    print(f"Error saving label encoder: {e}")
    raise

print("Model, tokenizer, and label encoder saved successfully.")
