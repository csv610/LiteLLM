"""Drug-Disease Interaction Analysis module."""

import argparse
import logging
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
from lite.utils import save_model_response

from drug_disease_interaction_models import DrugDiseaseInteractionModel, ModelOutput

logger = logging.getLogger(__name__)


class PromptStyle(str, Enum):
    DETAILED = "detailed"
    CONCISE = "concise"
    BALANCED = "balanced"

@dataclass
class DrugDiseaseInput:
    """Configuration and input for drug-disease interaction analysis."""
    medicine_name: str
    condition_name: str
    condition_severity: Optional[str] = None
    age: Optional[int] = None
    other_medications: Optional[str] = None
    prompt_style: PromptStyle = PromptStyle.DETAILED

    def __post_init__(self):
        """Validate input parameters."""
        if not self.medicine_name or not self.medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if not self.condition_name or not self.condition_name.strip():
            raise ValueError("Condition name cannot be empty")
        if self.age is not None and (self.age < 0 or self.age > 150):
            raise ValueError("Age must be between 0 and 150 years")


class PromptBuilder:
    """Builder class for creating prompts for drug-disease interaction analysis."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for drug-disease interaction analysis.

        Returns:
            str: System prompt defining the LLM's role and instructions
        """
        return """You are a clinical pharmacology expert specializing in drug-disease interactions. Your role is to analyze how medical conditions affect drug efficacy, safety, and metabolism.

When analyzing drug-disease interactions, you must:

1. **Assess Overall Interaction Severity**: Determine if the drug is contraindicated, requires caution, or is safe to use with the condition.

2. **Explain the Mechanism**: Describe the pharmacological and pathophysiological mechanisms underlying the interaction.

3. **Evaluate Efficacy Impact**: Analyze whether the disease affects the drug's therapeutic effectiveness, including:
   - Reduced efficacy due to disease state
   - Altered drug absorption, distribution, metabolism, or excretion
   - Disease-specific factors affecting treatment response

4. **Assess Safety Concerns**: Identify potential risks and adverse effects, including:
   - Increased risk of side effects or toxicity
   - Disease complications that may worsen with drug use
   - Monitoring requirements for safe use

5. **Provide Dosage Guidance**: Recommend dose adjustments if needed based on:
   - Organ function (hepatic, renal, cardiac)
   - Disease severity
   - Risk-benefit considerations

6. **Recommend Management Strategies**: Offer clinical recommendations for safe and effective use, including:
   - Monitoring parameters
   - Alternative therapies if contraindicated
   - Patient counseling points

7. **Create Patient-Friendly Guidance**: Translate technical information into clear, accessible language that patients can understand and act upon.

Base your analysis on established medical literature, clinical guidelines, and pharmacological principles. If data is limited or unavailable, clearly indicate this and explain the reasoning behind any recommendations.

Always prioritize patient safety while providing practical, evidence-based guidance for clinicians."""

    @staticmethod
    def create_user_prompt(config: DrugDiseaseInput) -> str:
        """
        Create the user prompt for drug-disease interaction analysis.

        Args:
            config: Configuration containing medicine, condition, and analysis parameters

        Returns:
            str: User prompt with context and formatted according to the specified style
        """
        # Build context parts
        context_parts = [f"Analyzing interaction between {config.medicine_name} and {config.condition_name}"]
        
        if config.condition_severity:
            context_parts.append(f"Condition severity: {config.condition_severity}")
            logger.debug(f"Condition severity: {config.condition_severity}")
        if config.age is not None:
            context_parts.append(f"Patient age: {config.age} years")
            logger.debug(f"Patient age: {config.age}")
        if config.other_medications:
            context_parts.append(f"Other medications: {config.other_medications}")
            logger.debug(f"Other medications: {config.other_medications}")

        context = ". ".join(context_parts) + "."
        base_query = f"Analyze the interaction between {config.medicine_name} and {config.condition_name}."

        if config.prompt_style == PromptStyle.CONCISE:
            return f"{base_query} {context} Provide a focused analysis of key safety concerns and essential management recommendations."

        elif config.prompt_style == PromptStyle.BALANCED:
            return f"{base_query} {context} Provide a balanced analysis covering mechanism, clinical significance, and practical management guidance."

        else:  # DETAILED
            return f"{base_query} {context} Provide a comprehensive analysis including detailed mechanism of interaction, complete efficacy and safety assessment, specific dosage recommendations, clinical management strategies, and patient counseling guidance."


class DrugDiseaseInteraction:
    """Analyzes drug-disease interactions based on provided configuration."""
    def __init__(self, model_config: ModelConfig):
        self.client = LiteClient(model_config)

    def generate_text(self, config: DrugDiseaseInput, structured: bool = False) -> ModelOutput:
        """
        Analyzes how a medical condition affects drug efficacy, safety, and metabolism.

        Args:
            config: Configuration and input for analysis

        Returns:
            tuple: A tuple containing:
                - DrugDiseaseInteractionResult: The analysis result
                - Path: Path to the saved response file
        """
        logger.debug(f"Starting drug-disease interaction analysis")
        logger.debug(f"Medicine: {config.medicine_name}")
        logger.debug(f"Condition: {config.condition_name}")

        user_prompt = PromptBuilder.create_user_prompt(config)
        response_format = None
        if structured:
            response_format = DrugDiseaseInteractionResult

        model_input = ModelInput(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=user_prompt,
            response_format=response_format,
        )
        result = self._ask_llm(model_input)
        
        logger.debug(f"✓ Successfully analyzed disease interaction")
        return result


    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Helper to call LiteClient with error handling."""
        logger.debug("Calling LiteClient...")
        try:
            return self.client.generate_text(model_input=model_input)
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            logger.exception("Full exception details:")
            raise
            
    def _save_interaction_result(self, result: ModelOutput,  medicine_name: str, condition_name: str) -> Path:
        """
        Save the interaction analysis result to a JSON or MD file.
        
        Args:
            result: The analysis result to save
            medicine_name: Name of the medicine
            condition_name: Name of the condition
            
        Returns:
            Path: Path to the saved file
        """
        suffix = ".json"
        if isinstance(result, str):
            suffix = ".md"
        output_file = f"{medicine_name.lower()}_{condition_name.lower().replace(' ', '_')}_interaction{suffix}"
        saved_path = save_model_response(result, output_file)
        logger.debug(f"Response saved to: {saved_path}")
        return saved_path


def parse_prompt_style(style_str: str) -> PromptStyle:
    """
    Parse prompt style string to PromptStyle enum.

    Args:
        style_str: String representation of prompt style

    Returns:
        PromptStyle: The corresponding enum value

    Raises:
        ValueError: If style string is not a valid prompt style
    """
    style_mapping = {
        "detailed": PromptStyle.DETAILED,
        "concise": PromptStyle.CONCISE,
        "balanced": PromptStyle.BALANCED,
    }

    if style_str.lower() not in style_mapping:
        raise ValueError(
            f"Invalid prompt style: {style_str}. "
            f"Choose from: {', '.join(style_mapping.keys())}"
        )
    return style_mapping[style_str.lower()]

def get_user_arguments():
    """
    Create and configure the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured parser for command-line arguments
    """
    parser = argparse.ArgumentParser(
        description="Drug-Disease Interaction Analyzer - Assess how medical conditions affect medicines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  python drug_disease_interaction.py "Metformin" "Kidney Disease"

  # With condition severity
  python drug_disease_interaction.py "Warfarin" "Liver Disease" --condition-severity severe

  # With patient details and other medications
  python drug_disease_interaction.py "Lisinopril" "Hypertension" --age 72 --other-medications "Atorvastatin, Aspirin"

  # With custom verbosity
  python drug_disease_interaction.py "NSAIDs" "Asthma" --verbose
        """,
    )

    parser.add_argument(
        "medicine_name",
        type=str,
        help="Name of the medicine to analyze",
    )

    parser.add_argument(
        "condition_name",
        type=str,
        help="Name of the medical condition",
    )

    parser.add_argument(
        "--severity",
        "-S",
        type=str,
        choices=["mild", "moderate", "severe"],
        default=None,
        help="Severity of the condition (mild, moderate, severe)",
    )

    parser.add_argument(
        "--age",
        "-a",
        type=int,
        default=None,
        help="Patient's age in years (0-150)",
    )

    parser.add_argument(
        "--medications",
        "-m",
        type=str,
        default=None,
        help="Other medications the patient is taking (comma-separated)",
    )

    parser.add_argument(
        "--style",
        "-s",
        type=str,
        choices=["detailed", "concise", "balanced"],
        default="detailed",
        help="Prompt style for analysis (default: detailed)",
    )

    parser.add_argument(
        "--verbosity",
        "-v",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).",
    )

    parser.add_argument(
        "--json",
        "-j",
        action="store_true",
        default=False,
        help="Output results as JSON to stdout (in addition to file)",
    )
    parser.add_argument(
        "--structured",
        "-t",
        action="store_true",
        default=False,
        help="Use structured output (Pydantic model) for the response"
    )

    parser.add_argument(
        "--model",
        type=str,
        default="ollama/gemma3",
        help="LLM model to use for analysis (default: ollama/gemma3)",
    )

    return parser.parse_args()

def main() -> int:
    """
    Main entry point for the drug-disease interaction CLI.

    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    args  = get_user_arguments()

    try:
        prompt_style = parse_prompt_style(args.prompt_style)

        configure_logging(
            log_file="drug_disease_interaction.log",
            verbosity=args.verbosity,
            enable_console=True
        )

        config = DrugDiseaseInput(
            medicine_name=args.medicine_name,
            condition_name=args.condition_name,
            condition_severity=args.condition_severity,
            age=args.age,
            other_medications=args.other_medications,
            prompt_style=prompt_style,
        )

        logger.info("Configuration created successfully")

        model_config = ModelConfig(model=args.model, temperature=0.7)
        analyzer = DrugDiseaseInteraction(model_config)
        result, saved_path = analyzer.generate_text(config, structured=args.structured)
        
        logger.debug(f"Analysis completed. Results saved to: {saved_path}")
        return 0

    except ValueError as e:
        console.print(f"[red]✗[/red] Invalid input: {e}", style="bold red")
        logger.error(f"Invalid input: {e}")
        return 1
    except Exception as e:
        console.print(f"[red]✗[/red] Error: {e}", style="bold red")
        logger.error(f"Unexpected error: {e}")
        logger.exception("Full exception details:")
        return 1



if __name__ == "__main__":
    sys.exit(main())
