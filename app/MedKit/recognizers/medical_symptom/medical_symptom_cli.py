import argparse
from lite.config import ModelConfig
from .medical_symptom_recognizer import MedicalSymptomIdentifier

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()
    
    identifier = MedicalSymptomIdentifier(ModelConfig(model="ollama/gemma3"))
    result = identifier.identify(args.name)
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
