import re
import csv
import os
import logging
from tqdm import tqdm

# Setup logging
logging.basicConfig(filename='cleaning.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to load words from a CSV file
def load_words_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    words = list(text.split(', '))
    return words


# Function to remove extra whitespaces, newlines, and tabs
def remove_extra_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()

# Function to remove URLs
def remove_urls(text):
    return re.sub(r'http\S+|www\S+|https\S+', '', text)

# Function to remove email addresses
def remove_emails(text):
    return re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)

# Function to remove contact numbers
def remove_contact_numbers(text):
    return re.sub(r'\b\d{10,13}\b|\+?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b', '', text)

# Function to remove HTML tags
def remove_html_tags(text):
    return re.sub(r'<.*?>', '', text)

# Function to preserve French characters (removing non-French characters)
def remove_non_french_characters(text):
    # Retain French accented characters, punctuation, and spaces
    return re.sub(r'[^a-zA-ZàâäéèêëîïôöùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ ,.!?\'"-]+', '', text)

# Function to remove bad words based on a predefined list
def remove_bad_words(text, bad_words):
    for bad_word in bad_words:
        text = re.sub(r'\b' + re.escape(bad_word) + r'\b', '', text)
    return text

# Function to remove common names
def remove_names(text, common_names):
    # Remove names from the common names list
    for name in common_names:
        text = re.sub(r'\b' + re.escape(name) + r'\b', '', text)
    
    # Optionally remove capitalized words that are not at the start of a sentence
    text = re.sub(r'(?<!\.\s)(?<!^)[A-Z][a-z]+', '', text)  # Look for capitalized words
    return text


def clean_french_text(text):
    text = remove_extra_whitespace(text)
    text = remove_urls(text)
    text = remove_emails(text)
    text = remove_contact_numbers(text)
    text = remove_html_tags(text)
    text = remove_non_french_characters(text)
    text = remove_bad_words(text, BAD_WORDS)
    text = remove_names(text, COMMON_FRENCH_NAMES)
    text = remove_extra_whitespace(text)
    return text

# Function to preserve directory structure and clean files
def clean_dataset(raw_dir, cleaned_dir):
    for root, dirs, files in tqdm(os.walk(raw_dir)):
        for file in tqdm(files):
            if file.endswith('.txt'):
                
                src_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(src_file_path, raw_dir)
                
                # Create matching directory structure in cleaned_dataset
                cleaned_file_dir = os.path.join(cleaned_dir, os.path.dirname(relative_path))
                os.makedirs(cleaned_file_dir, exist_ok=True)
                
                # Read raw text file
                with open(src_file_path, 'r', encoding='utf-8') as f:
                    raw_text = f.read()
                
                try:
                    # Clean the text
                    cleaned_text = clean_french_text(raw_text)

                    # Save the cleaned file
                    cleaned_file_path = os.path.join(cleaned_file_dir, file)

                    with open(cleaned_file_path, 'w', encoding='utf-8') as cleaned_file:
                        cleaned_file.write(cleaned_text)

                    # Log the successful cleaning of the file
                    # logging.info(f'Cleaned: {src_file_path} -> {cleaned_file_path}')
                except Exception as e:
                    # Log any errors during the cleaning process
                    logging.error(f'Error cleaning {src_file_path}: {e}')

# Usage example
if __name__ == "__main__":

    # Load bad words and names from CSV files
    BAD_WORDS = load_words_from_csv('/home/husainmalwat/french_nlp/CS613-Assign_1/data_cleaning/bad_words.csv')  # Path to your bad words CSV
    COMMON_FRENCH_NAMES = load_words_from_csv('/home/husainmalwat/french_nlp/CS613-Assign_1/data_cleaning/french_common_names.csv')  # Path to your names CSV

    raw_dataset_dir = '/home/husainmalwat/french_nlp/raw_data'
    cleaned_dataset_dir = '/home/husainmalwat/french_nlp/cleaned_data'
    clean_dataset(raw_dataset_dir, cleaned_dataset_dir)
