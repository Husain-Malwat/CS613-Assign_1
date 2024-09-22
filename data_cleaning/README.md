# Data Cleaning for LLM Training

This repository contains the code and steps for cleaning web-scraped Dzongkha text data for use in training a Dzongkha language large language model (LLM). The cleaning process ensures that the text is free from unwanted/personal data elements like URLs, contact numbers, email addresses, bad words, and non-Dzongkha content. The process is necessary to ensure high-quality training data and avoid introducing biased or inappropriate content into the model.

<!-- ## Table of Contents
- [Overview](#overview)
- [Data Cleaning Pipeline](#data-cleaning-pipeline)
  - [Step 1: Bad Word Removal](#step-1-bad-word-removal)
  - [Step 2: Removal of Pornographic, Hate, and Abuse Content](#step-2-removal-of-pornographic-hate-and-abuse-content)
  - [Step 3: Cleaning Process](#step-3-cleaning-process)
- [Usage](#usage)
- [Results and Statistics](#results-and-statistics)
  - [Before and After Cleaning](#before-and-after-cleaning)
- [Requirements](#requirements)
- [References](#references) -->

## Overview
We focus on cleaning a Tibetan language dataset to remove offensive or inappropriate content, specifically:
- **Bad words** (profanity, offensive terms)
- **Pornographic content**
- **Hate speech** or **abusive language**
  
Additionally, we remove other unwanted elements like contact numbers, email addresses, and URLs.

## Data Cleaning Pipeline

The cleaning process is divided into the following steps:

### Step 1: Bad Word Removal [10 pts]
We prepared a **bad-word dictionary** for the Tibetan language by:
- **Creating our own** list of bad words in Tibetan.
- **Using existing resources** for Tibetan profanity and offensive language.

The dictionary covers common Tibetan bad words, including terms of abuse, hate speech, and offensive slang.

### Step 2: Removal of Pornographic, Hate, and Abusive Content [30 pts]
Articles containing any of the following types of content are removed:
- **Pornographic content**
- **Hate speech** and **discriminatory language**
- **Abusive or violent language**

Using our bad-word dictionary and regular expressions, we automatically filter out articles with inappropriate content. We also manually reviewed certain cases for accuracy.

### Step 3: Cleaning Process
For general data cleaning, we applied the following steps:
- **Whitespace and Formatting**: Removed extra spaces, tabs, and newlines.
- **Non-Tibetan Characters**: Removed non-Tibetan script characters, ensuring the text contains only Tibetan script (Unicode range `U+0F00 - U+0FFF`).
- **URL, Email, and Contact Number Removal**: Cleaned URLs, email addresses, and contact numbers from the dataset.
- **HTML Tags**: Stripped out any residual HTML tags from the web-scraped data.
- **Bad Word Filtering**: Removed all articles containing bad words from the dataset.

For detailed code implementation, check the `cleaning_pipeline.py` file.

## Usage

1. **Install Requirements**: 
   ```bash
   pip install -r requirements.txt