import argparse
import logging
import re
import sys
import json
from pathlib import Path
from typing import Optional, Union

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response

from medicine_info_models import MedicineInfoResult

logger = logging.getLogger(__name__)

class MedicineInfoGenerator:
    """Fetches comprehensive medicine information using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def generate_text(self, medicine_name: str, structured: bool = False) -> Union[MedicineInfoResult, str]:
        """Fetch comprehensive medicine information (pharmacology, safety, etc.)."""
        if not medicine_name or not medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")

        logger.info("-" * 80)
        logger.info(f"Starting medicine information fetch for: {medicine_name}")

        user_prompt = f"Provide detailed information about the medicine {medicine_name}."
        model_input = ModelInput(
            user_prompt=user_prompt,
            response_format=MedicineInfoResult if structured else None,
        )
        result = self._ask_llm(model_input)

        logger.info(f"✓ Successfully fetched info for {medicine_name}")
        logger.info("-" * 80)
        return result

    def _create_prompt(self, medicine_name: str) -> str:
        """Create the user prompt for the LLM."""
        return f"Provide detailed information about the medicine {medicine_name}."

    def _create_model_input(self, user_prompt: str, structured: bool = False) -> ModelInput:
        """Create the ModelInput for the LiteClient."""
        response_format=None
        if structured:
            response_format = MedicineInfoResult
            
        return ModelInput(
            user_prompt=user_prompt,
            response_format=response_format,
        )

    def _ask_llm(self, model_input: ModelInput) -> Union[MedicineInfoResult, str]:
        """Helper to call LiteClient with error handling."""
        logger.info("Calling LiteClient.generate_text()...")
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during medicine info fetch: {e}")
            logger.exception("Full exception details:")
            raise

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal and invalid characters."""
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    sanitized = re.sub(r'\s+', '_', sanitized)
    sanitized = sanitized.strip('. ')
    return sanitized if sanitized else "medicine"

def get_user_arguments():
    """Create and configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Fetch comprehensive medicine information using AI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medicine_info.py "Ibuprofen"
  python medicine_info.py "Metformin" -m "anthropic/claude-3-5-sonnet"
        """,
    )
    parser.add_argument("medicine", help="Medicine name (e.g., 'Aspirin', 'Ibuprofen')")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="LLM model (default: ollama/gemma3)")
    parser.add_argument("-t", "--temperature", type=float, default=0.2, help="Temperature (0-1, default: 0.2)")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Verbosity level")
    parser.add_argument("--json-output", action="store_true", help="Output results as JSON to stdout")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")
    return parser.parse_args()

def main() -> int:
    """Main entry point for the Medicine Information CLI."""
    args = get_user_arguments()

    configure_logging(
        log_file="medicine_info.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=args.temperature)
        generator = MedicineInfoGenerator(model_config)
        result = generator.generate_text(args.medicine)

        # Handle saving to file
        sanitized_name = sanitize_filename(args.medicine).lower()
        output_dir = Path(__file__).parent / "outputs"
        output_dir.mkdir(exist_ok=True)
        suffix = ".json"
        if isinstance(result, str):
            suffix = ".md"
        output_filename = output_dir / f"{sanitized_name}{suffix}"

        save_model_response(result, output_filename)
        
        from rich.console import Console
        from rich.panel import Panel
        console = Console()
        if isinstance(result, str):
            console.print(Panel(result, title=f"Medicine Information: {args.medicine}", border_style="cyan"))
        else:
            # Basic display for structured result
            console.print(Panel(str(result.model_dump()), title=f"Medicine Information: {args.medicine}", border_style="cyan"))

        print(f"\n✓ Medicine information saved to: {output_filename}")

        if args.json_output:
            if isinstance(result, str):
                print(f"\n{result}")
            else:
                print(f"\n{result.model_dump_json(indent=2)}")

        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
