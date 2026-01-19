import argparse
import logging
import json
import sys
import os
import re
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field

# Add parent directory to path to import lite module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lite import LiteClient, ModelConfig
from lite.config import ModelInput
from logging_util import setup_logging

logger = setup_logging(str(Path(__file__).parent / "logs" / "millennium.log"))

# ==============================================================================
# Pydantic Models
# ==============================================================================

class MillenniumProblem(BaseModel):
    """Represents a Millennium Prize Problem."""
    title: str = Field(..., description="The official name of the problem")
    description: str = Field(..., description="Detailed explanation of the problem")
    field: str = Field(..., description="The mathematical or physics field the problem belongs to")
    status: str = Field(..., description="Current status (Unsolved or Solved)")
    solver: Optional[str] = Field(None, description="Name of solver if problem has been solved")
    year_solved: Optional[int] = Field(None, description="Year the problem was solved")
    significance: str = Field(..., description="Why this problem is important and its implications")
    current_progress: str = Field(..., description="Recent progress, approaches, or partial results")


class MillenniumProblemsResponse(BaseModel):
    """Response containing a list of Millennium Prize Problems."""
    total_problems: int = Field(..., description="Total number of Millennium Prize Problems")
    problems: list[MillenniumProblem]


# ==============================================================================
# Core Data
# ==============================================================================

MILLENNIUM_PROBLEMS_DATA = [
    {
        "title": "P versus NP",
        "description": "Asks whether every problem whose solution can be quickly verified can also be quickly solved. In other words, is P (problems solvable in polynomial time) equal to NP (problems whose solutions can be verified in polynomial time)?",
        "field": "Computer Science and Mathematics",
        "status": "Unsolved",
        "solver": None,
        "year_solved": None,
        "significance": "Fundamental to computational theory. If P=NP, many cryptographic systems would be broken, revolutionizing computer science and security.",
        "current_progress": "The problem remains open despite decades of research. Most experts believe P ≠ NP, but no proof exists. Many equivalent formulations have been discovered."
    },
    {
        "title": "Hodge Conjecture",
        "description": "States that for projective algebraic varieties, Hodge cycles are rational linear combinations of algebraic cycles. It connects topology and algebraic geometry.",
        "field": "Algebraic Geometry",
        "status": "Unsolved",
        "solver": None,
        "year_solved": None,
        "significance": "Central to understanding the relationship between algebraic topology and algebraic geometry. Verified in several special cases.",
        "current_progress": "Proven for specific classes of varieties (curves, surfaces). General case remains open. Deep connections to motives have been developed."
    },
    {
        "title": "Riemann Hypothesis",
        "description": "Proposes that all non-trivial zeros of the Riemann zeta function have real part equal to 1/2. This is one of the most famous unsolved problems in mathematics.",
        "field": "Number Theory and Analysis",
        "status": "Unsolved",
        "solver": None,
        "year_solved": None,
        "significance": "Has profound implications for the distribution of prime numbers. Many results in number theory assume its truth.",
        "current_progress": "Verified for over 10 trillion zeros. Equivalent formulations in different areas discovered. Deep connections to random matrix theory explored."
    },
    {
        "title": "Yang-Mills Existence and Mass Gap",
        "description": "Asks whether quantum Yang-Mills theory exists on a four-dimensional Euclidean space and whether the spectrum has a positive mass gap (lowest excitation energy is non-zero).",
        "field": "Mathematical Physics and Quantum Field Theory",
        "status": "Unsolved",
        "solver": None,
        "year_solved": None,
        "significance": "Central to understanding quantum chromodynamics and the strong nuclear force. A proof would rigorously establish a key physics principle.",
        "current_progress": "Well-established in physics through experiments and non-rigorous quantum field theory. Rigorous mathematical foundation remains elusive."
    },
    {
        "title": "Navier-Stokes Existence and Smoothness",
        "description": "Asks whether smooth solutions always exist for the three-dimensional Navier-Stokes equations (describing fluid motion) and whether they remain smooth for all time.",
        "field": "Fluid Dynamics and Partial Differential Equations",
        "status": "Unsolved",
        "solver": None,
        "year_solved": None,
        "significance": "Fundamental to understanding fluid dynamics, weather prediction, and aerodynamics. Practical solutions depend on existence of global smooth solutions.",
        "current_progress": "Solved in two dimensions (Ladyzhenskaya, 1969). Three-dimensional case remains open. Partial regularity results proven (Scheffer, Caffarelli-Kohn-Nirenberg)."
    },
    {
        "title": "Birch and Swinnerton-Dyer Conjecture",
        "description": "Relates the rank of the elliptic curve (number of rational points) to the behavior of the L-function at a special point. Predicts that rank equals the order of zero at s=1.",
        "field": "Number Theory and Algebraic Geometry",
        "status": "Unsolved",
        "solver": None,
        "year_solved": None,
        "significance": "Crucial for understanding rational solutions to cubic equations. Has connections to cryptography and number theory.",
        "current_progress": "Proven in many special cases (certain ranks, specific families). Partially verified computationally. Modularity theorem (Wiles et al.) provided key insights."
    },
    {
        "title": "Poincaré Conjecture",
        "description": "States that every simply connected, closed 3-manifold is homeomorphic to the 3-sphere. Characterizes which 3-dimensional spaces are topologically equivalent.",
        "field": "Topology",
        "status": "Solved",
        "solver": "Grigori Perelman",
        "year_solved": 2003,
        "significance": "Fundamental classification theorem in topology. First solved Millennium Prize Problem.",
        "current_progress": "Solved using Ricci flow and surgery techniques. Perelman proved the Thurston Geometrization Conjecture, which implies the Poincaré Conjecture."
    }
]


# ==============================================================================
# CLI Functions
# ==============================================================================

def arguments_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Get information about a Millennium Prize Problem",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python millennium_prize_problems.py -p 1 -m claude-3-opus
  python millennium_prize_problems.py -p 3 -m gpt-4
  python millennium_prize_problems.py -p 7
  python millennium_prize_problems.py
        """
    )

    parser.add_argument(
        "-p",
        "--problem",
        type=int,
        default=None,
        dest="problem_number",
        help="Problem number (1-7), or omit to list all problems"
    )

    parser.add_argument(
        "-m",
        "--model",
        default="ollama/gemma3",
        dest="model",
        help="LLM model to use for generating explanations (default: ollama/gemma3)"
    )

    return parser


def main() -> int:
    """
    Main entry point for the Millennium Prize Problems CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = arguments_parser()
    args = parser.parse_args()

    try:
        # Get all problems
        all_problems = [MillenniumProblem(**problem) for problem in MILLENNIUM_PROBLEMS_DATA]

        # If problem_number not specified, show all problems
        if args.problem_number is None:
            logger.info("Listing all Millennium Prize Problems")

            data_to_save = {
                "title": "Millennium Prize Problems",
                "total_problems": len(all_problems),
                "problems": [problem.model_dump() for problem in all_problems]
            }

            output_filename = "millennium_prize_problems.json"
            with open(output_filename, 'w') as f:
                json.dump(data_to_save, f, indent=4)

            os.chmod(output_filename, 0o600)

            logger.info(f"Successfully saved {len(all_problems)} Millennium Prize Problem(s) to {output_filename}")
            print(f"Successfully generated output for {len(all_problems)} Millennium Prize Problem(s)")
            print(f"Output saved to: {output_filename}")
            return 0

        # Validate problem number
        if args.problem_number < 1 or args.problem_number > len(all_problems):
            raise ValueError(f"Problem number must be between 1 and {len(all_problems)}")

        problem = all_problems[args.problem_number - 1]
        logger.info(f"Fetching problem {args.problem_number}: {problem.title}")

        # Generate explanation if model is provided
        explanation = ""
        if args.model is not None:
            logger.info(f"Generating explanation using model: {args.model}")

            try:
                model_config = ModelConfig(model=args.model, temperature=0.3)
                client = LiteClient(model_config=model_config)

                prompt = f"""Explain the following Millennium Prize Problem in detail:

Title: {problem.title}
Description: {problem.description}
Field: {problem.field}
Status: {problem.status}
Significance: {problem.significance}
Current Progress: {problem.current_progress}

Provide a comprehensive explanation including:
1. What the problem asks
2. Why it matters
3. Current status
4. Key historical figures involved
5. Any recent progress or notable attempts"""

                model_input = ModelInput(
                    user_prompt=prompt
                )

                response_content = client.generate_text(model_input=model_input)

                if isinstance(response_content, str):
                    explanation = response_content
                else:
                    explanation = str(response_content)

                logger.info("Successfully generated explanation using LLM")

            except Exception as e:
                logger.warning(f"Failed to generate LLM explanation: {e}")
                explanation = ""

        # Save output
        data_to_save = {
            "title": "Millennium Prize Problem",
            "problem_number": args.problem_number,
            "problem": problem.model_dump()
        }

        if explanation:
            data_to_save["generated_explanation"] = explanation

        output_filename = f"millennium_problem_{args.problem_number}.json"
        with open(output_filename, 'w') as f:
            json.dump(data_to_save, f, indent=4)

        os.chmod(output_filename, 0o600)

        logger.info(f"Successfully saved problem {args.problem_number} to {output_filename}")
        print(f"Successfully generated output for: {problem.title}")
        print(f"Output saved to: {output_filename}")
        return 0

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        logger.error(f"Runtime error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except IOError as e:
        logger.error(f"File I/O error: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
