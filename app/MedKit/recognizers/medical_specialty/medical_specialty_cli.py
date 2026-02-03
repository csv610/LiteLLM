import argparse
from lite.config import ModelConfig
from .medical_specialty_recognizer import MedicalSpecialtyIdentifier

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()
    
    identifier = MedicalSpecialtyIdentifier(ModelConfig(model="ollama/gemma3"))
    result = identifier.identify(args.name)
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
