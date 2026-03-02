from enum import Enum
from typing import List, Dict

class EquationCategory(Enum):
    """Categories for mathematical equations"""
    ALGEBRA = "Algebra"
    GEOMETRY = "Geometry"
    CALCULUS = "Calculus"
    PHYSICS = "Physics"
    TRIGONOMETRY = "Trigonometry"
    STATISTICS = "Statistics"
    NUMBER_THEORY = "Number Theory"
    LINEAR_ALGEBRA = "Linear Algebra"
    DIFFERENTIAL_EQUATIONS = "Differential Equations"
    COMPLEX_ANALYSIS = "Complex Analysis"
    DISCRETE_MATH = "Discrete Mathematics"
    PROBABILITY = "Probability"


class Equation:
    """Represents a mathematical equation with metadata"""
    
    def __init__(self, name: str, latex: str, category: EquationCategory, 
                 description: str, difficulty: str = "Intermediate"):
        self.name = name
        self.latex = latex
        self.category = category
        self.description = description
        self.difficulty = difficulty
    
    def to_dict(self) -> Dict:
        """Convert equation to dictionary format"""
        return {
            "name": self.name,
            "latex": self.latex,
            "category": self.category.value,
            "description": self.description,
            "difficulty": self.difficulty
        }
