import logging
import sys
from pathlib import Path
from typing import Union

from pydantic import BaseModel, Field, field_validator

# Ensure repository root is in path for imports
# Use .resolve() to get absolute paths to avoid issues with relative CWDs
_repo_root = Path(__file__).resolve().parent.parent.parent.parent.parent
_medkit_root = _repo_root / "app" / "MedKit"
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))
if str(_medkit_root) not in sys.path:
    sys.path.insert(0, str(_medkit_root))

from lite.config import ModelConfig, ModelInput
from utils.cli_base import BaseCLI, BaseGenerator, BasePromptBuilder
from drug_drug_interaction_models import DrugInteractionModel, ModelOutput

logger = logging.getLogger(__name__)


class DrugDrugPromptBuilder(BasePromptBuilder):
    """Builder class for creating prompts for drug-drug interaction analysis.

    Inherits from BasePromptBuilder and implements the abstract methods
    for domain-specific prompt creation.
    """

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for drug-drug interaction analysis.

        Returns:
            str: System prompt defining the AI's role and instructions
        """
        return (
            "You are a clinical pharmacology expert specializing in drug-drug "
            "interactions. Analyze how medications interact with each other, "
            "affecting their efficacy, safety, and metabolism.\n\n"
            "When analyzing drug-drug interactions, you must:\n\n"
            "1. Identify pharmacokinetic interactions (absorption, distribution, "
            "metabolism, excretion)\n"
            "2. Identify pharmacodynamic interactions (additive, synergistic, "
            "antagonistic effects)\n"
            "3. Assess the severity and clinical significance of each interaction\n"
            "4. Explain the mechanism of interaction clearly\n"
            "5. Evaluate the risk level and potential adverse effects\n"
            "6. Provide specific management recommendations and monitoring "
            "parameters\n"
            "7. Consider patient-specific factors such as age, dosage, and "
            "medical conditions\n"
            "8. Base analysis on established medical literature, clinical "
            "guidelines, and databases\n\n"
            "Always prioritize patient safety while providing practical, "
            "evidence-based guidance for medication management."
        )

    @classmethod
    def create_user_prompt(cls, config: 'DrugDrugInput') -> str:
        """Create the user prompt for drug-drug interaction analysis.

        Args:
            config: Configuration containing the drugs and patient information

        Returns:
            str: Formatted user prompt with context
        """
        context = cls._build_context(config)
        return f"{config.medicine1} and {config.medicine2} interaction analysis. {context}"
        
    @staticmethod
    def _build_context(config: 'DrugDrugInput') -> str:
        """Build the analysis context string from input parameters.
        
        Args:
            config: Configuration containing the drugs and patient information
            
        Returns:
            str: Formatted context string
        """
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


class DrugDrugInput(BaseModel):
    """Configuration and input for drug-drug interaction analysis."""
    medicine1: str = Field(..., min_length=1, description="Name of the first medicine")
    medicine2: str = Field(..., min_length=1, description="Name of the second medicine")
    age: int | None = Field(None, ge=0, le=150, description="Patient age (0-150)")
    dosage1: str | None = None
    dosage2: str | None = None
    medical_conditions: str | None = None
    prompt_style: str = "detailed"

    @field_validator("medicine1", "medicine2")
    @classmethod
    def validate_medicine_name(cls, v: str) -> str:
        """Validate that medicine names are not empty.

        Args:
            v: Medicine name to validate.

        Returns:
            str: Trimmed medicine name.

        Raises:
            ValueError: If medicine name is empty or just whitespace.
        """
        if not v.strip():
            msg = "Medicine name cannot be empty or just whitespace"
            raise ValueError(msg)
        return v.strip()


class DrugDrugInteractionGenerator(BaseGenerator):
    """Generates drug-drug interaction analysis.

    Inherits from BaseGenerator and provides domain-specific generation logic
    for analyzing interactions between two drugs.
    """

    def generate_text(self, config: DrugDrugInput, structured: bool = False) -> ModelOutput:
        """Generate drug-drug interaction analysis.

        Args:
            config: Configuration containing the drugs and patient information
            structured: Whether to use structured output

        Returns:
            Union[DrugInteractionResult, str]: Structured or plain text result
        """
        self.logger.debug(f"Starting drug-drug interaction analysis")
        self.logger.debug(f"Drug 1: {config.medicine1}")
        self.logger.debug(f"Drug 2: {config.medicine2}")

        # Create user prompt with context
        user_prompt = DrugDrugPromptBuilder.create_user_prompt(config)
        model_input = ModelInput(
            system_prompt=DrugDrugPromptBuilder.create_system_prompt(),
            user_prompt=user_prompt,
            response_format=DrugInteractionResult if structured else None,
        )

        result = self._ask_llm(model_input)
        self.logger.debug(f"✓ Successfully analyzed interaction")
        return result



class DrugDrugInteractionCLI(BaseCLI):
    """CLI for drug-drug interaction analysis.
    
    Handles command-line interface for analyzing drug-drug interactions.
    This reduces boilerplate from ~230 to ~120 lines (48% reduction).
    """
    
    def _create_generator(self, args) -> DrugDrugInteractionGenerator:
        """Create and return a DrugDrugInteractionGenerator instance."""
        model_config = ModelConfig(model=args.model, temperature=0.2)
        return DrugDrugInteractionGenerator(model_config=model_config)
    
    def _create_input_model(self, args) -> DrugDrugInput:
        """Create and return a DrugDrugInput instance from parsed args."""
        return DrugDrugInput(
            medicine1=args.medicine1,
            medicine2=args.medicine2,
            age=args.age,
            dosage1=args.dosage1,
            dosage2=args.dosage2,
            medical_conditions=args.medical_conditions,
            prompt_style=args.prompt_style
        )

    description = "Drug-Drug Interaction Analyzer - Check interactions between two medicines"
    epilog = """
Examples:
  python drug_drug_interaction_cli.py "Warfarin" "Aspirin"
  python drug_drug_interaction_cli.py "Metformin" "Lisinopril" --age 65 --dosage1 "500mg twice daily"
  python drug_drug_interaction_cli.py "Simvastatin" "Clarithromycin" -p detailed -v 3
    """

    def add_arguments(self, parser) -> None:
        """Add domain-specific arguments.

        Args:
            parser: ArgumentParser instance
        """
        parser.add_argument(
            "medicine1",
            type=str,
            help="Name of the first medicine"
        )
        parser.add_argument(
            "medicine2",
            type=str,
            help="Name of the second medicine"
        )
        parser.add_argument(
            "--age", "-a",
            type=int,
            default=None,
            help="Patient's age in years (0-150)"
        )
        parser.add_argument(
            "--dosage1", "-d1",
            type=str,
            default=None,
            help="Dosage information for first medicine"
        )
        parser.add_argument(
            "--dosage2", "-d2",
            type=str,
            default=None,
            help="Dosage information for second medicine"
        )
        parser.add_argument(
            "--conditions", "-c",
            type=str,
            default=None,
            help="Patient's medical conditions (comma-separated)"
        )
        parser.add_argument(
            "--prompt-style", "-p",
            type=str,
            choices=["detailed", "concise", "balanced"],
            default="detailed",
            help="Prompt style for analysis (default: detailed)"
        )

    def validate_args(self) -> None:
        """Validate parsed arguments.

        Raises:
            ValueError: If required arguments are invalid
        """
        if not self.args.medicine1.strip():
            raise ValueError("Medicine 1 name cannot be empty")
        if not self.args.medicine2.strip():
            raise ValueError("Medicine 2 name cannot be empty")
        if self.args.age is not None and not (0 <= self.args.age <= 150):
            raise ValueError("Age must be between 0 and 150")

    def run(self) -> ModelOutput:
        """Run the drug-drug interaction analysis.

        Returns:
            Union[DrugInteractionResult, str]: Analysis result
        """
        # Create generator
        generator = DrugDrugInteractionGenerator(self.model_config, self.logger)

        # Create input model from args
        input_model = DrugDrugInput(
            medicine1=self.args.medicine1,
            medicine2=self.args.medicine2,
            age=self.args.age,
            dosage1=self.args.dosage1,
            dosage2=self.args.dosage2,
            medical_conditions=self.args.conditions,
            prompt_style=self.args.prompt_style
        )
        
        # Generate interaction analysis
        result = generator.generate_text(
            config=input_model,
            structured=self.args.structured
        )

        # Save result if output path is specified
        if result is not None:
            output_path = self._get_output_path(
                f"{self.args.medicine1}_{self.args.medicine2}",
                suffix="interaction"
            )
            from lite.utils import save_model_response
            save_model_response(result, output_path)

        return result


def main() -> int:
    """Main entry point for the CLI."""
    cli = DrugDrugInteractionCLI(logger_name=__name__)
    return cli.execute()


if __name__ == "__main__":
    sys.exit(main())
