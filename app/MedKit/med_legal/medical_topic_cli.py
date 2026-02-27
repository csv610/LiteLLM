"""Patient Legal Rights Information Generator CLI."""

import argparse
import logging
from pathlib import Path
from tqdm import tqdm

from lite.config import ModelConfig
from lite.logging_config import configure_logging
from medical_topic import LegalRightsGenerator

logger = logging.getLogger(__name__)

def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate comprehensive information on patient legal rights.")
    parser.add_argument("topic", help="Legal right topic (e.g., 'Informed Consent') or file path containing topics.")
    parser.add_argument("-c", "--country", default="India", help="The country/jurisdiction for the legal rights (e.g., 'USA', 'UK', 'India'). Default is India.")
    parser.add_argument("-d", "--output-dir", default="outputs", help="Output directory.")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Verbosity level.")
    parser.add_argument("-s", "--structured", action="store_true", help="Use structured output.")
    parser.add_argument("-u", "--user-name", default="anonymous", help="Name of the user for the filename.")
    return parser.parse_args()

def main():
    args = get_user_arguments()
    configure_logging(log_file="medical_topic.log", verbosity=args.verbosity, enable_console=True)
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.topic)
    items = [line.strip() for line in open(input_path)] if input_path.is_file() else [args.topic]
    
    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = LegalRightsGenerator(model_config)
        
        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(topic=item, country=args.country, structured=args.structured)
            if result: generator.save(result, output_dir, user_name=args.user_name)
            
        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
