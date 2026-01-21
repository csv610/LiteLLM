"""Medical Myths Checker - Comprehensive analysis of medical myths and claims."""

import json
import sys
import argparse
from pathlib import Path
from typing import Optional, List

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from medical_myths_checker_models import MythAnalysisResponse

class MedicalMythsChecker:
    """Analyzes medical myths for factual accuracy based on peer-reviewed evidence."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the myths checker."""
        self.client = LiteClient(model_config=model_config)
        self.myth: Optional[str] = None

    def generate_text(self, myth: str) -> MythAnalysisResponse:
        """
        Analyze a medical myth and determine its status.

        Args:
            myth: The myth/claim to analyze.

        Returns:
            The generated MythAnalysisResponse object.
        
        Raises:
            ValueError: If myth is empty.
        """
        if not myth or not myth.strip():
            raise ValueError("Myth statement cannot be empty")

        self.myth = myth

        model_input = ModelInput(
            user_prompt=self._create_prompt(myth),
            response_format=MythAnalysisResponse,
        )

        result = self._ask_llm(model_input)
        return result

    def _ask_llm(self, model_input: ModelInput) -> MythAnalysisResponse:
        """
        Internal helper to call the LLM client.
        """
        return self.client.generate_text(model_input=model_input)

    def _create_prompt(self, myth: str) -> str:
        """Generate the prompt for myth analysis."""
        return f"""You are a medical fact-checker with expertise in evidence-based medicine. Your task is to analyze the following medical claim/myth and provide an assessment grounded EXCLUSIVELY in peer-reviewed scientific evidence.

CRITICAL REQUIREMENTS:
1. ALL claims must be verified against peer-reviewed medical literature, clinical trials, and established medical guidelines
2. Only cite evidence from peer-reviewed journals, systematic reviews, meta-analyses, or official medical organizations (WHO, NIH, CDC, etc.)
3. If a claim cannot be supported by peer-reviewed evidence, mark it as FALSE or UNCERTAIN and explain what peer-reviewed research contradicts or is lacking
4. Include specific journal names, publication years, and authors when possible
5. Do NOT use general knowledge or anecdotal evidence - only evidence-based medicine

Medical Myth/Claim to Analyze: {myth}

Respond ONLY with valid JSON in this exact format:
{{
    "myths": [
        {{
            "statement": "exact claim from the input",
            "status": "TRUE or FALSE or UNCERTAIN",
            "explanation": "detailed medical explanation grounded in peer-reviewed evidence",
            "peer_reviewed_sources": "Specific citations: Journal names, publication years, and research findings. Or: 'No peer-reviewed evidence found' with explanation of research gaps",
            "risk_level": "LOW or MODERATE or HIGH"
        }}
    ]
}}
"""

    def print_result(self, response: MythAnalysisResponse) -> None:
        """
        Print a summary of the analysis using rich.
        """
        from rich.console import Console
        from rich.panel import Panel
        
        console = Console()
        
        for myth in response.myths:
            console.print(Panel(
                f"[bold]Claim:[/bold] {myth.statement}\n"
                f"[bold]Status:[/bold] {myth.status}\n"
                f"[bold]Risk Level:[/bold] {myth.risk_level}\n\n"
                f"[bold]Explanation:[/bold] {myth.explanation}\n\n"
                f"[bold]Sources:[/bold] {myth.peer_reviewed_sources}",
                title="Medical Myth Analysis",
                border_style="magenta"
            ))


def main():
    parser = argparse.ArgumentParser(
        description="Analyze medical myths and provide evidence-based assessments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_myths_checker.py -i "Vitamin C prevents the common cold"
  python medical_myths_checker.py -i "Cracking knuckles causes arthritis" -o arthritis_myth.json
        """
    )
    parser.add_argument("-i", "--input", required=True, help="Medical myth/claim to analyze")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-m", "--model", default="gemini-1.5-pro", help="Model to use (default: gemini-1.5-pro)")

    args = parser.parse_args()

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        checker = MedicalMythsChecker(model_config=model_config)
        print("Starting medical myth analysis...")
        result = checker.generate_text(myth=args.input)
        
        checker.print_result(result)
        
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
