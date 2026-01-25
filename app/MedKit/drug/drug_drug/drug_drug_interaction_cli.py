import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, List, Union

from pydantic import BaseModel, Field, field_validator, model_validator

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from utils.output_formatter import print_result

from drug_drug_interaction_models import DrugInteractionResult

logger = logging.getLogger(__name__)


class PromptBuilder:
    """Builder class for creating prompts for drug-drug interaction analysis."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for drug-drug interaction analysis.

        Returns:
            str: System prompt defining the AI's role and instructions
        """
        return """You are a clinical pharmacology expert specializing in drug-drug interactions. Your role is to analyze how medications interact with each other, affecting their efficacy, safety, and metabolism.

When analyzing drug-drug interactions, you must:

1. Identify potential pharmacokinetic interactions (absorption, distribution, metabolism, excretion)
2. Identify potential pharmacodynamic interactions (additive, synergistic, or antagonistic effects)
3. Assess the severity and clinical significance of each interaction
4. Explain the mechanism of interaction clearly
5. Evaluate the risk level and potential adverse effects
6. Provide specific management recommendations and monitoring parameters
7. Consider patient-specific factors such as age, dosage, and medical conditions
8. Base analysis on established medical literature, clinical guidelines, and drug interaction databases

Always prioritize patient safety while providing practical, evidence-based guidance for medication management."""

    @staticmethod
    def create_user_prompt(medicine1: str, medicine2: str, context: str) -> str:
        """
        Create the user prompt for drug-drug interaction analysis.

        Args:
            medicine1: The name of the first medicine
            medicine2: The name of the second medicine
            context: Additional context for the analysis

        Returns:
            str: Formatted user prompt
        """
        return f"{medicine1} and {medicine2} interaction analysis. {context}"


class DrugDrugInput(BaseModel):
    """Configuration and input for drug-drug interaction analysis."""
    medicine1: str = Field(..., min_length=1, description="Name of the first medicine")
    medicine2: str = Field(..., min_length=1, description="Name of the second medicine")
    age: Optional[int] = Field(None, ge=0, le=150, description="Patient age (0-150)")
    dosage1: Optional[str] = None
    dosage2: Optional[str] = None
    medical_conditions: Optional[str] = None
    prompt_style: str = "detailed"

    @field_validator("medicine1", "medicine2")
    @classmethod
    def validate_medicine_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Medicine name cannot be empty or just whitespace")
        return v.strip()

class DrugDrugInteraction:
    """Analyzes drug-drug interactions based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def generate_text(self, config: DrugDrugInput, structured: bool = False) -> Union[DrugInteractionResult, str]:
        """Analyzes how two drugs interact."""

        logger.debug(f"Starting drug-drug interaction analysis")
        logger.debug(f"Drug 1: {config.medicine1}")
        logger.debug(f"Drug 2: {config.medicine2}")

        context = self._prepare_context(config)
        logger.debug(f"Context: {context}")

        user_prompt = PromptBuilder.create_user_prompt(config.medicine1, config.medicine2, context)
        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=user_prompt,
            response_format=DrugInteractionResult if structured else None,
        )
        result = self._ask_llm(model_input)

        logger.debug(f"✓ Successfully analyzed interaction")
        return result



    def _prepare_context(self, config: DrugDrugInput) -> str:
        """Build the analysis context string from input parameters."""
        context_parts = [f"Checking interaction between {config.medicine1} and {config.medicine2}"]
        
        if config.age is not None:
            context_parts.append(f"Patient age: {config.age} years")
        if config.dosage1:
            context_parts.append(f"{config.medicine1} dosage: {config.dosage1}")
        if config.dosage2:
            context_parts.append(f"{config.medicine2} dosage: {config.dosage2}")
        if config.medical_conditions:
            context_parts.append(f"Patient conditions: {config.medical_conditions}")

        return ". ".join(context_parts) + "."



    def _ask_llm(self, model_input: ModelInput) -> Union[DrugInteractionResult, str]:
        """Helper to call LiteClient with error handling."""
        logger.debug("Calling LiteClient.generate_text()...")
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during drug interaction analysis: {e}")
            logger.exception("Full exception details:")
            raise

    def save(self, result: Union[DrugInteractionResult, str], output_path: Path) -> Path:
        """Saves the interaction analysis to a JSON or MD file."""
        from lite.utils import save_model_response
        if isinstance(result, str) and output_path.suffix == ".json":
            output_path = output_path.with_suffix(".md")
        return save_model_response(result, output_path)

def get_user_arguments():
    """Create and configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Drug-Drug Interaction Analyzer - Check interactions between two medicines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=\"\"\"
Examples:
  python drug_drug_interaction.py "Warfarin" "Aspirin"
  python drug_drug_interaction.py "Metformin" "Lisinopril" --age 65 --dosage1 "500mg twice daily"
  python drug_drug_interaction.py "Simvastatin" "Clarithromycin" --prompt-style detailed --verbose
        \"\"\",
    )

    parser.add_argument("medicine1", type=str, help="Name of the first medicine")
    parser.add_argument("medicine2", type=str, help="Name of the second medicine")
    parser.add_argument("--age", "-a", type=int, default=None, help="Patient's age in years (0-150)")
    parser.add_argument("--dosage1", "-d1", type=str, default=None, help="Dosage information for first medicine")
    parser.add_argument("--dosage2", "-d2", type=str, default=None, help="Dosage information for second medicine")
    parser.add_argument("--conditions", "-c", type=str, default=None, help="Patient's medical conditions (comma-separated)")
    parser.add_argument("--prompt-style", "-p", type=str, choices=["detailed", "concise", "balanced"], default="detailed", help="Prompt style for analysis (default: detailed)")
    parser.add_argument("--json-output", "-j", action="store_true", default=False, help="Output results as JSON to stdout")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")

    return parser.parse_args()

def app_cli():
    """Main entry point for the drug-drug interaction CLI."""
    args = get_user_arguments()

    configure_logging(
        log_file="drug_drug_interaction.log",
        verbosity=args.verbosity,
        enable_console=True
    )

    try:
        config = DrugDrugInput(
            medicine1=args.medicine1,
            medicine2=args.medicine2,
            age=args.age,
            dosage1=args.dosage1,
            dosage2=args.dosage2,
            medical_conditions=args.conditions,
            prompt_style=args.prompt_style,
        )

        logger.info(f"Configuration created successfully")

        model_config = ModelConfig(model=args.model, temperature=0.7)
        analyzer = DrugDrugInteraction(model_config)
        result = analyzer.generate_text(config, structured=args.structured)
        
        if result is None:
            logger.error("✗ Failed to analyze interaction.")
            sys.exit(1)

        # Display formatted result
        print_result(result, title="Drug Interaction Analysis")

        if args.json_output:
            if isinstance(result, str):
                print(f"\n{result}")
            else:
                print(f"\n{result.model_dump_json(indent=2)}")

        # Save result
        output_dir = Path("outputs")
        output_dir.mkdir(parents=True, exist_ok=True)
        default_path = output_dir / f"{args.medicine1.lower()}_{args.medicine2.lower()}_interaction.json"
        analyzer.save(result, default_path)

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
    sys.exit(app_cli())
