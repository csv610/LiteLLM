import sys
import argparse
from pathlib import Path
from typing import List

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from .paradox_models import (
    Paradox, AudienceLevel
)
from .paradox_element import ParadoxExplainer

def arguments_parser():
    """Parse command-line arguments for the paradox explainer CLI."""
    parser = argparse.ArgumentParser(
        description="Fetch explanations for paradoxes across different audience levels"
    )
    parser.add_argument(
        "-p", "--paradox",
        type=str,
        default="Zeno's paradox",
        help="Specific paradox to explain (default: 'Zeno's paradox')"
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
        default="outputs/paradoxes",
        help="Output directory for Markdown files (default: 'outputs/paradoxes' directory)"
    )
    return parser.parse_args()


def fetch_paradox_info(paradox_name: str, model_config: ModelConfig, levels: List[AudienceLevel] = None) -> Paradox | None:
    """Fetch information for a single paradox."""
    # Initialize explainer with model config
    explainer = ParadoxExplainer(model_config)
    
    # Fetch paradox information
    return explainer.fetch_paradox_explanation(paradox_name, audience_levels=levels)


def paradox_to_markdown(paradox_info: Paradox) -> str:
    """Convert Paradox object to a formatted Markdown string."""
    md = [f"# {paradox_info.paradox_name}\n"]
    
    # Sort levels to maintain consistent order
    for level in AudienceLevel:
        if level in paradox_info.explanations:
            exp = paradox_info.explanations[level]
            level_name = level.value.replace("-", " ").title()
            md.append(f"## Audience Level: {level_name}\n")
            
            md.append(f"### Introduction\n{exp.introduction}\n")
            
            md.append(f"### Status\n**Current Scientific/Philosophical Standing:** {exp.status.value}\n")
            
            md.append(f"### Root Cause\n**The fundamental hidden assumptions causing this paradox:**\n{exp.root_cause}\n")
            
            md.append("### Key Concepts")
            for concept in exp.key_concepts:
                md.append(f"- {concept}")
            md.append("")
            
            md.append(f"### Historical Context\n{exp.historical_context}\n")
            md.append(f"### The Contradiction\n{exp.the_contradiction}\n")
            md.append(f"### Modern Relevance\n{exp.modern_relevance}\n")
            md.append(f"### Impact on Thought\n{exp.impact_on_thought}\n")
            md.append(f"### Current Debates\n{exp.current_debates}\n")
            
            md.append("### Resolutions")
            md.append(f"**Who Solved It:** {exp.resolutions.who_solved}")
            md.append(f"**How It Was Solved:** {exp.resolutions.how_it_was_solved}\n")
            md.append(f"**Logical Details:** {exp.resolutions.logical}")
            md.append(f"**Mathematical/Scientific Details:** {exp.resolutions.mathematical}\n")
            
            md.append("---\n")
            
    return "\n".join(md)


def paradox_cli():
    """CLI tool for fetching paradox explanations."""
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

    # Fetch specific paradox
    paradox_info = fetch_paradox_info(args.paradox, model_config, [selected_level])

    if paradox_info:
        # Save as Markdown
        markdown_content = paradox_to_markdown(paradox_info)
        safe_name = "".join([c if c.isalnum() else "_" for c in args.paradox]).lower()
        output_file = output_dir / f"{safe_name}_level{level_id}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"Saved explanation for '{args.paradox}' at level '{selected_level.value}' (ID: {level_id}) to {output_file}", file=sys.stderr)
    else:
        print(f"Failed to fetch explanation for '{args.paradox}'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    paradox_cli()
