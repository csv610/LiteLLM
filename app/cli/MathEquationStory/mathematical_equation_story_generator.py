"""
mathematical_equation_story_generator.py - Generator class for mathematical equation stories

Provides the main generation logic for creating narrative-driven explanations
of mathematical equations using LiteLLM models.
"""

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from mathematical_equation_story_models import MathematicalEquationStory
from mathematical_equation_story_prompts import PromptBuilder


class MathEquationStoryGenerator:
    """Generator class for creating mathematical equation stories."""
    
    def __init__(self, model_name: str = "ollama/gemma3", temperature: float = 0.7):
        """Initialize the story generator with specified model configuration.
        
        Args:
            model_name: The name of the model to use for generation
            temperature: The temperature setting for the model (0.0-1.0)
        """
        self.model_name = model_name
        self.model_config = ModelConfig(model=model_name, temperature=temperature)
        self.client = LiteClient(model_config=self.model_config)
    
    def generate_story(self, equation_name: str) -> MathematicalEquationStory:
        """Generate a narrative-driven explanation of a mathematical equation.

        This function creates a detailed prompt that instructs the AI model to
        write a compelling story about the specified equation, in the style of a
        popular science magazine. The story is designed to be accessible to a
        general audience and to convey the beauty and importance of the mathematics.

        Args:
            equation_name: The name of the equation to be explained (e.g.,
                          "Pythagorean Theorem", "E=mc²").

        Returns:
            MathematicalEquationStory: A Pydantic model containing the generated
                                       story and supporting materials.
        """
        # Create prompts using PromptBuilder
        prompt_data = PromptBuilder.create_model_input(equation_name)

        # Prepare input with response schema
        model_input = ModelInput(
            user_prompt=prompt_data["user_prompt"],
            system_prompt=prompt_data["system_prompt"],
            response_format=prompt_data["response_format"]
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
            "temperature": self.model_config.temperature
        }
