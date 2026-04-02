"""
paradox_element.py - ParadoxExplainer class for paradox explanations

Contains the ParadoxExplainer class for fetching and managing
paradox explanations with high academic rigor.
"""

import json
import logging
from typing import Optional, List

from lite import LiteClient, ModelConfig
from lite.config import ModelInput

from app.Paradox.shared.models import Paradox, ParadoxResponse, AudienceLevel


class ParadoxExplainer:
    """Class for fetching and managing paradox explanations."""
    
    def __init__(self, model_config: ModelConfig):
        """Initialize the explainer with a ModelConfig.
        
        Args:
            model_config: Configured ModelConfig for API calls
        """
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.logger = logging.getLogger(__name__)
    
    def fetch_paradox_explanation(self, paradox_name: str, audience_levels: List[AudienceLevel] = None) -> Optional[Paradox]:
        """Fetch explanations for a paradox across specified audience levels.
        
        Args:
            paradox_name: Name of the paradox
            audience_levels: List of AudienceLevel enums to fetch for. Defaults to all levels.
            
        Returns:
            Paradox object with detailed explanations, or None if failed
        """
        if audience_levels is None:
            audience_levels = [AudienceLevel.UNDERGRAD]
            
        levels_str = ", ".join([level.value for level in audience_levels])
        
        try:
            prompt = (
                f"Explain the paradox '{paradox_name}' to the following audiences: {levels_str}.\n"
                f"ACADEMIC RIGOR MANDATE:\n"
                f"1. ROOT CAUSE: Identify the exact 'hidden assumptions' or category errors in the underlying theories.\n"
                f"2. HISTORICAL ACCURACY: Reference key philosophers/scientists (e.g., Aristotle's potential vs. actual infinity, Russell's At-At theory, etc.).\n"
                f"3. STATUS & RESOLUTION: Distinguish between mathematical solutions (e.g., convergence) and physical/metaphysical resolutions.\n"
                f"For each audience level, provide:\n"
                f"1. Introduction\n"
                f"2. Status (Solved, Unsolved, Under Debate, or Partially Solved)\n"
                f"3. Root Cause (The specific hidden assumptions or theoretical category errors causing the paradox)\n"
                f"4. Key concepts (A list of fundamental concepts with precise definitions)\n"
                f"5. Historical context (Historical motivation and the specific school of thought)\n"
                f"6. The contradiction (The core counter-intuitive nature explained rigorously)\n"
                f"7. Modern relevance (Connection to modern physics, logic, or computer science)\n"
                f"8. Impact on thought (How it forced the evolution of human knowledge)\n"
                f"9. Current debates (High-level open questions or persistent philosophical issues)\n"
                f"10. Resolutions:\n"
                f"   - Who Solved It (Acknowledge multiple contributors: e.g., Aristotle, Newton, Russell)\n"
                f"   - How It Was Solved (The exact breakthrough: e.g., Real Analysis, Set Theory, at-at theory)\n"
                f"   - Logical details\n"
                f"   - Mathematical/Scientific details\n"
                f"Ensure the tone is scholarly and the logic is airtight."
            )
            
            model_input = ModelInput(user_prompt=prompt, response_format=ParadoxResponse)
            response_content = self.client.generate_text(model_input=model_input)

            if isinstance(response_content, ParadoxResponse):
                return response_content.paradox
            elif isinstance(response_content, str):
                data = json.loads(response_content)
                if "paradox" in data:
                    return Paradox(**data["paradox"])
            return None
        except Exception as e:
            self.logger.error(f"Error fetching paradox '{paradox_name}': {str(e)}")
            return None
