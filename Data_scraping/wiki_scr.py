# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# import os
# import time
# from tqdm import tqdm

# # Set the initial URL and output directory
# base_url = 'https://fr.wikipedia.org'
# start_url = 'https://fr.wikipedia.org/wiki/Wikip%C3%A9dia'
# output_dir = 'articles'

# # Create output directory if it does not exist
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# # Metadata dictionary to store file names and article names
# metadata = {}

# # Recursive function to scrape and save articles
# def scrape_article(url, visited_urls, file_counter):
#     try:
#         # Fetch the page content
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Extract and save the article title and content
#         title = soup.find('h1').get_text(strip=True)
#         content = soup.find('div', {'id': 'bodyContent'}).get_text(strip=True)
#         file_name = f"file_{file_counter}.txt"
#         file_path = os.path.join(output_dir, file_name)

#         with open(file_path, 'w', encoding='utf-8') as f:
#             f.write(content)

#         # Update metadata
#         metadata[file_name] = title

#         # Find all links in the article
#         links = soup.find_all('a', href=True)

#         # Iterate over links and recurse
#         for link in tqdm(links):
#             href = link['href']
#             full_url = urljoin(base_url, href)

#             # Check if the link is a Wikipedia article and hasn't been visited yet
#             if href.startswith('/wiki/') and ':' not in href and full_url not in visited_urls:
#                 visited_urls.add(full_url)
#                 file_counter = scrape_article(full_url, visited_urls, file_counter + 1)

#         return file_counter

#     except requests.RequestException as e:
#         print(f"Error fetching {url}: {e}")
#         return file_counter

# # Start the scraping process
# visited_urls = set()
# visited_urls.add(start_url)
# scrape_article(start_url, visited_urls, 1)

# # Save metadata to a file
# metadata_file_path = os.path.join(output_dir, 'metadata.txt')
# with open(metadata_file_path, 'w', encoding='utf-8') as meta_file:
#     for file_name, title in metadata.items():
#         meta_file.write(f"{file_name}: {title}\n")

# print("Scraping complete.")
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import csv
from tqdm import tqdm

def scrape_article(url, visited_urls, file_counter, url_queue, max_urls):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract and save the article title and content
        title = soup.find('h1').get_text(strip=True)
        content = soup.find('div', {'id': 'bodyContent'}).get_text(strip=True)
        file_name = f"file_{file_counter}.txt"
        file_path = os.path.join(output_dir, file_name)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Update metadata CSV file
        with open(metadata_file_path, 'a', newline='', encoding='utf-8') as meta_file:
            csv_writer = csv.writer(meta_file)
            csv_writer.writerow([file_name, title, url])

        # Mark the URL as visited
        visited_urls.add(url)
        file_counter += 1

        # Find all links in the article
        links = soup.find_all('a', href=True)

        # Iterate over links and add new links to the queue
        progress_bar = tqdm(links, desc=f"Scraping links from {title}", dynamic_ncols=True)
        for link in progress_bar:
            href = link['href']
            full_url = urljoin(base_url, href)

            # Check if the link is a Wikipedia article and hasn't been visited yet
            if href.startswith('/wiki/') and ':' not in href and full_url not in visited_urls:
                # Add to queue instead of recursive call
                url_queue.append(full_url)

        return file_counter

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return file_counter


# Set the initial URL and output directory
base_url = 'https://fr.wikipedia.org'
start_url = 'https://fr.wikipedia.org/wiki/Wikip%C3%A9dia'
output_dir = 'wiki_articles'

# Create output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Metadata file path
metadata_file_path = os.path.join(output_dir, 'metadata.csv')

# Load existing metadata if it exists
visited_urls = set()
file_counter = 1

# Load visited URLs from metadata if the file exists
if os.path.exists(metadata_file_path):
    with open(metadata_file_path, 'r', newline='', encoding='utf-8') as meta_file:
        csv_reader = csv.reader(meta_file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            file_name, title, url = row
            visited_urls.add(url)
            file_counter += 1
else:
    # Create metadata CSV file if it doesn't exist
    with open(metadata_file_path, 'w', newline='', encoding='utf-8') as meta_file:
        csv_writer = csv.writer(meta_file)
        # Write header
        csv_writer.writerow(['File Name', 'Article Title', 'URL'])


# Start the scraping process in batches
visited_urls.add(start_url)
url_queue = [start_url]  # Queue for URLs to visit

batch_size = 2000
max_urls = 1000000
while url_queue and file_counter < max_urls:
    current_batch = url_queue[:batch_size]  # Get a batch of 1000 URLs
    url_queue = url_queue[batch_size:]  # Remove the batch from the queue

    for url in current_batch:
        if file_counter >= max_urls:
            break  # Stop if we have reached the maximum URL count
        file_counter = scrape_article(url, visited_urls, file_counter, url_queue, max_urls)

print("Scraping complete.")
