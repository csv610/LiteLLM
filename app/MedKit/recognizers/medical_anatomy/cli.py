import argparse
import sys
from pathlib import Path

from lite.config import ModelConfig
from .recognizer import MedicalAnatomyIdentifier

def main():
    parser = argparse.ArgumentParser(description="Identify medical anatomy structures")
    parser.add_argument("name", help="Name of the anatomical structure to identify")
    args = parser.parse_args()
    
    identifier = MedicalAnatomyIdentifier(ModelConfig(model="ollama/gemma3"))
    result = identifier.identify_anatomy(args.name)
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
