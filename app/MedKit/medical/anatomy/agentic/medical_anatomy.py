#!/usr/bin/env python3
"""
Medical Anatomy module.

This module provides the core MedicalAnatomyGenerator class for generating
comprehensive anatomical information based on provided configuration.
"""

import logging
import sys
from pathlib import Path

# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

try:
    from .medical_anatomy_models import MedicalAnatomyModel, ModelOutput
    from .medical_anatomy_prompts import PromptBuilder
except (ImportError, ValueError):
    from medical.anatomy.agentic.medical_anatomy_models import MedicalAnatomyModel, ModelOutput
    from medical.anatomy.agentic.medical_anatomy_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalAnatomyGenerator:
    """Generates comprehensive anatomical information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.body_part = None  # Store the body part being analyzed
        logger.debug("Initialized MedicalAnatomyGenerator")

    def generate_text(self, body_part: str, structured: bool = False) -> ModelOutput:
        """Generates dual-stream (technical + layperson) anatomical information."""
        if not body_part or not str(body_part).strip():
            raise ValueError("Body part name cannot be empty")

        self.body_part = body_part
        logger.info(f"Starting dual-stream anatomical generation for: {body_part}")

        # 1. Technical Specialist Pass
        logger.debug(f"[Technical] Generating content for: {body_part}")
        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(body_part)

        response_format = MedicalAnatomyModel if structured else None
        tech_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        tech_result = self.ask_llm(tech_input)
        tech_md = tech_result.markdown if tech_result.markdown else ""
        
        # 2. Layperson Translator Pass
        logger.debug(f"[Layperson] Translating content for: {body_part}")
        lay_system = PromptBuilder.create_layperson_translator_system_prompt()
        lay_user = PromptBuilder.create_layperson_translator_user_prompt(tech_md)

        lay_input = ModelInput(
            system_prompt=lay_system,
            user_prompt=lay_user,
            response_format=None, # Translation is best as open markdown
        )

        lay_result = self.ask_llm(lay_input)
        lay_md = lay_result.markdown if lay_result.markdown else ""

        # 3. Combine Output
        combined_markdown = (
            f"# MEDICAL ANATOMY REPORT: {body_part.upper()}\n\n"
            f"## SECTION 1: FOR MEDICAL PROFESSIONALS (TECHNICAL)\n\n"
            f"{tech_md}\n\n"
            f"---\n\n"
            f"## SECTION 2: FOR PATIENTS & GENERAL AUDIENCE (PLAIN ENGLISH)\n\n"
            f"{lay_md}"
        )

        logger.info("✓ Successfully generated dual-stream anatomical information")
        
        return ModelOutput(
            data={"technical": tech_result.data, "layperson": lay_result.data},
            markdown=combined_markdown
        )

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the anatomical information to a file."""
        if self.body_part is None:
            raise ValueError(
                "No body part information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.body_part.lower().replace(' ', '_')}"

        return save_model_response(result, output_dir / base_filename)
