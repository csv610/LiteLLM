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

from unsolved_problems_models import UnsolvedProblem, UnsolvedProblemsModel
from unsolved_problems_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class UnsolvedProblemsExplorer:
    """Explorer class for fetching and managing unsolved problems."""
    
    def __init__(self, model_config: ModelConfig):
        """Initialize explorer with model configuration.
        
        Args:
            model_config: ModelConfig instance with model and temperature settings
        """
        self.model_config = model_config
        self.client = LiteClient(model_config=self.model_config)
    
    def generate_text(self, topic: str, num_problems: int) -> List[UnsolvedProblem]:
        """Fetch unsolved problems for a specific topic.
        
        Args:
            topic: The topic to find unsolved problems for
            num_problems: Number of unsolved problems to retrieve
            
        Returns:
            List of UnsolvedProblem instances
            
        Raises:
            ValueError: If API response is invalid or model response doesn't match schema
            RuntimeError: If API call fails or required credentials are missing
        """
        logger.info(f"Fetching {num_problems} unsolved problems in {topic} using model: {self.model_config.model}")
        
        # Build prompts
        system_prompt = PromptBuilder.get_system_prompt()
        user_prompt = PromptBuilder.get_user_prompt(topic, num_problems)
        
        # Create model input
        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=UnsolvedProblemsResponse
        )
        
        # Generate response using LiteClient
        response = self.client.generate(model_input)
        
        return response.problems
    
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
