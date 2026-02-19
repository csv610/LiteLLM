# Mathematical Equation Story Assets

This directory contains supporting assets for the Mathematical Equation Story Generator.

## Files

### `well_known_equations.py`
A comprehensive collection of famous mathematical equations organized by category, designed for use with the story generator.

## Features

### Equation Categories
- **Algebra** - Fundamental algebraic identities and formulas
- **Geometry** - Geometric relationships and formulas
- **Calculus** - Differential and integral calculus equations
- **Physics** - Famous physics equations and laws
- **Trigonometry** - Trigonometric identities and relationships
- **Statistics** - Statistical formulas and distributions
- **Number Theory** - Number theoretic equations and theorems
- **Linear Algebra** - Matrix operations and linear transformations
- **Complex Analysis** - Complex variable equations

### Equation Metadata
Each equation includes:
- **Name**: Common name of the equation
- **LaTeX**: Mathematical notation in LaTeX format
- **Category**: Mathematical field classification
- **Description**: Brief explanation of what the equation represents
- **Difficulty**: Beginner, Intermediate, or Advanced

## Usage Examples

### Basic Usage
```python
from assets.well_known_equations import (
    ALL_EQUATIONS, 
    get_equations_by_category,
    get_equation_by_name
)

# Get all equations
all_eqs = ALL_EQUATIONS

# Get equations by category
geometry_eqs = get_equations_by_category(EquationCategory.GEOMETRY)

# Get specific equation
pythagorean = get_equation_by_name("Pythagorean Theorem")
```

### Integration with Story Generator
```python
from assets.well_known_equations import get_random_equations
from mathematical_equation_story_generator import MathEquationStoryGenerator

# Get random equations for stories
random_eqs = get_random_equations(3)
generator = MathEquationStoryGenerator()

for eq in random_eqs:
    story = generator.generate_story(eq.name)
    print(f"Generated story for: {eq.name}")
```

### Filter by Difficulty
```python
from assets.well_known_equations import get_equations_by_difficulty

# Get beginner-friendly equations
beginner_eqs = get_equations_by_difficulty("Beginner")

# Get advanced equations
advanced_eqs = get_equations_by_difficulty("Advanced")
```

## Equation Collection Highlights

### Most Famous Equations
1. **E = mc²** - Einstein's mass-energy equivalence
2. **a² + b² = c²** - Pythagorean theorem
3. **F = ma** - Newton's second law
4. **e^(iπ) + 1 = 0** - Euler's identity
5. **PV = nRT** - Ideal gas law

### Educational Progression
- **Beginner**: High school level equations
- **Intermediate**: Undergraduate level equations
- **Advanced**: Graduate level equations

### Cross-Disciplinary
- Physics applications (mechanics, thermodynamics, quantum)
- Engineering formulas
- Computer science applications
- Financial mathematics

## Contributing

To add new equations:

1. Choose appropriate category
2. Provide accurate LaTeX notation
3. Write clear description
4. Assign appropriate difficulty level
5. Add to relevant equation list

Example:
```python
Equation(
    "New Equation Name",
    r"LaTeX notation here",
    EquationCategory.CATEGORY,
    "Clear description of what it represents",
    "Difficulty level"
)
```

## Statistics

- **Total Equations**: 40+
- **Categories**: 9
- **Difficulty Levels**: 3
- **LaTeX Support**: Full

## File Structure

```
assets/
├── README.md                    # This file
├── well_known_equations.py      # Main equation collection
└── future_extensions/           # Planned additions
    ├── historical_equations.py  # Historical mathematical equations
    ├── applied_equations.py     # Applied mathematics equations
    └── custom_equations.py      # User-defined equations
```

## Notes

- All LaTeX expressions are properly formatted for display
- Descriptions are written for general audience understanding
- Difficulty levels are based on typical educational progression
- Categories follow standard mathematical classification

This asset collection provides a rich foundation for generating engaging mathematical stories across various fields and difficulty levels.
