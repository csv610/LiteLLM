import argparse
import logging
import sys
import os
import re
from pathlib import Path
from typing import Optional

from lite import ModelConfig, configure_logging
from .deep_intuition_models import DeepIntuitionStory
from .deep_intuition import DeepIntuition

# Setup logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
configure_logging(log_file=str(log_dir / "storytelling.log"))
logger = logging.getLogger(__name__)


def run_story_mission(
    topic: str,
    model: Optional[str] = None,
    output_path: Optional[str] = None
) -> str:
    """Run the intuition storytelling mission."""
    model_name = model or os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3")
    model_config = ModelConfig(model=model_name, temperature=0.7)
    
    engine = DeepIntuition(model_config=model_config)
    return engine.generate_story(topic, output_path=output_path)


def arguments_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Deep Intuition - Uncovering the human story behind fundamental ideas",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "-t", "--topic",
        required=True,
        help="The fundamental idea or theorem to explore (e.g., 'Galois Theory')."
    )

    parser.add_argument(
        "-m", "--model",
        default=None,
        help="LLM model to use (default: $DEFAULT_LLM_MODEL or ollama/gemma3)."
    )

    return parser


def main() -> int:
    """Main entry point."""
    parser = arguments_parser()
    args = parser.parse_args()

    try:
        logger.info(f"Initiating Deep Intuition story on '{args.topic}'.")

        # Ensure outputs directory exists
        outputs_dir = Path(__file__).parent / "outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)

        safe_topic = re.sub(r'[^a-zA-Z0-9_-]', '_', args.topic.lower())
        output_filename = outputs_dir / f"story_{safe_topic}.md"

        result = run_story_mission(
            args.topic, 
            model=args.model, 
            output_path=str(output_filename)
        )

        print("\n" + "="*60)
        print(f"📖 DEEP INTUITION MISSION COMPLETE")
        print("="*60)
        
        print(result)
            
        print(f"\n✨ Story complete. Detailed Markdown archived to: {output_filename}")
        
        return 0

    except Exception as e:
        logger.exception(f"Unexpected error during storytelling: {e}")
        print(f"Storytelling failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
