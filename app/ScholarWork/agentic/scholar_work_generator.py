"""
scholar_work_generator.py - Multi-agent orchestration engine for scholar work

Orchestrates a 3-agent pipeline (Researcher -> Journalist -> Editor) using 
specialized prompts to produce high-quality narratives about a scholar's major work.
"""

from typing import Callable, Optional
from lite.lite_client import LiteClient
from lite.config import ModelConfig

from .scholar_work_models import ScholarMajorWork, ResearchBrief
from . import scholar_work_prompts as prompts


class ScholarWorkGenerator:
    """Multi-agent generator class for creating stories about a scholar's major work."""
    
    def __init__(self, model_name: str = "ollama/gemma3", temperature: float = 0.7):
        """Initialize the generator with specified model configuration."""
        self.model_name = model_name
        self.model_config = ModelConfig(model=model_name, temperature=temperature)
        self.client = LiteClient(model_config=self.model_config)
    
    def generate_text(self, scholar_name: str, major_contribution: str = "their most significant work", progress_callback: Optional[Callable[[int, str], None]] = None) -> ScholarMajorWork:
        """Execute the 3-agent pipeline to generate a high-quality story.

        Args:
            scholar_name: The name of the scholar.
            major_contribution: The name of the major work or breakthrough.
            progress_callback: Optional callback receiving (step_number, message).

        Returns:
            ScholarMajorWork: The final polished output.
        """
        
        # --- AGENT 1: THE RESEARCHER ---
        if progress_callback:
            progress_callback(1, f"Conducting deep research on {scholar_name}'s work...")
        brief: ResearchBrief = self.client.generate_text(
            model_input=prompts.get_researcher_input(scholar_name, major_contribution)
        )

        # --- AGENT 2: THE JOURNALIST ---
        if progress_callback:
            progress_callback(2, "Writing the narrative profile...")
        story_text: str = self.client.generate_text(
            model_input=prompts.get_journalist_input(brief)
        )

        # --- AGENT 3: THE EDITOR ---
        if progress_callback:
            progress_callback(3, "Finalizing and packaging the story...")
        final_story: ScholarMajorWork = self.client.generate_text(
            model_input=prompts.get_editor_input(scholar_name, major_contribution, story_text)
        )

        return final_story
    
    def update_model(self, model_name: str, temperature: float = 0.7) -> None:
        """Update the model configuration."""
        self.model_name = model_name
        self.model_config = ModelConfig(model=model_name, temperature=temperature)
        self.client = LiteClient(model_config=self.model_config)

    def get_model_info(self) -> dict:
        """Get information about the current model configuration.
        
        Returns:
            dict: Dictionary containing model information
        """
        return {
            "model_name": self.model_name,
            "temperature": self.model_config.temperature
        }
