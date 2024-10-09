# Data Cleaning for LLM Training

This repository contains the code and steps for cleaning web-scraped **French** text data for use in training a French language large language model (LLM). The cleaning process ensures that the text is free from unwanted or personal data elements like URLs, contact numbers, email addresses, bad words, names, and non-French content. This is necessary to ensure high-quality training data and avoid introducing biased or inappropriate content into the model.

## Overview

We focus on cleaning a French language dataset to remove offensive or inappropriate content, specifically:

- **Bad words** (profanity, offensive terms)
- **Names** (to avoid personal identification in the dataset)
- **Pornographic content**
- **Hate speech** or **abusive language**

Additionally, we remove other unwanted elements like contact numbers, email addresses, and URLs.

## Data Cleaning Pipeline

The cleaning process is divided into the following steps:

### Step 1: Bad Word Removal

We prepared a **bad-word dictionary** for the French language by:

- **Creating our own** list of bad words in French.
- **Using existing resources** for French profanity and offensive language.

The dictionary covers common French bad words, including terms of abuse, hate speech, and offensive slang.

### Step 2: Removal of Pornographic, Hate, and Abusive Content

Articles containing any of the following types of content are removed:

- **Pornographic content**
- **Hate speech** and **discriminatory language**
- **Abusive or violent language**

Using our bad-word dictionary and regular expressions, we automatically filter out articles with inappropriate content. We also manually review certain cases for accuracy.

### Step 3: Cleaning Process

For general data cleaning, we applied the following steps:

- **Whitespace and Formatting**: Removed extra spaces, tabs, and newlines.
- **Non-French Characters**: Removed non-French script characters, ensuring the text contains only valid French characters (including French accented characters).
- **URL, Email, and Contact Number Removal**: Cleaned URLs, email addresses, and contact numbers from the dataset.
- **HTML Tags**: Stripped out any residual HTML tags from the web-scraped data.
- **Bad Word and Name Filtering**: Removed all articles containing bad words or personal names from the dataset. Names were loaded from a dictionary of common French names.

For detailed code implementation, check the `cleaning_pipeline.py` file.

## Usage

<!-- 
1. **Install Requirements**:
   ```bash
   pip install -r requirements.txt -->
