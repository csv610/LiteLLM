"""
unsolved_problems_prompts.py - Prompt builder for unsolved problems

Contains the PromptBuilder class for creating comprehensive prompts
for generating detailed information about unsolved problems in various fields.
"""

from typing import Dict


class PromptBuilder:
    """Builder class for creating prompts for unsolved problems information."""
    
    @staticmethod
    def create_user_prompt(topic: str, num_problems: int) -> str:
        """Create the prompt for fetching unsolved problems in a given topic.
        
        Args:
            topic: The topic to find unsolved problems for
            num_problems: Number of unsolved problems to retrieve
            
        Returns:
            str: Formatted prompt string for the LLM
        """
        return f"""Provide a list of {num_problems} famous unsolved problems in {topic}.

For each problem, provide:
1. Title: The name of the problem
2. Description: A brief, clear explanation of what the problem is and why it matters
3. Field: The specific field or subfield it belongs to
4. Difficulty: Estimated difficulty level (Elementary, Moderate, or Advanced)
5. First Posed: When or by whom the problem was first posed (if known)
6. Prize Money: Any prize money associated with solving it (if applicable)
7. Significance: Why solving this problem would be significant for the field
8. Current Status: The best known results or current status as of today (describe recent progress, partial solutions, or approaches)

Focus on well-known, legitimate unsolved problems in {topic}. Use objective language and avoid speculation.
Ensure the problems are academically recognized and well-documented."""
    
    @staticmethod
    def create_model_input(prompt: str, response_format) -> Dict:
        """Create model input dictionary for LLM generation.
        
        Args:
            prompt: The formatted prompt string
            response_format: The Pydantic model class for response format
            
        Returns:
            dict: Dictionary containing user_prompt and response_format for ModelInput
        """
        return {
            "user_prompt": prompt,
            "response_format": response_format
        }
    
    @staticmethod
    def create_complete_prompt_data(topic: str, num_problems: int, response_format) -> Dict:
        """Create complete prompt data for unsolved problems generation.
        
        Args:
            topic: The topic to find unsolved problems for
            num_problems: Number of unsolved problems to retrieve
            response_format: The Pydantic model class for response format
            
        Returns:
            dict: Dictionary containing formatted prompt and model input data
        """
        prompt = PromptBuilder.create_user_prompt(topic, num_problems)
        return {
            "prompt": prompt,
            "model_input": PromptBuilder.create_model_input(prompt, response_format)
        }
