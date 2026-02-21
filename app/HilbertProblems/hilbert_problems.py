#!/usr/bin/env python3
"""
Hilbert's 23 Problems Reference Guide
Dynamically fetches and documents all 23 problems proposed by David Hilbert in 1900,
using LiteClient (ollama/gemma3) for current and comprehensive information
"""

import sys
import logging
import json
import re
from pathlib import Path
from typing import Dict, Optional

from tqdm import tqdm
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite import logging_config
from hilbert_problems_models import HilbertProblemModel
from hilbert_problems_prompts import PromptBuilder

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

            problem = self.client.generate(model_input)

            if isinstance(problem, HilbertProblemModel):
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

    
    
