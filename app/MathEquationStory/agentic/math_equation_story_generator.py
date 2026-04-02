"""
math_equation_story_generator.py - Multi-agent orchestration engine for equation stories

Orchestrates a 3-agent pipeline (Researcher -> Journalist -> Editor) using
specialized prompts to produce high-quality mathematical narratives.
"""

from typing import Callable, Optional
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from .math_equation_story_models import MathematicalEquationStory, ResearchBrief, ModelOutput
from . import math_equation_story_prompts as prompts


class MathEquationStoryGenerator:
    """Multi-agent generator class for creating mathematical equation stories."""

    def __init__(self, model_name: str = "ollama/gemma3", temperature: float = 0.7):
        """Initialize the story generator with specified model configuration."""
        self.model_config = ModelConfig(model=model_name, temperature=temperature)
        self.client = LiteClient(model_config=self.model_config)

    def generate_text(
        self,
        equation_name: str,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> ModelOutput:
        """Execute the 3nd-tier multi-agent pipeline to generate a ModelOutput artifact.

        Args:
            equation_name: The name of the equation (e.g., "Pythagorean Theorem").
            progress_callback: Optional callback receiving (step_number, message).

        Returns:
            ModelOutput: The final standardized artifact.
        """

        # --- AGENT 1: THE RESEARCHER (Tier 1 Specialist) ---
        if progress_callback:
            progress_callback(1, "Gathering historical and technical context...")
        brief_res = self.client.generate_text(
            model_input=prompts.get_researcher_input(equation_name)
        )
        brief: ResearchBrief = brief_res.data

        # --- AGENT 2: THE JOURNALIST (Tier 1 Specialist) ---
        if progress_callback:
            progress_callback(2, "Crafting the narrative essay...")
        story_res = self.client.generate_text(
            model_input=prompts.get_journalist_input(brief)
        )
        story_text = story_res.markdown

        # --- AGENT 3: THE EDITOR (Tier 3 Closer) ---
        if progress_callback:
            progress_callback(3, "Finalizing the published format...")
        # Update prompt to explicitly request Markdown
        editor_input = prompts.get_editor_input(equation_name, story_text)
        editor_input.response_format = None # Final synthesis is Markdown
        editor_input.user_prompt += "\n\nFINAL INSTRUCTION: Synthesize this story into a beautiful, engaging Markdown report. Use LaTeX for math, include historical anecdotes, and ensure a logical narrative flow."
        
        final_markdown_res = self.client.generate_text(model_input=editor_input)
        final_markdown = final_markdown_res.markdown

        # Standardized Data Object
        final_data = MathematicalEquationStory(
            equation_name=equation_name,
            title=f"The Story of {equation_name}",
            narrative_essay=story_text,
            key_takeaways=[]
        )

        return ModelOutput(
            data=final_data,
            markdown=final_markdown,
            metadata={"research_brief": brief.model_dump() if hasattr(brief, 'model_dump') else {}}
        )

    def update_model(self, model_name: str, temperature: float = 0.7) -> None:
        """Update the model configuration."""
        self.model_config = ModelConfig(model=model_name, temperature=temperature)
        self.client = LiteClient(model_config=self.model_config)
