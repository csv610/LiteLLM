import argparse

from drug_recognizer import DrugIdentifier
from lite.config import ModelConfig


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()

    model_config = ModelConfig(model="ollama/gemma3")
    identifier = DrugIdentifier(model_config)
    result = identifier.identify_drug(args.name)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
