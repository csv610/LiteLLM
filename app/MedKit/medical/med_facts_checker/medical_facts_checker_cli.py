import json
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.config import ModelConfig

from medical_facts_checker import MedicalFactsChecker

def get_user_arguments():
    parser = argparse.ArgumentParser(
        description="Analyze statements and determine if they are fact or fiction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default output to console
  python medical_facts_checker.py -i "The Earth is round"

  # Custom output path
  python medical_facts_checker.py -i "Gravity causes objects to fall" -o gravity_analysis.json
        """
    )
    parser.add_argument("-i", "--statement", required=True, help="Statement to analyze")
    parser.add_argument("-o", "--output", type=Path, help="Path to save JSON output.")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use (default: gemini-1.5-pro)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level")
    parser.add_argument("-s", "--structured", action="store_true", default=False, help="Use structured output (Pydantic model) for the response.")

    return parser.parse_args()
   
def create_medical_fact_check_report(args):

    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        checker = MedicalFactsChecker(model_config=model_config)
        print("Starting evaluation...")
        result = checker.generate_text(statement=args.statement, structured=args.structured)
        print (result)
        
        if args.output:
            output_dir = Path("output")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / args.output.name

            if isinstance(result, str) and output_path.suffix == ".json":
                output_path = output_path.with_suffix(".md")
            save_model_response(result, output_path)
            print(f"✓ Results saved to {output_path}")

    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    args = get_user_arguments()
    create_medical_fact_check_report(args)
