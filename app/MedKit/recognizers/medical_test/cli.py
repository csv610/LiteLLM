import argparse
from lite.config import ModelConfig
from .recognizer import MedicalTestIdentifier

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()
    
    identifier = MedicalTestIdentifier(ModelConfig(model="ollama/gemma3"))
    result = identifier.identify_test(args.name)
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
