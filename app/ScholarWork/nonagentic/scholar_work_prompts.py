"""
scholar_work_prompts.py - Prompt builder for scholar major works

Provides comprehensive prompt building functionality for generating narrative-driven
explanations of major scientific work done by a given scientist.
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

from app.ScholarWork.nonagentic.scholar_work_models import ScholarMajorWork


class PromptBuilder:
    """Builder class for creating prompts for scholar major work generation."""

    @staticmethod
    def create_user_prompt(
        scholar_name: str, major_contribution: str = "their most significant work"
    ) -> str:
        """Create the user prompt for generating a scholar's major work story.

        Args:
            scholar_name: The name of the scholar
            major_contribution: The specific contribution or theory (optional)

        Returns:
            str: The formatted user prompt
        """
        return f"""
Write a compelling narrative essay about {scholar_name}'s major contribution, specifically {major_contribution}, written like an article you'd find in Scientific American, The New Yorker, or a high-quality science publication.

CORE PRINCIPLES:
============================================================================

1. NARRATIVE FLOW: Write as a single, coherent story with natural transitions—NOT as sections or labeled parts. The story should flow like a professional essay.

2. ACCESSIBILITY: Make this accessible to intelligent readers with a general science background. Use clear, elegant language.

3. ENGAGEMENT: Draw readers in with genuine intellectual interest. Show why this scientist's work was revolutionary and why it matters.

4. ACCURACY: Be scientifically accurate about the core concepts, though you can simplify complex details for general understanding.

5. STRUCTURE (But integrated seamlessly):
   - Hook readers with a compelling scene or insight from {scholar_name}'s life or research
   - Introduce the context: What was the scientific landscape before this work?
   - Describe the journey: What was the problem they were trying to solve?
   - Explain the core "Aha!" moment or the central thesis of {major_contribution}
   - Show how the discovery changed our understanding of the world
   - Connect the work to modern science and society
   - Leave readers with a sense of the legacy of {scholar_name}

THE STORY SHOULD:
============================================================================
- Feel like you're reading a professional profile or science essay, not a Wikipedia entry
- Use vivid details and historical context to ground the abstract science
- Build intellectual momentum—the logic of the discovery should build piece by piece
- Include moments that highlight {scholar_name}'s unique approach or insight
- Make the subject matter feel important and relevant
- Be substantial enough to fully explore the work (800-1500 words)

SPECIFIC GUIDANCE FOR {scholar_name}:
============================================================================
Research and explore:
1. What was the specific breakthrough of {major_contribution}?
2. What were the obstacles—scientific or social—that {scholar_name} faced?
3. How did this work overturn existing paradigms?
4. What is the most enduring legacy of this specific contribution?
5. How does this work influence science today?

Then weave these elements into a flowing narrative that brings the scholar's work to life.

TONE & STYLE:
============================================================================
- Professional but warm and intellectually stimulating
- Story-driven rather than encyclopedic
- Use specific anecdotes and historical context
- Build a sense of discovery as readers follow the logic
- Celebrate the human endeavor behind scientific progress

Write this as a complete essay that could be published in a major science magazine.
The reader should finish feeling they understand the essence of {scholar_name}'s contribution."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for the scholar major work generator.

        Returns:
            str: The formatted system prompt
        """
        return """You are a science historian and journalist for top-tier publications. You specialize in bringing the work of great scientists to life for a general audience.

Your approach:
- You write flowing narrative essays, not listicles or reference entries
- You focus on the intellectual journey and the core logic of discovery
- You place scientific breakthroughs in their historical and human context
- You make complex theories feel intuitive and important
- You respect your readers' intelligence while ensuring the science is accessible
- You show why a scientist's work remains relevant to our modern world

Your strength is finding the core "beauty" and "revolutionary power" in scientific ideas.

Write engaging, flowing prose that reads like high-quality science journalism."""

    @staticmethod
    def create_model_input(
        scholar_name: str, major_contribution: str = "their most significant work"
    ) -> dict:
        """Create the complete model input with user prompt, system prompt, and response format.

        Args:
            scholar_name: The name of the scholar
            major_contribution: The specific contribution or theory (optional)

        Returns:
            dict: Dictionary containing user_prompt, system_prompt, and response_format
        """
        return {
            "user_prompt": PromptBuilder.create_user_prompt(
                scholar_name, major_contribution
            ),
            "system_prompt": PromptBuilder.create_system_prompt(),
            "response_format": ScholarMajorWork,
        }
