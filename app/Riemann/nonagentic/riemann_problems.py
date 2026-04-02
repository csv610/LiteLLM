#!/usr/bin/env python3
"""
Riemann Theory Reference Guide (Non-Agentic Version)
"""

import logging
import json
from pathlib import Path
from typing import Optional, List

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite import logging_config

try:
    from app.Riemann.shared.models import RiemannTheoryModel
    from app.Riemann.shared.prompts import PromptBuilder
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from riemann_problems_models import RiemannTheoryModel
    from riemann_problems_prompts import PromptBuilder

# Setup logging
logging_config.configure_logging(str(Path(__file__).parent / "logs" / "riemann_theory.log"))
logger = logging.getLogger(__name__)


class RiemannTheoryGuide:
    """Reference guide for various Riemann theories using LiteClient."""

    def __init__(self, config: Optional[ModelConfig] = None):
        """Initialize the guide with API client."""
        self.config = config or ModelConfig(model="ollama/gemma3", temperature=0.3)
        self.client = LiteClient(self.config)
        self.theories_file = Path(__file__).parent.parent / "assets" / "riemann.txt"
        self.available_theories = self._load_theories()

    def _load_theories(self) -> List[str]:
        """Load available theories from the assets file."""
        try:
            if self.theories_file.exists():
                with open(self.theories_file, "r") as f:
                    return [line.strip() for line in f if line.strip()]
            return []
        except Exception:
            return []

    def generate_text(self, theory_name: str) -> Optional[RiemannTheoryModel]:
        """Fetch information for a specific Riemann theory."""
        try:
            model_input = ModelInput(
                system_prompt=PromptBuilder.get_system_prompt(),
                user_prompt=PromptBuilder.get_user_prompt(theory_name),
                response_format=RiemannTheoryModel
            )
            return self.client.generate_text(model_input)
        except Exception as e:
            logger.error(f"Error fetching theory '{theory_name}': {str(e)}")
            return None

    @staticmethod
    def display_theory(theory: RiemannTheoryModel):
        """Display detailed information about a Riemann theory."""
        if not theory:
            print("\n❌ Error: No theory information available.")
            return

        print(f"\n{'='*80}")
        print(f"RIEMANN THEORY: {theory.name.upper()}")
        print(f"{'='*80}")
        
        print(f"\nLAYPERSON EXPLANATION:\n{theory.layperson_explanation}")
        print(f"\nDEFINITION:\n{theory.definition}")
        print(f"\nINTUITION & BIGGER PICTURE:\n{theory.intuition}")
        print(f"\nRIEMANN'S MOTIVATION:\n{theory.motivation}")
        
        print("\nCOMMON MISCONCEPTIONS:")
        for misc in theory.misconceptions:
            print(f" • {misc}")
            
        print(f"\nHISTORICAL CONTEXT:\n{theory.historical_context}")
        print(f"\nLIMITATIONS:\n{theory.limitations}")
        print(f"\nMODERN DEVELOPMENTS:\n{theory.modern_developments}")
        print(f"\nCOUNTERFACTUAL ANALYSIS:\n{theory.counterfactual_impact}")
        
        print("\nKEY PROPERTIES:")
        for prop in theory.key_properties:
            print(f" - {prop}")
            
        print("\nAPPLICATIONS:")
        for app in theory.applications:
            print(f" - {app}")
            
        print(f"\nRELATED CONCEPTS: {', '.join(theory.related_concepts)}")
        print(f"\nSIGNIFICANCE:\n{theory.significance}")
        print(f"\n{'='*80}\n")

    def display_summary(self):
        """Display a summary of available Riemann theories."""
        print(f"\n{'='*80}")
        print("SUMMARY OF RIEMANN THEORIES AND CONCEPTS")
        print(f"{'='*80}")
        
        if not self.available_theories:
            print("\n❌ Error: No theories found.")
            return

        try:
            user_prompt = PromptBuilder.get_summary_prompt(self.available_theories)
            model_input = ModelInput(
                system_prompt=PromptBuilder.get_system_prompt(),
                user_prompt=user_prompt
            )
            summary_text = self.client.generate_text(model_input)
            print(f"\n{summary_text}")
        except Exception as e:
            print(f"\n❌ Error fetching summary: {str(e)}")
        
        print(f"\n{'='*80}\n")
