#!/usr/bin/env python3
"""
Hilbert's 23 Problems Reference Guide
Uses a two-agent pipeline:
1. A researcher agent drafts the answer.
2. A reviewer agent validates and corrects the draft.
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

logger = logging.getLogger(__name__)


def _configure_module_logging() -> None:
    """Configure file logging lazily to avoid import-time filesystem side effects."""
    if getattr(_configure_module_logging, "_configured", False):
        return
    logging_config.configure_logging(str(Path(__file__).parent / "logs" / "hilbert_problems.log"))
    _configure_module_logging._configured = True


class HilbertProblemsGuide:
    """Reference guide for Hilbert's 23 problems using a two-agent LiteClient flow."""

    def __init__(self, config: Optional[ModelConfig] = None):
        """
        Initialize the guide with API client and cache.

        Args:
            config: Optional ModelConfig. If not provided, uses sensible defaults.
        """
        _configure_module_logging()
        self.config = config or ModelConfig(model="ollama/gemma3", temperature=0.3)
        self.research_client = LiteClient(self.config)
        self.review_client = LiteClient(self.config)

    @staticmethod
    def _validate_problem_number(problem_number: int) -> None:
        """Validate that the requested problem number is within Hilbert's canonical list."""
        if not 1 <= problem_number <= 23:
            raise ValueError(f"Problem number must be between 1 and 23, got {problem_number}")

    def _run_structured_agent(
        self,
        client: LiteClient,
        role_name: str,
        system_prompt: str,
        user_prompt: str
    ) -> Optional[HilbertProblemModel]:
        """Run one structured agent pass and return validated output if available."""
        logger.info(f"{role_name} agent running structured pass")
        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=HilbertProblemModel
        )
        result = client.generate_text(model_input)
        return result if isinstance(result, HilbertProblemModel) else None

    def _run_text_agent(
        self,
        client: LiteClient,
        role_name: str,
        system_prompt: str,
        user_prompt: str
    ) -> Optional[str]:
        """Run one text agent pass and return text output if available."""
        logger.info(f"{role_name} agent running text pass")
        model_input = ModelInput(system_prompt=system_prompt, user_prompt=user_prompt)
        result = client.generate_text(model_input)
        return result if isinstance(result, str) else None

    def _generate_problem_draft(self, problem_number: int) -> Optional[HilbertProblemModel]:
        """Generate the first-pass draft for a problem."""
        return self._run_structured_agent(
            client=self.research_client,
            role_name="Researcher",
            system_prompt=PromptBuilder.get_system_prompt(),
            user_prompt=PromptBuilder.get_user_prompt(problem_number)
        )

    def _review_problem_draft(
        self,
        problem_number: int,
        draft_problem: HilbertProblemModel
    ) -> Optional[HilbertProblemModel]:
        """Review and correct the first-pass draft with a second agent."""
        return self._run_structured_agent(
            client=self.review_client,
            role_name="Reviewer",
            system_prompt=PromptBuilder.get_reviewer_system_prompt(),
            user_prompt=PromptBuilder.get_reviewer_prompt(
                problem_number,
                json.dumps(draft_problem.model_dump(), indent=2, ensure_ascii=False)
            ),
        )

    def generate_text(self, problem_number: int) -> Optional[HilbertProblemModel]:
        """
        Fetch a specific Hilbert problem using a researcher-reviewer pipeline.

        Args:
            problem_number: Problem number (1-23)

        Returns:
            HilbertProblemModel instance or None if fetch fails

        Raises:
            ValueError: If problem_number is not between 1 and 23
        """
        self._validate_problem_number(problem_number)

        try:
            logger.info(f"Fetching Hilbert problem {problem_number} with two agents")

            draft_problem = self._generate_problem_draft(problem_number)
            if draft_problem is None:
                logger.error(f"Researcher agent did not return structured output for problem {problem_number}")
                return None

            reviewed_problem = self._review_problem_draft(problem_number, draft_problem)
            if reviewed_problem is None:
                logger.warning(
                    f"Reviewer agent did not return structured output for problem {problem_number}; "
                    "falling back to researcher draft"
                )
                reviewed_problem = draft_problem

            if reviewed_problem.number != problem_number:
                reviewed_problem.number = problem_number
            if reviewed_problem.title != PromptBuilder.PROBLEM_TITLES.get(problem_number):
                reviewed_problem.title = PromptBuilder.PROBLEM_TITLES[problem_number]

            logger.info(f"Successfully fetched problem {problem_number}: {reviewed_problem.title}")
            return reviewed_problem

        except Exception as e:
            logger.error(f"Error fetching problem {problem_number}: {str(e)}")
            return None

    def _generate_summary_draft(self) -> Optional[str]:
        """Generate the first-pass summary draft."""
        titles_context = "\n".join([f"#{n}: {t}" for n, t in PromptBuilder.PROBLEM_TITLES.items()])
        user_prompt = f"Using this verified list of titles:\n{titles_context}\n\n{PromptBuilder.get_summary_prompt()}"
        return self._run_text_agent(
            client=self.research_client,
            role_name="Researcher",
            system_prompt=PromptBuilder.get_system_prompt(),
            user_prompt=user_prompt
        )

    def _review_summary_draft(self, summary_text: str) -> Optional[str]:
        """Review and refine the summary draft."""
        return self._run_text_agent(
            client=self.review_client,
            role_name="Reviewer",
            system_prompt=PromptBuilder.get_reviewer_system_prompt(),
            user_prompt=PromptBuilder.get_summary_reviewer_prompt(summary_text)
        )

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
        """Display a summary of all 23 Hilbert problems using two agents."""
        print(f"\n{'='*80}")
        print("SUMMARY OF HILBERT'S 23 PROBLEMS")
        print(f"{'='*80}")
        print("\nFetching summary information from two agents...")
        
        try:
            draft_summary = self._generate_summary_draft()
            if draft_summary is None:
                raise ValueError("Researcher agent did not return summary text")

            reviewed_summary = self._review_summary_draft(draft_summary)
            if reviewed_summary is None:
                logger.warning("Reviewer agent did not return summary text; falling back to researcher draft")
                reviewed_summary = draft_summary

            print(f"\n{reviewed_summary}")
        except Exception as e:
            logger.error(f"Error fetching summary: {str(e)}")
            print(f"\n❌ Error fetching summary: {str(e)}")
        
        print(f"\n{'='*80}\n")
