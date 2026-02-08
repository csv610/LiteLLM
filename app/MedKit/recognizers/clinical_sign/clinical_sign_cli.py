#!/usr/bin/env python3
"""
CLI for ClinicalSignIdentifier

Identify whether a given name is a recognized clinical sign in medical literature
"""

import argparse
import sys
from pathlib import Path


from lite.config import ModelConfig
from .clinical_sign_recognizer import ClinicalSignIdentifier


def create_parser():
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog="clinical_sign_identifier",
        description="Identify whether a given name is a recognized clinical sign in medical literature",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "example_clinical_sign"
  %(prog)s "example_clinical_sign" --model ollama/llama2
  %(prog)s "example_clinical_sign" --temperature 0.1
        """
    )
    
    # Positional argument
    parser.add_argument(
        "name",
        help=f"Name of the clinical sign to identify"
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
        identifier = ClinicalSignIdentifier(config)
        
        # Perform identification
        result = identifier.identify(args.name)
        
        # Output JSON result
        print(result.model_dump_json(indent=2))
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
