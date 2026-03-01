"""Patient Medical History Questions Generator CLI."""

import sys
from pathlib import Path
# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


import argparse
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging
try:
    from .patient_medical_history import PatientMedicalHistoryGenerator
except (ImportError, ValueError):
    from medical.med_history.patient_medical_history import PatientMedicalHistoryGenerator
try:
    from .patient_medical_history_prompts import MedicalHistoryInput
except (ImportError, ValueError):
    from medical.med_history.patient_medical_history_prompts import MedicalHistoryInput

logger = logging.getLogger(__name__)

def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate patient medical history questions.")
    parser.add_argument("-e", "--exam", required=True, help="Type of medical exam.")
    parser.add_argument("-a", "--age", type=int, required=True, help="Patient age.")
    parser.add_argument("-g", "--gender", required=True, help="Patient gender.")
    parser.add_argument("-p", "--purpose", default="physical_exam", help="Purpose of medical history.")
    parser.add_argument("-d", "--output-dir", default="outputs", help="Output directory.")
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument("-v", "--verbosity", type=int, default=2, choices=[0, 1, 2, 3, 4], help="Verbosity level.")
    parser.add_argument("-s", "--structured", action="store_true", help="Use structured output.")
    return parser.parse_args()

def main():
    args = get_user_arguments()
    configure_logging(log_file="patient_medical_history.log", verbosity=args.verbosity, enable_console=True)
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        model_config = ModelConfig(model=args.model, temperature=0.3)
        generator = PatientMedicalHistoryGenerator(model_config)
        
        input_data = MedicalHistoryInput(
            exam=args.exam,
            age=args.age,
            gender=args.gender,
            purpose=args.purpose
        )
        
        logger.info(f"Generating questions for {args.exam} exam...")
        result = generator.generate_text(input_data, structured=args.structured)
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
