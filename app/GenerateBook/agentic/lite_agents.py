"""
liteagents.py - Unified LiteClient-based agents for GenerateBook.
"""

from app.GenerateBook.shared.models import BookInput, BookChapters, ModelOutput
from app.GenerateBook.shared.prompts import PromptBuilder
from app.GenerateBook.shared.utils import (
    save_model_response,
    extract_text_from_response,
)
from bookchapters_generator import BookChaptersGenerator
from bookchapters_models import BookInput as BookInputDSPy
from dspy.teleprompt import BootstrapFewShot
from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from pathlib import Path
from typing import Any, List, Optional
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_or_init_client():
    """Initialize or load existing LiteClient configuration."""
    config_path = Path("generatebook_client_config.json")

    if config_path.exists():
        with open(config_path, "r") as f:
            config_data = json.load(f)
            return LiteClient(
                model_name=config_data.get("model_name", "gemma3:4b"),
                base_url=config_data.get("base_url", "http://localhost:11434"),
            )
    else:
        client = LiteClient(model_name="gemma3:4b")
        config_data = {
            "model_name": client.model_name,
            "base_url": client.base_url,
        }
        with open(config_path, "w") as f:
            json.dump(config_data, f)
        return client


def create_optimization_examples(generator: BookChaptersGenerator) -> List[Any]:
    """Create a small set of optimization examples."""
    examples = []

    return examples


def optimize_generator():
    """Optimize the generator using DSPy."""
    generator = BookChaptersGenerator()

    examples = create_optimization_examples(generator)

    if not examples:
        print("No optimization examples found. Skipping optimization.")
        return

    teleprompter = BootstrapFewShot(metric=generated_chapters_metric)
    optimized_generator = teleprompter.compile(generator, trainset=examples)

    print("\nOptimization scripts created for BookInput validation.")
    print("For optimizing actual chapter generation, you would:")
    print("1. Collect examples of good chapter suggestions from the generator")
    print("2. Train on those examples using the generated_chapters_metric")
    print("3. Use the optimized generator to produce better educational content")

    return optimized_generator


class GenerateBookLiteAgent:
    """LiteClient-based agent for generating educational book chapters."""

    def __init__(
        self, model_name: str = "gemma3:4b", base_url: str = "http://localhost:11434"
    ):
        self.client = LiteClient(model_name=model_name, base_url=base_url)
        self.prompt_builder = PromptBuilder()

    def generate_book(
        self, subject: str, level: Optional[str] = None, num_chapters: int = 12
    ) -> ModelOutput:
        """Generate a complete book with educational chapters on the given subject."""
        prompt = self.prompt_builder.build_chapters_prompt(subject, level, num_chapters)

        response = self.client.generate(prompt)

        data = extract_text_from_response(response)

        markdown = f"# {subject}\n\n"
        markdown += f"## Chapters ({num_chapters})\n\n"
        markdown += data

        return ModelOutput(
            data={"subject": subject, "level": level, "chapters": data},
            markdown=markdown,
            metadata={"num_chapters": num_chapters},
        )

    def save_book(self, output: ModelOutput, filename: str = "generated_book.md"):
        """Save the generated book to a file."""
        save_model_response(output, filename)


__all__ = [
    "GenerateBookLiteAgent",
    "load_or_init_client",
    "optimize_generator",
    "ModelOutput",
]
