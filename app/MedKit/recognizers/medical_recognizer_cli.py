#!/usr/bin/env python3
"""
Unified CLI for all MedKit recognizers.
Usage: python unified_cli.py <type> <name> [options]
Example: python unified_cli.py drug "Aspirin"
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to sys.path to allow imports from .
sys.path.append(str(Path(__file__).parent))

from lite.config import ModelConfig
from .recognizer_factory import RecognizerFactory

def create_parser():
    # Force registration by listing available
    available_types = RecognizerFactory.list_available()
    
    parser = argparse.ArgumentParser(
        prog="medical_recognizer_cli.py",
        description="Unified CLI for medical entity identification",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "type",
        choices=available_types,
        help="Type of medical entity to identify"
    )
    
    parser.add_argument(
        "name",
        help="Name of the entity to identify"
    )
    
    parser.add_argument(
        "--model", "-m",
        default="ollama/gemma3",
        help="Model to use (default: ollama/gemma3)"
    )
    
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        default=0.2,
        help="Temperature for model generation (default: 0.2)"
    )
    
    parser.add_argument(
        "--structured", "-s",
        action="store_true",
        help="Use structured output (JSON)"
    )

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        config = ModelConfig(
            model=args.model,
            temperature=args.temperature
        )
        
        recognizer = RecognizerFactory.get(args.type, config)
        
        # All refactored recognizers now have the identify() method
        result = recognizer.identify(args.name, structured=args.structured)

        if args.structured and hasattr(result, 'model_dump_json'):
            print(result.model_dump_json(indent=2))
        else:
            # Handle ModelOutput with markdown/data
            if hasattr(result, 'markdown') and result.markdown:
                print(result.markdown)
            elif hasattr(result, 'data') and result.data:
                if hasattr(result.data, 'model_dump_json'):
                    print(result.data.model_dump_json(indent=2))
                else:
                    print(result.data)
            else:
                print(result)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
