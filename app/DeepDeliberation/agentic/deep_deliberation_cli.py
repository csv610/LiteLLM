import argparse
import logging
import sys
import os
import re
from pathlib import Path
from typing import Optional

from lite import ModelConfig, configure_logging
from .deep_deliberation_models import KnowledgeSynthesis
from .deep_deliberation import DeepDeliberation

# Setup logging
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)
configure_logging(log_file=str(log_dir / "discovery.log"))
logger = logging.getLogger(__name__)


def run_discovery_mission(
    topic: str,
    num_rounds: int,
    num_faqs: int = 5,
    model: Optional[str] = None,
    output_path: Optional[str] = None
) -> KnowledgeSynthesis:
    """Run the knowledge discovery mission."""
    model_name = model or os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3")
    model_config = ModelConfig(model=model_name, temperature=0.7)
    
    engine = DeepDeliberation(model_config=model_config)
    return engine.run(topic, num_rounds, num_faqs, output_path=output_path)


def arguments_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Knowledge Discovery Engine - Probing the boundaries of a topic",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "-t", "--topic",
        required=True,
        help="The field or topic of inquiry."
    )

    parser.add_argument(
        "-n", "--num-rounds",
        type=int,
        default=3,
        help="Number of discovery rounds (default: 3)."
    )

    parser.add_argument(
        "-f", "--num-faqs",
        type=int,
        default=5,
        help="Number of initial strategic probes to generate (default: 5)."
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
        logger.info(f"Initiating Discovery Mission on '{args.topic}' for {args.num_rounds} rounds.")
        print(f"Executing Discovery Mission on '{args.topic}'...")

        # Ensure outputs directory exists
        outputs_dir = Path(__file__).parent / "outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)

        safe_topic = re.sub(r'[^a-zA-Z0-9_-]', '_', args.topic.lower())
        output_filename = outputs_dir / f"discovery_{safe_topic}.json"

        result = run_discovery_mission(
            args.topic, 
            args.num_rounds, 
            args.num_faqs, 
            model=args.model, 
            output_path=str(output_filename)
        )

        print("\n--- STRATEGIC KNOWLEDGE MAP ---\n")
        print(f"TOPIC: {result.topic}")
        print(f"\nEXECUTIVE SUMMARY:\n{result.executive_summary}")
        
        print("\nHIDDEN CONNECTIONS:")
        for conn in result.hidden_connections:
            print(f" - {conn}")
            
        print("\nRESEARCH FRONTIERS:")
        for frontier in result.research_frontiers:
            print(f" - {frontier}")
            
        print(f"\nMission complete. Data archived to: {output_filename}")
        
        return 0

    except Exception as e:
        logger.exception(f"Unexpected error during mission: {e}")
        print(f"Mission failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
