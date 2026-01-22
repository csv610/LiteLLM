"""medical_term_extractor.py - Extract and categorize medical concepts from text."""

import json
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

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

    def generate_text(self, text: str) -> MedicalTerms:
        """Extract medical terms from text."""
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty")

        model_input = ModelInput(
            user_prompt=PromptBuilder.create_user_prompt(text),
            response_format=MedicalTerms,
            system_prompt=PromptBuilder.create_system_prompt()
        )

        result = self._ask_llm(model_input)
        return result

    def _ask_llm(self, model_input: ModelInput) -> MedicalTerms:
        """Internal helper to call the LLM client."""
        return self.client.generate_text(model_input=model_input)

    def print_result(self, terms: MedicalTerms) -> None:
        """Print a summary of the extracted terms using rich."""
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table
        
        console = Console()
        console.print(Panel(
            "Medical concepts extracted successfully.",
            title="Medical Term Extraction Results",
            border_style="cyan"
        ))

        table = Table(title="Extraction Summary")
        table.add_column("Category", style="cyan")
        table.add_column("Count", justify="right", style="magenta")

        categories = {
            "Diseases": terms.diseases,
            "Medicines": terms.medicines,
            "Symptoms": terms.symptoms,
            "Treatments": terms.treatments,
            "Procedures": terms.procedures,
            "Specialties": terms.specialties,
            "Anatomical Terms": terms.anatomical_terms,
            "Side Effects": terms.side_effects,
            "Relationships": terms.causation_relationships,
        }

        for cat, items in categories.items():
            if items:
                table.add_row(cat, str(len(items)))

        console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Extract medical terms from text or a file.")
    parser.add_argument("input", help="The input text file path or a string of text.")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-m", "--model", default="gemini-1.5-pro", help="Model to use (default: gemini-1.5-pro)")

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
        result = extractor.generate_text(text=input_text)
        
        extractor.print_result(result)
        
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, 'w') as f:
                json.dump(result.model_dump(), f, indent=2)
            print(f"✓ Results saved to {args.output}")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
