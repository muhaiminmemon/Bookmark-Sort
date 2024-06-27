# Load the dataset
import pandas as pd

file_path = 'C:/Users/muhai/Documents/Code/Extension/AI Model/cleaned_combined_dataset.csv'
df = pd.read_csv(file_path)

# Remove entries with missing text data
df = df.dropna(subset=['text'])

# Remove entries with very short or generic text
df = df[df['text'].str.len() > 6]  # Keep entries where text length is greater than 10 characters
df = df[~df['text'].str.contains(r'\bbrowse\b|\ball\b|\binterviewing\b|\blesson\b', case=False, regex=True)]

# Remove duplicate entries
df = df.drop_duplicates(subset=['text'])

# Check the balance of the categories
category_counts = df['label'].value_counts()
print("Category Counts Before Balancing:")
print(category_counts)

# Balance the dataset by ensuring each category has approximately the same number of entries
min_entries_per_category = category_counts.min()

balanced_df = pd.concat([df[df['label'] == category].sample(min_entries_per_category, random_state=42) for category in category_counts.index])

# Shuffle the dataset
balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save the cleaned dataset to a new CSV file
cleaned_output_path = 'C:/Users/muhai/Documents/Code/Extension/AI Model/cleaned_combined_dataset.csv'
balanced_df.to_csv(cleaned_output_path, index=False)

print(f"Cleaned and balanced dataset saved to '{cleaned_output_path}'.")

# Display the cleaned dataset information
balanced_df.info(), balanced_df.head()
