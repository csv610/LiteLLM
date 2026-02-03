import argparse
from lite.config import ModelConfig
from .drug_recognizer import DrugIdentifier

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()
    
    identifier = DrugIdentifier(ModelConfig(model="ollama/gemma3"))
    result = identifier.identify_drug(args.name)
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
