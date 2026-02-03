import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging

from medical_anatomy_identifier import MedicalAnatomyIdentifier

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Identify medical anatomy terms and structures.")
    parser.add_argument("-i", "--name", type=str, required=True, help="Medical anatomy term to identify.")
    parser.add_argument("-d", "--output-dir", type=str, default="outputs", help="Directory for output files (default: outputs).")
    parser.add_argument("-m", "--model", type=str, default="ollama/gemma3", help="Model to use for generation (default: ollama/gemma3).")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Logging verbosity level: 0=CRITICAL, 1=ERROR, 2=WARNING, 3=INFO, 4=DEBUG (default: 2).")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")
    
    return parser.parse_args()


def main():
    """Main CLI function."""
    args = get_user_arguments()
    
    # Configure logging
    configure_logging(
        log_file=str(Path(__file__).parent / "logs" / "medical_anatomy_identifier.log"),
        verbosity=args.verbosity,
        enable_console=True
    )
    
    logger.info(f"Identifying medical anatomy: {args.name}")
    
    try:
        # Initialize the identifier
        model_config = ModelConfig(model=args.model, temperature=0.2)
        identifier = MedicalAnatomyIdentifier(model_config)
        
        # Generate identification
        result = identifier.identify(args.name, structured=args.structured)
        
        if result is None:
            logger.error("✗ Failed to identify medical anatomy.")
            return 1
        
        # Output result
        print(result.model_dump_json(indent=2))
        logger.info("✓ Medical anatomy identification completed successfully.")
        
        # Save to file if output directory specified
        if args.output_dir:
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_file = output_dir / f"{args.name.lower().replace(' ', '_')}_anatomy.json"
            with open(output_file, 'w') as f:
                f.write(result.model_dump_json(indent=2))
            logger.info(f"✓ Result saved to: {output_file}")
        
        return 0
        
    except Exception as e:
        logger.error(f"✗ Error during medical anatomy identification: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())
