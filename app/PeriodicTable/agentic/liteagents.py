"""
liteagents.py - Unified LiteClient-based agents for PeriodicTable.
"""

from app.PeriodicTable.shared.models import *
from app.PeriodicTable.shared.models import ElementInfo, ElementResponse, ModelOutput
from app.PeriodicTable.shared.utils import *
from lite import LiteClient, ModelConfig
from lite.config import ModelInput
from typing import Optional
import json
import logging

"""
periodic_table_element.py - PeriodicTableElement class for element information

Contains the PeriodicTableElement class for fetching and managing
periodic table element information with a 3-tier artifact-based approach.
"""

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

class PeriodicTableElement:
    """Class for fetching and managing periodic table element information."""
    
    def __init__(self, model_config: ModelConfig):
        """Initialize the element fetcher with a ModelConfig.
        
        Args:
            model_config: Configured ModelConfig for API calls
        """
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.logger = logging.getLogger(__name__)
    
    def fetch_element_info(self, element: str) -> Optional[ModelOutput]:
        """Fetch information for a single element using a 3-tier approach.
        
        Args:
            element: Name of the element to fetch information for
            
        Returns:
            ModelOutput object containing structured data and markdown synthesis.
        """
        try:
            self.logger.info(f"Fetching 3-tier info for element: {element}")

            # Tier 1: Specialist (JSON)
            prompt = f"Provide detailed technical information about the periodic table element {element}."
            model_input = ModelInput(user_prompt=prompt, response_format=ElementResponse)
            res = self.client.generate_text(model_input=model_input)
            element_data: ElementInfo = res.data.element

            # Tier 3: Output Synthesis (Markdown Closer)
            synth_prompt = f"Synthesize a beautiful, educational Markdown report for the element {element}.\n\nDATA:\n{element_data.model_dump_json(indent=2)}"
            synth_input = ModelInput(
                system_prompt="You are a Lead Science Editor. Synthesize raw element data into a professional and engaging Markdown report.",
                user_prompt=synth_prompt,
                response_format=None
            )
            final_markdown = self.client.generate_text(synth_input).markdown

            return ModelOutput(
                data=element_data,
                markdown=final_markdown,
                metadata={"process": "2-stage fetch-and-synthesize"}
            )
        except Exception as e:
            self.logger.error(f"Error fetching {element}: {str(e)}")
            return None
    
    def fetch_multiple_elements(self, elements: list[str]) -> dict[str, Optional[ModelOutput]]:
        """Fetch information for multiple elements."""
        results = {}
        for element in elements:
            results[element] = self.fetch_element_info(element)
        return results
    
    def validate_element_name(self, element: str, valid_elements: list[str]) -> bool:
        """Validate that an element name is in the list of valid elements."""
        return element in valid_elements
    
    def get_element_summary(self, element_info: ElementInfo) -> dict:
        """Get a summary dictionary of key element information."""
        return {
            "name": element_info.name,
            "symbol": element_info.symbol,
            "atomic_number": element_info.atomic_number,
            "atomic_mass": element_info.atomic_mass,
            "category": element_info.category,
            "period": element_info.period,
            "group": element_info.group,
            "block": element_info.block,
            "state": element_info.physical_characteristics.standard_state,
            "density": element_info.physical_characteristics.density,
            "melting_point": element_info.physical_characteristics.melting_point,
            "boiling_point": element_info.physical_characteristics.boiling_point
        }
    
    def get_uses_list(self, element_info: ElementInfo) -> list[str]:
        """Get the list of uses for an element."""
        return element_info.uses
    
    def get_properties_list(self, element_info: ElementInfo) -> list[str]:
        """Get the list of key properties for an element."""
        return element_info.properties
    
    def get_isotope_info(self, element_info: ElementInfo) -> Optional[list]:
        """Get isotope information for an element."""
        return element_info.isotopes
    
    def get_discovery_info(self, element_info: ElementInfo) -> dict:
        """Get discovery information for an element."""
        return {
            "discovered_by": element_info.discovered_by,
            "year_discovered": element_info.year_discovered
        }
    
    def get_safety_info(self, element_info: ElementInfo) -> Optional[str]:
        """Get safety and toxicity information for an element."""
        return element_info.toxicity_and_safety

