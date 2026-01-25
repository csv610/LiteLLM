"""medical_term_extractor.py - Extract and categorize medical concepts from text."""

import json
import sys
import argparse
from pathlib import Path
from typing import Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response
from utils.output_formatter import print_result

from medical_term_extractor_models import MedicalTerms


class PromptBuilder:
    """Builder class for creating prompts for medical term extraction."""

    @staticmethod
    def create_system_prompt() -> str:
        """Generate the system prompt for medical term extraction."""
        return "You are an expert medical documentation specialist. Extract medical terms accurately from the provided text."

    @staticmethod
    def create_user_prompt(text: str) -> str:
        """Generate the user prompt for term extraction."""
        return f"""Extract all medical terms from the following text and structure them according to the provided schema.

Text to extract from:
{text}

For each category:
- Extract only relevant terms that appear in the text
- Include the context (the sentence or phrase where it appears)
- For side_effects, include the related_medicine if mentioned
- For causation_relationships, identify connections between medical concepts (e.g., "disease X causes symptom Y")

Be thorough and accurate. Extract ALL medical terms found in the text."""


class MedicalTermExtractor:
    """Extracts and categorizes medical terms from text using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the extractor."""
        self.client = LiteClient(model_config=model_config)

    def generate_text(self, text: str, structured: bool = False) -> Union[MedicalTerms, str]:
        """Extract medical terms from text."""
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")

        response_format = None
        if structured:
            response_format = MedicalTerms

        model_input = ModelInput(
            user_prompt=PromptBuilder.create_user_prompt(text),
            response_format=response_format,
            system_prompt=PromptBuilder.create_system_prompt()
        )

        result = self._ask_llm(model_input)
        return result

    def _ask_llm(self, model_input: ModelInput) -> Union[MedicalTerms, str]:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)


def main():
    parser = argparse.ArgumentParser(description="Extract medical terms from text or a file.")
    parser.add_argument("input", help="The input text file path or a string of text.")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-m", "--model", default="gemini-1.5-pro", help="Model to use (default: gemini-1.5-pro)")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")

    args = parser.parse_args()

    try:
        model_config = ModelConfig(model=args.model, temperature=0.1)
        extractor = MedicalTermExtractor(model_config=model_config)
        
        input_text = args.input
        input_path = Path(args.input)
        if input_path.is_file():
            with open(input_path, 'r', encoding='utf-8') as f:
                input_text = f.read()

        print("Extracting medical terms...")
        result = extractor.generate_text(text=input_text, structured=args.structured)
        
        print_result(result, title="Medical Term Extraction Results")
        
        if args.output:
            output_path = args.output
            if isinstance(result, str) and output_path.suffix == ".json":
                output_path = output_path.with_suffix(".md")
            save_model_response(result, output_path)
            print(f"✓ Results saved to {output_path}")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
