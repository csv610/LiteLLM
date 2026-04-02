"""
millennium_prize_prompts.py - Prompt builder for Millennium Prize Problems

Contains the PromptBuilder class for creating comprehensive prompts
for generating detailed explanations of Millennium Prize Problems.
"""

from typing import Dict


class PromptBuilder:
    """Builder class for creating prompts for Millennium Prize Problems explanations."""
    
    @staticmethod
    def create_explanation_prompt(problem) -> str:
        """Create a comprehensive prompt for explaining a Millennium Prize Problem.
        
        Args:
            problem: MillenniumProblem object containing problem details
            
        Returns:
            str: Formatted prompt for LLM to generate explanation
        """
        return f"""Explain the following Millennium Prize Problem in detail:

Title: {problem.title}
Description: {problem.description}
Field: {problem.field}
Status: {problem.status}
Significance: {problem.significance}
Current Progress: {problem.current_progress}

Provide a comprehensive explanation including:
1. What the problem asks
2. Why it matters
3. Current status
4. Key historical figures involved
5. Any recent progress or notable attempts"""
    
    @staticmethod
    def create_model_input(prompt: str) -> Dict:
        """Create model input dictionary for LLM generation.
        
        Args:
            prompt: The formatted prompt string
            
        Returns:
            dict: Dictionary containing user_prompt for ModelInput
        """
        return {
            "user_prompt": prompt
        }
    
    @staticmethod
    def create_complete_prompt_data(problem) -> Dict:
        """Create complete prompt data for a Millennium Prize Problem.
        
        Args:
            problem: MillenniumProblem object containing problem details
            
        Returns:
            dict: Dictionary containing formatted prompt and model input data
        """
        prompt = PromptBuilder.create_explanation_prompt(problem)
        return {
            "prompt": prompt,
            "model_input": PromptBuilder.create_model_input(prompt)
        }
