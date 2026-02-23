import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from dictionary_builder import DictionaryBuilder, configure_logging

# Configure logging at entry point
log_file = Path(__file__).parent / "logs" / "medical_dictionary.log"
configure_logging(str(log_file))
logger = logging.getLogger(__name__)

def main():
    # Add the current directory to sys.path to support relative imports
    sys.path.append(str(Path(__file__).parent))

    parser = argparse.ArgumentParser(description="Build medical dictionary definitions with LLM.")
    parser.add_argument("input", help="Medical term, or path to JSON/text file containing terms")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="The model to use (default: ollama/gemma3)")

    args = parser.parse_args()
    
    try:
        model_config = ModelConfig(model=args.model)
        builder = DictionaryBuilder(model_config)
        builder.generate_text(input_data=args.input)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
   main()
