"""
periodic_table_element.py - PeriodicTableElement class for element information

Contains the PeriodicTableElement class for fetching and managing
periodic table element information with comprehensive data validation.
"""

import json
import logging
from typing import Optional

from lite import LiteClient, ModelConfig
from lite.config import ModelInput

from periodic_table_models import ElementInfo, ElementResponse


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
    
    def fetch_element_info(self, element: str) -> Optional[ElementInfo]:
        """Fetch information for a single element.
        
        Args:
            element: Name of the element to fetch information for
            
        Returns:
            ElementInfo object with detailed element data, or None if failed
        """
        try:
            prompt = f"Provide detailed information about the periodic table element {element}."
            model_input = ModelInput(user_prompt=prompt, response_format=ElementResponse)
            response_content = self.client.generate_text(model_input=model_input)

            if isinstance(response_content, ElementResponse):
                return response_content.element
            elif isinstance(response_content, str):
                data = json.loads(response_content)
                return ElementInfo(**data.get("element", {}))
            return None
        except Exception as e:
            self.logger.error(f"Error fetching {element}: {str(e)}")
            return None
    
    def fetch_multiple_elements(self, elements: list[str]) -> dict[str, Optional[ElementInfo]]:
        """Fetch information for multiple elements.
        
        Args:
            elements: List of element names to fetch information for
            
        Returns:
            Dictionary mapping element names to ElementInfo objects (or None if failed)
        """
        results = {}
        for element in elements:
            results[element] = self.fetch_element_info(element)
        return results
    
    def validate_element_name(self, element: str, valid_elements: list[str]) -> bool:
        """Validate that an element name is in the list of valid elements.
        
        Args:
            element: Element name to validate
            valid_elements: List of valid element names
            
        Returns:
            True if element is valid, False otherwise
        """
        return element in valid_elements
    
    def get_element_summary(self, element_info: ElementInfo) -> dict:
        """Get a summary dictionary of key element information.
        
        Args:
            element_info: ElementInfo object containing full element data
            
        Returns:
            Dictionary with key element information
        """
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
        """Get the list of uses for an element.
        
        Args:
            element_info: ElementInfo object containing full element data
            
        Returns:
            List of element uses
        """
        return element_info.uses
    
    def get_properties_list(self, element_info: ElementInfo) -> list[str]:
        """Get the list of key properties for an element.
        
        Args:
            element_info: ElementInfo object containing full element data
            
        Returns:
            List of element properties
        """
        return element_info.properties
    
    def get_isotope_info(self, element_info: ElementInfo) -> Optional[list]:
        """Get isotope information for an element.
        
        Args:
            element_info: ElementInfo object containing full element data
            
        Returns:
            List of isotope information or None if not available
        """
        return element_info.isotopes
    
    def get_discovery_info(self, element_info: ElementInfo) -> dict:
        """Get discovery information for an element.
        
        Args:
            element_info: ElementInfo object containing full element data
            
        Returns:
            Dictionary with discovery information
        """
        return {
            "discovered_by": element_info.discovered_by,
            "year_discovered": element_info.year_discovered
        }
    
    def get_safety_info(self, element_info: ElementInfo) -> Optional[str]:
        """Get safety and toxicity information for an element.
        
        Args:
            element_info: ElementInfo object containing full element data
            
        Returns:
            Safety information string or None if not available
        """
        return element_info.toxicity_and_safety
