"""
wikipedia_equations.py - Important mathematical equations from Wikipedia

Contains a curated collection of equations that appear on Wikipedia's
"List of important equations" and other mathematical reference lists.
"""

from typing import List, Dict
from enum import Enum

from well_known_equations import Equation, EquationCategory


class WikipediaImportance(Enum):
    """Importance level of equations on Wikipedia"""
    HIGHEST = "Highest"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class WikiEquation:
    """Represents an equation from Wikipedia's important equations list"""
    
    def __init__(self, name: str, latex: str, field: str, 
                 description: str, importance: WikipediaImportance,
                 year: str = "", discoverer: str = ""):
        self.name = name
        self.latex = latex
        self.field = field
        self.description = description
        self.importance = importance
        self.year = year
        self.discoverer = discoverer
    
    def to_dict(self) -> Dict:
        """Convert equation to dictionary format"""
        return {
            "name": self.name,
            "latex": self.latex,
            "field": self.field,
            "description": self.description,
            "importance": self.importance.value,
            "year": self.year,
            "discoverer": self.discoverer
        }


# ============================================================================
# WIKIPEDIA IMPORTANT EQUATIONS
# ============================================================================

# From Wikipedia's "List of important equations" and related mathematical reference lists

WIKIPEDIA_EQUATIONS = [
    # Fundamental Laws
    WikiEquation(
        "Pythagorean Theorem",
        r"a^2 + b^2 = c^2",
        "Geometry",
        "Fundamental relationship in Euclidean geometry between sides of right triangle",
        WikipediaImportance.HIGHEST,
        "570-495 BCE",
        "Pythagoras"
    ),
    WikiEquation(
        "Logarithm",
        r"\log_b(x) = \frac{\log_k(x)}{\log_k(b)}",
        "Algebra",
        "Inverse operation to exponentiation, fundamental to information theory",
        WikipediaImportance.HIGH,
        "17th century",
        "John Napier"
    ),
    WikiEquation(
        "Euler's Identity",
        r"e^{i\pi} + 1 = 0",
        "Complex Analysis",
        "Fundamental relationship between exponential, trigonometric, and complex numbers",
        WikipediaImportance.HIGHEST,
        "1748",
        "Leonhard Euler"
    ),
    WikiEquation(
        "Fundamental Theorem of Calculus",
        r"\int_a^b f'(x) dx = f(b) - f(a)",
        "Calculus",
        "Connects differentiation and integration, foundational theorem of calculus",
        WikipediaImportance.HIGHEST,
        "17th century",
        "Isaac Newton & Gottfried Leibniz"
    ),
    WikiEquation(
        "Bayes' Theorem",
        r"P(A|B) = \frac{P(B|A)P(A)}{P(B)}",
        "Probability",
        "Describes conditional probability, fundamental to Bayesian inference",
        WikipediaImportance.HIGH,
        "18th century",
        "Thomas Bayes"
    ),
    
    # Physics Equations
    WikiEquation(
        "Newton's Second Law",
        r"F = ma",
        "Classical Mechanics",
        "Force equals mass times acceleration, fundamental to dynamics",
        WikipediaImportance.HIGHEST,
        "1687",
        "Isaac Newton"
    ),
    WikiEquation(
        "Einstein's Mass-Energy Equivalence",
        r"E = mc^2",
        "Relativity",
        "Mass-energy equivalence, foundation of modern physics",
        WikipediaImportance.HIGHEST,
        "1905",
        "Albert Einstein"
    ),
    WikiEquation(
        "Schrödinger Equation",
        r"i\hbar\frac{\partial\psi}{\partial t} = \hat{H}\psi",
        "Quantum Mechanics",
        "Fundamental equation of quantum mechanics, describes wave function evolution",
        WikipediaImportance.HIGHEST,
        "1925",
        "Erwin Schrödinger"
    ),
    WikiEquation(
        "Maxwell's Equations",
        r"\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}",
        "Electromagnetism",
        "Complete set of equations describing electricity, magnetism, and light",
        WikipediaImportance.HIGHEST,
        "1865",
        "James Clerk Maxwell"
    ),
    WikiEquation(
        "Heisenberg Uncertainty Principle",
        r"\Delta x \cdot \Delta p \geq \frac{\hbar}{2}",
        "Quantum Mechanics",
        "Fundamental limit on precision of simultaneous measurements",
        WikipediaImportance.HIGHEST,
        "1927",
        "Werner Heisenberg"
    ),
    WikiEquation(
        "Planck's Equation",
        r"E = h\nu",
        "Quantum Mechanics",
        "Energy of photon is proportional to frequency",
        WikipediaImportance.HIGH,
        "1900",
        "Max Planck"
    ),
    
    # Information Theory
    WikiEquation(
        "Shannon Entropy",
        r"H = -\sum_{i} p_i \log_2 p_i",
        "Information Theory",
        "Fundamental limit on data compression and information transmission",
        WikipediaImportance.HIGH,
        "1948",
        "Claude Shannon"
    ),
    WikiEquation(
        "Euler's Formula",
        r"e^{i\pi} = -1",
        "Complex Analysis",
        "Most beautiful equation in mathematics, connects five fundamental constants",
        WikipediaImportance.HIGHEST,
        "1748",
        "Leonhard Euler"
    ),
    
    # Number Theory
    WikiEquation(
        "Prime Number Theorem",
        r"\pi(x) \sim \frac{x}{\ln x}",
        "Number Theory",
        "Asymptotic distribution of prime numbers",
        WikipediaImportance.HIGH,
        "19th century",
        "Carl Friedrich Gauss"
    ),
    WikiEquation(
        "Fermat's Last Theorem",
        r"a^n + b^n \neq c^n \text{ for } n > 2",
        "Number Theory",
        "No three positive integers satisfy for n > 2",
        WikipediaImportance.HIGH,
        "17th century",
        "Pierre de Fermat"
    ),
    
    # Statistics and Probability
    WikiEquation(
        "Normal Distribution",
        r"f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}",
        "Statistics",
        "Bell curve describing many natural phenomena",
        WikipediaImportance.HIGH,
        "19th century",
        "Pierre-Simon Laplace & Adolphe Quetelet"
    ),
    WikiEquation(
        "Central Limit Theorem",
        r"\bar{X}_n \to_d N(\mu, \sigma^2/n)",
        "Statistics",
        "Sample mean approaches normal distribution as n increases",
        WikipediaImportance.HIGH,
        "20th century",
        "Pierre-Simon Laplace"
    ),
    
    # Modern and Applied Mathematics
    WikiEquation(
        "Black-Scholes Equation",
        r"\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS\frac{\partial V}{\partial S} - rV = 0",
        "Financial Mathematics",
        "Options pricing model, foundation of modern finance",
        WikipediaImportance.HIGH,
        "1973",
        "Fischer Black & Myron Scholes"
    ),
    WikiEquation(
        "Navier-Stokes Equations",
        r"\rho \left(\frac{\partial \mathbf{v}}{\partial t} + \mathbf{v} \cdot \nabla \mathbf{v}\right) = -\nabla p + \mu \nabla^2 \mathbf{v} + \mathbf{f}",
        "Fluid Dynamics",
        "Fundamental equations of fluid motion",
        WikipediaImportance.HIGH,
        "19th century",
        "Claude-Louis Navier & George Gabriel Stokes"
    ),
    WikiEquation(
        "Fourier Transform",
        r"F(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt",
        "Signal Processing",
        "Transforms between time and frequency domains",
        WikipediaImportance.HIGH,
        "19th century",
        "Joseph Fourier"
    ),
]

# ============================================================================
# CONVERSION FUNCTIONS
# ============================================================================

def wiki_to_standard_equation(wiki_eq: WikiEquation) -> Equation:
    """Convert Wikipedia equation to standard Equation format"""
    # Map Wikipedia importance to difficulty levels
    difficulty_map = {
        WikipediaImportance.HIGHEST: "Beginner",
        WikipediaImportance.HIGH: "Intermediate", 
        WikipediaImportance.MEDIUM: "Intermediate",
        WikipediaImportance.LOW: "Advanced"
    }
    
    # Map Wikipedia fields to our categories
    field_map = {
        "Geometry": EquationCategory.GEOMETRY,
        "Algebra": EquationCategory.ALGEBRA,
        "Calculus": EquationCategory.CALCULUS,
        "Classical Mechanics": EquationCategory.PHYSICS,
        "Relativity": EquationCategory.PHYSICS,
        "Quantum Mechanics": EquationCategory.PHYSICS,
        "Electromagnetism": EquationCategory.PHYSICS,
        "Probability": EquationCategory.STATISTICS,
        "Information Theory": EquationCategory.STATISTICS,
        "Number Theory": EquationCategory.NUMBER_THEORY,
        "Financial Mathematics": EquationCategory.STATISTICS,
        "Fluid Dynamics": EquationCategory.PHYSICS,
        "Signal Processing": EquationCategory.CALCULUS,
    }
    
    # Get mapped category or default to ALGEBRA
    category = field_map.get(wiki_eq.field, EquationCategory.ALGEBRA)
    
    # Get mapped difficulty or default to Intermediate
    difficulty = difficulty_map.get(wiki_eq.importance, "Intermediate")
    
    return Equation(
        wiki_eq.name,
        wiki_eq.latex,
        category,
        wiki_eq.description,
        difficulty
    )

def get_wikipedia_equations() -> List[WikiEquation]:
    """Get all Wikipedia important equations"""
    return WIKIPEDIA_EQUATIONS

def get_wikipedia_equations_by_importance(importance: WikipediaImportance) -> List[WikiEquation]:
    """Get Wikipedia equations by importance level"""
    return [eq for eq in WIKIPEDIA_EQUATIONS if eq.importance == importance]

def get_wikipedia_equations_by_field(field: str) -> List[WikiEquation]:
    """Get Wikipedia equations by field"""
    return [eq for eq in WIKIPEDIA_EQUATIONS if eq.field == field]

def convert_all_wiki_to_standard() -> List[Equation]:
    """Convert all Wikipedia equations to standard format"""
    return [wiki_to_standard_equation(wiki_eq) for wiki_eq in WIKIPEDIA_EQUATIONS]

def print_wikipedia_equations(equations: List[WikiEquation] = None):
    """Print formatted list of Wikipedia equations"""
    if equations is None:
        equations = get_wikipedia_equations()
    
    print("Wikipedia Important Equations")
    print("=" * 50)
    
    current_importance = None
    for eq in equations:
        if current_importance != eq.importance:
            current_importance = eq.importance
            print(f"\n{eq.importance.value} Importance:")
            print("-" * len(eq.importance.value))
        
        print(f"  • {eq.name}")
        print(f"    {eq.latex}")
        print(f"    Field: {eq.field}")
        print(f"    {eq.description}")
        if eq.year:
            print(f"    Year: {eq.year}")
        if eq.discoverer:
            print(f"    Discoverer: {eq.discoverer}")
        print()

if __name__ == "__main__":
    print_wikipedia_equations()
