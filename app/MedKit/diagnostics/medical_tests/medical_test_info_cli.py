import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response
from utils.output_formatter import print_result
from medical_test_info_models import MedicalTestInfo

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for medical test information generation."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create a system prompt that defines the AI's role and guidelines.

        Returns:
            A system prompt string defining the AI's role as a medical information specialist.
        """
        system_prompt = """You are a medical information specialist with expertise in clinical laboratory testing and diagnostic procedures. Your role is to provide comprehensive, accurate, and evidence-based information about medical tests.

When generating medical test information, you must:

1. Provide scientifically accurate information based on current medical knowledge and standards
2. Use clear, professional medical terminology while remaining accessible
3. Include specific details about test procedures, methodologies, and interpretations
4. Cite appropriate reference ranges with units of measurement
5. Describe clinical significance and practical applications
6. Address patient preparation requirements and potential limitations
7. Maintain objectivity and avoid making diagnostic conclusions
8. Structure information logically and comprehensively

Remember: This information is for educational and reference purposes. Always emphasize that test results should be interpreted by qualified healthcare professionals in the context of the patient's clinical presentation."""
        return system_prompt

    @staticmethod
    def create_user_prompt(test_name: str) -> str:
        """
        Create a comprehensive prompt for generating medical test information.

        Args:
            test_name: The name of the medical test.

        Returns:
            A formatted prompt string for the AI model.
        """
        prompt = f"""Generate comprehensive medical test information for: {test_name}

Include detailed information about:
1. Test name and alternative names
2. Purpose and clinical use
3. Test indications and when it is ordered
4. Sample requirements and collection procedures
5. Test methodology and technology
6. Normal reference ranges and result interpretation
7. Preparatory requirements and restrictions
8. Risks, benefits, and limitations
9. Cost and availability information
10. Results interpretation and follow-up actions

Provide accurate, evidence-based medical test information."""
        return prompt


class MedicalTestInfoGenerator:
    """Generate comprehensive information for medical tests."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator.

        Args:
            model_config: ModelConfig object containing model settings.
        """
        self.model_config = model_config
        self.client = LiteClient(model_config)

    def generate_text(self, test_name: str, structured: bool = False) -> Union[MedicalTestInfo, str]:
        """
        Generate the core medical test information.

        Args:
            test_name: The name of the medical test.
            structured: Whether to use structured output mode (default: False)

        Returns:
            Union[MedicalTestInfo, str]: Validated evaluation results or raw string
        """
        logger.debug(f"Generating medical test information for: {test_name}")

        # Build prompts and create ModelInput
        system_prompt = PromptBuilder.create_system_prompt()
        prompt = PromptBuilder.create_user_prompt(test_name)

        response_format = None
        if structured:
           response_format = MedicalTestInfo

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=prompt,
            response_format=response_format
        )
        
        try:
            result = self.ask_llm(model_input)
            logger.debug(f"Successfully generated medical test information for: {test_name}")
            return result
        except Exception as e:
            logger.error(f"Error generating medical test information for {test_name}: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> Union[MedicalTestInfo, str]:
        """
        Call the LLM client to generate information.

        Args:
            model_input: ModelInput object.

        Returns:
            The generated results (MedicalTestInfo or str).
        """
        return self.client.generate_text(model_input=model_input)


    def save(self, result: Union[MedicalTestInfo, str], output_path: Path) -> Path:
        """Save the generated test information to a JSON or MD file."""
        if isinstance(result, str) and output_path.suffix == ".json":
            output_path = output_path.with_suffix(".md")
        return save_model_response(result, output_path)


def get_user_arguments() -> argparse.Namespace:
    """
    Create and configure the argument parser for the CLI.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate comprehensive information for a medical test."
    )
    parser.add_argument(
        "-i",
        "--test",
        type=str,
        required=True,
        help="The name of the medical test to generate information for."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Optional: The path to save the output JSON file."
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="ollama/gemma3", 
        help="Model to use for generation (default: gemini-1.5-flash)."
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        help="Logging verbosity level (0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG). Default: 2."
    )
    parser.add_argument(
        "-s", "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response."
    )
    return parser.parse_args()

def app_cli():
    """
    Main CLI entry point for the medical test information generator.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    args = get_user_arguments()

    # Apply logging configuration at the entry point
    configure_logging(
        log_file="medical_test_info.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = MedicalTestInfoGenerator(model_config=model_config)
        
        # Generate the test information
        result = generator.generate_text(args.test, structured=args.structured)

        # No raw print here, print_result will handle it if we want formatted output
        # result is always an object, so we use print_result
        print_result(result, title="Medical Test Information")
        
        # Save to file
        if args.output:
            output_path = Path(args.output)
        else:
            output_dir = Path("outputs")
            output_path = output_dir / f"{args.test.lower().replace(' ', '_')}_info.json"
        
        generator.save(result, output_path)

    except Exception as e:
        logger.error(f"CLI execution failed: {e}")

if __name__ == "__main__":
    app_cli()
