"""
math_equation_story_generator.py - Multi-agent orchestration engine

Orchestrates a 3-agent pipeline (Researcher -> Journalist -> Editor) using 
specialized prompts to produce high-quality mathematical narratives.
"""

from typing import Callable, Optional
from lite.lite_client import LiteClient
from lite.config import ModelConfig

from math_equation_story_models import MathematicalEquationStory, ResearchBrief
import math_equation_story_prompts as prompts


class MathEquationStoryGenerator:
    """Multi-agent generator class for creating mathematical equation stories."""
    
    def __init__(self, model_name: str = "ollama/gemma3", temperature: float = 0.7):
        """Initialize the story generator with specified model configuration."""
        self.model_config = ModelConfig(model=model_name, temperature=temperature)
        self.client = LiteClient(model_config=self.model_config)
    
    def generate_text(self, equation_name: str, progress_callback: Optional[Callable[[int, str], None]] = None) -> MathematicalEquationStory:
        """Execute the 3-agent pipeline to generate a high-quality story.

        Args:
            equation_name: The name of the equation (e.g., "Pythagorean Theorem").
            progress_callback: Optional callback receiving (step_number, message).

        Returns:
            MathematicalEquationStory: The final polished output.
        """
        
        # --- AGENT 1: THE RESEARCHER ---
        if progress_callback:
            progress_callback(1, "Gathering historical and technical context...")
        brief: ResearchBrief = self.client.generate_text(
            model_input=prompts.get_researcher_input(equation_name)
        )

        # --- AGENT 2: THE JOURNALIST ---
        if progress_callback:
            progress_callback(2, "Crafting the narrative essay...")
        story_text: str = self.client.generate_text(
            model_input=prompts.get_journalist_input(brief)
        )

        # --- AGENT 3: THE EDITOR ---
        if progress_callback:
            progress_callback(3, "Finalizing the published format...")
        final_story: MathematicalEquationStory = self.client.generate_text(
            model_input=prompts.get_editor_input(equation_name, story_text)
        )

        return final_story
    
    def update_model(self, model_name: str, temperature: float = 0.7) -> None:
        """Update the model configuration."""
        self.model_config = ModelConfig(model=model_name, temperature=temperature)
        self.client = LiteClient(model_config=self.model_config)
