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
from lite.utils import save_model_response

from drug_food_interaction_models import DrugFoodInteractionModel, ModelOutput

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

    @classmethod
    def create_user_prompt(cls, config: DrugFoodInput) -> str:
        """
        Create the user prompt for drug-food interaction analysis.

        Args:
            config: Configuration containing the medicine and patient information

        Returns:
            str: Formatted user prompt with context
        """
        context = cls._build_context(config)
        return f"{config.medicine_name} food and beverage interactions analysis. {context}"
    
    @staticmethod
    def _build_context(config: DrugFoodInput) -> str:
        """Build the analysis context string from input parameters.
        
        Args:
            config: Configuration containing the medicine and patient information
            
        Returns:
            str: Formatted context string
        """
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


@dataclass
class DrugFoodInput:
    """Configuration and input for drug-food interaction analysis."""
    medicine_name: str
    diet_type: Optional[str] = None
    medical_conditions: Optional[str] = None
    age: Optional[int] = None
    specific_food: Optional[str] = None
    prompt_style: str = "detailed"
    
    def validate(self) -> None:
        """Validate the input parameters.
        
        Raises:
            ValueError: If any parameter is invalid
        """
        if not self.medicine_name or not self.medicine_name.strip():
            raise ValueError("Medicine name cannot be empty or just whitespace")
        
        if self.age is not None and (self.age < 0 or self.age > 150):
            raise ValueError("Age must be between 0 and 150 years")

class DrugFoodInteraction:
    """Analyzes drug-food interactions based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def generate_text(self, config: DrugFoodInput, structured: bool = False) -> ModelOutput:
        """Analyzes how food and beverages interact with a medicine."""
        logger.debug(f"Starting drug-food interaction analysis")
        logger.debug(f"Medicine: {config.medicine_name}")

        # Create user prompt with context
        user_prompt = PromptBuilder.create_user_prompt(config)
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=user_prompt,
            response_format=DrugFoodInteractionModel if structured else None,
        )
        result = self._ask_llm(model_input)

        logger.debug(f"✓ Successfully analyzed food interactions")
        return result




    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
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
    parser.add_argument("-o", "--output", type=str, help="Output file path (default: auto-generated)")

    return parser.parse_args()


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
        
        # Validate the input
        config.validate()

        logger.info(f"Configuration created successfully")

        model_config = ModelConfig(model=args.model, temperature=0.2)
        analyzer = DrugFoodInteraction(model_config)
        result = analyzer.generate_text(config, structured=args.structured)

        # Save result to file if output path is specified
        if args.output:
            output_path = Path(args.output)
            save_model_response(result, output_path)
            logger.info(f"Result saved to: {output_path}")
        elif not args.json_output:
            # If no output file and not json output, print a summary
            print(f"\n✓ Drug-food interaction analysis completed for {config.medicine_name}")
            print(f"Use --output to save results to a file or --json-output to see the full result")

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
    main()
