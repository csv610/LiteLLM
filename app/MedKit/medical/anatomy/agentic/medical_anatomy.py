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
        """Generates 3-tier anatomical information: Specialist -> Auditor -> Output."""
        if not body_part or not str(body_part).strip():
            raise ValueError("Body part name cannot be empty")

        self.body_part = body_part
        logger.info(f"Starting 3-tier anatomical generation for: {body_part}")

        # 1. Technical Specialist Pass (JSON Specialist)
        logger.debug(f"[Specialist] Generating content for: {body_part}")
        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(body_part)

        response_format = MedicalAnatomyModel if structured else None
        tech_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        tech_result = self.ask_llm(tech_input)
        if structured:
            tech_content = tech_result.data.model_dump_json(indent=2)
        else:
            tech_content = tech_result.markdown
        
        # 2. Compliance Auditor Pass (JSON Auditor)
        logger.debug(f"[Auditor] Auditing content for: {body_part}")
        audit_system = PromptBuilder.create_fact_checker_system_prompt()
        audit_user = PromptBuilder.create_fact_checker_user_prompt(tech_content)

        audit_input = ModelInput(
            system_prompt=audit_system,
            user_prompt=audit_user,
            response_format=None, # For simplicity, can be JSON if a model exists
        )

        audit_result = self.ask_llm(audit_input)
        audit_content = audit_result.markdown # Usually JSON string in markdown
        
        # 3. Final Output Synthesis (Markdown Closer)
        logger.debug(f"[Output] Synthesizing final report for: {body_part}")
        out_sys, out_user = PromptBuilder.create_output_synthesis_prompts(
            body_part, tech_content, audit_content
        )

        output_input = ModelInput(
            system_prompt=out_sys,
            user_prompt=out_user,
            response_format=None,
        )

        output_result = self.ask_llm(output_input)
        final_markdown = output_result.markdown

        logger.info("✓ Successfully generated 3-tier anatomical information")
        
        return ModelOutput(
            data=tech_result.data if structured else None,
            markdown=final_markdown,
            metadata={"audit": audit_content}
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
