#!/usr/bin/env python3
"""Clean up myths.json to remove non-myth headings and ensure proper formatting."""

import json
import re

# Phrases that indicate section headings rather than myths
SECTION_HEADINGS = [
    'the take-home',
    'the takehome',
    'take home',
    'what is',
    'where did',
    'why does',
    'how vaccines work',
    'approved',
    'recommendations',
    'getting a',
    'frequently asked questions',
    'ongoing research',
    'an important final word',
    'moving forward',
    'ways to test',
    'other causes',
    'preventions and treatments',
    'genetics and',
    'are some',
    'what should we do'
]


def is_section_heading(myth_text):
    """Check if the text is a section heading rather than a myth."""
    lower_text = myth_text.lower()

    # Check against known section headings
    for heading in SECTION_HEADINGS:
        if heading in lower_text:
            return True

    # Check if it's a question without a statement (likely a section heading)
    if '?' in myth_text and len(myth_text) < 50:
        return True

    # Check if it's too short to be a proper myth
    if len(myth_text) < 15:
        return True

    return False


def clean_myth_text(myth_text):
    """Clean up myth text."""
    # Remove any remaining numbering
    text = re.sub(r'^\d+\.\s*', '', myth_text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    return text.strip()


def main():
    """Main function to clean myths.json."""
    # Load the myths file
    with open('myths.json', 'r') as f:
        data = json.load(f)

    cleaned_myths = []

    for topic_group in data['myths']:
        topic = topic_group['topic']
        myths = topic_group['myths']

        # Filter out section headings and clean the remaining myths
        cleaned_topic_myths = []
        for myth in myths:
            cleaned_text = clean_myth_text(myth)

            if not is_section_heading(cleaned_text):
                cleaned_topic_myths.append(cleaned_text)

        # Only include topics that have at least one valid myth
        if cleaned_topic_myths:
            cleaned_myths.append({
                'topic': topic,
                'myths': cleaned_topic_myths
            })

    # Save cleaned data
    output = {'myths': cleaned_myths}
    with open('myths.json', 'w') as f:
        json.dump(output, f, indent=2)

    original_count = sum(len(group['myths']) for group in data['myths'])
    cleaned_count = sum(len(group['myths']) for group in cleaned_myths)

    print(f"Original myths: {original_count}")
    print(f"Cleaned myths: {cleaned_count}")
    print(f"Removed: {original_count - cleaned_count}")
    print(f"Topics: {len(cleaned_myths)}")


if __name__ == "__main__":
    main()
