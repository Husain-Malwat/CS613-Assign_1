import re

# Define bad words list (replace with actual Tibetan bad words)
BAD_WORDS = ["badword1", "badword2"]  # Example placeholder

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

# Function to remove non-Tibetan characters (preserving Tibetan script)
def remove_non_tibetan_characters(text):
    return re.sub(r'[^\u0F00-\u0FFF ]+', '', text)  # Tibetan script range is U+0F00 to U+0FFF

# Function to remove English text
def remove_english_text(text):
    return re.sub(r'[A-Za-z]+', '', text)

# Function to remove bad words based on a predefined list
def remove_bad_words(text, bad_words):
    for bad_word in bad_words:
        text = re.sub(bad_word, '', text)
    return text

# Main function to clean the Tibetan text
def clean_tibetan_text(text):
    text = remove_extra_whitespace(text)
    text = remove_urls(text)
    text = remove_emails(text)
    text = remove_contact_numbers(text)
    text = remove_html_tags(text)
    text = remove_non_tibetan_characters(text)
    text = remove_bad_words(text, BAD_WORDS)
    text = remove_extra_whitespace(text)  # Final whitespace cleaning
    return text

# # Sample Tibetan text to clean
# sample_text = """
# བོད་ཡིག་ཚགས་བསྡུའི་ཡིག་རྒྱུན། Contact me at 123-456-7890 or +1234567890, 
# email: someone@example.com. Visit: http://example.com. badword1
# """

# # Clean the sample text using the modular functions
# cleaned_text = clean_tibetan_text(sample_text)
# print(cleaned_text)
