"""
well_known_equations.py - Comprehensive list of well-known mathematical equations

Contains a curated collection of famous mathematical equations organized by category
for use with the Mathematical Equation Story Generator.
"""

from typing import List, Dict
from enum import Enum
from wikipedia_equations import WikiEquation, get_wikipedia_equations, wiki_to_standard_equation


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


# ============================================================================
# COMPREHENSIVE EQUATION COLLECTION
# ============================================================================

ALGEBRA_EQUATIONS = [
    Equation(
        "Pythagorean Theorem",
        r"a^2 + b^2 = c^2",
        EquationCategory.ALGEBRA,
        "Fundamental relationship in right-angled triangles - #1 equation that changed the world",
        "Beginner"
    ),
    Equation(
        "Logarithms",
        r"\log(xy) = \log x + \log y",
        EquationCategory.ALGEBRA,
        "Logarithmic relationship that enabled complex calculations - #2 equation that changed the world",
        "Intermediate"
    ),
    Equation(
        "Calculus (Fundamental Theorem)",
        r"\frac{dy}{dx} = \lim_{h \to 0} \frac{y(x+h) - y(x)}{h}",
        EquationCategory.ALGEBRA,
        "Derivative definition that revolutionized mathematics and science - #3 equation that changed the world",
        "Intermediate"
    ),
    Equation(
        "Newton's Law of Gravity",
        r"F = G\frac{m_1 m_2}{r^2}",
        EquationCategory.ALGEBRA,
        "Universal gravitation that explained planetary motion - #4 equation that changed the world",
        "Intermediate"
    ),
    Equation(
        "Square Root of Minus One",
        r"i^2 = -1",
        EquationCategory.ALGEBRA,
        "Imaginary unit that enabled complex mathematics - #5 equation that changed the world",
        "Intermediate"
    ),
    Equation(
        "Euler's Formula for Polyhedra",
        r"V - E + F = 2",
        EquationCategory.ALGEBRA,
        "Relationship between vertices, edges, and faces of convex polyhedra - #6 equation that changed the world",
        "Intermediate"
    ),
    Equation(
        "Normal Distribution",
        r"f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}",
        EquationCategory.ALGEBRA,
        "Bell curve that describes natural phenomena - #7 equation that changed the world",
        "Intermediate"
    ),
    Equation(
        "Wave Equation",
        r"\frac{\partial^2 u}{\partial t^2} = c^2 \nabla^2 u",
        EquationCategory.ALGEBRA,
        "Describes propagation of waves in various media - #8 equation that changed the world",
        "Intermediate"
    ),
    Equation(
        "Fourier Transform",
        r"F(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} dt",
        EquationCategory.ALGEBRA,
        "Transforms functions between time and frequency domains - #9 equation that changed the world",
        "Advanced"
    ),
    Equation(
        "Navier-Stokes Equation",
        r"\rho \left(\frac{\partial \mathbf{v}}{\partial t} + \mathbf{v} \cdot \nabla \mathbf{v}\right) = -\nabla p + \mu \nabla^2 \mathbf{v} + \mathbf{f}",
        EquationCategory.ALGEBRA,
        "Fundamental equations of fluid dynamics - #10 equation that changed the world",
        "Advanced"
    ),
    Equation(
        "Maxwell's Equations",
        r"\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}",
        EquationCategory.ALGEBRA,
        "Unified electricity, magnetism, and light - #11 equation that changed the world",
        "Advanced"
    ),
    Equation(
        "Second Law of Thermodynamics",
        r"dS \geq \frac{dQ}{T}",
        EquationCategory.ALGEBRA,
        "Entropy always increases in isolated systems - #12 equation that changed the world",
        "Intermediate"
    ),
    Equation(
        "Einstein's Mass-Energy Equivalence",
        r"E = mc^2",
        EquationCategory.ALGEBRA,
        "Relationship between mass and energy - #13 equation that changed the world",
        "Beginner"
    ),
    Equation(
        "Schrödinger Equation",
        r"i\hbar\frac{\partial\psi}{\partial t} = \hat{H}\psi",
        EquationCategory.ALGEBRA,
        "Fundamental equation of quantum mechanics - #14 equation that changed the world",
        "Advanced"
    ),
    Equation(
        "Information Theory",
        r"H = -\sum p_i \log_2 p_i",
        EquationCategory.ALGEBRA,
        "Shannon entropy that defined the information age - #15 equation that changed the world",
        "Intermediate"
    ),
    Equation(
        "Chaos Theory",
        r"x_{n+1} = rx_n(1-x_n)",
        EquationCategory.ALGEBRA,
        "Logistic map that revealed deterministic chaos - #16 equation that changed the world",
        "Intermediate"
    ),
    Equation(
        "Black-Scholes Equation",
        r"\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS\frac{\partial V}{\partial S} - rV = 0",
        EquationCategory.ALGEBRA,
        "Revolutionized financial mathematics and derivatives trading - #17 equation that changed the world",
        "Advanced"
    ),
    Equation(
        "Quadratic Formula",
        r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
        EquationCategory.ALGEBRA,
        "Solves quadratic equations of the form ax² + bx + c = 0",
        "Beginner"
    ),
    Equation(
        "Difference of Squares",
        r"a^2 - b^2 = (a - b)(a + b)",
        EquationCategory.ALGEBRA,
        "Fundamental algebraic identity for factoring differences",
        "Beginner"
    ),
    Equation(
        "Binomial Theorem",
        r"(a + b)^n = \sum_{k=0}^{n} \binom{n}{k} a^{n-k} b^k",
        EquationCategory.ALGEBRA,
        "Expands powers of binomials using combinatorial coefficients",
        "Intermediate"
    ),
    Equation(
        "Arithmetic Series Sum",
        r"S_n = \frac{n}{2}(a_1 + a_n)",
        EquationCategory.ALGEBRA,
        "Sum of arithmetic progression with n terms",
        "Beginner"
    ),
    Equation(
        "Geometric Series Sum",
        r"S_n = a_1 \frac{1 - r^n}{1 - r}",
        EquationCategory.ALGEBRA,
        "Sum of geometric progression with ratio r",
        "Intermediate"
    ),
]

GEOMETRY_EQUATIONS = [
    Equation(
        "Pythagorean Theorem",
        r"a^2 + b^2 = c^2",
        EquationCategory.GEOMETRY,
        "Fundamental relationship in right-angled triangles",
        "Beginner"
    ),
    Equation(
        "Circle Area",
        r"A = \pi r^2",
        EquationCategory.GEOMETRY,
        "Area of a circle with radius r",
        "Beginner"
    ),
    Equation(
        "Circle Circumference",
        r"C = 2\pi r",
        EquationCategory.GEOMETRY,
        "Circumference of a circle with radius r",
        "Beginner"
    ),
    Equation(
        "Sphere Volume",
        r"V = \frac{4}{3}\pi r^3",
        EquationCategory.GEOMETRY,
        "Volume of a sphere with radius r",
        "Intermediate"
    ),
    Equation(
        "Heron's Formula",
        r"A = \sqrt{s(s-a)(s-b)(s-c)}",
        EquationCategory.GEOMETRY,
        "Area of triangle given side lengths, where s is semi-perimeter",
        "Intermediate"
    ),
    Equation(
        "Euler's Formula for Polyhedra",
        r"V - E + F = 2",
        EquationCategory.GEOMETRY,
        "Relationship between vertices, edges, and faces of convex polyhedra",
        "Intermediate"
    ),
]

CALCULUS_EQUATIONS = [
    Equation(
        "Fundamental Theorem of Calculus",
        r"\int_a^b f(x) dx = F(b) - F(a)",
        EquationCategory.CALCULUS,
        "Connects differentiation and integration",
        "Intermediate"
    ),
    Equation(
        "Power Rule",
        r"\frac{d}{dx} x^n = nx^{n-1}",
        EquationCategory.CALCULUS,
        "Basic differentiation rule for power functions",
        "Beginner"
    ),
    Equation(
        "Chain Rule",
        r"\frac{d}{dx} f(g(x)) = f'(g(x)) \cdot g'(x)",
        EquationCategory.CALCULUS,
        "Differentiation of composite functions",
        "Intermediate"
    ),
    Equation(
        "Integration by Parts",
        r"\int u dv = uv - \int v du",
        EquationCategory.CALCULUS,
        "Integration technique for product of functions",
        "Intermediate"
    ),
    Equation(
        "Taylor Series",
        r"f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x-a)^n",
        EquationCategory.CALCULUS,
        "Represents functions as infinite polynomial series",
        "Advanced"
    ),
]

PHYSICS_EQUATIONS = [
    Equation(
        "Einstein's Mass-Energy Equivalence",
        r"E = mc^2",
        EquationCategory.PHYSICS,
        "Relationship between mass and energy",
        "Beginner"
    ),
    Equation(
        "Newton's Second Law",
        r"F = ma",
        EquationCategory.PHYSICS,
        "Force equals mass times acceleration",
        "Beginner"
    ),
    Equation(
        "Universal Gravitation",
        r"F = G\frac{m_1 m_2}{r^2}",
        EquationCategory.PHYSICS,
        "Gravitational force between two masses",
        "Intermediate"
    ),
    Equation(
        "Ideal Gas Law",
        r"PV = nRT",
        EquationCategory.PHYSICS,
        "Relationship between pressure, volume, and temperature of ideal gas",
        "Intermediate"
    ),
    Equation(
        "Maxwell's Equations (Gauss's Law)",
        r"\nabla \cdot \mathbf{E} = \frac{\rho}{\epsilon_0}",
        EquationCategory.PHYSICS,
        "Electric field divergence relates to charge density",
        "Advanced"
    ),
    Equation(
        "Schrödinger Equation",
        r"i\hbar\frac{\partial\psi}{\partial t} = \hat{H}\psi",
        EquationCategory.PHYSICS,
        "Fundamental equation of quantum mechanics",
        "Advanced"
    ),
    Equation(
        "Einstein's Field Equations",
        r"G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}",
        EquationCategory.PHYSICS,
        "Fundamental equations of general relativity describing gravity",
        "Advanced"
    ),
    Equation(
        "Planck's Equation",
        r"E = h\nu",
        EquationCategory.PHYSICS,
        "Energy of a photon is proportional to its frequency",
        "Intermediate"
    ),
    Equation(
        "Heisenberg Uncertainty Principle",
        r"\Delta x \cdot \Delta p \geq \frac{\hbar}{2}",
        EquationCategory.PHYSICS,
        "Fundamental limit on precision of measuring position and momentum",
        "Intermediate"
    ),
    Equation(
        "Wave Equation",
        r"\frac{\partial^2 u}{\partial t^2} = c^2 \nabla^2 u",
        EquationCategory.PHYSICS,
        "Describes propagation of waves in various media",
        "Intermediate"
    ),
    Equation(
        "Lorentz Force",
        r"\mathbf{F} = q(\mathbf{E} + \mathbf{v} \times \mathbf{B})",
        EquationCategory.PHYSICS,
        "Force on charged particle in electromagnetic fields",
        "Intermediate"
    ),
    Equation(
        "Coulomb's Law",
        r"F = k\frac{q_1 q_2}{r^2}",
        EquationCategory.PHYSICS,
        "Electrostatic force between two point charges",
        "Beginner"
    ),
    Equation(
        "Ohm's Law",
        r"V = IR",
        EquationCategory.PHYSICS,
        "Relationship between voltage, current, and resistance",
        "Beginner"
    ),
    Equation(
        "Bernoulli's Equation",
        r"P + \frac{1}{2}\rho v^2 + \rho gh = \text{constant}",
        EquationCategory.PHYSICS,
        "Conservation of energy in fluid flow",
        "Intermediate"
    ),
    Equation(
        "Stefan-Boltzmann Law",
        r"P = \sigma A T^4",
        EquationCategory.PHYSICS,
        "Power radiated by black body is proportional to fourth power of temperature",
        "Intermediate"
    ),
    Equation(
        "Dirac Equation",
        r"(i\hbar\gamma^\mu \partial_\mu - mc)\psi = 0",
        EquationCategory.PHYSICS,
        "Relativistic quantum mechanical wave equation for spin-1/2 particles",
        "Advanced"
    ),
    Equation(
        "Navier-Stokes Equation",
        r"\rho \left(\frac{\partial \mathbf{v}}{\partial t} + \mathbf{v} \cdot \nabla \mathbf{v}\right) = -\nabla p + \mu \nabla^2 \mathbf{v} + \mathbf{f}",
        EquationCategory.PHYSICS,
        "Fundamental equations of fluid dynamics",
        "Advanced"
    ),
    Equation(
        "Einstein's Photoelectric Effect",
        r"E_k = h\nu - \phi",
        EquationCategory.PHYSICS,
        "Kinetic energy of emitted electron depends on light frequency and work function",
        "Intermediate"
    ),
    Equation(
        "Hooke's Law",
        r"F = -kx",
        EquationCategory.PHYSICS,
        "Force exerted by spring is proportional to displacement",
        "Beginner"
    ),
    Equation(
        "Kepler's Third Law",
        r"T^2 = \frac{4\pi^2}{GM}a^3",
        EquationCategory.PHYSICS,
        "Square of orbital period proportional to cube of semi-major axis",
        "Intermediate"
    ),
    Equation(
        "Doppler Effect",
        r"f' = f\frac{v \pm v_o}{v \mp v_s}",
        EquationCategory.PHYSICS,
        "Frequency change due to relative motion between source and observer",
        "Intermediate"
    ),
    Equation(
        "Euler-Bernoulli Beam Equation",
        r"EI\frac{d^4w}{dx^4} = q(x)",
        EquationCategory.PHYSICS,
        "Describes deflection of beams under load",
        "Advanced"
    ),
    Equation(
        "Lagrange's Equation",
        r"\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}_i}\right) - \frac{\partial L}{\partial q_i} = 0",
        EquationCategory.PHYSICS,
        "Fundamental equation of Lagrangian mechanics",
        "Advanced"
    ),
    Equation(
        "Hamilton's Equations",
        r"\dot{q} = \frac{\partial H}{\partial p}, \quad \dot{p} = -\frac{\partial H}{\partial q}",
        EquationCategory.PHYSICS,
        "Fundamental equations of Hamiltonian mechanics",
        "Advanced"
    ),
]

TRIGONOMETRY_EQUATIONS = [
    Equation(
        "Pythagorean Identity",
        r"\sin^2\theta + \cos^2\theta = 1",
        EquationCategory.TRIGONOMETRY,
        "Fundamental trigonometric identity",
        "Beginner"
    ),
    Equation(
        "Euler's Formula",
        r"e^{i\theta} = \cos\theta + i\sin\theta",
        EquationCategory.TRIGONOMETRY,
        "Connects exponential and trigonometric functions",
        "Intermediate"
    ),
    Equation(
        "Law of Cosines",
        r"c^2 = a^2 + b^2 - 2ab\cos\gamma",
        EquationCategory.TRIGONOMETRY,
        "Generalization of Pythagorean theorem for any triangle",
        "Intermediate"
    ),
    Equation(
        "Law of Sines",
        r"\frac{a}{\sin\alpha} = \frac{b}{\sin\beta} = \frac{c}{\sin\gamma}",
        EquationCategory.TRIGONOMETRY,
        "Relationship between sides and angles in any triangle",
        "Intermediate"
    ),
    Equation(
        "Double Angle Formula",
        r"\sin(2\theta) = 2\sin\theta\cos\theta",
        EquationCategory.TRIGONOMETRY,
        "Trigonometric identity for double angles",
        "Intermediate"
    ),
]

STATISTICS_EQUATIONS = [
    Equation(
        "Normal Distribution",
        r"f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}",
        EquationCategory.STATISTICS,
        "Probability density function of normal distribution",
        "Intermediate"
    ),
    Equation(
        "Standard Deviation",
        r"\sigma = \sqrt{\frac{1}{N}\sum_{i=1}^{N}(x_i - \mu)^2}",
        EquationCategory.STATISTICS,
        "Measure of data spread around mean",
        "Beginner"
    ),
    Equation(
        "Correlation Coefficient",
        r"r = \frac{n\sum xy - \sum x \sum y}{\sqrt{n\sum x^2 - (\sum x)^2}\sqrt{n\sum y^2 - (\sum y)^2}}",
        EquationCategory.STATISTICS,
        "Measures linear relationship between two variables",
        "Intermediate"
    ),
    Equation(
        "Bayes' Theorem",
        r"P(A|B) = \frac{P(B|A)P(A)}{P(B)}",
        EquationCategory.STATISTICS,
        "Updates probability based on new evidence",
        "Intermediate"
    ),
]

NUMBER_THEORY_EQUATIONS = [
    Equation(
        "Fermat's Last Theorem",
        r"a^n + b^n \neq c^n \text{ for } n > 2",
        EquationCategory.NUMBER_THEORY,
        "No three positive integers satisfy this equation for n > 2",
        "Advanced"
    ),
    Equation(
        "Prime Number Theorem",
        r"\pi(x) \sim \frac{x}{\ln x}",
        EquationCategory.NUMBER_THEORY,
        "Asymptotic distribution of prime numbers",
        "Advanced"
    ),
    Equation(
        "Euler's Totient Function",
        r"\phi(n) = n \prod_{p|n}\left(1 - \frac{1}{p}\right)",
        EquationCategory.NUMBER_THEORY,
        "Count of integers less than n that are coprime to n",
        "Intermediate"
    ),
    Equation(
        "Goldbach Conjecture",
        r"2n = p_1 + p_2 \text{ (for } n > 1\text{)}",
        EquationCategory.NUMBER_THEORY,
        "Every even integer greater than 2 is sum of two primes",
        "Advanced"
    ),
]

LINEAR_ALGEBRA_EQUATIONS = [
    Equation(
        "Matrix Multiplication",
        r"(AB)_{ij} = \sum_{k} A_{ik}B_{kj}",
        EquationCategory.LINEAR_ALGEBRA,
        "Rule for multiplying matrices",
        "Intermediate"
    ),
    Equation(
        "Determinant (2x2)",
        r"\det\begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc",
        EquationCategory.LINEAR_ALGEBRA,
        "Determinant of 2x2 matrix",
        "Beginner"
    ),
    Equation(
        "Eigenvalue Equation",
        r"A\mathbf{v} = \lambda\mathbf{v}",
        EquationCategory.LINEAR_ALGEBRA,
        "Defines eigenvalues and eigenvectors",
        "Intermediate"
    ),
    Equation(
        "Cauchy-Schwarz Inequality",
        r"|\langle \mathbf{u}, \mathbf{v} \rangle| \leq \|\mathbf{u}\| \|\mathbf{v}\|",
        EquationCategory.LINEAR_ALGEBRA,
        "Fundamental inequality for inner product spaces",
        "Intermediate"
    ),
]

COMPLEX_ANALYSIS_EQUATIONS = [
    Equation(
        "Cauchy's Integral Formula",
        r"f(a) = \frac{1}{2\pi i} \oint_\gamma \frac{f(z)}{z-a} dz",
        EquationCategory.COMPLEX_ANALYSIS,
        "Values of analytic functions from contour integrals",
        "Advanced"
    ),
    Equation(
        "Residue Theorem",
        r"\oint_\gamma f(z) dz = 2\pi i \sum \text{Res}(f, a_k)",
        EquationCategory.COMPLEX_ANALYSIS,
        "Contour integrals via residues",
        "Advanced"
    ),
]

# ============================================================================
# COMPREHENSIVE COLLECTION
# ============================================================================

# Convert Wikipedia equations to standard format
WIKIPEDIA_STANDARD_EQS = [wiki_to_standard_equation(wiki_eq) for wiki_eq in get_wikipedia_equations()]

ALL_EQUATIONS = (
    ALGEBRA_EQUATIONS + 
    GEOMETRY_EQUATIONS + 
    CALCULUS_EQUATIONS + 
    PHYSICS_EQUATIONS + 
    TRIGONOMETRY_EQUATIONS + 
    STATISTICS_EQUATIONS + 
    NUMBER_THEORY_EQUATIONS + 
    LINEAR_ALGEBRA_EQUATIONS + 
    COMPLEX_ANALYSIS_EQUATIONS +
    WIKIPEDIA_STANDARD_EQS
)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_world_changing_equations() -> List[Equation]:
    """Get the 17 equations that changed the world (Ian Stewart's selection)"""
    world_changing_names = [
        "Pythagorean Theorem",
        "Logarithms", 
        "Calculus (Fundamental Theorem)",
        "Newton's Law of Gravity",
        "Square Root of Minus One",
        "Euler's Formula for Polyhedra",
        "Normal Distribution",
        "Wave Equation",
        "Fourier Transform",
        "Navier-Stokes Equation",
        "Maxwell's Equations",
        "Second Law of Thermodynamics",
        "Einstein's Mass-Energy Equivalence",
        "Schrödinger Equation",
        "Information Theory",
        "Chaos Theory",
        "Black-Scholes Equation"
    ]
    
    return [get_equation_by_name(name) for name in world_changing_names]

def print_world_changing_equations():
    """Print the 17 equations that changed the world"""
    equations = get_world_changing_equations()
    
    print("The 17 Equations That Changed the World")
    print("=" * 50)
    print("Based on Ian Stewart's book '17 Equations That Changed the World'")
    print()
    
    for i, eq in enumerate(equations, 1):
        print(f"{i}. {eq.name}")
        print(f"   {eq.latex}")
        print(f"   {eq.description}")
        print(f"   Difficulty: {eq.difficulty}")
        print()

def get_equations_by_category(category: EquationCategory) -> List[Equation]:
    """Get all equations in a specific category"""
    return [eq for eq in ALL_EQUATIONS if eq.category == category]

def get_equations_by_difficulty(difficulty: str) -> List[Equation]:
    """Get all equations by difficulty level"""
    return [eq for eq in ALL_EQUATIONS if eq.difficulty == difficulty]

def get_equation_names() -> List[str]:
    """Get list of all equation names"""
    return [eq.name for eq in ALL_EQUATIONS]

def get_equation_by_name(name: str) -> Equation:
    """Get equation by name (case-insensitive)"""
    for eq in ALL_EQUATIONS:
        if eq.name.lower() == name.lower():
            return eq
    raise ValueError(f"Equation '{name}' not found")

def get_random_equations(count: int = 5) -> List[Equation]:
    """Get random selection of equations"""
    import random
    return random.sample(ALL_EQUATIONS, min(count, len(ALL_EQUATIONS)))

def print_equation_list(equations: List[Equation] = None):
    """Print formatted list of equations"""
    if equations is None:
        equations = ALL_EQUATIONS
    
    print("Mathematical Equations Collection")
    print("=" * 50)
    
    current_category = None
    for eq in equations:
        if current_category != eq.category.value:
            current_category = eq.category.value
            print(f"\n{current_category}:")
            print("-" * len(current_category))
        
        print(f"  • {eq.name}")
        print(f"    {eq.latex}")
        print(f"    {eq.description}")
        print(f"    Difficulty: {eq.difficulty}")
        print()

if __name__ == "__main__":
    print("Mathematical Equations Collection")
    print("Choose an option:")
    print("1. Show all equations")
    print("2. Show 17 equations that changed the world")
    print("3. Show equations by category")
    print("4. Show equations by difficulty")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        print_equation_list()
    elif choice == "2":
        print_world_changing_equations()
    elif choice == "3":
        print("\nAvailable categories:")
        for i, category in enumerate(EquationCategory, 1):
            print(f"{i}. {category.value}")
        
        cat_choice = input("\nEnter category number: ").strip()
        try:
            cat_index = int(cat_choice) - 1
            categories = list(EquationCategory)
            if 0 <= cat_index < len(categories):
                selected_cat = categories[cat_index]
                equations = get_equations_by_category(selected_cat)
                print_equation_list(equations)
            else:
                print("Invalid category number")
        except ValueError:
            print("Invalid input")
    elif choice == "4":
        print("\nAvailable difficulties:")
        difficulties = ["Beginner", "Intermediate", "Advanced"]
        for i, diff in enumerate(difficulties, 1):
            print(f"{i}. {diff}")
        
        diff_choice = input("\nEnter difficulty number: ").strip()
        try:
            diff_index = int(diff_choice) - 1
            if 0 <= diff_index < len(difficulties):
                selected_diff = difficulties[diff_index]
                equations = get_equations_by_difficulty(selected_diff)
                print_equation_list(equations)
            else:
                print("Invalid difficulty number")
        except ValueError:
            print("Invalid input")
    else:
        print("Invalid choice")
