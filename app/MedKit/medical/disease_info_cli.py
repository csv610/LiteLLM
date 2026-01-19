"""Module docstring - Disease Information Generator.

Generate comprehensive, evidence-based disease information using structured
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
from pydantic import BaseModel
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
from disease_info_models import (
    RiskFactors,
    DiagnosticCriteria,
    DiseaseIdentity,
    DiseaseBackground,
    DiseaseEpidemiology,
    DiseaseClinicalPresentation,
    DiseaseDiagnosis,
    DiseaseManagement,
    DiseaseResearch,
    DiseaseSpecialPopulations,
    DiseaseLivingWith,
    DiseaseInfo,
)

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

# ==============================================================================
# CONFIGURATION CLASS
# ==============================================================================

@dataclass
class DiseaseInfoConfig:
    """Configuration for generating disease information."""
    output_path: Optional[Path] = None
    output_dir: Path = Path("outputs")
    verbosity: bool = False
    enable_cache: bool = True
# ==============================================================================
# MAIN CLASS
# ==============================================================================

class DiseaseInfoGenerator:
    """Generates comprehensive disease information based on provided configuration."""

    def __init__(self, config: DiseaseInfoConfig):
        self.config = config
        self.client = LiteClient(
            ModelConfig(model="ollama/gemma3", temperature=0.7)
        )
        self.config.output_dir.mkdir(parents=True, exist_ok=True)

        # Apply verbosity to logger
        if self.config.verbosity:
            logger.setLevel("DEBUG")
        else:
            logger.setLevel("INFO")

        logger.info(f"Initialized DiseaseInfoGenerator")
        if self.config.verbosity:
            logger.debug(f"Config: {self.config}")

    def generate(
        self,
        disease: str,
        output_path: Optional[str] = None,
    ) -> DiseaseInfo:
        """
        Generates comprehensive disease information.

        Args:
            disease: Name of the disease
            output_path: Optional path to save the output JSON file

        Returns:
            DiseaseInfo: Validated disease information object
        """
        # Validate inputs
        if not disease or not str(disease).strip():
            raise ValueError("Disease name cannot be empty")

        logger.info("-" * 80)
        logger.info(f"Starting disease information generation")
        logger.info(f"Disease Name: {disease}")

        # Determine output path
        output_path_obj = Path(output_path) if output_path else None
        if output_path_obj is None:
            output_path_obj = self.config.output_dir / f"{disease.lower().replace(' ', '_')}_info.json"

        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output path: {output_path_obj}")

        # Generate disease information
        logger.info("Calling LiteClient.generate_text()...")
        try:
            prompt = f"Generate comprehensive information for the disease: {disease}."
            logger.debug(f"Prompt: {prompt}")

            result = self.client.generate_text(
                model_input=ModelInput(
                    user_prompt=prompt,
                    response_format=DiseaseInfo,
                )
            )

            logger.info(f"✓ Successfully generated disease information")
            logger.info(f"Disease: {result.identity.disease_name}")
            logger.info("-" * 80)
            return result
        except Exception as e:
            logger.error(f"✗ Error generating disease information: {e}")
            logger.exception("Full exception details:")
            logger.info("-" * 80)
            raise

    def save(self, disease_info: DiseaseInfo, output_path: str):
        """
        Saves the disease information to a JSON file.

        Args:
            disease_info: The DiseaseInfo object to save
            output_path: Path where the JSON file should be saved
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Saving disease information to: {output_file}")

        try:
            with open(output_file, "w") as f:
                json.dump(disease_info.model_dump(), f, indent=2)
            file_size = output_file.stat().st_size
            logger.info(f"✓ Successfully saved disease information")
            logger.info(f"File: {output_file}")
            logger.info(f"File size: {file_size} bytes")
        except Exception as e:
            logger.error(f"✗ Error saving disease information: {e}")
            logger.exception("Full exception details:")
            raise


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def print_result(result: DiseaseInfo, verbose: bool = False) -> None:
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


def get_disease_info(
    disease: str,
    config: DiseaseInfoConfig,
    output_path: Optional[str] = None,
) -> Optional[DiseaseInfo]:
    """
    Get comprehensive disease information.

    This is a convenience function that instantiates and runs the
    DiseaseInfoGenerator.

    Args:
        disease: Name of the disease
        config: Configuration object for the generation
        output_path: Optional path to save the output JSON file

    Returns:
        DiseaseInfo: The result of the generation, or None if it fails
    """
    try:
        generator = DiseaseInfoGenerator(config)
        return generator.generate(disease=disease, output_path=output_path)
    except Exception as e:
        logger.error(f"Failed to generate disease information: {e}")
        return None


# ==============================================================================
# ARGUMENT PARSER
# ==============================================================================


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main() -> int:
    """
    CLI entry point for generating disease information.
    """
    logger.info("="*80)
    logger.info("DISEASE INFO CLI - Starting")
    logger.info("="*80)

    parser = argparse.ArgumentParser(
        description="Generate comprehensive disease information.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python disease_info_cli.py -i diabetes
  python disease_info_cli.py -i "heart disease" -o output.json -v
  python disease_info_cli.py -i pneumonia -d outputs/diseases
        """
    )
    parser.add_argument(
        "-i", "--disease",
        required=True,
        help="The name of the disease to generate information for."
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
    config = DiseaseInfoConfig(
        output_path=Path(args.output) if args.output else None,
        output_dir=Path(args.output_dir),
        verbosity=args.verbose
    )

    logger.info(f"CLI Arguments:")
    logger.info(f"  Disease: {args.disease}")
    logger.info(f"  Output Dir: {args.output_dir}")
    logger.info(f"  Output File: {args.output if args.output else 'Default'}")
    logger.info(f"  Verbose: {args.verbose}")

    # Generate disease information
    try:
        generator = DiseaseInfoGenerator(config)
        disease_info = generator.generate(disease=args.disease, output_path=args.output)

        if disease_info is None:
            logger.error("✗ Failed to generate disease information.")
            sys.exit(1)

        # Display formatted result
        print_result(disease_info, args.verbose)

        # Save if output path is specified
        if args.output:
            generator.save(disease_info, args.output)
        else:
            # Save to default location
            default_path = config.output_dir / f"{args.disease.lower().replace(' ', '_')}_info.json"
            generator.save(disease_info, str(default_path))

        logger.info("="*80)
        logger.info("✓ Disease information generation completed successfully")
        logger.info("="*80)
        return 0
    except Exception as e:
        logger.error("="*80)
        logger.error(f"✗ Disease information generation failed: {e}")
        logger.exception("Full exception details:")
        logger.error("="*80)
        sys.exit(1)


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    sys.exit(main())
