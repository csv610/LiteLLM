#!/usr/bin/env python3
"""
Script to scrape all medical terms from Merriam-Webster Medical Dictionary (A-Z)
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from typing import List, Set
import re

BASE_URL = "https://www.merriam-webster.com/browse/medical"
DELAY = 1  # Delay between requests to be respectful


def get_page_terms(letter: str, page_num: int) -> tuple[List[str], int]:
    """
    Get all medical terms from a specific page.
    Returns: (list of terms, total number of pages)
    """
    url = f"{BASE_URL}/{letter}/{page_num}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract terms from the list
        terms = []
        term_links = soup.select('ul.row li a')
        for link in term_links:
            term = link.get_text(strip=True)
            if term:
                terms.append(term)

        # Get total number of pages from the counters span
        total_pages = 1
        counters = soup.select('span.counters')
        if counters:
            # Look for "page X of Y" text
            counter_text = counters[0].get_text()
            match = re.search(r'page\s+\d+\s+of\s+(\d+)', counter_text)
            if match:
                total_pages = int(match.group(1))

        return terms, total_pages

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return [], 0


def scrape_letter(letter: str) -> Set[str]:
    """
    Scrape all medical terms for a given letter.
    """
    print(f"\n{'='*60}")
    print(f"Scraping letter: {letter.upper()}")
    print(f"{'='*60}")

    all_terms = set()

    # Get first page to determine total pages
    terms, total_pages = get_page_terms(letter, 1)
    all_terms.update(terms)
    print(f"Page 1/{total_pages}: Found {len(terms)} terms")

    # Get remaining pages
    for page_num in range(2, total_pages + 1):
        time.sleep(DELAY)  # Be respectful to the server
        terms, _ = get_page_terms(letter, page_num)
        all_terms.update(terms)
        print(f"Page {page_num}/{total_pages}: Found {len(terms)} terms")

    print(f"Total unique terms for '{letter}': {len(all_terms)}")
    return all_terms


def scrape_all_medical_terms() -> List[str]:
    """
    Scrape all medical terms from A-Z and 0-9.
    """
    all_terms = set()

    # Letters a-z
    letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    # Add 0-9
    letters.append('0')

    for letter in letters:
        letter_terms = scrape_letter(letter)
        all_terms.update(letter_terms)
        time.sleep(DELAY)

    # Convert to sorted list
    return sorted(list(all_terms))


def main():
    print("Starting Merriam-Webster Medical Dictionary Scraper")
    print(f"Base URL: {BASE_URL}")
    print(f"Delay between requests: {DELAY} seconds")

    # Scrape all terms
    all_terms = scrape_all_medical_terms()

    # Save to text file (one term per line)
    output_file = "merriam_webster_medical_terms.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for term in all_terms:
            f.write(f"{term}\n")

    print(f"\n{'='*60}")
    print(f"SCRAPING COMPLETE")
    print(f"{'='*60}")
    print(f"Total unique medical terms: {len(all_terms)}")
    print(f"Saved to: {output_file}")

    # Also save as JSON for easier programmatic access
    json_output_file = "merriam_webster_medical_terms.json"
    with open(json_output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'source': 'Merriam-Webster Medical Dictionary',
            'url': BASE_URL,
            'total_terms': len(all_terms),
            'terms': all_terms
        }, f, indent=2, ensure_ascii=False)

    print(f"Also saved as JSON: {json_output_file}")


if __name__ == "__main__":
    main()
