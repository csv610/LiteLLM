"""Medical Facts Checker - Comprehensive fact vs. fiction analysis with confidence scoring."""

import json
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

from medical_facts_checker_models import MedicalFactFictionAnalysisModel, ModelOutput

class MedicalFactsChecker:
    """Analyzes medical statements for factual accuracy."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the facts checker."""
        self.client = LiteClient(model_config=model_config)
        self.statement: Optional[str] = None
        self.output_path: Optional[Path] = None

    def generate_text(self, statement: str, structured: bool = False) -> ModelOutput:
        """
        Analyze a statement and determine if it is a fact or fiction.

        Args:
            statement: The statement to analyze.

        Returns:
            The generated FactFictionAnalysis object.
        
        Raises:
            ValueError: If statement is empty.
        """
        if not statement or not statement.strip():
            raise ValueError("Statement cannot be empty")

        self.statement = statement

        response_format = None
        if structured:
            response_format = MedicalFactFictionAnalysisModel

        model_input = ModelInput(
            user_prompt=f"Analyze the following statement and determine if it is a fact or fiction: {statement}",
            response_format=response_format,
        )

        result = self._ask_llm(model_input)
        return result

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """
        Internal helper to call the LLM client.
        """
        return self.client.generate_text(model_input=model_input)

    

def main():
    parser = argparse.ArgumentParser(
        description="Analyze statements and determine if they are fact or fiction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default output to console
  python medical_facts_checker.py -i "The Earth is round"

  # Custom output path
  python medical_facts_checker.py -i "Gravity causes objects to fall" -o gravity_analysis.json
        """
    )
    parser.add_argument("-i", "--statement", required=True, help="Statement to analyze")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use (default: gemini-1.5-pro)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")

    args = parser.parse_args()

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        checker = MedicalFactsChecker(model_config=model_config)
        print("Starting evaluation...")
        result = checker.generate_text(statement=args.statement, structured=args.structured)
        print (result)
        
        if args.output:
            output_dir = Path("output")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / args.output.name

            if isinstance(result, str) and output_path.suffix == ".json":
                output_path = output_path.with_suffix(".md")
            save_model_response(result, output_path)
            print(f"✓ Results saved to {output_path}")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
   main()
