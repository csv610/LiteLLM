import sys
import json
import argparse
from pathlib import Path
from tqdm import tqdm

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging

from periodic_table_models import (
    PhysicalCharacteristics, AtomicDimensions, ChemicalCharacteristics,
    IsotopeInfo, ElementInfo, ElementResponse
)
from periodic_table_element import PeriodicTableElement, ALL_ELEMENTS

def arguments_parser():
    """Parse command-line arguments for the element info CLI."""
    parser = argparse.ArgumentParser(
        description="Fetch periodic table element information"
    )
    parser.add_argument(
        "-e", "--element",
        type=str,
        help="Specific element name to fetch (e.g., 'Hydrogen', 'Gold')"
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default="ollama/gemma3:12b",
        help="Model to use (default: ollama/gemma3:12b)"
    )
    parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=0.2,
        help="Temperature for model (default: 0.2)"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=".",
        help="Output directory for JSON files (default: current directory)"
    )
    return parser.parse_args()


def fetch_element_info(element: str, model_config: ModelConfig) -> ElementInfo | None:
    """Fetch information for a single element."""
    # Initialize element fetcher with model config
    element_fetcher = PeriodicTableElement(model_config)
    
    # Fetch element information using the element fetcher
    return element_fetcher.fetch_element_info(element)


def element_info_cli():
    """Fetch information for periodic table elements."""
    configure_logging()
    args = arguments_parser()

    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_config = ModelConfig(model=args.model, temperature=args.temperature)

    # Fetch specific element or all elements
    if args.element:
        # Fetch specific element
        element = args.element.capitalize()
        if element not in ALL_ELEMENTS:
            print(f"Error: '{args.element}' is not a valid element. Use one of: {', '.join(ALL_ELEMENTS)}", file=sys.stderr)
            sys.exit(1)

        element_info = fetch_element_info(element, model_config)

        if element_info:
            output = {"element": element_info.model_dump()}
            output_file = output_dir / f"{element}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            print(f"Saved to {output_file}", file=sys.stderr)
        else:
            print(f"Failed to fetch {element}", file=sys.stderr)
            sys.exit(1)
    else:
        # Fetch all elements
        all_elements_data = []
        failed_elements = []

        for element in tqdm(ALL_ELEMENTS, desc="Fetching elements", unit="element"):
            element_info = fetch_element_info(element, model_config)

            if element_info:
                # Save individual element file
                output = {"element": element_info.model_dump()}
                output_file = output_dir / f"{element}.json"
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(output, f, indent=2, ensure_ascii=False)
                all_elements_data.append(element_info.model_dump())

                # Save consolidated file after each element
                consolidated_output = {"elements": all_elements_data, "total_count": len(all_elements_data)}
                consolidated_file = output_dir / "all_elements.json"
                with open(consolidated_file, "w", encoding="utf-8") as f:
                    json.dump(consolidated_output, f, indent=2, ensure_ascii=False)
            else:
                failed_elements.append(element)

        # Print summary
        print(f"\nCompleted: {len(all_elements_data)}/{len(ALL_ELEMENTS)} elements fetched", file=sys.stderr)
        if failed_elements:
            print(f"Failed: {len(failed_elements)} elements", file=sys.stderr)
            print(f"Failed elements: {', '.join(failed_elements)}", file=sys.stderr)


if __name__ == "__main__":
    element_info_cli()
