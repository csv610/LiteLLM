"""Medical Myths Checker - Comprehensive analysis of medical myths and claims."""

import json
import sys
import argparse
from pathlib import Path
from typing import Optional, List, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response
from utils.output_formatter import print_result

from medical_myths_checker_models import MythAnalysisResponse


class PromptBuilder:
    """Builder for constructing prompts for medical myth analysis."""

    @staticmethod
    def system_prompt() -> str:
        """Generate the system prompt for myth analysis."""
        return """You are a medical fact-checker with expertise in evidence-based medicine. Your task is to analyze medical claims/myths and provide an assessment grounded EXCLUSIVELY in peer-reviewed scientific evidence.

CRITICAL REQUIREMENTS:
1. ALL claims must be verified against peer-reviewed medical literature, clinical trials, and established medical guidelines
2. Only cite evidence from peer-reviewed journals, systematic reviews, meta-analyses, or official medical organizations (WHO, NIH, CDC, etc.)
3. If a claim cannot be supported by peer-reviewed evidence, mark it as FALSE or UNCERTAIN and explain what peer-reviewed research contradicts or is lacking
4. Include specific journal names, publication years, and authors when possible
5. Do NOT use general knowledge or anecdotal evidence - only evidence-based medicine"""

    @staticmethod
    def user_prompt(myth: str) -> str:
        """Generate the user prompt for myth analysis."""
        return f"""Medical Myth/Claim to Analyze: {myth}

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
}}"""


class MedicalMythsChecker:
    """Analyzes medical myths for factual accuracy based on peer-reviewed evidence."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the myths checker."""
        self.client = LiteClient(model_config=model_config)
        self.myth: Optional[str] = None

    def generate_text(self, myth: str, structured: bool = False) -> Union[MythAnalysisResponse, str]:
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

        response_format = None
        if structured:
            response_format = MythAnalysisResponse

        model_input = ModelInput(
            system_prompt=PromptBuilder.system_prompt(),
            user_prompt=PromptBuilder.user_prompt(myth),
            response_format=response_format,
        )

        result = self._ask_llm(model_input)
        return result

    def _ask_llm(self, model_input: ModelInput) -> Union[MythAnalysisResponse, str]:
        """
        Internal helper to call the LLM client.
        """
        return self.client.generate_text(model_input=model_input)

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
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")

    args = parser.parse_args()

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        checker = MedicalMythsChecker(model_config=model_config)
        print("Starting medical myth analysis...")
        result = checker.generate_text(myth=args.input, structured=args.structured)
        
        print_result(result, title="Medical Myth Analysis")
        
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
