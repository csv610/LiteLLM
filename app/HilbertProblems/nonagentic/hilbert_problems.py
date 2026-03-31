#!/usr/bin/env python3
"""
Hilbert's 23 Problems Reference Guide
Dynamically fetches and documents all 23 problems proposed by David Hilbert in 1900,
using LiteClient (ollama/gemma3) for current and comprehensive information
"""

import logging
import json
from pathlib import Path
from typing import Optional

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite import logging_config
from .hilbert_problems_models import HilbertProblemModel
from .hilbert_problems_prompts import PromptBuilder

# Setup logging
logging_config.configure_logging(str(Path(__file__).parent / "logs" / "hilbert_problems.log"))
logger = logging.getLogger(__name__)


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

    def generate_text(self, problem_number: int) -> HilbertProblemModel:
        """
        Fetch a specific Hilbert problem from cache or API.

        Args:
            problem_number: Problem number (1-23)

        Returns:
            HilbertProblem instance or None if fetch fails

        Raises:
            ValueError: If problem_number is not between 1 and 23
        """
        if not (1 <= problem_number <= 23):
            raise ValueError("Problem number must be between 1 and 23")

        try:
            logger.info(f"Fetching Hilbert problem {problem_number} from API")

            # Build prompts using PromptBuilder
            system_prompt = PromptBuilder.get_system_prompt()
            user_prompt = PromptBuilder.get_user_prompt(problem_number)

            model_input = ModelInput(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=HilbertProblemModel
            )

            problem = self.client.generate_text(model_input)

            if isinstance(problem, HilbertProblemModel):
                # Review and refine output
                review_prompt = f"Review this Hilbert problem information for accuracy and completeness:\n{json.dumps(problem.model_dump(), indent=2)}"
                refined_problem = self.client.generate_text(ModelInput(user_prompt=review_prompt, response_format=HilbertProblemModel))
                
                if isinstance(refined_problem, HilbertProblemModel):
                    problem = refined_problem

                # Ensure number field is set correctly
                if problem.number != problem_number:
                    problem.number = problem_number
                logger.info(f"Successfully fetched problem {problem_number}: {problem.title}")
                return problem
            else:
                logger.error(f"No structured output received for problem {problem_number}")
                return None

        except Exception as e:
            logger.error(f"Error fetching problem {problem_number}: {str(e)}")
            return None

    def save_to_file(self, problem: HilbertProblemModel, output_dir: str) -> str:
        """
        Save a Hilbert problem to a JSON file.
        
        Args:
            problem: HilbertProblemModel instance to save
            output_dir: Directory path where to save the file
            
        Returns:
            Path to the saved file
            
        Raises:
            ValueError: If output_dir is invalid
            OSError: If file cannot be written
        """
        try:
            # Create output directory if it doesn't exist
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            filename = f"hilbert_problem_{problem.number:02d}_{problem.title.replace(' ', '_').replace('/', '_').replace(':', '_')}.json"
            file_path = output_path / filename
            
            # Convert model to dictionary and save
            problem_dict = problem.model_dump()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(problem_dict, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved Hilbert problem {problem.number} to {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error saving problem {problem.number}: {str(e)}")
            raise

    @staticmethod
    def display_problem(problem: HilbertProblemModel):
        """Display detailed information about a Hilbert problem."""
        if not problem:
            print("\n❌ Error: No problem information available.")
            return

        print(f"\n{'='*80}")
        print(f"HILBERT'S PROBLEM #{problem.number}: {problem.title}")
        print(f"{'='*80}")
        print(f"\nSTATUS: {problem.status.upper()}")
        
        if problem.solved_by:
            print(f"SOLVED BY: {problem.solved_by}")
        if problem.solution_year:
            print(f"YEAR: {problem.solution_year}")
            
        print(f"\nDESCRIPTION:\n{problem.description}")
        print(f"\nSOLUTION METHOD:\n{problem.solution_method}")
        print(f"\nRELATED FIELDS: {', '.join(problem.related_fields)}")
        print(f"\nNOTES:\n{problem.notes}")
        print(f"\n{'='*80}\n")

    def display_summary(self):
        """Display a summary of all 23 Hilbert problems."""
        print(f"\n{'='*80}")
        print("SUMMARY OF HILBERT'S 23 PROBLEMS")
        print(f"{'='*80}")
        print("\nFetching summary information from AI...")
        
        try:
            # Provide the titles mapping in the summary prompt for grounding
            titles_context = "\n".join([f"#{n}: {t}" for n, t in PromptBuilder.PROBLEM_TITLES.items()])
            user_prompt = f"Using this verified list of titles:\n{titles_context}\n\n{PromptBuilder.get_summary_prompt()}"

            model_input = ModelInput(
                system_prompt=PromptBuilder.get_system_prompt(),
                user_prompt=user_prompt
            )
            summary_text = self.client.generate_text(model_input)
            
            # Review and refine summary
            review_prompt = f"Review this summary of Hilbert's problems for clarity and completeness:\n{summary_text}"
            refined_summary = self.client.generate_text(ModelInput(user_prompt=review_prompt))
            if refined_summary and isinstance(refined_summary, str):
                summary_text = refined_summary

            print(f"\n{summary_text}")
        except Exception as e:
            logger.error(f"Error fetching summary: {str(e)}")
            print(f"\n❌ Error fetching summary: {str(e)}")
        
        print(f"\n{'='*80}\n")
