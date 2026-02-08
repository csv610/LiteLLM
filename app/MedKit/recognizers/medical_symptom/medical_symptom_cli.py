#!/usr/bin/env python3
"""
CLI for MedicalSymptomIdentifier

Identify whether a given name is a recognized medical symptom in medical literature
"""

import argparse
import sys
from pathlib import Path


from lite.config import ModelConfig
from medical_symptom_identifier import MedicalSymptomIdentifier


def create_parser():
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog="medical_symptom_identifier",
        description="Identify whether a given name is a recognized medical symptom in medical literature",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "example_medical_symptom"
  %(prog)s "example_medical_symptom" --model ollama/llama2
  %(prog)s "example_medical_symptom" --temperature 0.1
        """
    )
    
    # Positional argument
    parser.add_argument(
        "name",
        help=f"Name of the medical symptom to identify"
    )
    
    # Model configuration options
    parser.add_argument(
        "--model", "-m",
        default="ollama/gemma3",
        help="Model to use for identification (default: ollama/gemma3)"
    )
    
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        default=0.2,
        help="Temperature for model generation (default: 0.2)"
    )
    
    return parser


def main():
    """Main CLI function."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # Create model configuration
        config = ModelConfig(
            model=args.model,
            temperature=args.temperature
        )
        
        # Initialize identifier
        identifier = MedicalSymptomIdentifier(config)
        
        # Perform identification
        result = identifier.identify(args.name)

        print(result)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
