import sys
import json
import argparse
from pathlib import Path
from tqdm import tqdm

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

from periodic_table_models import (
    PhysicalCharacteristics, AtomicDimensions, ChemicalCharacteristics,
    IsotopeInfo, ElementInfo, ElementResponse
)


# List of all 118 elements by atomic number
ALL_ELEMENTS = [
    "Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon", "Nitrogen", "Oxygen",
    "Fluorine", "Neon", "Sodium", "Magnesium", "Aluminum", "Silicon", "Phosphorus", "Sulfur",
    "Chlorine", "Argon", "Potassium", "Calcium", "Scandium", "Titanium", "Vanadium", "Chromium",
    "Manganese", "Iron", "Cobalt", "Nickel", "Copper", "Zinc", "Gallium", "Germanium",
    "Arsenic", "Selenium", "Bromine", "Krypton", "Rubidium", "Strontium", "Yttrium", "Zirconium",
    "Niobium", "Molybdenum", "Technetium", "Ruthenium", "Rhodium", "Palladium", "Silver", 
    "Cadmium", "Indium", "Tin", "Antimony", "Tellurium", "Iodine", "Xenon", "Cesium", "Barium",
    "Lanthanum", "Cerium", "Praseodymium", "Neodymium", "Promethium", "Samarium", "Europium", 
    "Gadolinium", "Terbium", "Dysprosium", "Holmium", "Erbium", "Thulium", "Ytterbium", 
    "Lutetium", "Hafnium", "Tantalum", "Tungsten", "Rhenium", "Osmium", "Iridium", "Platinum", 
    "Gold", "Mercury", "Thallium", "Lead", "Bismuth", "Polonium", "Astatine", "Radon", 
    "Francium", "Radium", "Actinium", "Thorium", "Protactinium", "Uranium", "Neptunium", 
    "Plutonium", "Americium", "Curium", "Berkelium", "Californium", "Einsteinium", "Fermium", 
    "Mendelevium", "Nobelium", "Lawrencium", "Rutherfordium", "Dubnium", "Seaborgium", 
    "Bohrium", "Hassium", "Meitnerium", "Darmstadtium", "Roentgenium", "Copernicium",
    "Nihonium", "Flerovium", "Moscovium", "Livermorium", "Tennessine", "Oganesson"
]

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


def fetch_element_info(element: str, client: LiteClient) -> ElementInfo | None:
    """Fetch information for a single element."""
    try:
        prompt = f"Provide detailed information about the periodic table element {element}."
        model_input = ModelInput(user_prompt=prompt, response_format=ElementResponse)
        response_content = client.generate_text(model_input=model_input)

        if isinstance(response_content, ElementResponse):
            return response_content.element
        elif isinstance(response_content, str):
            data = json.loads(response_content)
            return ElementInfo(**data.get("element", {}))
        return None
    except Exception as e:
        tqdm.write(f"Error fetching {element}: {str(e)}", file=sys.stderr)
        return None


def element_info_cli():
    """Fetch information for periodic table elements."""
    args = arguments_parser()

    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    model_config = ModelConfig(model=args.model, temperature=args.temperature)
    client = LiteClient(model_config=model_config)

    # Fetch specific element or all elements
    if args.element:
        # Fetch specific element
        element = args.element.capitalize()
        if element not in ALL_ELEMENTS:
            print(f"Error: '{args.element}' is not a valid element. Use one of: {', '.join(ALL_ELEMENTS)}", file=sys.stderr)
            sys.exit(1)

        element_info = fetch_element_info(element, client)

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
            element_info = fetch_element_info(element, client)

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
