"""
Drug Identifier module.

This module provides the DrugIdentifier class for determining if a drug
is well-known in the industry.
"""

import logging
from pathlib import Path

from lite.utils import save_model_response

from ..base_recognizer import BaseRecognizer
from .drug_recognizer_model import DrugIdentifierModel, ModelOutput
from .drug_recognizer_prompts import DrugIdentifierInput, PromptBuilder

logger = logging.getLogger(__name__)


class DrugIdentifier(BaseRecognizer):
    """Identifies drugs and their industry recognition status."""

    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        """
        Identifies if a drug is well-known in the industry.

        Args:
            name: Name of the drug to identify
            structured: Whether to use structured output

        Returns:
            ModelOutput: The identification result
        """
        config = DrugIdentifierInput(drug_name=name)
        self.config = config

        logger.debug(f"Starting drug identification for: {name}")

        response = self._generate(
            system_prompt=PromptBuilder.create_system_prompt(),
            user_prompt=PromptBuilder.create_user_prompt(config),
            response_format=DrugIdentifierModel if structured else None,
        )

        logger.debug(f"✓ Successfully identified drug: {name}")

        if structured:
            return ModelOutput(data=response)
        else:
            return ModelOutput(markdown=response)

    def identify_drug(self, drug_name: str, structured: bool = False) -> ModelOutput:
        """Legacy method for backward compatibility."""
        return self.identify(drug_name, structured)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the drug identification analysis to a file."""
        if not hasattr(self, "config") or self.config is None:
            raise ValueError(
                "No configuration information available. Call identify first."
            )

        drug_safe = self.config.drug_name.lower().replace(" ", "_")
        base_filename = f"{drug_safe}_identification"

        return save_model_response(result, output_dir / base_filename)
