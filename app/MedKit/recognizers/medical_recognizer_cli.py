#!/usr/bin/env python3
"""
Unified CLI for all MedKit recognizers.
Usage: python unified_cli.py <type> <name> [options]
Example: python unified_cli.py drug "Aspirin"
"""

import argparse
import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from lite.config import ModelConfig
from recognizers.recognizer_factory import RecognizerFactory

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
        choices=available_types + ["list"],
        help="Type of medical entity to identify or 'list' to see all available types"
    )
    
    parser.add_argument(
        "name",
        nargs="?",
        help="Name of the entity to identify (not required for 'list' command)"
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
    
    if args.type == "list":
        available_types = RecognizerFactory.list_available()
        print("\n🔍 Available Medical Entity Recognizers:\n")
        for i, r_type in enumerate(sorted(available_types), 1):
            print(f"  {i}. {r_type}")
        print("\nUsage: medkit-recognizer <type> <name> [options]\n")
        return

    if not args.name:
        parser.error("the following arguments are required: name")

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
