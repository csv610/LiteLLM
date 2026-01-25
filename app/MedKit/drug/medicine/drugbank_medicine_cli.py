import argparse
import logging
import re
import sys
from pathlib import Path
from typing import Optional, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response
from utils.output_formatter import print_result

from drugbank_medicine_models import MedicineInfo

logger = logging.getLogger(__name__)

class DrugBankMedicine:
    """Fetches comprehensive medicine information using LiteClient."""

    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def generate_text(self, medicine_name: str, structured: bool = False) -> Union[MedicineInfo, str]:
        """Fetch comprehensive medicine information (pharmacology, safety, etc.)."""
        if not medicine_name or not medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")

        logger.debug(f"Starting medicine information fetch for: {medicine_name}")

        user_prompt = f"Provide detailed information about the medicine {medicine_name}."
        model_input = ModelInput(
            user_prompt=user_prompt,
            response_format=MedicineInfo if structured else None,
        )
        result = self._ask_llm(model_input)

        logger.debug(f"✓ Successfully fetched info for {medicine_name}")
        return result



    def _ask_llm(self, model_input: ModelInput) -> Union[MedicineInfo, str]:
        """Helper to call LiteClient with error handling."""
        logger.debug("Calling LiteClient.generate_text()...")
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
        description="Fetch comprehensive medicine information (pharmacology, safety, interactions, regulatory data).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python drugbank_medicine.py "Aspirin"
  python drugbank_medicine.py "Metformin" -m "anthropic/claude-3-5-sonnet"
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
    """Main entry point for the DrugBank Medicine CLI."""
    args = get_user_arguments()

    configure_logging(
        log_file="drugbank_medicine.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=args.temperature)
        analyzer = DrugBankMedicine(model_config)
        result = analyzer.generate_text(args.medicine, structured=args.structured)

        # Handle saving to file
        sanitized_name = sanitize_filename(args.medicine).lower()
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        suffix = ".json"
        if isinstance(result, str):
            suffix = ".md"
        output_filename = output_dir / f"{sanitized_name}{suffix}"

        save_model_response(result, output_filename)
        
        print_result(result, title=f"Medicine Information: {args.medicine}")

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

