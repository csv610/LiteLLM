#!/usr/bin/env python3
"""
CLI for generating patient legal rights information.
"""

import argparse
import logging
import sys
from pathlib import Path

from lite.config import ModelConfig
from lite.logging_config import configure_logging

try:
    from med_legal.nonagentic.legal_rights import LegalRightsGenerator
except (ImportError, ValueError):
    from legal_rights import LegalRightsGenerator

def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive patient legal rights information.")
    parser.add_argument(
        "--topic",
        type=str,
        required=True,
        help="The legal right topic or a description of a patient situation.",
    )
    parser.add_argument(
        "--country",
        type=str,
        required=True,
        help="The jurisdiction/country to focus on.",
    )
    parser.add_argument(
        "--structured",
        action="store_true",
        help="Generate structured JSON output instead of plain text.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd() / "output",
        help="Directory to save the generated output.",
    )
    parser.add_argument(
        "--user-name",
        type=str,
        default="anonymous",
        help="User name for naming the output file.",
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="gemini",
        help="The LLM provider to use (e.g., gemini, openai).",
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default="gemini-2.5-flash",
        help="The specific model name to use.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="The temperature parameter for the model.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level.",
    )

    args = parser.parse_args()

    # Configure logging
    configure_logging(level=getattr(logging, args.log_level))
    logger = logging.getLogger(__name__)

    try:
        # Create output directory if it doesn't exist
        args.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize model config
        model_config = ModelConfig(
            provider=args.provider,
            model_name=args.model_name,
            temperature=args.temperature,
        )

        # Initialize generator
        generator = LegalRightsGenerator(model_config=model_config)

        # Generate text
        logger.info(f"Generating legal rights info for topic: '{args.topic}' in '{args.country}'...")
        result = generator.generate_text(
            topic=args.topic,
            country=args.country,
            structured=args.structured
        )

        # Save result
        output_file = generator.save(
            result=result,
            output_dir=args.output_dir,
            user_name=args.user_name
        )
        
        logger.info(f"Successfully saved generated legal rights info to: {output_file}")
        print(f"File saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"Failed to generate legal rights info: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
