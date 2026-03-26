"""
math_theory_element.py - MathTheoryExplainer class for mathematical theory explanations

Contains the MathTheoryExplainer class for fetching and managing
mathematical theory information tailored to different audience levels.
"""

import json
import logging
from typing import Optional, List

from lite import LiteClient, ModelConfig
from lite.config import ModelInput

from math_theory_models import MathTheory, TheoryResponse, AudienceLevel


class MathTheoryExplainer:
    """Class for fetching and managing mathematical theory explanations."""
    
    def __init__(self, model_config: ModelConfig):
        """Initialize the explainer with a ModelConfig.
        
        Args:
            model_config: Configured ModelConfig for API calls
        """
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.logger = logging.getLogger(__name__)
    
    def fetch_theory_explanation(self, theory_name: str, audience_levels: List[AudienceLevel] = None) -> Optional[MathTheory]:
        """Fetch explanations for a mathematical theory across specified audience levels.
        
        Args:
            theory_name: Name of the mathematical theory
            audience_levels: List of AudienceLevel enums to fetch for. Defaults to all levels.
            
        Returns:
            MathTheory object with detailed explanations, or None if failed
        """
        if audience_levels is None:
            audience_levels = [AudienceLevel.UNDERGRAD]
            
        levels_str = ", ".join([level.value for level in audience_levels])
        
        try:
            prompt = (
                f"Explain the mathematical theory '{theory_name}' to the following audiences: {levels_str}.\n"
                f"For the 'general' audience, assume they have NO mathematical background; use analogies and avoid technical jargon.\n"
                f"For each audience level, provide:\n"
                f"1. Introduction\n"
                f"2. Key concepts (A list of fundamental concepts necessary to understand this theory)\n"
                f"3. Why it was created (Historical context and motivation)\n"
                f"4. What problems it solved or simplified\n"
                f"5. How it is used today (Modern applications)\n"
                f"6. How it was the foundation for other theories\n"
                f"7. New research (Current areas and open questions)\n"
                f"8. Solution methods (Analytical and numerical)\n"
                f"Ensure the tone and complexity are appropriate for each audience level."
            )
            
            model_input = ModelInput(user_prompt=prompt, response_format=TheoryResponse)
            response_content = self.client.generate_text(model_input=model_input)

            if isinstance(response_content, TheoryResponse):
                return response_content.theory
            elif isinstance(response_content, str):
                data = json.loads(response_content)
                if "theory" in data:
                    return MathTheory(**data["theory"])
            return None
        except Exception as e:
            self.logger.error(f"Error fetching theory '{theory_name}': {str(e)}")
            return None
