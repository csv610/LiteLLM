"""
periodic_table_models.py - Pydantic models for periodic table element data

Defines comprehensive data models for chemical elements with detailed physical,
chemical, and structural properties organized in hierarchical tiers.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class PhysicalCharacteristics(BaseModel):
    """Physical properties and state characteristics of an element"""
    standard_state: Optional[str] = Field(None, description="Standard state of the element at 25°C and 1 atm (solid, liquid, gas)")
    density: Optional[float] = Field(None, description="Density of the element (g/cm³ or g/L for gases)")
    melting_point: Optional[float] = Field(None, description="Melting point of the element (K)")
    boiling_point: Optional[float] = Field(None, description="Boiling point of the element (K)")
    appearance: Optional[str] = Field(None, description="Detailed visual description of the element")


class AtomicDimensions(BaseModel):
    """Atomic and molecular dimensions including various radius measurements"""
    atomic_radius: Optional[float] = Field(None, description="Atomic radius (pm)")
    covalent_radius: Optional[float] = Field(None, description="Covalent radius for bonded atoms (pm)")
    ionic_radius: Optional[float] = Field(None, description="Ionic radius when ionized (pm)")
    van_der_waals_radius: Optional[float] = Field(None, description="Van der Waals radius for non-bonded interactions (pm)")


class ChemicalCharacteristics(BaseModel):
    """Chemical reactivity and bonding properties of an element"""
    oxidation_states: Optional[str] = Field(None, description="Common oxidation states")
    reactivity: Optional[str] = Field(None, description="Reactivity description")
    electronegativity: Optional[float] = Field(None, description="Electronegativity value (Pauling scale)")
    electron_affinity: Optional[float] = Field(None, description="Electron affinity value (eV)")
    ionization_energy: Optional[float] = Field(None, description="First ionization energy (eV)")


class IsotopeInfo(BaseModel):
    """Information about isotopes of an element"""
    isotope: str = Field(..., description="Isotope notation (e.g., Au-197)")
    abundance: Optional[str] = Field(None, description="Natural abundance percentage or 'stable'")
    half_life: Optional[str] = Field(None, description="Half-life if radioactive, or 'stable' if not")


class ElementInfo(BaseModel):
    """Comprehensive information about a chemical element organized in hierarchical tiers"""
    
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
    electron_configuration_semantic: Optional[str] = Field(None, description="Abbreviated electron configuration (e.g., [Ne] 3s²)")

    # Tier 4: Physical Properties
    physical_characteristics: PhysicalCharacteristics = Field(..., description="Physical properties and state characteristics")
    atomic_dimensions: AtomicDimensions = Field(..., description="Atomic and molecular dimensions (various radius measurements)")

    # Tier 5: Chemical Properties
    chemical_characteristics: ChemicalCharacteristics = Field(..., description="Chemical reactivity and bonding properties")

    # Tier 6: Supplementary Scientific Data
    crystal_structure: Optional[str] = Field(None, description="Crystal lattice type the element forms (e.g., face-centered cubic)")
    magnetic_properties: Optional[str] = Field(None, description="Magnetic classification (diamagnetic, paramagnetic, ferromagnetic, etc.)")
    thermal_conductivity: Optional[float] = Field(None, description="Thermal conductivity (W/(m·K))")

    # Tier 7: Natural Occurrence & Abundance
    natural_occurrence: Optional[str] = Field(None, description="How the element is found in nature")
    abundance_in_earth_crust: Optional[float] = Field(None, description="Abundance in Earth's crust (percentage or ppm)")
    isotopes: Optional[List[IsotopeInfo]] = Field(None, description="Common and stable isotopes with abundance and half-life data")

    # Tier 8: Historical & Context
    discovered_by: Optional[str] = Field(None, description="Name(s) of the discoverer(s)")
    year_discovered: Optional[int] = Field(None, description="Year the element was discovered")

    # Tier 9: Applications & Safety
    uses: List[str] = Field(..., description="Common uses and applications of the element")
    properties: List[str] = Field(..., description="Key physical and chemical properties summary")
    toxicity_and_safety: Optional[str] = Field(None, description="Toxicity information and safety notes for handling and applications")


class ElementResponse(BaseModel):
    """Response wrapper for element information"""
    element: ElementInfo
