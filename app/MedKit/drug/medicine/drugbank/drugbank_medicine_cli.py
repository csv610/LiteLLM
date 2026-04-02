import argparse
import logging
import re
from pathlib import Path

try:
    from .drugbank_medicine import DrugBankMedicine
except ImportError:
    from drugbank_medicine import DrugBankMedicine
from lite.config import ModelConfig
from lite.logging_config import configure_logging
from lite.utils import save_model_response

logger = logging.getLogger(__name__)


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal and invalid characters."""
    sanitized = re.sub(r'[<>:"/\\|?*]', "", filename)
    sanitized = re.sub(r"\s+", "_", sanitized)
    sanitized = sanitized.strip(". ")
    return sanitized if sanitized else "medicine"


def get_user_arguments():
    """Create and configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Fetch comprehensive medicine information (pharmacology, safety, interactions, regulatory data).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("medicine", help="Medicine name (e.g., 'Aspirin', 'Ibuprofen')")
    parser.add_argument(
        "-m",
        "--model",
        default="ollama/gemma3",
        help="LLM model (default: ollama/gemma3)",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        default=0.2,
        help="Temperature (0-1, default: 0.2)",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Verbosity level",
    )
    parser.add_argument(
        "--json-output", action="store_true", help="Output results as JSON to stdout"
    )
    parser.add_argument(
        "-s",
        "--structured",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response.",
    )
    return parser.parse_args()


def cli(
    medicine: str,
    model: str = "ollama/gemma3",
    temperature: float = 0.2,
    verbosity: int = 2,
    structured: bool = False,
):
    """CLI entry point for testing and programmatic use."""

    class Args:
        pass

    args = Args()
    args.medicine = medicine
    args.model = model
    args.temperature = temperature
    args.verbosity = verbosity
    args.structured = structured
    args.json_output = (
        False  # Not used in create_drugbank_medicine_report but present in parser
    )

    return create_drugbank_medicine_report(args)


def create_drugbank_medicine_report(args):
    try:
        configure_logging(
            log_file=str(Path(__file__).parent / "logs" / "drugbank_medicine.log"),
            verbosity=args.verbosity,
            enable_console=True,
        )
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
