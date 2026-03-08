import sys
import argparse
from pathlib import Path
from typing import List

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from math_theory_models import (
    MathTheory, AudienceLevel
)
from math_theory_element import MathTheoryExplainer

def arguments_parser():
    """Parse command-line arguments for the math theory explainer CLI."""
    parser = argparse.ArgumentParser(
        description="Fetch explanations for mathematical theories across different audience levels"
    )
    parser.add_argument(
        "-t", "--theory",
        type=str,
        default="Group theory",
        help="Specific mathematical theory to explain (default: 'Group theory')"
    )
    parser.add_argument(
        "-l", "--level",
        type=str,
        default="undergrad",
        choices=[l.value for l in AudienceLevel],
        help="Specify audience level to fetch (default: 'undergrad')"
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default="ollama/gemma3:12b",
        help="Model to use (default: ollama/gemma3:12b)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Temperature for model (default: 0.2)"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default="outputs/theories",
        help="Output directory for Markdown files (default: 'outputs/theories' directory)"
    )
    return parser.parse_args()


def fetch_theory_info(theory_name: str, model_config: ModelConfig, levels: List[AudienceLevel] = None) -> MathTheory | None:
    """Fetch information for a single mathematical theory."""
    # Initialize explainer with model config
    explainer = MathTheoryExplainer(model_config)
    
    # Fetch theory information
    return explainer.fetch_theory_explanation(theory_name, audience_levels=levels)


def math_theory_to_markdown(theory_info: MathTheory) -> str:
    """Convert MathTheory object to a formatted Markdown string."""
    md = [f"# {theory_info.theory_name}\n"]
    
    # Sort levels to maintain consistent order
    for level in AudienceLevel:
        if level in theory_info.explanations:
            exp = theory_info.explanations[level]
            level_name = level.value.replace("-", " ").title()
            md.append(f"## Audience Level: {level_name}\n")
            
            md.append(f"### Introduction\n{exp.introduction}\n")
            
            md.append("### Key Concepts")
            for concept in exp.key_concepts:
                md.append(f"- {concept}")
            md.append("")
            
            md.append(f"### Why It Was Created\n{exp.why_it_was_created}\n")
            md.append(f"### Problems Solved or Simplified\n{exp.problems_solved_or_simplified}\n")
            md.append(f"### How It Is Used Today\n{exp.how_it_is_used_today}\n")
            md.append(f"### Foundation for Other Theories\n{exp.foundation_for_other_theories}\n")
            md.append(f"### New Research\n{exp.new_research}\n")
            
            md.append("### Solution Methods")
            md.append(f"**Analytical:** {exp.solution_methods.analytical}")
            md.append(f"**Numerical:** {exp.solution_methods.numerical}\n")
            
            md.append("---\n")
            
    return "\n".join(md)


def math_theory_cli():
    """CLI tool for fetching mathematical theory explanations."""
    configure_logging()
    args = arguments_parser()

    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_config = ModelConfig(model=args.model, temperature=args.temperature)
    
    # Convert level string back to AudienceLevel enum
    selected_level = AudienceLevel(args.level)
    
    # Mapping for level IDs
    LEVEL_ID_MAP = {
        AudienceLevel.GENERAL: 0,
        AudienceLevel.HIGH_SCHOOL: 1,
        AudienceLevel.UNDERGRAD: 2,
        AudienceLevel.MASTER: 3,
        AudienceLevel.PHD: 4,
        AudienceLevel.RESEARCHER: 5
    }
    level_id = LEVEL_ID_MAP.get(selected_level, 0)

    # Fetch specific theory
    theory_info = fetch_theory_info(args.theory, model_config, [selected_level])

    if theory_info:
        # Save as Markdown
        markdown_content = math_theory_to_markdown(theory_info)
        safe_name = "".join([c if c.isalnum() else "_" for c in args.theory]).lower()
        output_file = output_dir / f"{safe_name}_level{level_id}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Saved explanation for '{args.theory}' at level '{selected_level.value}' (ID: {level_id}) to {output_file}", file=sys.stderr)
    else:
        print(f"Failed to fetch explanation for '{args.theory}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    math_theory_cli()
