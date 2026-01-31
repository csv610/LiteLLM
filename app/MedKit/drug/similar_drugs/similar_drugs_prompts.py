"""Prompt templates for Similar Drugs module.

This module contains the PromptBuilder class for generating consistent prompts
for finding similar medicines.
"""

from typing import List


class PromptBuilder:
    """Builds prompts for similar medicines generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for similar medicines analysis."""
        return """You are a pharmaceutical expert and clinical pharmacist with extensive knowledge of medications, their active ingredients, therapeutic classes, and mechanisms of action.

Your task is to find similar medicines to a given drug, prioritizing:
1. Same active ingredients (identical or very similar chemical compounds)
2. Same therapeutic class (drugs treating the same conditions)
3. Similar mechanisms of action (similar pharmacological effects)

For each similar medicine found, provide:
- Generic and brand names
- Active ingredients
- Therapeutic class
- Mechanism of action
- Key similarities and differences
- Clinical considerations
- Availability status

Focus on clinically relevant alternatives that healthcare providers would consider when looking for substitutes. Include both prescription and over-the-counter options where applicable.

Ensure all information is accurate, evidence-based, and includes important clinical considerations for medication substitution."""

    @staticmethod
    def create_user_prompt(medicine_name: str, context: str = "") -> str:
        """Create the user prompt for finding similar medicines.
        
        Args:
            medicine_name: Name of the medicine to find alternatives for
            context: Additional context or requirements
            
        Returns:
            Formatted user prompt
        """
        base_prompt = f"Find the top 10-15 most similar medicines to {medicine_name}"
        
        if context:
            base_prompt += f" - {context}"
        
        base_prompt += """
        
Please provide a comprehensive analysis including:
1. Direct generic equivalents (same active ingredients)
2. Therapeutic class alternatives (same drug class)
3. Mechanism-based alternatives (similar pharmacological action)
4. Key differences in formulation, dosage, or administration
5. Clinical considerations for substitution
6. Availability and cost considerations where relevant

Organize the results by similarity priority and include both prescription and OTC options where applicable."""
        
        return base_prompt

    @staticmethod
    def create_contextual_prompt(medicine_name: str, requirements: List[str]) -> str:
        """Create a contextual prompt with specific requirements.
        
        Args:
            medicine_name: Name of the medicine to find alternatives for
            requirements: List of specific requirements or constraints
            
        Returns:
            Formatted contextual prompt
        """
        context = ". ".join(requirements) if requirements else ""
        
        return PromptBuilder.create_user_prompt(medicine_name, context)
