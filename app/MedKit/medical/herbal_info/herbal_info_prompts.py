"""
Prompt builder for herbal information generation.
"""

class PromptBuilder:
    """Builder class for creating prompts for herbal information generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for herbal information generation."""
        return """You are an expert herbalist and natural medicine specialist with extensive knowledge of medicinal plants.
Your role is to provide comprehensive, accurate, and evidence-based information about herbs and their uses.
Focus on safety, traditional uses, active compounds, and modern research where available."""

    @staticmethod
    def create_user_prompt(herb: str) -> str:
        """Create the user prompt for herbal information generation.

        Args:
            herb: The name of the herb to generate information for.
        """
        return f"Generate comprehensive information for the herb: {herb}."
