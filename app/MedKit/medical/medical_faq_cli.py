"""Module docstring - Medical FAQ Generator.

Generate comprehensive, patient-friendly FAQs for medical topics using structured
data models and the LiteClient with schema-aware prompting for clinical reference
and patient education purposes.
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
from medical_faq_models import ComprehensiveFAQ

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
class MedicalFAQConfig:
    """Configuration for generating medical FAQs."""
    output_path: Optional[Path] = None
    output_dir: Path = Path("outputs")
    verbosity: bool = False


# ==============================================================================
# MAIN CLASS
# ==============================================================================

class MedicalFAQGenerator:
    """Generates comprehensive FAQ content based on provided configuration."""

    def __init__(self, config: MedicalFAQConfig):
        self.config = config
        self.client = LiteClient(
            ModelConfig(model="ollama/gemma3", temperature=0.7)
        )
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        if self.config.verbosity:
            logger.setLevel("DEBUG")
        else:
            logger.setLevel("INFO")

        logger.info(f"Initialized MedicalFAQGenerator")
        if self.config.verbosity:
            logger.debug(f"Config: {self.config}")

    def generate(
        self,
        topic: str,
        output_path: Optional[str] = None,
    ) -> ComprehensiveFAQ:
        """
        Generates comprehensive FAQ content.

        Args:
            topic: Name of the medical topic
            output_path: Optional path to save the output JSON file

        Returns:
            ComprehensiveFAQ: Validated FAQ object
        """
        # Validate inputs
        if not topic or not str(topic).strip():
            raise ValueError("Topic name cannot be empty")

        logger.info("-" * 80)
        logger.info(f"Starting FAQ generation")
        logger.info(f"Topic Name: {topic}")

        # Determine output path
        output_path_obj = Path(output_path) if output_path else None
        if output_path_obj is None:
            output_path_obj = self.config.output_dir / f"{topic.lower().replace(' ', '_')}_faq.json"

        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path_obj}")

        # Generate FAQ
        logger.info("Calling LiteClient.generate_text()...")
        try:
            prompt = f"Generate comprehensive patient-friendly FAQs for: {topic}."
            logger.debug(f"Prompt: {prompt}")

            result = self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=prompt,
                    response_format=ComprehensiveFAQ,
                )
            )

            logger.info(f"✓ Successfully generated FAQ")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error generating FAQ: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise

    def save(self, faq: ComprehensiveFAQ, output_path: str):
        """
        Saves the FAQ to a JSON file.

        Args:
            faq: The ComprehensiveFAQ object to save
            output_path: Path where the JSON file should be saved
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving FAQ to: {output_file}")

        try:
            with open(output_file, "w") as f:
                json.dump(faq.model_dump(), f, indent=2)
            file_size = output_file.stat().st_size
            logger.info(f"✓ Successfully saved FAQ")
            logger.info(f"File: {output_file}")
            logger.info(f"File size: {file_size} bytes")
        except Exception as e:
            logger.error(f"✗ Error saving FAQ: {e}")
            logger.exception("Full exception details:")
            raise


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def print_result(result: ComprehensiveFAQ, verbose: bool = False) -> None:
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


def generate_faq(
    topic: str,
    config: MedicalFAQConfig,
    output_path: Optional[str] = None,
) -> Optional[ComprehensiveFAQ]:
    """
    Generate comprehensive FAQ content.

    This is a convenience function that instantiates and runs the
    MedicalFAQGenerator.

    Args:
        topic: Name of the medical topic
        config: Configuration object for the generation
        output_path: Optional path to save the output JSON file

    Returns:
        ComprehensiveFAQ: The result of the generation, or None if it fails
    """
    try:
        generator = MedicalFAQGenerator(config)
        return generator.generate(topic=topic, output_path=output_path)
    except Exception as e:
        logger.error(f"Failed to generate FAQ: {e}")
        return None


# ==============================================================================
# ARGUMENT PARSER
# ==============================================================================


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main() -> int:
    """
    CLI entry point for generating medical FAQs.
    """
    logger.info("="*80)
    logger.info("MEDICAL FAQ CLI - Starting")
    logger.info("="*80)

    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical FAQs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python medical_faq_cli.py -i diabetes
  python medical_faq_cli.py -i "heart disease" -o output.json -v
  python medical_faq_cli.py -i hypertension -d outputs/faq
        """
    )
    parser.add_argument(
        "-i", "--topic",
        required=True,
        help="The name of the medical topic to generate FAQs for."
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
    config = MedicalFAQConfig(
        output_path=Path(args.output) if args.output else None,
        output_dir=Path(args.output_dir),
        verbosity=args.verbose
    )

    logger.info(f"CLI Arguments:")
    logger.info(f"  Topic: {args.topic}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbose: {args.verbose}")

    # Generate FAQ
    try:
        generator = MedicalFAQGenerator(config)
        faq = generator.generate(topic=args.topic, output_path=args.output)

        if faq is None:
            logger.error("✗ Failed to generate FAQ.")
            sys.exit(1)

        # Display formatted result
        print_result(faq, args.verbose)

        # Save if output path is specified
        if args.output:
            generator.save(faq, args.output)
        else:
            # Save to default location
            default_path = config.output_dir / f"{args.topic.lower().replace(' ', '_')}_faq.json"
            generator.save(faq, str(default_path))

        logger.info("="*80)
        logger.info("✓ FAQ generation completed successfully")
        logger.info("="*80)
        return 0
    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ FAQ generation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(main())
