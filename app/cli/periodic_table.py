import sys
import json
import argparse
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydantic import BaseModel, Field
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput


class PhysicalCharacteristics(BaseModel):
    standard_state: str | None = Field(None, description="Standard state of the element at 25°C and 1 atm (solid, liquid, gas)")
    density: float | None = Field(None, description="Density of the element (g/cm³ or g/L for gases)")
    melting_point: float | None = Field(None, description="Melting point of the element (K)")
    boiling_point: float | None = Field(None, description="Boiling point of the element (K)")
    appearance: str | None = Field(None, description="Detailed visual description of the element")


class AtomicDimensions(BaseModel):
    atomic_radius: float | None = Field(None, description="Atomic radius (pm)")
    covalent_radius: float | None = Field(None, description="Covalent radius for bonded atoms (pm)")
    ionic_radius: float | None = Field(None, description="Ionic radius when ionized (pm)")
    van_der_waals_radius: float | None = Field(None, description="Van der Waals radius for non-bonded interactions (pm)")


class ChemicalCharacteristics(BaseModel):
    oxidation_states: str | None = Field(None, description="Common oxidation states")
    reactivity: str | None = Field(None, description="Reactivity description")
    electronegativity: float | None = Field(None, description="Electronegativity value (Pauling scale)")
    electron_affinity: float | None = Field(None, description="Electron affinity value (eV)")
    ionization_energy: float | None = Field(None, description="First ionization energy (eV)")


class IsotopeInfo(BaseModel):
    isotope: str = Field(..., description="Isotope notation (e.g., Au-197)")
    abundance: str | None = Field(None, description="Natural abundance percentage or 'stable'")
    half_life: str | None = Field(None, description="Half-life if radioactive, or 'stable' if not")

class ElementInfo(BaseModel):
    # Tier 1: Core Identification
    atomic_number: int = Field(..., description="Atomic number (number of protons)")
    symbol: str = Field(..., description="Chemical symbol of the element (1-2 letters)")
    name: str = Field(..., description="Full name of the element")
    atomic_mass: float = Field(..., description="Atomic mass of the element (u)")

    # Tier 2: Periodic Table Position & Classification
    period: int = Field(..., description="Period (row) in the periodic table (1-7)")
    group: str = Field(..., description="Group (column) in the periodic table (1-18)")
    block: str = Field(..., description="Orbital block (s, p, d, or f)")
    category: str = Field(..., description="Element category (e.g., alkali metal, halogen, noble gas, transition metal)")

    # Tier 3: Electronic Structure
    electron_configuration: str = Field(..., description="Full electron configuration (e.g., 1s² 2s² 2p⁶)")
    electron_configuration_semantic: str | None = Field(None, description="Abbreviated electron configuration (e.g., [Ne] 3s²)")

    # Tier 4: Physical Properties
    physical_characteristics: PhysicalCharacteristics = Field(..., description="Physical properties and state characteristics")
    atomic_dimensions: AtomicDimensions = Field(..., description="Atomic and molecular dimensions (various radius measurements)")

    # Tier 5: Chemical Properties
    chemical_characteristics: ChemicalCharacteristics = Field(..., description="Chemical reactivity and bonding properties")

    # Tier 6: Supplementary Scientific Data
    crystal_structure: str | None = Field(None, description="Crystal lattice type the element forms (e.g., face-centered cubic)")
    magnetic_properties: str | None = Field(None, description="Magnetic classification (diamagnetic, paramagnetic, ferromagnetic, etc.)")
    thermal_conductivity: float | None = Field(None, description="Thermal conductivity (W/(m·K))")

    # Tier 7: Natural Occurrence & Abundance
    natural_occurrence: str | None = Field(None, description="How the element is found in nature")
    abundance_in_earth_crust: float | None = Field(None, description="Abundance in Earth's crust (percentage or ppm)")
    isotopes: list[IsotopeInfo] | None = Field(None, description="Common and stable isotopes with abundance and half-life data")

    # Tier 8: Historical & Context
    discovered_by: str | None = Field(None, description="Name(s) of the discoverer(s)")
    year_discovered: int | None = Field(None, description="Year the element was discovered")

    # Tier 9: Applications & Safety
    uses: list[str] = Field(..., description="Common uses and applications of the element")
    properties: list[str] = Field(..., description="Key physical and chemical properties summary")
    toxicity_and_safety: str | None = Field(None, description="Toxicity information and safety notes for handling and applications")


class ElementResponse(BaseModel):
    element: ElementInfo


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

def fetch_element_info(element: str, client: LiteClient) -> ElementInfo | None:
    """Fetch information for a single element."""
    try:
        prompt = f"Provide detailed information about the periodic table element {element}."
        model_input = ModelInput(user_prompt=prompt, response_format=ElementResponse)
        response_content = client.generate_text(model_input=model_input)

        if isinstance(response_content, str):
            data = json.loads(response_content)
            return ElementInfo(**data.get("element", {}))
        return None
    except Exception as e:
        print(f"Error fetching {element}: {str(e)}", file=sys.stderr)
        return None


def main():
    """Fetch information for periodic table elements."""
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
        default="gemini/gemini-2.5-flash",
        help="Model to use (default: gemini/gemini-2.5-flash)"
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

    args = parser.parse_args()

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

        print(f"Fetching {element}...", file=sys.stderr)
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

        print(f"Fetching information for {len(ALL_ELEMENTS)} elements...", file=sys.stderr)

        for i, element in enumerate(ALL_ELEMENTS, 1):
            print(f"[{i}/{len(ALL_ELEMENTS)}] Fetching {element}...", file=sys.stderr)
            element_info = fetch_element_info(element, client)

            if element_info:
                # Save individual element file
                output = {"element": element_info.model_dump()}
                output_file = output_dir / f"{element}.json"
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(output, f, indent=2, ensure_ascii=False)
                all_elements_data.append(element_info.model_dump())
            else:
                print(f"Failed to fetch {element}", file=sys.stderr)

        # Output all elements as a single JSON file
        output = {"elements": all_elements_data, "total_count": len(all_elements_data)}
        output_file = output_dir / "all_elements.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Saved to {output_file}", file=sys.stderr)


if __name__ == "__main__":
    main()
