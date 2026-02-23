"""Medical Specialist Referral CLI."""

import argparse
import logging
from pathlib import Path
from tqdm import tqdm

from lite.config import ModelConfig
from lite.logging_config import configure_logging
from .med_refer import MedReferral

logger = logging.getLogger(__name__)

def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recommend medical specialists based on symptoms.")
    parser.add_argument("question", help="Symptoms or file path containing questions.")
    parser.add_argument("-d", "--output-dir", default="outputs", help="Output directory.")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Verbosity level.")
    return parser.parse_args()

def main():
    args = get_user_arguments()
    configure_logging(log_file="med_refer.log", verbosity=args.verbosity, enable_console=True)
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.question)
    items = [line.strip() for line in open(input_path)] if input_path.is_file() else [args.question]
    
    try:
        model_config = ModelConfig(model=args.model, temperature=0.0)
        med_referral = MedReferral(model_config)
        
        for item in tqdm(items, desc="Recommending"):
            result = med_referral.generate_text(item)
            if result and not result.startswith("Error"):
                fname = "".join([c if c.isalnum() else "_" for c in item.lower()])[:50]
                with open(output_dir / f"{fname}.md", "w") as f:
                    f.write(result)
            
        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
