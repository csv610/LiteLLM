"""Similar Drugs Finder.

This module contains the core logic for finding similar medicines based on
active ingredients, therapeutic classes, and mechanisms of action.
"""

from pathlib import Path
from typing import Optional, Union

from lite.config import ModelConfig
from lite.lite_client import LiteClient
from lite.logging_config import configure_logging
from lite.config import ModelInput

from similar_drugs_models import SimilarMedicinesResult
from similar_drugs_prompts import PromptBuilder


class SimilarDrugs:
    """Finds similar drugs based on provided configuration."""

    def __init__(self, config: 'SimilarDrugsConfig', model_config: ModelConfig):
        self.config = config
        self.client = LiteClient(model_config)

        # Apply verbosity level using centralized logging configuration
        configure_logging(
            log_file=str(Path(__file__).parent / "logs" / "similar_drugs.log"),
            verbosity=self.config.verbosity,
            enable_console=True
        )

    def find(
        self,
        medicine_name: str,
        include_generics: bool = True,
        patient_age: Optional[int] = None,
        patient_conditions: Optional[str] = None,
        structured: bool = False,
    ) -> Union[SimilarMedicinesResult, str]:
        """
        Finds top 10-15 medicines similar to a given medicine.

        Args:
            medicine_name: Name of the medicine to find alternatives for
            include_generics: Whether to include generic formulations (default: True)
            patient_age: Patient's age in years (optional, 0-150)
            patient_conditions: Patient's medical conditions (optional, comma-separated)
            structured: Whether to return structured output (default: False)

        Returns:
            SimilarMedicinesResult or str: Top 10-15 similar medicines with detailed information
        """
        # Validate inputs
        if not medicine_name or not medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if patient_age is not None and (patient_age < 0 or patient_age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        output_path = self.config.output_path
        if output_path is None:
            medicine_clean = medicine_name.lower().replace(' ', '_')
            output_path = Path("outputs") / f"{medicine_clean}_similar_medicines.json"

        output_path.parent.mkdir(parents=True, exist_ok=True)

        context_parts = [f"Finding top 10-15 medicines similar to {medicine_name}"]
        if include_generics:
            context_parts.append("Include generic formulations")
        if patient_age is not None:
            context_parts.append(f"Patient age: {patient_age} years")
        if patient_conditions:
            context_parts.append(f"Patient conditions: {patient_conditions}")

        context = ". ".join(context_parts) + "." if context_parts else ""

        response_format = None
        if structured:
            response_format = SimilarMedicinesResult

        # Use PromptBuilder for consistent prompt generation
        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(medicine_name, context)

        result = self.client.generate_text(
            model_input=ModelInput(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=response_format,
            )
        )

        return result
