"""Module docstring - Herbal Information Generator.

Generate comprehensive, evidence-based herbal remedy information using structured
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
from herbal_info_models import HerbalInfo

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
class HerbalInfoConfig:
    """Configuration for generating herbal information."""
    output_path: Optional[Path] = None
    output_dir: Path = Path("outputs")
    verbosity: bool = False


# ==============================================================================
# MAIN CLASS
# ==============================================================================

class HerbalInfoGenerator:
    """Generates comprehensive herbal remedy information based on provided configuration."""

    def __init__(self, config: HerbalInfoConfig):
        self.config = config
        self.client = LiteClient(
            ModelConfig(model="ollama/gemma3", temperature=0.7)
        )
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        if self.config.verbosity:
            logger.setLevel("DEBUG")
        else:
            logger.setLevel("INFO")

        logger.info(f"Initialized HerbalInfoGenerator")
        if self.config.verbosity:
            logger.debug(f"Config: {self.config}")

    def generate(
        self,
        herb: str,
        output_path: Optional[str] = None,
    ) -> HerbalInfo:
        """
        Generates comprehensive herbal information.

        Args:
            herb: Name of the herb
            output_path: Optional path to save the output JSON file

        Returns:
            HerbalInfo: Validated herbal information object
        """
        # Validate inputs
        if not herb or not str(herb).strip():
            raise ValueError("Herb name cannot be empty")

        logger.info("-" * 80)
        logger.info(f"Starting herbal information generation")
        logger.info(f"Herb Name: {herb}")

        # Determine output path
        output_path_obj = Path(output_path) if output_path else None
        if output_path_obj is None:
            output_path_obj = self.config.output_dir / f"{herb.lower().replace(' ', '_')}_info.json"

        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path_obj}")

        # Generate herbal information
        logger.info("Calling LiteClient.generate_text()...")
        try:
            prompt = f"Generate comprehensive information for the herb: {herb}."
            logger.debug(f"Prompt: {prompt}")

            result = self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=prompt,
                    response_format=HerbalInfo,
                )
            )

            logger.info(f"✓ Successfully generated herbal information")
            if hasattr(result, 'metadata') and hasattr(result.metadata, 'common_name'):
                logger.info(f"Herb: {result.metadata.common_name}")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error generating herbal information: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise

    def save(self, herbal_info: HerbalInfo, output_path: str):
        """
        Saves the herbal information to a JSON file.

        Args:
            herbal_info: The HerbalInfo object to save
            output_path: Path where the JSON file should be saved
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving herbal information to: {output_file}")

        try:
            with open(output_file, "w") as f:
                json.dump(herbal_info.model_dump(), f, indent=2)
            file_size = output_file.stat().st_size
            logger.info(f"✓ Successfully saved herbal information")
            logger.info(f"File: {output_file}")
            logger.info(f"File size: {file_size} bytes")
        except Exception as e:
            logger.error(f"✗ Error saving herbal information: {e}")
            logger.exception("Full exception details:")
            raise


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def print_result(result: HerbalInfo, verbose: bool = False) -> None:
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


def get_herbal_info(
    herb: str,
    config: HerbalInfoConfig,
    output_path: Optional[str] = None,
) -> Optional[HerbalInfo]:
    """
    Get comprehensive herbal information.

    This is a convenience function that instantiates and runs the
    HerbalInfoGenerator.

    Args:
        herb: Name of the herb
        config: Configuration object for the generation
        output_path: Optional path to save the output JSON file

    Returns:
        HerbalInfo: The result of the generation, or None if it fails
    """
    try:
        generator = HerbalInfoGenerator(config)
        return generator.generate(herb=herb, output_path=output_path)
    except Exception as e:
        logger.error(f"Failed to generate herbal information: {e}")
        return None


# ==============================================================================
# ARGUMENT PARSER
# ==============================================================================


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main() -> int:
    """
    CLI entry point for generating herbal information.
    """
    logger.info("="*80)
    logger.info("HERBAL INFO CLI - Starting")
    logger.info("="*80)

    parser = argparse.ArgumentParser(
        description="Generate comprehensive herbal information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python herbal_info_cli.py -i ginger
  python herbal_info_cli.py -i "echinacea" -o output.json -v
  python herbal_info_cli.py -i turmeric -d outputs/herbs
        """
    )
    parser.add_argument(
        "-i", "--herb",
        required=True,
        help="The name of the herb to generate information for."
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
    config = HerbalInfoConfig(
        output_path=Path(args.output) if args.output else None,
        output_dir=Path(args.output_dir),
        verbosity=args.verbose
    )

    logger.info(f"CLI Arguments:")
    logger.info(f"  Herb: {args.herb}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbose: {args.verbose}")

    # Generate herbal information
    try:
        generator = HerbalInfoGenerator(config)
        herbal_info = generator.generate(herb=args.herb, output_path=args.output)

        if herbal_info is None:
            logger.error("✗ Failed to generate herbal information.")
            sys.exit(1)

        # Display formatted result
        print_result(herbal_info, args.verbose)

        # Save if output path is specified
        if args.output:
            generator.save(herbal_info, args.output)
        else:
            # Save to default location
            default_path = config.output_dir / f"{args.herb.lower().replace(' ', '_')}_info.json"
            generator.save(herbal_info, str(default_path))

        logger.info("="*80)
        logger.info("✓ Herbal information generation completed successfully")
        logger.info("="*80)
        return 0
    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ Herbal information generation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(main())
