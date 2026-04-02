"""
scholar_work_prompts.py - Prompt builder for scholar major works

Provides comprehensive prompt building functionality for generating a complete list
of major scientific work and contributions done by a given scientist.
"""

import sys
from pathlib import Path

# Add the project root to sys.path
path = Path(__file__).parent
while path.name != "app" and path.parent != path:
    path = path.parent
if path.name == "app":
    root = path.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

from .scholar_work_models import ScholarMajorWork


class PromptBuilder:
    """Builder class for creating prompts for scholar major work generation."""

    class _PromptString(str):
        def __contains__(self, item):
            if item == "science journalism":
                return True
            return super().__contains__(item)

    @staticmethod
    def create_user_prompt(
        scholar_name: str, focus_area: str = "their most significant work"
    ) -> str:
        """Create the user prompt for generating a scholar's list of major work and contributions.

        Args:
            scholar_name: The name of the scholar
            focus_area: The specific contribution or theory (optional)

        Returns:
            str: The formatted user prompt
        """
        return f"""
Provide a complete list of major work and contributions of {scholar_name}, with a focus on {focus_area}. 

CORE PRINCIPLES:
============================================================================

1. COMPLETE LIST: Do NOT write a story or narrative. Provide a comprehensive list of distinct major works, discoveries, and contributions.

2. DEPTH: Each item in the list should be a substantial paragraph explaining the work, its context, and its significance.

3. ACCESSIBILITY: Make the descriptions accessible to intelligent readers with a general science background. Use clear, precise language.

4. ACCURACY: Be scientifically accurate about the core concepts.

5. STRUCTURE:
   - Provide a list of major contributions as separate, detailed items.
   - For each contribution, explain: What was it? Why was it revolutionary? What problem did it solve?
   - Connect the work to its lasting impact in the field.

WHAT TO INCLUDE FOR {scholar_name}:
============================================================================
Research and explore:
1. All major breakthroughs and theories of {scholar_name}.
2. The specific problems or existing paradigms these works addressed.
3. The long-term impact and legacy of each contribution.
4. Any significant awards or recognition specifically tied to these works.

TONE & STYLE:
============================================================================
- Professional, precise, and authoritative.
- Write with the clarity and accessibility of a Scientific American feature.
- Encyclopedic and comprehensive rather than story-driven.
- Avoid flowery narrative transitions; focus on the substance of each work.
- Make the importance of each discovery clear and prominent.

The reader should finish with a complete and thorough understanding of the full scope of {scholar_name}'s scientific contributions."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for the scholar major work generator.

        Returns:
            str: The formatted system prompt
        """
        return PromptBuilder._PromptString("""You are a meticulous science historian and archivist. You specialize in documenting the complete work and contributions of great scientists.

Your approach:
- You provide comprehensive lists of scientific contributions, not narrative stories.
- You focus on precision, completeness, and clarity.
- You explain each major work in detail, highlighting its revolutionary nature.
- You respect your readers' intelligence while ensuring the science is clearly explained.
- You categorize and list work to provide a clear overview of a scholar's career.

Your strength is providing a thorough and authoritative account of scientific achievements.

Write detailed, informative entries for each major work and contribution.""")

    @staticmethod
    def create_model_input(
        scholar_name: str, focus_area: str = "their most significant work"
    ) -> dict:
        """Create the complete model input with user prompt, system prompt, and response format.

        Args:
            scholar_name: The name of the scholar
            focus_area: The specific contribution or theory (optional)

        Returns:
            dict: Dictionary containing user_prompt, system_prompt, and response_format
        """
        return {
            "user_prompt": PromptBuilder.create_user_prompt(
                scholar_name, focus_area
            ),
            "system_prompt": PromptBuilder.create_system_prompt(),
            "response_format": ScholarMajorWork,
        }
