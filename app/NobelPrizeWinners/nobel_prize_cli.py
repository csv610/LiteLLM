"""nobel_prize_cli.py - CLI interface for Nobel Prize information

Contains command-line interface functions for the Nobel Prize information tool,
including argument parsing, validation, and main entry point.
"""

import argparse
import logging
import json
import sys
import os
from datetime import datetime
from pathlib import Path

from lite import logging_config
from nobel_prize_info import fetch_nobel_winners

# Global logger for application
logger = None

def validate_year(year_str: str) -> int:
    """
    Validate and convert year string to integer.

    Args:
        year_str: Year as string

    Returns:
        Year as integer

    Raises:
        argparse.ArgumentTypeError: If year is invalid
    """
    try:
        year_int = int(year_str)
        current_year = datetime.now().year
        if year_int < 1901:
            raise argparse.ArgumentTypeError(
                f"Nobel Prizes began in 1901, got {year_int}"
            )
        if year_int > current_year:
            raise argparse.ArgumentTypeError(
                f"Year cannot be in the future (current year: {current_year})"
            )
        return year_int
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Year must be a valid number, got '{year_str}'"
        )


def validate_category(category_str: str) -> str:
    """
    Validate and normalize Nobel Prize category.

    Args:
        category_str: Category name (case-insensitive)

    Returns:
        Normalized category name

    Raises:
        argparse.ArgumentTypeError: If category is invalid
    """
    valid_fields = ["Physics", "Chemistry", "Medicine", "Literature", "Peace", "Economics"]
    valid_fields_lower = [f.lower() for f in valid_fields]

    if category_str.lower() not in valid_fields_lower:
        raise argparse.ArgumentTypeError(
            f"'{category_str}' is not a valid Nobel Prize category. "
            f"Valid categories are: {', '.join(valid_fields)}"
        )

    # Return normalized (proper case) field
    return valid_fields[valid_fields_lower.index(category_str.lower())]


def arguments_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Fetch detailed information about Nobel Prize winners",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python nobel_prize_cli.py -c Physics -y 2023
  python nobel_prize_cli.py --category Chemistry --year 2022
  python nobel_prize_cli.py -c Medicine -y 2021 -m claude-3-opus
  NOBEL_PRIZE_MODEL=gpt-4 python nobel_prize_cli.py -c Literature -y 2020
        """
    )

    parser.add_argument(
        "-c", "--category",
        required=True,
        type=validate_category,
        help="Nobel Prize category (Physics, Chemistry, Medicine, Literature, Peace, Economics)"
    )

    parser.add_argument(
        "-y", "--year",
        required=True,
        type=validate_year,
        help="Year of the Nobel Prize (1901 onwards)"
    )

    parser.add_argument(
        "-m", "--model",
        default=None,
        help="LLM model to use (default: $NOBEL_PRIZE_MODEL or gemini/gemini-2.5-flash)"
    )

    return parser


def main() -> int:
    """
    Main entry point for the Nobel Prize information CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    global logger
    
    parser = arguments_parser()
    args = parser.parse_args()

    try:
        # Initialize global logger
        logger = logging_config.setup_logging(str(Path(__file__).parent / "logs" / "nobel_prize_cli.log"))
        
        logger.info(f"Fetching Nobel Prize information for {args.category} in {args.year}...")

        winners = fetch_nobel_winners(args.category, str(args.year), model=args.model)

        # Save to JSON file with format: {category}_{year}.json
        output_filename = f"{args.category.lower()}_{args.year}.json"

        data_to_save = {
            "category": args.category,
            "year": args.year,
            "winners_count": len(winners),
            "winners": [winner.model_dump() for winner in winners]
        }

        with open(output_filename, 'w') as f:
            json.dump(data_to_save, f, indent=4)

        os.chmod(output_filename, 0o600)

        logger.info(f"Successfully saved {len(winners)} winner(s) to {output_filename}")
        print(f"Results saved to {output_filename}")
        print(f"Winners retrieved: {len(winners)}")
        for i, winner in enumerate(winners, 1):
            print(f"  {i}. {winner.name} ({winner.year})")

        return 0

    except Exception as e:
        logger.exception(f"Error: {e}")
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
