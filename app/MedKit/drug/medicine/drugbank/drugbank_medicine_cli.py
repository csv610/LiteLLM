import argparse
import logging
import re
from pathlib import Path
from typing import Optional, Union

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response

from drugbank_medicine_models import MedicineInfo
from drugbank_medicine import DrugBankMedicine

logger = logging.getLogger(__name__)


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

def create_drugbank_medicine_report(args):

    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "drugbank_medicine.log"),
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
        
        print(f"\n✓ Medicine information saved to: {output_filename}")

        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    args = get_user_arguments()
    create_drugbank_medicine_report(args)

