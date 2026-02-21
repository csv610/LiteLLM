"""
hilbert_problems_prompts.py - PromptBuilder class for Hilbert's 23 Problems

Contains the PromptBuilder class for creating structured prompts
for fetching comprehensive information about Hilbert's mathematical problems.
"""

from typing import Optional


class PromptBuilder:
    """Builder class for creating Hilbert problem prompts."""
    
    @staticmethod
    def get_system_prompt() -> str:
        """
        Get the system prompt for Hilbert problems generation.
        
        Returns:
            System prompt string for LLM
        """
        return """You are an expert mathematical historian and mathematician specializing in the history of mathematics and the work of David Hilbert. Your task is to provide comprehensive, accurate, and well-structured information about Hilbert's 23 problems proposed in 1900.

Key Principles:
1. Historical Accuracy: Ensure all historical facts, dates, and names are correct
2. Mathematical Precision: Provide clear and accurate mathematical descriptions
3. Current Status: Include up-to-date information about solution status
4. Comprehensive Coverage: Include all relevant details about each problem
5. Clear Structure: Organize information in a logical, easy-to-read format

Quality Standards:
- Use precise mathematical terminology
- Provide historical context and significance
- Include current mathematical understanding
- Reference important developments and breakthroughs
- Connect problems to broader mathematical fields
- Ensure all information is factually accurate and well-sourced"""

    @staticmethod
    def get_user_prompt(problem_number: int) -> str:
        """
        Get the user prompt for a specific Hilbert problem.
        
        Args:
            problem_number: The problem number (1-23)
            
        Returns:
            User prompt string for LLM
        """
        return f"""Provide comprehensive information about Hilbert's Problem #{problem_number}. Include the following details:

1. **Title**: The official or commonly accepted title of the problem
2. **Mathematical Description**: Clear and precise mathematical formulation
3. **Current Status**: Whether solved, unsolved, or partially solved
4. **Solution Details**: If solved, who solved it and when
5. **Solution Method**: Detailed explanation of the approach used
6. **Related Fields**: Mathematical areas connected to this problem
7. **Important Notes**: Additional context, implications, or interesting facts

Requirements:
- Ensure mathematical accuracy and precision
- Include historical context and significance
- Provide current understanding of the problem
- Reference key developments and breakthroughs
- Connect to broader mathematical concepts
- Use clear, accessible language while maintaining mathematical rigor

Return the response with these exact field names: number, title, description, status, solved_by, solution_year, solution_method, related_fields, notes"""

    @staticmethod
    def get_summary_prompt() -> str:
        """
        Get the user prompt for generating a summary of all Hilbert problems.
        
        Returns:
            User prompt string for LLM
        """
        return """Provide a comprehensive overview of all 23 of Hilbert's problems, including:

1. **Problem Numbers and Titles**: List all 23 problems with their titles
2. **Status Overview**: Current status of each problem (solved/unsolved/partially solved)
3. **Historical Significance**: Impact on 20th century mathematics
4. **Key Solvers**: Mathematicians who contributed to solutions
5. **Mathematical Fields**: Areas of mathematics influenced by these problems
6. **Open Problems**: Which problems remain unsolved and their importance

Requirements:
- Provide accurate historical information
- Include current status of each problem
- Highlight major mathematical breakthroughs
- Emphasize the collective impact on mathematics
- Use clear, organized structure
- Reference important dates and contributors

Focus on the collective impact of these problems on mathematical research and their continuing influence on the field."""
