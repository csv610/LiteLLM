"""Organ-specific Disease Information Generator CLI."""

import argparse
import logging
from pathlib import Path
from tqdm import tqdm

from lite.config import ModelConfig
from lite.logging_config import configure_logging
from .organ_disease_info import DiseaseInfoGenerator

logger = logging.getLogger(__name__)

def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate comprehensive disease information based on an organ.")
    parser.add_argument("organ", help="Organ name or file path containing organs.")
    parser.add_argument("-d", "--output-dir", default="outputs", help="Output directory.")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Verbosity level.")
    parser.add_argument("-s", "--structured", action="store_true", help="Use structured output.")
    return parser.parse_args()

def main():
    args = get_user_arguments()
    configure_logging(log_file="organ_disease.log", verbosity=args.verbosity, enable_console=True)
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.organ)
    items = [line.strip() for line in open(input_path)] if input_path.is_file() else [args.organ]
    
    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = DiseaseInfoGenerator(model_config)
        
        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(organ=item, structured=args.structured)
            if result:
                generator.save(result, output_dir)
            
        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
