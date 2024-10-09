import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm


def get_all_urls(webpage_url):
    try:
        # Send a GET request to the webpage
        response = requests.get(webpage_url)
        response.raise_for_status()

        # Parse the webpage content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all anchor tags and extract href attributes
        urls = set()
        for anchor in soup.find_all('a', href=True):
            full_url = urljoin(webpage_url, anchor['href'])
            urls.add(full_url)

        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return set()

def get_text_file_url(ebook_url):
    try:
        # Extract the ebook number from the URL
        ebook_number = ebook_url.split('/')[-1]

        # Construct the URL for the text file
        text_file_url = f"https://www.gutenberg.org/cache/epub/{ebook_number}/pg{ebook_number}.txt"

        return text_file_url
    except Exception as e:
        print(f"Error: {e}")
        return None

def download_text_file(text_file_url, ebook_number, destination_folder):
    try:
        # Create the destination folder if it does not exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Send a GET request to the text file URL
        response = requests.get(text_file_url)
        response.raise_for_status()

        # Write the content to a text file in the destination folder
        filename = os.path.join(destination_folder, f"file_{ebook_number}.txt")
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)

        # print(f"Text file downloaded and saved as: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Example usage
webpage_url = 'https://www.gutenberg.org/browse/languages/fr'
destination_folder = 'proj_gutenberg'

# Get all URLs from the webpage
all_urls = get_all_urls(webpage_url)

# Filter URLs to only keep those that contain "/ebooks/"
ebook_urls = {url for url in all_urls if '/ebooks/' in url}

# Download text files for each ebook URL
for ebook_url in tqdm(ebook_urls):
    text_file_url = get_text_file_url(ebook_url)
    if text_file_url:
        ebook_number = ebook_url.split('/')[-1]
        download_text_file(text_file_url, ebook_number, destination_folder)
