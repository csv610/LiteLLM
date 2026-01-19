#!/usr/bin/env python3
"""
Script to collect all medical diagnostic test names from Cleveland Clinic website
by systematically going through each letter (A-Z, #).
"""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def collect_tests_for_letter(driver, letter):
    """
    Navigate to a specific letter and collect all diagnostic test names.
    """
    try:
        # Find and click the letter link
        letter_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, letter))
        )
        letter_link.click()

        # Wait for content to load
        time.sleep(2)

        # Scroll to load all content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # Extract test names using JavaScript
        tests = driver.execute_script("""
            const testLinks = document.querySelectorAll('a[href*="/health/diagnostics/"]');
            const tests = new Set();

            testLinks.forEach(link => {
                const heading = link.querySelector('h2, h3, h4, [class*="heading"]');
                if (heading) {
                    const testName = heading.textContent.trim();
                    if (testName && testName !== 'Diagnostics & Testing') {
                        tests.add(testName);
                    }
                }
            });

            return Array.from(tests).sort();
        """)

        print(f"Letter {letter}: Found {len(tests)} tests")
        return tests

    except Exception as e:
        print(f"Error collecting tests for letter {letter}: {e}")
        return []

def main():
    """Main function to collect all diagnostic tests."""
    # Initialize Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the diagnostics page
        url = "https://my.clevelandclinic.org/health/diagnostics"
        print(f"Navigating to {url}")
        driver.get(url)
        time.sleep(3)

        # Define all letters to search
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '#']

        all_tests = {}
        all_tests_flat = []

        # Collect tests for each letter
        for letter in letters:
            tests = collect_tests_for_letter(driver, letter)
            all_tests[letter] = tests
            all_tests_flat.extend(tests)

        # Remove duplicates and sort
        all_tests_flat = sorted(list(set(all_tests_flat)))

        # Save results
        results = {
            'total_tests': len(all_tests_flat),
            'by_letter': all_tests,
            'all_tests_alphabetical': all_tests_flat
        }

        output_file = 'cleveland_clinic_diagnostic_tests.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n{'='*60}")
        print(f"Collection complete!")
        print(f"Total unique tests found: {len(all_tests_flat)}")
        print(f"Results saved to: {output_file}")
        print(f"{'='*60}")

        # Also save a simple text file with just the test names
        text_output_file = 'cleveland_clinic_diagnostic_tests.txt'
        with open(text_output_file, 'w') as f:
            for test in all_tests_flat:
                f.write(f"{test}\n")

        print(f"Test names also saved to: {text_output_file}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
