#!/usr/bin/env python3
"""
Riemann Theory Reference Guide
Dynamically fetches and documents Riemann-related mathematical theories and concepts,
using LiteClient (ollama/gemma3) for current and comprehensive information.
"""

import logging
import json
from pathlib import Path
from typing import Optional, List

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite import logging_config

try:
    from app.Riemann.shared.models import RiemannTheoryModel, ModelOutput
    from app.Riemann.shared.prompts import PromptBuilder
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from riemann_problems_models import RiemannTheoryModel, ModelOutput
    from riemann_problems_prompts import PromptBuilder

# Setup logging
logging_config.configure_logging(str(Path(__file__).parent / "logs" / "riemann_theory.log"))
logger = logging.getLogger(__name__)


class RiemannTheoryGuide:
    """Reference guide for various Riemann theories using LiteClient."""

    def __init__(self, config: Optional[ModelConfig] = None):
        """
        Initialize the guide with API client.

        Args:
            config: Optional ModelConfig. If not provided, uses sensible defaults.
        """
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
            else:
                logger.warning(f"Theories file not found: {self.theories_file}")
                return []
        except Exception as e:
            logger.error(f"Error loading theories: {str(e)}")
            return []

    def generate_text(self, theory_name: str) -> Optional[ModelOutput]:
        """
        Fetch information for a specific Riemann theory using a 3-tier approach.

        Args:
            theory_name: Name of the theory or concept

        Returns:
            ModelOutput instance or None if fetch fails
        """
        try:
            logger.info(f"Fetching 3-tier Riemann theory '{theory_name}' from API")

            # Tier 1: Specialist (JSON)
            model_input = ModelInput(
                system_prompt=PromptBuilder.get_system_prompt(),
                user_prompt=PromptBuilder.get_user_prompt(theory_name),
                response_format=RiemannTheoryModel
            )
            theory_res = self.client.generate_text(model_input)
            theory_data: RiemannTheoryModel = theory_res.data

            # Tier 3: Output Synthesis (Markdown Closer)
            # In this simple app, we can use the LLM to generate a nice narrative from the data
            synth_prompt = f"Synthesize a beautiful Markdown reference report for the theory: {theory_name}\n\nDATA:\n{theory_data.model_dump_json(indent=2)}"
            synth_input = ModelInput(
                system_prompt="You are a Lead Mathematical Editor. Synthesize raw theory data into a professional Markdown report.",
                user_prompt=synth_prompt,
                response_format=None
            )
            final_markdown = self.client.generate_text(synth_input).markdown

            logger.info(f"Successfully synthesized theory: {theory_name}")
            return ModelOutput(
                data=theory_data,
                markdown=final_markdown,
                metadata={"process": "2-stage fetch-and-synthesize"}
            )

        except Exception as e:
            logger.error(f"Error fetching theory '{theory_name}': {str(e)}")
            return None

    def save_to_file(self, output: ModelOutput, theory_name: str, output_dir: str) -> str:
        """
        Save a Riemann theory artifact to Markdown and JSON.
        """
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            safe_name = theory_name.lower().replace(' ', '_').replace('/', '_').replace(':', '_')
            md_path = output_path / f"riemann_{safe_name}.md"
            json_path = output_path / f"riemann_{safe_name}.json"
            
            if output.markdown:
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(output.markdown)
            
            if output.data:
                with open(json_path, 'w', encoding='utf-8') as f:
                    f.write(output.data.model_dump_json(indent=4))
            
            logger.info(f"Saved theory artifact '{theory_name}' to {output_dir}")
            return str(md_path)
            
        except Exception as e:
            logger.error(f"Error saving theory '{theory_name}': {str(e)}")
            raise

    @staticmethod
    def display_theory(output: ModelOutput):
        """Display synthesized information about a Riemann theory."""
        if not output or not output.markdown:
            print("\n❌ Error: No theory information available.")
            return

        print(f"\n{output.markdown}\n")

    def display_summary(self):
        """Display a summary of available Riemann theories."""
        print(f"\n{'='*80}")
        print("SUMMARY OF RIEMANN THEORIES AND CONCEPTS")
        print(f"{'='*80}")
        
        if not self.available_theories:
            print("\n❌ Error: No theories found in assets.")
            return

        print(f"\nFound {len(self.available_theories)} theories in assets/riemann.txt.")
        print("\nFetching overview information from AI...")
        
        try:
            user_prompt = PromptBuilder.get_summary_prompt(self.available_theories)
            model_input = ModelInput(
                system_prompt=PromptBuilder.get_system_prompt(),
                user_prompt=user_prompt
            )
            summary_text = self.client.generate_text(model_input).markdown
            print(f"\n{summary_text}")
        except Exception as e:
            logger.error(f"Error fetching summary: {str(e)}")
            print(f"\n❌ Error fetching summary: {str(e)}")
        
        print(f"\n{'='*80}\n")
