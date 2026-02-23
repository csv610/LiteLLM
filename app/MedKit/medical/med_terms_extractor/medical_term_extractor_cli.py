"""Medical Term Extractor CLI."""

import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging
from .medical_term_extractor import MedicalTermExtractor

logger = logging.getLogger(__name__)

def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract medical terms from text or a file.")
    parser.add_argument("input", help="Input text or file path containing text.")
    parser.add_argument("-d", "--output-dir", default="outputs", help="Output directory.")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Verbosity level.")
    parser.add_argument("-s", "--structured", action="store_true", help="Use structured output.")
    return parser.parse_args()

def main():
    args = get_user_arguments()
    configure_logging(log_file="medical_term_extractor.log", verbosity=args.verbosity, enable_console=True)
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.input)
    input_text = open(input_path).read() if input_path.is_file() else args.input
    
    try:
        model_config = ModelConfig(model=args.model, temperature=0.1)
        extractor = MedicalTermExtractor(model_config)
        
        logger.info("Extracting medical terms...")
        result = extractor.generate_text(input_text, structured=args.structured)
        if result: extractor.save(result, output_dir)
            
        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
