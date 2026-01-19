"""Module docstring - Medical Decision Guide Generator.

Generate medical decision trees for symptom assessment using structured data models
and the LiteClient with schema-aware prompting for clinical decision support.
"""

# ==============================================================================
# STANDARD LIBRARY IMPORTS
# ==============================================================================
import argparse
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# ==============================================================================
# THIRD-PARTY IMPORTS
# ==============================================================================
from rich.console import Console
from rich.panel import Panel

# ==============================================================================
# LOCAL IMPORTS (LiteClient setup)
# ==============================================================================
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

# ==============================================================================
# LOCAL IMPORTS (Module models)
# ==============================================================================
from medical_decision_guide_models import MedicalDecisionGuide

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==============================================================================
# CONSTANTS
# ==============================================================================
console = Console()

# ==============================================================================
# CONFIGURATION CLASS
# ==============================================================================

@dataclass
class MedicalDecisionGuideConfig:
    """Configuration for generating medical decision guides."""
    output_path: Optional[Path] = None
    output_dir: Path = Path("outputs")
    verbosity: bool = False


# ==============================================================================
# MAIN CLASS
# ==============================================================================

class MedicalDecisionGuideGenerator:
    """Generates medical decision guides based on provided configuration."""

    def __init__(self, config: MedicalDecisionGuideConfig):
        self.config = config
        self.client = LiteClient(
            ModelConfig(model="ollama/gemma3", temperature=0.7)
        )
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        if self.config.verbosity:
            logger.setLevel("DEBUG")
        else:
            logger.setLevel("INFO")

        logger.info(f"Initialized MedicalDecisionGuideGenerator")
        if self.config.verbosity:
            logger.debug(f"Config: {self.config}")

    def generate(
        self,
        symptom: str,
        output_path: Optional[str] = None,
    ) -> MedicalDecisionGuide:
        """
        Generates a medical decision guide for symptom assessment.

        Args:
            symptom: Name of the symptom
            output_path: Optional path to save the output JSON file

        Returns:
            MedicalDecisionGuide: Validated decision guide object
        """
        # Validate inputs
        if not symptom or not str(symptom).strip():
            raise ValueError("Symptom name cannot be empty")

        logger.info("-" * 80)
        logger.info(f"Starting decision guide generation")
        logger.info(f"Symptom Name: {symptom}")

        # Determine output path
        output_path_obj = Path(output_path) if output_path else None
        if output_path_obj is None:
            output_path_obj = self.config.output_dir / f"{symptom.lower().replace(' ', '_')}_decision_tree.json"

        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path_obj}")

        # Generate decision guide
        logger.info("Calling LiteClient.generate_text()...")
        try:
            prompt = f"Generate a comprehensive medical decision tree for: {symptom}."
            logger.debug(f"Prompt: {prompt}")

            result = self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=prompt,
                    response_format=MedicalDecisionGuide,
                )
            )

            logger.info(f"✓ Successfully generated decision guide")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error generating decision guide: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise

    def save(self, guide: MedicalDecisionGuide, output_path: str):
        """
        Saves the decision guide to a JSON file.

        Args:
            guide: The MedicalDecisionGuide object to save
            output_path: Path where the JSON file should be saved
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving decision guide to: {output_file}")

        try:
            with open(output_file, "w") as f:
                json.dump(guide.model_dump(), f, indent=2)
            file_size = output_file.stat().st_size
            logger.info(f"✓ Successfully saved decision guide")
            logger.info(f"File: {output_file}")
            logger.info(f"File size: {file_size} bytes")
        except Exception as e:
            logger.error(f"✗ Error saving decision guide: {e}")
            logger.exception("Full exception details:")
            raise


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def print_result(result: MedicalDecisionGuide, verbose: bool = False) -> None:
    """Print result in a formatted manner using rich."""
    console = Console()

    # Extract main fields from the result model
    result_dict = result.model_dump()

    # Create a formatted panel showing the result
    # Use semantic formatting: green for success/positive, yellow for warnings, blue for info
    # Display the data in organized sections

    for section_name, section_value in result_dict.items():
        if section_value is not None:
            if isinstance(section_value, dict):
                formatted_text = "\n".join([f"  [bold]{k}:[/bold] {v}" for k, v in section_value.items()])
            else:
                formatted_text = str(section_value)

            console.print(Panel(
                formatted_text,
                title=section_name.replace('_', ' ').title(),
                border_style="cyan",
            ))


def create_decision_tree(
    symptom: str,
    config: MedicalDecisionGuideConfig,
    output_path: Optional[str] = None,
) -> Optional[MedicalDecisionGuide]:
    """
    Create a medical decision tree for symptom assessment.

    Args:
        symptom: Name of the symptom
        config: Configuration object for the generation
        output_path: Optional path to save the output JSON file

    Returns:
        MedicalDecisionGuide: The result of the generation, or None if it fails
    """
    try:
        generator = MedicalDecisionGuideGenerator(config)
        return generator.generate(symptom=symptom, output_path=output_path)
    except Exception as e:
        logger.error(f"Failed to generate decision guide: {e}")
        return None


# ==============================================================================
# ARGUMENT PARSER
# ==============================================================================


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main() -> int:
    """
    CLI entry point for generating medical decision guides.
    """
    logger.info("="*80)
    logger.info("MEDICAL DECISION GUIDE CLI - Starting")
    logger.info("="*80)

    parser = argparse.ArgumentParser(
        description="Generate medical decision trees for symptom assessment.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_decision_guide_cli.py -i fever
  python medical_decision_guide_cli.py -i "sore throat" -o output.json -v
  python medical_decision_guide_cli.py -i cough -d outputs/guides
        """
    )
    parser.add_argument(
        "-i", "--symptom",
        required=True,
        help="The name of the symptom to generate a decision tree for."
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to save the output JSON file."
    )
    parser.add_argument(
        "-d", "--output-dir",
        default="outputs",
        help="Directory for output files (default: outputs)."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose/debug logging output."
    )

    args = parser.parse_args()

    # Create configuration
    config = MedicalDecisionGuideConfig(
        output_path=Path(args.output) if args.output else None,
        output_dir=Path(args.output_dir),
        verbosity=args.verbose
    )

    logger.info(f"CLI Arguments:")
    logger.info(f"  Symptom: {args.symptom}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbose: {args.verbose}")

    # Generate decision guide
    try:
        generator = MedicalDecisionGuideGenerator(config)
        guide = generator.generate(symptom=args.symptom, output_path=args.output)

        if guide is None:
            logger.error("✗ Failed to generate decision guide.")
            sys.exit(1)

        # Display formatted result
        print_result(guide, args.verbose)

        # Save if output path is specified
        if args.output:
            generator.save(guide, args.output)
        else:
            # Save to default location
            default_path = config.output_dir / f"{args.symptom.lower().replace(' ', '_')}_decision_tree.json"
            generator.save(guide, str(default_path))

        logger.info("="*80)
        logger.info("✓ Decision guide generation completed successfully")
        logger.info("="*80)
        return 0
    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ Decision guide generation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(main())
