import argparse
import logging
from pathlib import Path
from typing import Optional, Union


from lite.config import ModelConfig
from lite.logging_config import configure_logging

from drug_addiction import DrugAddiction
from drug_addiction_models import DrugAddictionModel, ModelOutput
from drug_addiction_prompts import PromptBuilder, DrugAddictionInput

logger = logging.getLogger(__name__)


def get_user_arguments():
    """Create and configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Drug Addiction Risk Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("medicine_name", type=str, help="Name of the medicine or substance to analyze")
    parser.add_argument("--duration", "-d", type=str, default=None, help="Duration of use")
    parser.add_argument("--prompt-style", "-p", type=str, choices=["detailed", "concise", "balanced"], default="detailed", help="Prompt style")
    parser.add_argument("--verbosity", "-v", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Logging verbosity level")
    parser.add_argument("--model", "-m", type=str, default="ollama/gemma3", help="Model ID")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")
    parser.add_argument("-o", "--output-dir", default="outputs", help="Directory for output files (default: outputs).")

    return parser.parse_args()


def main() -> int:
    """Main entry point for the drug addiction analysis CLI."""
    args = get_user_arguments()

    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "drug_addiction.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        user_input = DrugAddictionInput(
            medicine_name=args.medicine_name,
            usage_duration=args.duration,
            prompt_style=args.prompt_style,
        )
        
        # Validate the input
        user_input.validate()

        logger.info(f"Configuration created successfully")

        model_config = ModelConfig(model=args.model, temperature=0.2)
        analyzer = DrugAddiction(model_config)
        result = analyzer.generate_text(user_input, structured=args.structured)
        
        if result is None:
            logger.error("✗ Failed to generate drug addiction analysis.")
            return 1

        # Save result to output directory
        analyzer.save(result, output_dir)

        logger.debug("✓ Drug addiction analysis completed successfully")
        return 0

    except ValueError as e:
        print(f"\n❌ Invalid input: {e}")
        logger.error(f"Invalid input: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full exception details:")
        return 1

if __name__ == "__main__":
    main()
