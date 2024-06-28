# AI Bookmark Manager

AI Bookmark Manager is a Chrome extension that automatically categorizes your bookmarks into predefined folders using AI. This project leverages FastAPI for the backend and BERT for categorizing the bookmarks.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Python Libraries Used](#python-libraries-used)
- [Deployment on Azure](#deployment-on-azure)
- [Installation](#installation)
- [Usage](#usage)

## About

The AI Bookmark Manager uses a BERT (Bidirectional Encoder Representations from Transformers) model fine-tuned for the task of bookmark categorization. BERT is a transformer-based model that has been pre-trained on a large set of text data. 

### Fine-tuning the BERT Model

1. **Data Collection**: I collected a dataset of bookmarks categorized into various folders. The dataset included bookmark titles and their respective categories.

3. **Tokenization**: I used the BERT tokenizer to convert the bookmark titles into a format suitable for the BERT model. This involves splitting the text into tokens and converting them into numerical representations.

4. **Model Training**: The pre-trained BERT model was fine-tuned on our dataset using the `TFBertForSequenceClassification` class from the `transformers` library. The model was trained to classify the bookmarks into the predefined categories.

5. **Model Evaluation**: The fine-tuned model was evaluated on a validation set to ensure its accuracy, it has an objective accurary of 87%.

6. **Model Deployment**: The trained model was saved and integrated into a FastAPI backend, which serves as the API for the Chrome extension. When a bookmark is created or changed, the extension sends the bookmark title to the API, which returns the predicted category. The model has been deployed on Azure for public use.

The result is an AI model that can accurately categorize bookmarks based on their titles, making it easier to organize and manage bookmarks in the browser.

### Example

#### Before Sorting
![Before Sorting](path/to/your/image1.png)

#### Using the Extension
![Using the Extension](path/to/your/image2.png)

#### After Sorting
![After Sorting](path/to/your/image3.png)
![After Sorting](path/to/your/image4.png)


## Features

- Automatically categorizes bookmarks into folders:
  - Education / E-Learning
  - Lifestyle
  - Movies & TV Shows
  - Career & Job Searching
- Sort bookmarks manually using the context menu

## Technologies Used

- **Python**: Programming language used for backend development.
- **FastAPI**: Web framework for building APIs with Python.
- **BERT**: Transformer-based model for natural language processing tasks.
- **TensorFlow**: Open-source machine learning framework used to fine-tune the BERT model.
- **Transformers Library (Hugging Face)**: Library providing pre-trained transformer models.
- **Docker**: Containerization platform used to deploy the backend.
- **Chrome Extensions API**: API used to develop the Chrome extension.
- **JavaScript**: Programming language used for the extension's frontend.
- **HTML/CSS**: Markup and styling languages used for the extension's popup interface.

## Python Libraries Used

- **tensorflow**: For training and running the BERT model.
- **transformers**: For using pre-trained BERT models and tokenizers.
- **fastapi**: For creating the API backend.
- **uvicorn**: For running the FastAPI application.
- **pydantic**: For data validation in FastAPI.
- **numpy**: For numerical operations.
- **scikit-learn**: For loading the label encoder.
- **joblib**: For saving and loading the label encoder.
- **pandas**: For data manipulation and cleaning during the training process (if applicable).
  
    ```
### How It Works

Once deployed, the FastAPI server is running on Azure and can be accessed via the provided URL. The Chrome extension sends HTTP requests to this server to categorize bookmarks. When a bookmark is created or changed, the extension sends the bookmark title to the server, which processes the title using the fine-tuned BERT model and returns the predicted category. The extension then moves the bookmark to the corresponding folder based on the category returned by the server.

## Installation

### Chrome Extension Setup

1. Open Chrome and go to `chrome://extensions/`.
2. Enable "Developer mode".
3. Click on "Load unpacked" and select the folder.

## Installation if you want to host locally

### Prerequisites

- Docker
- Git
- Chrome Browser

### Backend Setup

1. Clone the repository:

    ```sh
    git clone https://github.com/muhaiminmemon/Bookmark-Sort.git
    cd Bookmark-Sort
    ```

2. Build and run the Docker container:

    ```sh
    docker build -t bookmarksort .
    docker run -p 8000:8000 bookmarksort
    ```

3. Your FastAPI server should be running at `http://localhost:8000`.

### Chrome Extension Setup

1. Open Chrome and go to `chrome://extensions/`.
2. Enable "Developer mode".
3. Click on "Load unpacked" and select the `Bookmark-Sort` directory.

## Usage

1. Click on the extension icon in the Chrome toolbar to open the popup.
2. Click the "Sort Bookmarks" button to categorize your bookmarks.
3. You will see a message in the popup indicating that bookmarks have been sorted.
