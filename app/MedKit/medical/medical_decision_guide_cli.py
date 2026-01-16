import argparse
import sys
import logging
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional

from medkit.core.medkit_client import MedKitClient, MedKitConfig
from medkit.utils.pydantic_prompt_generator import PromptStyle
from medkit.utils.logging_config import setup_logger

import hashlib
from medkit.utils.lmdb_storage import LMDBStorage, LMDBConfig
from medical_decision_guide_models import DecisionNode, Outcome, MedicalDecisionGuide

# Configure logging
logger = setup_logger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class Config(MedKitConfig):
    """Configuration for the medical decision guide generator."""


    def __post_init__(self):
        """Set default db_path if not provided, then validate."""
        if self.db_path is None:
            self.db_path = str(
                Path(__file__).parent.parent / "storage" / "medical_decision_guide.lmdb"
            )
        # Call parent validation
        super().__post_init__()

def append_decision_tree_suffix(output_path: Path) -> Path:
    """
    Append '_decision_tree' suffix to filename if not already present.

    Args:
        output_path: Path to the output file

    Returns:
        Path with '_decision_tree' appended before the file extension
    """
    if output_path.name.endswith("decision_tree.json"):
        return output_path

    stem = output_path.stem
    suffix = output_path.suffix
    return output_path.parent / f"{stem}_decision_tree{suffix}"


def create_decision_tree(
    symptom_name: str,
    output_path: Path,
    age_group: str = "all",
    prompt_style: PromptStyle = PromptStyle.DETAILED,
    tree_depth: int = 3,
) -> MedicalDecisionGuide:
    """
    Create a decision tree for medical symptom assessment.

    Args:
        symptom_name: Name of the symptom to create a tree for
        output_path: Path to save the decision tree JSON file
        age_group: Target age group (all, pediatric, adult, geriatric)
        prompt_style: Style of schema prompt (DETAILED, CONCISE, TECHNICAL)
        tree_depth: Maximum depth of decision tree (1-5, default: 3)

    Returns:
        MedicalDecisionGuide: Validated decision tree object

    Raises:
        ValueError: If symptom_name is empty or tree_depth is invalid
    """
    if not symptom_name or not symptom_name.strip():
        raise ValueError("Symptom name cannot be empty")

    if not (1 <= tree_depth <= 5):
        raise ValueError("tree_depth must be between 1 and 5")

    # Load model name from ModuleConfig


    model_name = "gemini-1.5-pro"  # Default model for this module


    


    client = MedKitClient(model_name=model_name)
    output_path = Path(output_path)
    output_path = append_decision_tree_suffix(output_path)

    # Build context for prompt
    age_context = f"Focus on {age_group} population." if age_group != "all" else "Cover all age groups."
    depth_context = f"Create a decision tree with approximately {tree_depth} levels of depth (more levels = more detailed assessment)."

    result = client.generate(
        subject=f"Decision tree for {symptom_name} assessment ({age_group})",
        schema=MedicalDecisionGuide,
        output_path=output_path,
        specialty="Medicine/General",
        use_schema_prompt=True,
        prompt_style=prompt_style,
        context=f"{age_context} {depth_context}",
    )

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Create medical decision trees for symptom assessment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create default decision tree
  python medical_decision_guide.py -i "Fever" -o outputs/fever.json

  # Create pediatric tree with depth 4
  python medical_decision_guide.py -i "Fever" -o outputs/fever.json -a pediatric -d 4

  # Create with concise style
  python medical_decision_guide.py -i "Sore Throat" -o outputs/sore_throat.json --concise

  # Create adult cough tree with maximum depth
  python medical_decision_guide.py -i "Cough" -o outputs/cough.json -a adult -d 5
        """
    )

    parser.add_argument(
        "-i", "--symptom",
        nargs='+',
        help="Name of the symptom to create tree for"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Path to save decision tree JSON file"
    )
    parser.add_argument(
        "-a", "--age-group",
        choices=["all", "pediatric", "adult", "geriatric"],
        default="all",
        help="Target age group (default: all)"
    )
    parser.add_argument(
        "--concise",
        action="store_true",
        help="Use concise prompt style"
    )
    parser.add_argument(
        "-d", "--depth",
        type=int,
        choices=[1, 2, 3, 4, 5],
        default=3,
        help="Tree depth: 1=simple, 3=detailed, 5=very detailed (default: 3)"
    )
    parser.add_argument(
        "-v", "--verbosity",
        type=int,
        choices=[0, 1, 2, 3, 4],
        default=2,
        help="Verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2)"
    )

    args = parser.parse_args()

    # Configure logging based on verbosity level
    config = Config(verbosity=args.verbosity)
    verbosity_levels = {0: "CRITICAL", 1: "ERROR", 2: "WARNING", 3: "INFO", 4: "DEBUG"}
    logger.setLevel(verbosity_levels.get(config.verbosity, "WARNING"))

    try:
        symptom_name = " ".join(args.symptom)
        prompt_style = PromptStyle.CONCISE if args.concise else PromptStyle.DETAILED

        # Calculate actual output path
        output_path = append_decision_tree_suffix(Path(args.output))

        guide = create_decision_tree(
            symptom_name=symptom_name,
            output_path=args.output,
            age_group=args.age_group,
            prompt_style=prompt_style,
            tree_depth=args.depth,
        )

        if config.verbosity >= 3:  # INFO level or higher
            print(f"✓ Decision tree created for '{symptom_name}'")
            print(f"  Saved to: {output_path}")

    except ValueError as e:
        print(f"✗ Validation error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


    def close(self):
        """Close LMDB storage and release resources."""
        if self.storage:
            try:
                self.storage.close()
                logger.info("LMDB storage closed successfully.")
            except Exception as e:
                logger.error(f"Error closing LMDB storage: {e}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
