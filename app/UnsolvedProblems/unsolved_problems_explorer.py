"""
unsolved_problems_explorer.py - Explorer class for unsolved problems

Contains the UnsolvedProblemsExplorer class for fetching and managing
unsolved problems in various academic fields.
"""

import logging
import os
import re
from typing import Optional, List

from lite import LiteClient, ModelConfig
from lite.config import ModelInput

from unsolved_problems_models import UnsolvedProblem, UnsolvedProblemsResponse
from unsolved_problems_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class UnsolvedProblemsExplorer:
    """Explorer class for fetching and managing unsolved problems."""
    
    def __init__(self, model: Optional[str] = None, temperature: float = 0.2):
        """Initialize the explorer with model configuration.
        
        Args:
            model: LLM model to use (defaults to environment variable or ollama/gemma3)
            temperature: Temperature setting for model generation
        """
        self.model = model or os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3")
        self.temperature = temperature
        self.model_config = ModelConfig(model=self.model, temperature=self.temperature)
        self.client = LiteClient(model_config=self.model_config)
    
    def validate_model_name(self, model: str) -> None:
        """Validate model name format.
        
        Args:
            model: Model name to validate
            
        Raises:
            ValueError: If model name is invalid
        """
        if not re.match(r'^[a-zA-Z0-9\-\./_]+$', model):
            raise ValueError(f"Invalid model name: {model}. Only alphanumeric characters, hyphens, slashes, dots, and underscores are allowed.")
    
    def validate_num_problems(self, num_problems: int) -> None:
        """Validate number of problems.
        
        Args:
            num_problems: Number of problems to validate
            
        Raises:
            ValueError: If number of problems is out of range
        """
        if num_problems < 1 or num_problems > 50:
            raise ValueError(f"Number of problems must be between 1 and 50, got {num_problems}")
    
    def _handle_api_error(self, error: Exception) -> None:
        """Handle and translate API errors to meaningful exceptions.
        
        Args:
            error: Exception raised during API call
            
        Raises:
            RuntimeError: With appropriate error message
        """
        error_str = str(error).lower()
        
        if "401" in str(error) or "authentication" in error_str:
            logger.error("Authentication failed: Check your API credentials")
            raise RuntimeError("API authentication failed. Check LITELLM_API_KEY or model-specific credentials.")
        elif "429" in str(error):
            logger.error("Rate limit exceeded")
            raise RuntimeError("API rate limit exceeded. Please try again later.")
        elif "404" in str(error):
            logger.error("Model not found")
            raise RuntimeError("Model not found or not available.")
        else:
            logger.error(f"Unexpected error: {error}")
            raise RuntimeError(f"Failed to fetch unsolved problems: {error}")
    
    def fetch_problems(self, topic: str, num_problems: int) -> List[UnsolvedProblem]:
        """Fetch unsolved problems for a specific topic.
        
        Args:
            topic: The topic to find unsolved problems for
            num_problems: Number of unsolved problems to retrieve
            
        Returns:
            List of UnsolvedProblem instances
            
        Raises:
            ValueError: If API response is invalid or parameters are invalid
            RuntimeError: If API call fails or required credentials are missing
        """
        # Validate inputs
        self.validate_model_name(self.model)
        self.validate_num_problems(num_problems)
        
        logger.info(f"Fetching {num_problems} unsolved problems in {topic} using model: {self.model}")
        
        try:
            # Create prompt using PromptBuilder
            prompt_data = PromptBuilder.create_complete_prompt_data(topic, num_problems, UnsolvedProblemsResponse)
            
            # Create ModelInput with prompt and response format
            model_input = ModelInput(**prompt_data["model_input"])
            
            # Generate text using LiteClient
            response_content = self.client.generate_text(model_input=model_input)
            
            # Parse the response
            if isinstance(response_content, str):
                response = UnsolvedProblemsResponse.model_validate_json(response_content)
            elif isinstance(response_content, UnsolvedProblemsResponse):
                response = response_content
            else:
                raise ValueError(f"Unexpected response type: {type(response_content)}")
            
            if not response.problems or len(response.problems) == 0:
                raise ValueError("No unsolved problems returned in response")
            
            logger.info(f"Successfully fetched {len(response.problems)} unsolved problem(s)")
            return response.problems
            
        except Exception as e:
            self._handle_api_error(e)
    
    def update_model(self, model: str, temperature: Optional[float] = None) -> None:
        """Update the model configuration.
        
        Args:
            model: New model name to use
            temperature: New temperature setting (optional)
        """
        self.validate_model_name(model)
        self.model = model
        
        if temperature is not None:
            self.temperature = temperature
        
        self.model_config = ModelConfig(model=self.model, temperature=self.temperature)
        self.client = LiteClient(model_config=self.model_config)
    
    def get_model_info(self) -> dict:
        """Get information about the current model configuration.
        
        Returns:
            dict: Dictionary containing model information
        """
        return {
            "model": self.model,
            "temperature": self.temperature
        }
