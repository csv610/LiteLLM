"""
scholar_work_generator.py - Generator class for scholar major works

Provides the main generation logic for creating narrative-driven explanations
of major scientific work done by a given scientist using LiteLLM models.
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

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from app.ScholarWork.nonagentic.scholar_work_models import ScholarMajorWork
from app.ScholarWork.nonagentic.scholar_work_prompts import PromptBuilder


class ScholarWorkGenerator:
    """Generator class for creating narrative stories about scholar work."""

    def __init__(self, model_name: str = "ollama/gemma3", temperature: float = 0.7):
        """Initialize the generator with specified model configuration.

        Args:
            model_name: The name of the model to use for generation
            temperature: The temperature setting for the model (0.0-1.0)
        """
        self.model_name = model_name
        self.model_config = ModelConfig(model=model_name, temperature=temperature)
        self.client = LiteClient(model_config=self.model_config)

    def generate_text(
        self, scholar_name: str, major_contribution: str = "their most significant work"
    ) -> ScholarMajorWork:
        """Generate a narrative-driven explanation of a scientist's work.

        Args:
            scholar_name: The name of the scholar to be described
            major_contribution: The specific scientific breakthrough or theory

        Returns:
            ScholarMajorWork: A Pydantic model containing the generated story and materials.
        """
        # Create prompts using PromptBuilder
        prompt_data = PromptBuilder.create_model_input(scholar_name, major_contribution)

        # Prepare input with response schema
        model_input = ModelInput(
            user_prompt=prompt_data["user_prompt"],
            system_prompt=prompt_data["system_prompt"],
            response_format=prompt_data["response_format"],
        )

        # Generate structured response
        response = self.client.generate_text(model_input=model_input)

        return response

    def update_model(self, model_name: str, temperature: float = 0.7) -> None:
        """Update the model configuration.

        Args:
            model_name: The new model name to use
            temperature: The new temperature setting
        """
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
            "temperature": self.model_config.temperature,
        }
