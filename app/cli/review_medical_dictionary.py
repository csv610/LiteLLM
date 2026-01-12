import sys
import json
import argparse
import logging
import re
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass, asdict
from tqdm import tqdm

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from logging_util import setup_logging

# Configure logging
log_file = Path(__file__).parent / "logs" / "review_medical_dictionary.log"
logger = setup_logging(str(log_file))


@dataclass
class ReviewIssue:
    """Represents a single review issue found in a medical term."""
    issue_type: str
    description: str


@dataclass
class TermReview:
    """Complete review result for a single term."""
    term: str
    definition: str
    is_medically_recognized: bool
    has_abbreviation: bool
    term_in_definition: bool
    is_precise_and_accurate: bool
    issues: List[ReviewIssue]
    overall_status: str  # "pass", "fail"


class MedicalDictionaryReviewer:
    """Validates and reviews medical dictionary entries with 4 key checks.

    Check 1: Term is medically recognized
    Check 2: No abbreviation used in the term
    Check 3: Full form not used in the definition
    Check 4: Definition is verifiable, objective, simple, and professional
    """

    # Common medical abbreviation patterns
    ABBREVIATION_PATTERNS = [
        r'^[A-Z]{2,}$',  # All caps (e.g., EKG, CT, MRI)
        r'^[A-Z][A-Z]+\d+$',  # Caps with numbers (e.g., COVID19)
        r'^[A-Z]{1,3}-\d+$',  # Format like IL-6, TNF-α
    ]

    MIN_DEFINITION_WORDS = 10
    MAX_DEFINITION_WORDS = 100

    def __init__(self):
        """Initialize the reviewer."""
        pass

    def check_1_medical_recognition(self, term: str, definition: str) -> bool:
        """Check 1: Is the term medically recognized?"""
        negative_indicators = [
            "not a medically recognized term",
            "not a recognized medical term",
            "no medical definition",
            "not found in medical",
            "not a valid medical",
            "i cannot find",
            "unable to find",
            "not a real term",
        ]

        definition_lower = definition.lower()
        for indicator in negative_indicators:
            if indicator in definition_lower:
                return False

        # Check if definition is meaningful
        if len(definition.split()) < 3:
            return False

        return True

    def check_2_no_abbreviation(self, term: str) -> bool:
        """Check 2: Term should not be an abbreviation."""
        term = term.strip()

        # Check against known patterns
        for pattern in self.ABBREVIATION_PATTERNS:
            if re.match(pattern, term):
                return False

        return True

    def check_3_term_not_in_definition(self, term: str, definition: str) -> bool:
        """Check 3: Term (full form) should not be used in the definition."""
        term_lower = term.lower()
        definition_lower = definition.lower()

        # Check if the term appears in the definition
        return term_lower not in definition_lower

    def check_4_precise_and_accurate(self, definition: str) -> bool:
        """Check 4: Definition must be verifiable, objective, simple, and professional."""
        words = definition.split()
        word_count = len(words)
        definition_lower = definition.lower()

        # Check word count (10-100 words for precision)
        if word_count < self.MIN_DEFINITION_WORDS or word_count > self.MAX_DEFINITION_WORDS:
            return False

        # Check for proper sentence structure
        if not definition[0].isupper():
            return False
        if not definition.rstrip().endswith(('.', ')', ']')):
            return False

        # Check for OBJECTIVE language (no subjective opinions)
        subjective_indicators = [
            "i think", "i believe", "in my opinion", "it seems", "probably",
            "likely", "arguably", "supposedly", "allegedly", "rumored",
        ]
        for indicator in subjective_indicators:
            if indicator in definition_lower:
                return False

        # Check for SIMPLE language (no conversational or casual language)
        conversational_indicators = [
            "would you like", "let me know", "feel free", "do you have",
            "is there anything", "hope this helps", "in summary", "basically",
            "kind of", "sort of", "a lot of", "tons of", "lots of",
        ]
        for indicator in conversational_indicators:
            if indicator in definition_lower:
                return False

        # Check for PROFESSIONAL language (no informal or colloquial terms)
        unprofessional_indicators = [
            "stuff", "thing", "things", "weird", "crazy", "awesome", "terrible",
            "cool", "neat", "pretty much", "you know", "obviously", "clearly",
            "just", "simply put", "easy", "hard", "difficult", "confusing",
        ]
        for indicator in unprofessional_indicators:
            if f" {indicator} " in f" {definition_lower} ":
                return False

        # Check for VERIFIABLE language (no vague or unverifiable claims)
        vague_indicators = [
            "some people", "many believe", "often thought", "generally considered",
            "commonly believed", "widely thought", "sometimes called", "may or may not",
            "could be", "might have", "perhaps", "possibly", "potentially",
        ]
        for indicator in vague_indicators:
            if indicator in definition_lower:
                return False

        # Check for personal pronouns (should be objective)
        personal_pronouns = [" i ", " you ", " we ", " us ", " our ", " your "]
        for pronoun in personal_pronouns:
            if pronoun in f" {definition_lower} ":
                return False

        # Check for exclamation marks (unprofessional)
        if "!" in definition:
            return False

        # Check for question marks (should be declarative)
        if "?" in definition:
            return False

        return True


    def review_single_entry(self, term: str, definition: str) -> TermReview:
        """Review a single medical term and its definition with 4 key checks."""
        issues: List[ReviewIssue] = []

        # Check 1: Is the term medically recognized?
        is_recognized = self.check_1_medical_recognition(term, definition)
        if not is_recognized:
            issues.append(ReviewIssue(
                issue_type="not_medically_recognized",
                description="Term is not medically recognized"
            ))

        # Check 2: No abbreviation in term?
        no_abbreviation = self.check_2_no_abbreviation(term)
        if not no_abbreviation:
            issues.append(ReviewIssue(
                issue_type="has_abbreviation",
                description="Term is an abbreviation"
            ))

        # Check 3: Term not used in definition?
        term_not_in_def = self.check_3_term_not_in_definition(term, definition)
        if not term_not_in_def:
            issues.append(ReviewIssue(
                issue_type="term_in_definition",
                description="Term appears in its own definition"
            ))

        # Check 4: Is definition verifiable, objective, simple, and professional?
        is_precise = self.check_4_precise_and_accurate(definition)
        if not is_precise:
            issues.append(ReviewIssue(
                issue_type="not_precise",
                description="Definition is not verifiable, objective, simple, and professional"
            ))

        # Determine overall status
        overall_status = "pass" if len(issues) == 0 else "fail"

        return TermReview(
            term=term,
            definition=definition,
            is_medically_recognized=is_recognized,
            has_abbreviation=not no_abbreviation,
            term_in_definition=not term_not_in_def,
            is_precise_and_accurate=is_precise,
            issues=issues,
            overall_status=overall_status
        )

    def review_dictionary(self, definitions: List[Dict]) -> List[TermReview]:
        """Review all entries in a dictionary."""
        results = []
        with tqdm(total=len(definitions), desc="Reviewing entries", unit="entry") as pbar:
            for entry in definitions:
                term = entry.get("term", "").strip()
                definition = entry.get("definition", "").strip()

                if term and definition:
                    review = self.review_single_entry(term, definition)
                    results.append(review)

                pbar.update(1)

        return results

    def load_definitions(self, file_path: Path) -> List[Dict]:
        """Load medical dictionary definitions from JSON file."""
        try:
            file_path = Path(file_path)

            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return []

            with open(file_path, 'r') as f:
                definitions = json.load(f)

                # Handle both list and dict formats
                if isinstance(definitions, dict):
                    # Convert dict to list format
                    definitions = [{"term": k, "definition": v} for k, v in definitions.items()]

                logger.info(f"Loaded {len(definitions)} definitions from {file_path}")
                return definitions

        except json.JSONDecodeError:
            logger.error(f"Invalid JSON file: {file_path}")
            return []
        except Exception as e:
            logger.error(f"Failed to load definitions: {e}")
            return []

    def generate_review_report(self, results: List[TermReview]) -> Dict:
        """Generate summary statistics from review results."""
        total = len(results)
        passed = sum(1 for r in results if r.overall_status == "pass")
        failed = sum(1 for r in results if r.overall_status == "fail")

        issues_by_type = {}
        for result in results:
            for issue in result.issues:
                issue_type = issue.issue_type
                if issue_type not in issues_by_type:
                    issues_by_type[issue_type] = 0
                issues_by_type[issue_type] += 1

        return {
            "total_entries": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": f"{(passed/total*100):.1f}%" if total > 0 else "0%",
            "issues_by_type": issues_by_type,
        }


def save_review_results(results: List[TermReview], output_dir: Path = None):
    """Save review results to JSON file."""
    try:
        if output_dir is None:
            output_dir = Path(__file__).parent / "outputs"

        output_dir.mkdir(exist_ok=True)

        # Convert results to dictionaries
        results_data = []
        with tqdm(total=len(results), desc="Saving results", unit="entry") as pbar:
            for result in results:
                result_dict = {
                    "term": result.term,
                    "definition": result.definition,
                    "is_medically_recognized": result.is_medically_recognized,
                    "has_abbreviation": result.has_abbreviation,
                    "term_in_definition": result.term_in_definition,
                    "is_precise_and_accurate": result.is_precise_and_accurate,
                    "overall_status": result.overall_status,
                    "issues": [asdict(issue) for issue in result.issues],
                }
                results_data.append(result_dict)
                pbar.update(1)

        output_file = output_dir / "review_medical_dict.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Review results saved to {output_file}")
        return output_file
    except Exception as e:
        logger.error(f"Failed to save review results: {e}")
        return None


def print_review_summary(all_results: List[TermReview], failed_results: List[TermReview]):
    """Print a formatted summary of review results."""
    reviewer = MedicalDictionaryReviewer()
    report = reviewer.generate_review_report(all_results)

    print("\n" + "="*60)
    print("MEDICAL DICTIONARY REVIEW REPORT")
    print("="*60)
    print(f"Total Entries Reviewed: {report['total_entries']}")
    print(f"Passed:                 {report['passed']}")
    print(f"Failed:                 {report['failed']}")
    print(f"Pass Rate:              {report['pass_rate']}")

    if report['issues_by_type']:
        print("\nIssues Found by Type:")
        for issue_type, count in report['issues_by_type'].items():
            print(f"  - {issue_type}: {count}")

    print("="*60 + "\n")


def print_failed_entries(results: List[TermReview], limit: int = None):
    """Print entries that failed review."""
    failed = results  # Already filtered in cli()

    if not failed:
        print("No failed entries.\n")
        return

    display_count = limit if limit is not None else len(failed)
    print(f"\nFAILED ENTRIES (showing {min(display_count, len(failed))} of {len(failed)}):")
    print("-" * 60)

    for result in failed[:display_count]:
        print(f"\nTerm: {result.term}")
        print(f"Definition: {result.definition[:100]}...")
        print("Issues:")
        for issue in result.issues:
            print(f"  - {issue.description}")
        print("-" * 60)


def cli(json_file: str, model: str = None):
    """Main CLI function to review medical dictionary.

    Args:
        json_file: Path to JSON file containing medical dictionary
        model: Deprecated, no longer used
    """
    try:
        reviewer = MedicalDictionaryReviewer()

        # Load definitions from provided JSON file
        definitions = reviewer.load_definitions(json_file)
        if not definitions:
            print(f"No definitions found in: {json_file}")
            return

        print(f"\nReviewing {len(definitions)} medical dictionary entries...")

        # Review all entries
        all_results = reviewer.review_dictionary(definitions)

        # Filter to only failed entries
        failed_results = [r for r in all_results if r.overall_status == "fail"]

        # Save results (save only failed entries)
        output_file = save_review_results(failed_results)
        if output_file:
            print(f"Review results saved to: {output_file}\n")

        # Print summary
        print_review_summary(all_results, failed_results)

        # Print failed entries
        if failed_results:
            print_failed_entries(failed_results)
        else:
            print("All entries passed the review!\n")

        logger.info(f"Review completed for {len(all_results)} entries ({len(failed_results)} failed)")

    except Exception as e:
        logger.error(f"Unexpected error in cli: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Review and validate medical dictionary entries",
        epilog="Validates entries for medical recognition, abbreviations, definition quality, and accuracy",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "json_file",
        help="Path to JSON file containing medical dictionary (dict or list format)"
    )
    parser.add_argument(
        "-m", "--model",
        default="ollama/gemma3",
        help="Model name used for review logging (default: ollama/gemma3)"
    )

    args = parser.parse_args()
    cli(args.json_file, args.model)
