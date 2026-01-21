#!/usr/bin/env python3

import sys
import json
import argparse
from pathlib import Path
from difflib import SequenceMatcher
from typing import List, Dict, Tuple

# Try to import rapidfuzz for better fuzzy matching, fall back to difflib
try:
    from rapidfuzz import fuzz
    HAVE_RAPIDFUZZ = True
except ImportError:
    HAVE_RAPIDFUZZ = False

def load_dictionary(json_file: Path) -> List[Dict]:
    """Load medical dictionary from JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle both list and dict formats
        if isinstance(data, dict):
            # Convert dict to list of entries
            entries = [{"term": term, "definition": defn}
                      for term, defn in data.items()]
            return entries
        elif isinstance(data, list):
            return data
        else:
            print(f"Error: JSON file must contain a list or dictionary, got {type(data)}")
            return []
    except FileNotFoundError:
        print(f"Error: File not found: {json_file}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {json_file}: {e}")
        return []


def calculate_similarity_score(user_term: str, dict_term: str) -> float:
    """Calculate similarity score between two terms."""
    if HAVE_RAPIDFUZZ:
        # Use rapidfuzz for better matching
        return fuzz.token_sort_ratio(user_term.lower(), dict_term.lower()) / 100.0
    else:
        # Fall back to difflib
        return SequenceMatcher(None, user_term.lower(), dict_term.lower()).ratio()


def find_closest_matches(user_term: str, dictionary: List[Dict],
                         num_matches: int = 5) -> List[Tuple[str, str, float]]:
    """
    Find the closest matching terms in the dictionary.

    Returns list of tuples: (term, definition, similarity_score)
    sorted by similarity score (highest first)
    """
    matches = []

    for entry in dictionary:
        term = entry.get("term", "")
        definition = entry.get("definition", "")

        if not term:
            continue

        score = calculate_similarity_score(user_term, term)
        matches.append((term, definition, score))

    # Sort by similarity score (descending)
    matches.sort(key=lambda x: x[2], reverse=True)

    return matches[:num_matches]


def search_term(user_term: str, dictionary: List[Dict]) -> Tuple[bool, Dict | None]:
    """Search for exact term in dictionary (case-insensitive)."""
    user_term_lower = user_term.lower()

    for entry in dictionary:
        term = entry.get("term", "")
        if term.lower() == user_term_lower:
            return True, entry

    return False, None


def search_prefix(prefix: str, dictionary: List[Dict]) -> List[str]:
    """
    Search for all terms matching the prefix (case-insensitive).

    Args:
        prefix: The prefix to match (without the *)
        dictionary: The medical dictionary

    Returns:
        List of matching term names sorted alphabetically
    """
    prefix_lower = prefix.lower()
    matches = []

    for entry in dictionary:
        term = entry.get("term", "")
        if term.lower().startswith(prefix_lower):
            matches.append(term)

    # Sort alphabetically
    matches.sort()
    return matches


def display_definition(entry: Dict) -> None:
    """Display the definition for a term."""
    term = entry.get("term", "")
    definition = entry.get("definition", "")

    print(f"\n✓ Found: {term}")
    print(f"Definition: {definition}\n")

    # Display additional fields if available
    if "concept_type" in entry and entry["concept_type"]:
        print(f"Type: {entry['concept_type']}")

    if "abbreviation" in entry and entry["abbreviation"]:
        print(f"Abbreviation: {entry['abbreviation']}")

    if "synonyms" in entry and entry["synonyms"]:
        print(f"Synonyms: {', '.join(entry['synonyms'])}")

    if "medical_specialty" in entry and entry["medical_specialty"]:
        print(f"Specialties: {', '.join(entry['medical_specialty'])}")


def display_closest_matches(user_term: str, matches: List[Tuple[str, str, float]]) -> None:
    """Display the closest matching terms when exact match not found."""
    print(f"\n✗ No exact match for '{user_term}'")
    print(f"Did you mean one of these?\n")

    for i, (term, definition, score) in enumerate(matches, 1):
        confidence = int(score * 100)
        print(f"{i}. {term} ({confidence}% similarity)")
        print(f"   {definition[:150]}{'...' if len(definition) > 150 else ''}")
        print()


def display_prefix_matches(prefix: str, matches: List[str]) -> None:
    """Display all terms matching the prefix pattern."""
    if not matches:
        print(f"\nNo terms found starting with '{prefix}'")
        return

    print(f"\nFound {len(matches)} term(s) starting with '{prefix}':")
    print("-" * 70)
    for term in matches:
        print(f"  {term}")
    print()


def main(json_file: str, keys_pattern: str | None = None) -> None:
    """
    Main function for exploring medical dictionary.

    Args:
        json_file: Path to the medical dictionary JSON file
        keys_pattern: Optional prefix pattern for non-interactive search (e.g., "A*")
    """
    json_path = Path(json_file)

    # Load dictionary
    print(f"\nLoading medical dictionary from {json_path}...")
    dictionary = load_dictionary(json_path)

    if not dictionary:
        print("Failed to load dictionary.")
        sys.exit(1)

    print(f"Loaded {len(dictionary)} medical terms\n")

    # Handle non-interactive prefix search mode
    if keys_pattern is not None:
        # Strip the trailing * if present
        prefix = keys_pattern.rstrip('*').strip()
        matches = search_prefix(prefix, dictionary)
        display_prefix_matches(prefix, matches)
        return  # Exit after displaying results

    if HAVE_RAPIDFUZZ:
        print("Using RapidFuzz for fuzzy matching\n")
    else:
        print("Using basic fuzzy matching (install 'rapidfuzz' for better results)\n")

    # Interactive loop
    print("Enter medical terms to search (type 'quit' or 'exit' to quit)\n")
    print("-" * 70)

    while True:
        try:
            user_input = input("\nEnter term: ").strip()

            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nExiting...")
                break

            if not user_input:
                print("Please enter a term")
                continue

            # Search for exact match
            found, entry = search_term(user_input, dictionary)

            if found:
                display_definition(entry)
            else:
                # Find and display closest matches
                matches = find_closest_matches(user_input, dictionary, num_matches=5)
                if matches:
                    display_closest_matches(user_input, matches)
                else:
                    print(f"\nNo matches found for '{user_input}'")

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


def cli():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Explore medical dictionary with fuzzy matching for misspelled terms",
        epilog="The script will accept your queries one by one.\n"
               "If a term is spelled correctly, you'll see its definition.\n"
               "If misspelled, you'll see the 5 closest matching terms.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "dictionary",
        help="Path to the medical dictionary JSON file"
    )

    parser.add_argument(
        "-k", "--keys",
        metavar="PATTERN",
        help="List all keys matching the prefix pattern (e.g., 'A*' or 'Ab*'). "
             "Non-interactive mode - displays results and exits."
    )

    args = parser.parse_args()
    main(args.dictionary, keys_pattern=args.keys)


if __name__ == "__main__":
    cli()
