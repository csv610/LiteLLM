import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, Union


sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.config import ModelConfig
from lite.logging_config import configure_logging

from drug_food_interaction import DrugFoodInteraction
from drug_food_interaction_models import DrugFoodInteractionModel, ModelOutput
from drug_food_interaction_prompts import PromptBuilder, DrugFoodInput

logger = logging.getLogger(__name__)


def get_user_arguments():
    """Create and configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Drug-Food Interaction Checker - Analyze interactions between medicines and foods",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  python drug_food_interaction.py "Warfarin"
  python drug_food_interaction.py "Metformin" --age 65 --conditions "kidney disease"
  python drug_food_interaction.py "Simvastatin" --verbose
"""
    )

    parser.add_argument("medicine_name", type=str, help="Name of the medicine to analyze")
    parser.add_argument("--diet-type", type=str, default=None, help="Patient's diet type")
    parser.add_argument("--age", "-a", type=int, default=None, help="Patient's age in years (0-150)")
    parser.add_argument("--conditions", "-c", type=str, default=None, help="Patient's medical conditions")
    parser.add_argument("--prompt-style", "-p", type=str, choices=["detailed", "concise", "balanced"], default="detailed", help="Prompt style")
    parser.add_argument("--no-schema", action="store_true", help="Disable schema-based prompt generation")
    parser.add_argument("--verbosity", "-v", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Logging verbosity level")
    parser.add_argument("--model", "-m", type=str, default="ollama/gemma3", help="Model ID")
    parser.add_argument("--json-output", action="store_true", help="Output results as JSON to stdout")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")
    parser.add_argument("-d", "--output-dir", default="outputs", help="Directory for output files (default: outputs).")

    return parser.parse_args()


def main() -> int:
    """Main entry point for the drug-food interaction CLI."""
    args = get_user_arguments()

    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "drug_food_interaction.log"),
        verbosity=args.verbosity,
        enable_console=True
    )

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        config = DrugFoodInput(
            medicine_name=args.medicine_name,
            diet_type=args.diet_type,
            medical_conditions=args.conditions,
            age=args.age,
            specific_food=None,
            prompt_style=args.prompt_style,
        )
        
        # Validate the input
        config.validate()

        logger.info(f"Configuration created successfully")

        model_config = ModelConfig(model=args.model, temperature=0.2)
        analyzer = DrugFoodInteraction(model_config)
        result = analyzer.generate_text(config, structured=args.structured)
        
        if result is None:
            logger.error("✗ Failed to generate drug-food interaction information.")
            return 1

        # Save result to output directory
        analyzer.save(result, output_dir)

        logger.debug("✓ Drug-food interaction generation completed successfully")
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
