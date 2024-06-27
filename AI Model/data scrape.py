import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import random

# Define the combined categories and the URLs to scrape data from
categories = {
    "Education / E-Learning": [
        "https://stackoverflow.com/questions/tagged/python",
        "https://stackoverflow.com/questions/tagged/javascript",
        "https://www.edutopia.org/",
        "https://www.education.com/articles/",
        "https://www.coursera.org/",
        "https://www.khanacademy.org/"
    ],
    "Lifestyle": [
        "https://www.lifehack.org/articles/lifestyle",
        "https://www.mindbodygreen.com/",
        "https://www.healthline.com/",
        "https://www.self.com/"
    ],
    "Movies & TV Shows": [
        "https://www.imdb.com/news/movie/",
        "https://www.rottentomatoes.com/news/",
        "https://screenrant.com/movie-news/",
        "https://www.cinemablend.com/news/",
        "https://www.hollywoodreporter.com/c/movie-news",
        "https://www.indiewire.com/c/film/",
        "https://www.slashfilm.com/category/movie-news/"
    ],
    "Shopping": [
        "https://www.dealnews.com/",
        "https://www.consumerreports.org/cro/a-to-z-index/shopping.htm",
        "https://www.retailmenot.com/blog/",
        "https://www.slickdeals.net/",
        "https://www.coupons.com/thegoodstuff/"
    ],
    "Career & Job Searching": [
        "https://www.indeed.com/career-advice",
        "https://www.themuse.com/advice",
        "https://www.monster.com/career-advice",
        "https://www.glassdoor.com/blog/",
        "https://www.forbes.com/careers/"
    ]
}

# Function to clean the text
def clean_text(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'\W', ' ', text)  # Remove non-alphanumeric characters
    text = text.lower()  # Convert to lowercase
    return text

# Function to scrape data from a list of URLs
def scrape_data(urls, category):
    data = []
    for url in urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract relevant text based on the structure of the website
            if "stackoverflow" in url:
                questions = soup.find_all('a', class_='question-hyperlink')
                for question in questions:
                    text = question.get_text()
                    data.append({"text": clean_text(text), "label": category})

            elif "edutopia" in url or "education.com" in url:
                articles = soup.find_all('a', href=True, string=True)
                for article in articles:
                    text = article.get_text()
                    data.append({"text": clean_text(text), "label": category})

            elif "coursera" in url or "khanacademy" in url:
                courses = soup.find_all('a', href=True, string=True)
                for course in courses:
                    text = course.get_text()
                    data.append({"text": clean_text(text), "label": category})

            elif "lifehack" in url or "mindbodygreen" in url:
                articles = soup.find_all('a', href=True, string=True)
                for article in articles:
                    text = article.get_text()
                    data.append({"text": clean_text(text), "label": category})

            elif "healthline" in url or "self" in url:
                articles = soup.find_all('a', href=True, string=True)
                for article in articles:
                    text = article.get_text()
                    data.append({"text": clean_text(text), "label": category})

            elif "imdb" in url or "rottentomatoes" in url:
                articles = soup.find_all('a', href=True, string=True)
                for article in articles:
                    text = article.get_text()
                    data.append({"text": clean_text(text), "label": category})

            elif "screenrant" in url or "cinemablend" in url or "hollywoodreporter" in url or "indiewire" in url or "slashfilm" in url:
                articles = soup.find_all('a', href=True, string=True)
                for article in articles:
                    text = article.get_text()
                    data.append({"text": clean_text(text), "label": category})

            elif "dealnews" in url or "slickdeals" in url or "coupons" in url:
                deals = soup.find_all('a', class_='mainTitle')
                for deal in deals:
                    text = deal.get_text()
                    data.append({"text": clean_text(text), "label": category})

            elif "consumerreports" in url:
                articles = soup.find_all('a', href=True, string=True)
                for article in articles:
                    text = article.get_text()
                    data.append({"text": clean_text(text), "label": category})

            elif "indeed" in url or "themuse" in url:
                articles = soup.find_all('a', href=True, string=True)
                for article in articles:
                    text = article.get_text()
                    data.append({"text": clean_text(text), "label": category})

            elif "monster" in url or "glassdoor" in url or "forbes" in url:
                articles = soup.find_all('a', href=True, string=True)
                for article in articles:
                    text = article.get_text()
                    data.append({"text": clean_text(text), "label": category})
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            continue

    return data

# Scrape data for all categories
all_data = []
for category, urls in categories.items():
    category_data = scrape_data(urls, category)
    all_data.extend(category_data)

# Shuffle data and limit to around 2000 entries total
random.shuffle(all_data)
max_entries_per_category = 2000 // len(categories)
balanced_data = []

# Balance the data
category_counts = {category: 0 for category in categories.keys()}
for entry in all_data:
    if category_counts[entry["label"]] < max_entries_per_category:
        balanced_data.append(entry)
        category_counts[entry["label"]] += 1

# Convert to DataFrame and add index
df = pd.DataFrame(balanced_data)
df.reset_index(inplace=True)
df.rename(columns={"index": "ID"}, inplace=True)

# Define the output path
output_path = 'C:/Users/muhai/Documents/Code/Extension/AI Model/cleaned_combined_dataset.csv'

# Save to CSV
df.to_csv(output_path, index=False)

print(f"Data scraping complete. Dataset saved to '{output_path}'.")
