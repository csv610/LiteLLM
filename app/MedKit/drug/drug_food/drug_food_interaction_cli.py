import argparse
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union


sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from utils.output_formatter import print_result

from drug_food_interaction_models import DrugFoodInteractionResult

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for drug-food interaction analysis."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for drug-food interaction analysis.

        Returns:
            str: System prompt defining the AI's role and instructions
        """
        return """You are a clinical pharmacology expert specializing in drug-food interactions. Your role is to analyze how foods and beverages affect drug absorption, metabolism, efficacy, and safety.

When analyzing drug-food interactions, you must:

1. Identify significant food interactions that affect drug absorption, distribution, metabolism, or excretion
2. Assess the severity and clinical significance of each interaction
3. Provide specific guidance on which foods to avoid and which are safe to consume
4. Explain the mechanism of interaction in clear terms
5. Recommend optimal timing for medication administration relative to meals
6. Highlight any special dietary considerations or restrictions
7. Base analysis on established medical literature and clinical guidelines

Always prioritize patient safety while providing practical, evidence-based guidance for optimal medication use."""

    @staticmethod
    def create_user_prompt(medicine_name: str, context: str) -> str:
        """
        Create the user prompt for drug-food interaction analysis.

        Args:
            medicine_name: The name of the medicine to analyze
            context: Additional context for the analysis

        Returns:
            str: Formatted user prompt
        """
        return f"{medicine_name} food and beverage interactions analysis. {context}"


@dataclass
class DrugFoodInput:
    """Configuration and input for drug-food interaction analysis."""
    medicine_name: str
    diet_type: Optional[str] = None
    medical_conditions: Optional[str] = None
    age: Optional[int] = None
    specific_food: Optional[str] = None
    prompt_style: str = "detailed"

class DrugFoodInteraction:
    """Analyzes drug-food interactions based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def generate_text(self, config: DrugFoodInput, structured: bool = False) -> Union[DrugFoodInteractionResult, str]:
        """Analyzes how food and beverages interact with a medicine."""
        self._validate_input(config)

        logger.debug(f"Starting drug-food interaction analysis")
        logger.debug(f"Medicine: {config.medicine_name}")

        context = self._prepare_context(config)
        logger.debug(f"Context: {context}")

        user_prompt = PromptBuilder.create_user_prompt(config.medicine_name, context)
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=user_prompt,
            response_format=DrugFoodInteractionResult if structured else None,
        )
        result = self._ask_llm(model_input)

        logger.debug(f"✓ Successfully analyzed food interactions")
        return result

    def _validate_input(self, config: DrugFoodInput) -> None:
        """Validate input parameters."""
        if not config.medicine_name or not config.medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if config.age is not None and (config.age < 0 or config.age > 150):
            raise ValueError("Age must be between 0 and 150 years")

    def _prepare_context(self, config: DrugFoodInput) -> str:
        """Build the analysis context string from input parameters."""
        context_parts = [f"Analyzing food interactions for {config.medicine_name}"]
        if config.specific_food:
            context_parts.append(f"Specific foods to check: {config.specific_food}")
        if config.diet_type:
            context_parts.append(f"Patient diet type: {config.diet_type}")
        if config.age is not None:
            context_parts.append(f"Patient age: {config.age} years")
        if config.medical_conditions:
            context_parts.append(f"Patient conditions: {config.medical_conditions}")
        return ". ".join(context_parts) + "."


    def _ask_llm(self, model_input: ModelInput) -> Union[DrugFoodInteractionResult, str]:
        """Helper to call LiteClient with error handling."""
        logger.debug("Calling LiteClient.generate_text()...")
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            logger.exception("Full exception details:")
            raise

def get_user_arguments():
    """Create and configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Drug-Food Interaction Checker - Analyze interactions between medicines and foods",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=\"\"\"
Examples:
  python drug_food_interaction.py "Warfarin"
  python drug_food_interaction.py "Metformin" --age 65 --conditions "kidney disease"
  python drug_food_interaction.py "Simvastatin" --verbose
        \"\"\",
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

    return parser.parse_args()


    # Save to file if output is needed (Wait, main doesn't have output arg, but let's check)
    # Actually main in this file doesn't have --output. Let's add it if missing or just handle JSON output.

def main() -> int:
    """Main entry point for the drug-food interaction CLI."""
    args = get_user_arguments()

    configure_logging(
        log_file="drug_food_interaction.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    try:
        config = DrugFoodInput(
            medicine_name=args.medicine_name,
            diet_type=args.diet_type,
            medical_conditions=args.conditions,
            age=args.age,
            specific_food=None,
            prompt_style=args.prompt_style,
        )

        logger.info(f"Configuration created successfully")

        model_config = ModelConfig(model=args.model, temperature=0.7)
        analyzer = DrugFoodInteraction(model_config)
        result = analyzer.generate_text(config, structured=args.structured)

        print_result(result, title="Drug-Food Interaction Analysis")

        if args.json_output:
            if isinstance(result, str):
                print(f"\n{result}")
            else:
                print(f"\n{result.model_dump_json(indent=2)}")

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
    sys.exit(main())
