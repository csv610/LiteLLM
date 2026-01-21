"""Medical Facts Checker - Comprehensive fact vs. fiction analysis with confidence scoring."""

import json
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from medical_facts_checker_models import FactFictionAnalysis

class MedicalFactsChecker:
    """Analyzes medical statements for factual accuracy."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the facts checker."""
        self.client = LiteClient(model_config=model_config)
        self.statement: Optional[str] = None
        self.output_path: Optional[Path] = None

    def generate_text(self, statement: str) -> FactFictionAnalysis:
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

        model_input = ModelInput(
            user_prompt=self._create_prompt(statement),
            response_format=FactFictionAnalysis,
        )

        result = self._ask_llm(model_input)
        return result

    def _ask_llm(self, model_input: ModelInput) -> FactFictionAnalysis:
        """
        Internal helper to call the LLM client.
        """
        return self.client.generate_text(model_input=model_input)

    def _create_prompt(self, statement: str) -> str:
        """Generate the prompt for fact checking."""
        return f"Analyze the following statement and determine if it is a fact or fiction: {statement}"

    def print_result(self, analysis: FactFictionAnalysis) -> None:
        """
        Print a summary of the analysis using rich.
        """
        from rich.console import Console
        from rich.panel import Panel
        
        console = Console()
        
        console.print(Panel(
            f"[bold]Statement:[/bold] {analysis.detailed_analysis.statement_analysis.statement}\n"
            f"[bold]Classification:[/bold] {analysis.detailed_analysis.statement_analysis.classification}\n"
            f"[bold]Confidence:[/bold] {analysis.detailed_analysis.statement_analysis.confidence_level} ({analysis.detailed_analysis.statement_analysis.confidence_percentage}%)\n\n"
            f"[bold]Explanation:[/bold] {analysis.detailed_analysis.explanation}",
            title="Fact Check Results",
            border_style="cyan"
        ))


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
    parser.add_argument("-m", "--model", default="gemini-1.5-pro", help="Model to use (default: gemini-1.5-pro)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level")

    args = parser.parse_args()

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        checker = MedicalFactsChecker(model_config=model_config)
        print("Starting evaluation...")
        result = checker.generate_text(statement=args.statement)
        
        checker.print_result(result)
        
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, 'w') as f:
                json.dump(result.model_dump(), f, indent=2)
            print(f"✓ JSON evaluation saved to {args.output}")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
   main()
