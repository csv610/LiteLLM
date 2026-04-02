#!/usr/bin/env python3
"""riemann_problems_cli.py - Non-Agentic CLI interface"""

import sys
import argparse
import random
from pathlib import Path

try:
    from .riemann_problems import RiemannTheoryGuide
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from riemann_problems import RiemannTheoryGuide

def argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Riemann Theory Reference Guide (Non-Agentic)")
    parser.add_argument("-t", "--theory", type=str, help="Theory name")
    parser.add_argument("-e", "--example", action="store_true", help="Random example")
    parser.add_argument("-l", "--list", action="store_true", help="List theories")
    return parser

def main():
    parser = argument_parser()
    args = parser.parse_args()
    guide = RiemannTheoryGuide()

    if args.list:
        print("\nAvailable Riemann Theories:")
        for theory in guide.available_theories:
            print(f" - {theory}")
        return

    theory_to_fetch = args.theory
    if args.example and not theory_to_fetch:
        if guide.available_theories:
            theory_to_fetch = random.choice(guide.available_theories)

    if theory_to_fetch:
        print(f"\n🔄 Fetching: '{theory_to_fetch}'...")
        theory_data = guide.generate_text(theory_to_fetch)
        RiemannTheoryGuide.display_theory(theory_data)
    else:
        guide.display_summary()

if __name__ == "__main__":
    main()
