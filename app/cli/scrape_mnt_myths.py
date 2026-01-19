#!/usr/bin/env python3
"""Script to scrape medical myths from Medical News Today articles."""

import json
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# List of article URLs
ARTICLE_URLS = [
    ("Medical myths: All about aging", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-aging/"),
    ("Medical Myths: All about lung cancer", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-lung-cancer/"),
    ("Medical Myths: All about psoriasis", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-psoriasis/"),
    ("Medical Myths: IBS myths and facts", "https://www.medicalnewstoday.com/articles/medical-myths-ibs-myths-and-facts/"),
    ("Medical Myths: Endometriosis facts vs. fiction", "https://www.medicalnewstoday.com/articles/medical-myths-endometriosis-facts-vs-fiction/"),
    ("Medical Myths: All about stroke", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-stroke/"),
    ("Medical Myths: All about COPD", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-copd/"),
    ("Medical Myths: All about IBD", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-ibd/"),
    ("Medical Myths: All about epilepsy", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-epilepsy/"),
    ("Medical Myths: 15 breast cancer misconceptions", "https://www.medicalnewstoday.com/articles/medical-myths-15-breast-cancer-misconceptions/"),
    ("Medical Myths: All about cholesterol", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-cholesterol/"),
    ("Medical Myths: Sexual health", "https://www.medicalnewstoday.com/articles/medical-myths-sexual-health/"),
    ("Medical myths: All about skin", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-skin/"),
    ("Medical Myths: All about hepatitis", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-hepatitis/"),
    ("Medical myths: 11 migraine misunderstandings", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-migraines/"),
    ("Medical Myths: All about blood donation", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-blood-donation/"),
    ("Medical myths: All about allergies", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-allergies/"),
    ("Medical Myths: All about arthritis", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-arthritis/"),
    ("Medical myths: All about cancer", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-cancer/"),
    ("Medical Myths: All about Parkinson's disease", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-parkinsons-disease/"),
    ("Medical Myths: All about tuberculosis", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-tuberculosis/"),
    ("Medical myths: All about multiple sclerosis", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-multiple-sclerosis/"),
    ("Medical myths: All about heart disease", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-heart-disease/"),
    ("Addressing 13 COVID-19 vaccine myths", "https://www.medicalnewstoday.com/articles/healthy/medical-myths-13-covid-19-vaccine-myths/"),
    ("Coronavirus myths explored", "https://www.medicalnewstoday.com/articles/coronavirus-myths-explored/"),
    ("Medical myths: All about sugar", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-sugar/"),
    ("Medical myths: All about weight loss", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-weight-loss/"),
    ("Medical Myths: All about hypertension", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-hypertension/"),
    ("Medical Myths: 5 common myths about obesity", "https://www.medicalnewstoday.com/articles/medical-myths-5-common-myths-about-obesity/"),
    ("Medical myths: All about diabetes", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-diabetes/"),
    ("Medical myths: Vegetarian and vegan diets", "https://www.medicalnewstoday.com/articles/medical-myths-vegetarian-and-vegan-diets/"),
    ("Medical myths: Mental health misconceptions", "https://www.medicalnewstoday.com/articles/medical-myths-mental-health-misconceptions/"),
    ("Medical myths: All about dementia", "https://www.medicalnewstoday.com/articles/medical-myths-all-about-dementia/"),
    ("Medical myths: How much sleep do we need?", "https://www.medicalnewstoday.com/articles/medical-myths-how-much-sleep-do-we-need/"),
    ("Medical myths: The mystery of sleep", "https://www.medicalnewstoday.com/articles/medical-myths-the-mystery-of-sleep/"),
    ("Medical myths: Does sugar make children hyperactive?", "https://www.medicalnewstoday.com/articles/medical-myths-does-sugar-make-children-hyperactive/"),
]


def extract_myths_from_article(driver, url, title):
    """Extract myths from a single article."""
    print(f"Processing: {title}")
    driver.get(url)
    time.sleep(3)  # Wait for page to load

    myths = []

    try:
        # Find all h2 headings that contain myth statements
        # Medical News Today articles typically have numbered headings like "1. Myth statement"
        article = driver.find_element(By.TAG_NAME, "article")
        headings = article.find_elements(By.TAG_NAME, "h2")

        for heading in headings:
            text = heading.text.strip()
            # Remove numbering like "1.", "2.", etc.
            cleaned_text = re.sub(r'^\d+\.\s*', '', text)

            # Skip empty headings and non-myth headings
            if cleaned_text and len(cleaned_text) > 10 and len(cleaned_text) < 200:
                # Skip common section headings
                if cleaned_text.lower() not in ['the takehome', 'medical myths', 'more in medical myths',
                                                  'view all', 'summary', 'introduction', 'conclusion']:
                    myths.append(cleaned_text)

    except Exception as e:
        print(f"Error extracting myths from {title}: {e}")

    return myths


def main():
    """Main function to scrape all articles."""
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)

    all_myths = []

    try:
        for title, url in ARTICLE_URLS:
            myths = extract_myths_from_article(driver, url, title)
            if myths:
                # Extract topic from title
                topic = title.replace("Medical myths:", "").replace("Medical Myths:", "").strip()
                all_myths.append({
                    "topic": topic,
                    "myths": myths
                })
            time.sleep(2)  # Be polite, don't hammer the server

    finally:
        driver.quit()

    # Load existing myths
    try:
        with open('myths.json', 'r') as f:
            existing_data = json.load(f)
            existing_myths = existing_data.get('myths', [])
    except FileNotFoundError:
        existing_myths = []

    # Combine with new myths
    all_combined_myths = existing_myths + all_myths

    # Save to JSON
    output = {"myths": all_combined_myths}
    with open('myths.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nExtracted myths from {len(all_myths)} articles")
    print(f"Total myths topics in file: {len(all_combined_myths)}")


if __name__ == "__main__":
    main()
