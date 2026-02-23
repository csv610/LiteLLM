"""Medical Quiz Generator CLI."""

import argparse
import logging
from pathlib import Path
from tqdm import tqdm

from lite.config import ModelConfig
from lite.logging_config import configure_logging
from .medical_quiz import MedicalQuizGenerator

logger = logging.getLogger(__name__)

def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate comprehensive medical quizzes.")
    parser.add_argument("topic", help="Medical topic or file path containing topics.")
    parser.add_argument("-d", "--output-dir", default="outputs", help="Output directory.")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Logging verbosity level.")
    parser.add_argument("--difficulty", default="Intermediate", help="Quiz difficulty.")
    parser.add_argument("--num-questions", type=int, default=5, help="Number of questions.")
    parser.add_argument("--num-options", type=int, default=4, help="Number of options per question.")
    return parser.parse_args()

def main():
    args = get_user_arguments()
    configure_logging(log_file="medical_quiz.log", verbosity=args.verbosity, enable_console=True)
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.topic)
    items = [line.strip() for line in open(input_path)] if input_path.is_file() else [args.topic]
    
    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = MedicalQuizGenerator(model_config)
        
        for item in tqdm(items, desc="Generating Quizzes"):
            result = generator.generate_text(
                topic=item, 
                difficulty=args.difficulty, 
                num_questions=args.num_questions, 
                num_options=args.num_options,
                structured=True
            )
            if result: generator.save(result, output_dir)
            
        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
