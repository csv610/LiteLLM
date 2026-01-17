#!/usr/bin/env python3
"""
Hilbert's 23 Problems Reference Guide
Dynamically fetches and documents all 23 problems proposed by David Hilbert in 1900,
using LiteClient (ollama/gemma3) for current and comprehensive information
"""

import sys
import argparse
import logging
import json
import re
from pathlib import Path
from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from enum import Enum
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("hilbert_problems.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ProblemStatus(str, Enum):
    """Status of Hilbert problems."""
    SOLVED = "solved"
    UNSOLVED = "unsolved"
    PARTIALLY_SOLVED = "partially_solved"


class HilbertProblem(BaseModel):
    """Structured data for a Hilbert problem."""
    number: int = Field(description="Problem number (1-23)")
    title: str = Field(description="Title of the problem")
    description: str = Field(description="Mathematical description of the problem")
    status: ProblemStatus = Field(description="Current status of the problem")
    solved_by: Optional[str] = Field(description="Mathematician(s) who solved it")
    solution_year: Optional[int] = Field(description="Year the problem was solved")
    solution_method: str = Field(description="Detailed explanation of the solution method")
    related_fields: List[str] = Field(description="Related mathematical fields")
    notes: str = Field(description="Additional notes and implications")


class HilbertProblemsGuide:
    """Reference guide for Hilbert's 23 problems using LiteClient."""

    def __init__(self, config: Optional[ModelConfig] = None):
        """
        Initialize the guide with API client and cache.

        Args:
            config: Optional ModelConfig. If not provided, uses sensible defaults.
        """
        self.config = config or ModelConfig(model="ollama/gemma3", temperature=0.3)
        self.client = LiteClient(self.config)
        self.cache: Dict[int, HilbertProblem] = {}
        self.output_file = self._get_output_file()
        self._load_from_file()

    def _get_output_file(self) -> Path:
        """
        Get the output file path based on the model name.

        Returns:
            Path to the output markdown file
        """
        model_name = self.config.model.replace("/", "_")
        return Path.cwd() / f"hilbert_problems_{model_name}.md"

    def _load_from_file(self) -> None:
        """Load existing problems from the markdown file into cache."""
        if not self.output_file.exists():
            return

        try:
            with open(self.output_file, "r") as f:
                content = f.read()

            # Split by problem blocks (## Problem N:)
            matches = list(re.finditer(r'^## Problem (\d+):', content, flags=re.MULTILINE))

            for i, match in enumerate(matches):
                problem_num = int(match.group(1))
                start = match.end()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
                block = content[start:end]

                try:
                    problem_data = self._parse_problem_block(block, problem_num)
                    if problem_data:
                        self.cache[problem_num] = HilbertProblem(**problem_data)
                except Exception as e:
                    logger.warning(f"Failed to parse problem {problem_num}: {str(e)}")

            logger.info(f"Loaded {len(self.cache)} problems from {self.output_file.name}")
        except Exception as e:
            logger.warning(f"Failed to load from file: {str(e)}")

    @staticmethod
    def _parse_problem_block(block: str, problem_num: int) -> Optional[Dict]:
        """
        Parse a markdown problem block into a dictionary.

        Args:
            block: A markdown block for one problem
            problem_num: The problem number

        Returns:
            Dictionary with problem data or None if parsing fails
        """
        try:
            lines = block.strip().split('\n')
            data = {'number': problem_num}

            # Extract title from first line (after Problem N:)
            first_line = lines[0].strip()
            data['title'] = first_line.split('**Status**')[0].strip()

            current_section = None
            section_content = []

            for line in lines:
                # Check for section headers
                if line.startswith('### '):
                    if current_section and section_content:
                        data[current_section] = '\n'.join(section_content).strip()
                    current_section = line.replace('### ', '').strip().lower()
                    section_content = []
                elif line.startswith('**'):
                    # Parse metadata like **Status**: Solved
                    if '**' in line:
                        parts = line.split('**')
                        if len(parts) >= 3:
                            key = parts[1].lower()
                            value = parts[2].lstrip(':').strip()
                            if key == 'status':
                                # Extract status from "Solved ✅" or "Unsolved ❓"
                                status_val = value.split()[0].lower()
                                data['status'] = status_val
                            elif key == 'solved by':
                                data['solved_by'] = value
                            elif key == 'year':
                                data['solution_year'] = int(value) if value.isdigit() else None
                elif line.startswith('- ') and current_section == 'related fields':
                    # Handle list items for related fields
                    section_content.append(line.lstrip('- ').strip())
                elif line.strip() and not line.startswith('#') and not line.startswith('---'):
                    section_content.append(line)

            # Save last section
            if current_section and section_content:
                if current_section == 'related fields':
                    data[current_section] = [item.strip() for item in section_content if item.strip()]
                else:
                    data[current_section] = '\n'.join(section_content).strip()

            return data
        except Exception as e:
            logger.warning(f"Error parsing problem block: {str(e)}")
            return None

    def _save_to_file(self) -> None:
        """Save all cached problems to the markdown file."""
        try:
            md_content = "# Hilbert's 23 Problems\n\n"

            for num in sorted(self.cache.keys()):
                problem = self.cache[num]
                status_emoji = {
                    ProblemStatus.SOLVED: "✅",
                    ProblemStatus.UNSOLVED: "❓",
                    ProblemStatus.PARTIALLY_SOLVED: "⚠️"
                }
                emoji = status_emoji.get(problem.status, "")

                md_content += f"## Problem {problem.number}: {problem.title} {emoji}\n\n"
                md_content += f"**Status**: {problem.status.value.capitalize()}\n"

                if problem.solved_by:
                    md_content += f"**Solved by**: {problem.solved_by}\n"
                if problem.solution_year:
                    md_content += f"**Year**: {problem.solution_year}\n"

                md_content += f"\n### Description\n\n{problem.description}\n\n"

                md_content += f"### Solution Method\n\n{problem.solution_method}\n\n"

                md_content += "### Related Fields\n\n"
                for field in problem.related_fields:
                    md_content += f"- {field}\n"

                md_content += f"\n### Notes\n\n{problem.notes}\n\n"
                md_content += "---\n\n"

            with open(self.output_file, "w") as f:
                f.write(md_content)
            logger.info(f"Saved {len(self.cache)} problems to {self.output_file.name}")
        except Exception as e:
            logger.error(f"Failed to save to file: {str(e)}")

    @staticmethod
    def _validate_problem_number(problem_number: int) -> None:
        """
        Validate that problem number is between 1 and 23.

        Args:
            problem_number: Problem number to validate

        Raises:
            ValueError: If problem_number is not between 1 and 23
        """
        if problem_number < 1 or problem_number > 23:
            raise ValueError(f"Problem number must be between 1 and 23, got {problem_number}")

    def get_problem(self, problem_number: int) -> Optional[HilbertProblem]:
        """
        Fetch a specific Hilbert problem from cache or API.

        Args:
            problem_number: Problem number (1-23)

        Returns:
            HilbertProblem instance or None if fetch fails

        Raises:
            ValueError: If problem_number is not between 1 and 23
        """
        self._validate_problem_number(problem_number)

        if problem_number in self.cache:
            logger.info(f"Using cached problem {problem_number}")
            return self.cache[problem_number]

        try:
            logger.info(f"Fetching Hilbert problem {problem_number} from API")

            prompt = f"""
            Provide comprehensive information about Hilbert's Problem #{problem_number}.
            Include:
            - Title
            - Mathematical description
            - Current status (solved/unsolved/partially solved)
            - Who solved it and when
            - Detailed solution method/explanation
            - Related mathematical fields (as a list)
            - Important notes

            Return the response with these exact field names: number, title, description, status,
            solved_by, solution_year, solution_method, related_fields, notes
            """

            model_input = ModelInput(
                user_prompt=prompt,
                response_format=HilbertProblem
            )

            problem = self.client.generate_text(model_input)

            if isinstance(problem, HilbertProblem):
                # Ensure number field is set correctly
                if problem.number != problem_number:
                    problem.number = problem_number
                self.cache[problem_number] = problem
                self._save_to_file()
                logger.info(f"Successfully fetched problem {problem_number}: {problem.title}")
                return problem
            else:
                logger.error(f"No structured output received for problem {problem_number}")
                return None

        except Exception as e:
            logger.error(f"Error fetching problem {problem_number}: {str(e)}")
            return None

    def get_all_problems(self) -> Dict[int, HilbertProblem]:
        """
        Fetch all 23 Hilbert problems from the API.

        Returns:
            Dictionary mapping problem numbers to HilbertProblem instances
        """
        all_problems = {}
        for problem_num in tqdm(range(1, 24), desc="Fetching Hilbert Problems"):
            problem = self.get_problem(problem_num)
            if problem:
                all_problems[problem_num] = problem

        logger.info(f"Fetched {len(all_problems)} Hilbert problems")
        return all_problems

    @staticmethod
    def display_problem(problem: Optional[HilbertProblem]) -> None:
        """
        Display a Hilbert problem in formatted terminal output.

        Args:
            problem: HilbertProblem instance to display
        """
        if not problem:
            print("\n❌ Problem not found")
            return

        status_emoji = {
            ProblemStatus.SOLVED: "✅",
            ProblemStatus.UNSOLVED: "❓",
            ProblemStatus.PARTIALLY_SOLVED: "⚠️"
        }

        print("\n" + "=" * 90)
        print(f"Problem {problem.number}: {problem.title} {status_emoji[problem.status]}")
        print("=" * 90)

        print(f"\n📝 DESCRIPTION:")
        print("-" * 90)
        print(problem.description)

        print(f"\n📊 STATUS: {problem.status.value.upper()}")
        if problem.solved_by:
            print(f"   Solved by: {problem.solved_by}")
        if problem.solution_year:
            print(f"   Year: {problem.solution_year}")

        print(f"\n🔬 SOLUTION METHOD:")
        print("-" * 90)
        print(problem.solution_method.strip())

        print(f"\n🏷️  RELATED FIELDS:")
        print("-" * 90)
        for field in problem.related_fields:
            print(f"   • {field}")

        print(f"\n💡 NOTES:")
        print("-" * 90)
        print(problem.notes)

        print("\n" + "=" * 90 + "\n")

    def display_summary(self) -> None:
        """Display a summary of all Hilbert problems with their status."""
        all_problems = self.get_all_problems()

        if not all_problems:
            print("\n⚠️  Could not fetch problems. Please check your API configuration.\n")
            return

        solved = sum(1 for p in all_problems.values() if p.status == ProblemStatus.SOLVED)
        unsolved = sum(1 for p in all_problems.values() if p.status == ProblemStatus.UNSOLVED)
        partial = sum(1 for p in all_problems.values() if p.status == ProblemStatus.PARTIALLY_SOLVED)

        print("\n" + "=" * 90)
        print("HILBERT'S 23 PROBLEMS - SUMMARY")
        print("=" * 90)

        print(f"\n📊 OVERALL STATUS:")
        print(f"   ✅ Solved:           {solved}/23")
        print(f"   ❓ Unsolved:         {unsolved}/23")
        print(f"   ⚠️  Partially Solved: {partial}/23")

        print(f"\n✅ SOLVED PROBLEMS:")
        for num, problem in sorted(all_problems.items()):
            if problem.status == ProblemStatus.SOLVED:
                print(f"   {num:2d}. {problem.title}")

        print(f"\n❓ UNSOLVED PROBLEMS:")
        for num, problem in sorted(all_problems.items()):
            if problem.status == ProblemStatus.UNSOLVED:
                print(f"   {num:2d}. {problem.title}")

        print(f"\n⚠️  PARTIALLY SOLVED PROBLEMS:")
        for num, problem in sorted(all_problems.items()):
            if problem.status == ProblemStatus.PARTIALLY_SOLVED:
                print(f"   {num:2d}. {problem.title}")

        print("\n" + "=" * 90 + "\n")


def argument_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for the Hilbert problems guide.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Hilbert's 23 Problems Reference Guide - Dynamically fetches comprehensive documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python hilbert_problems.py                              # Show all problems summary
  python hilbert_problems.py -p 1                         # Show details of problem 1
  python hilbert_problems.py -p 8 -m ollama/gemma3       # Show problem 8 using specific model
  python hilbert_problems.py -m ollama/mistral           # Show all problems with custom model
        """
    )

    parser.add_argument(
        "-p", "--problem",
        type=int,
        help="Problem number (1-23) to display details. If not specified, shows summary of all problems"
    )

    parser.add_argument(
        "-m", "--model",
        default="ollama/gemma3",
        help="Model to use for fetching problem information (default: ollama/gemma3)"
    )

    return parser


def main():
    """Main entry point for the Hilbert problems reference guide."""
    parser = argument_parser()
    args = parser.parse_args()

    try:
        # Initialize the guide with specified model
        config = ModelConfig(model=args.model, temperature=0.3)
        guide = HilbertProblemsGuide(config)

        # Display specific problem or summary
        if args.problem:
            if args.problem < 1 or args.problem > 23:
                print(f"\n❌ Invalid problem number: {args.problem}")
                print("Please specify a number between 1 and 23\n")
                return

            print(f"\n🔄 Fetching Problem {args.problem}...")
            problem = guide.get_problem(args.problem)
            HilbertProblemsGuide.display_problem(problem)
        else:
            guide.display_summary()

    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
