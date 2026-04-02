#!/usr/bin/env python3
"""
Disease Information module.

This module provides the core DiseaseInfoGenerator class for generating
comprehensive disease information based on provided configuration.
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
    from .disease_info_models import DiseaseInfoModel, ModelOutput
    from .disease_info_prompts import PromptBuilder
except (ImportError, ValueError):
    from medical.disease_info.agentic.disease_info_models import DiseaseInfoModel, ModelOutput
    from medical.disease_info.agentic.disease_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class DiseaseInfoGenerator:
    """Generates comprehensive disease information."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.disease = None  # Store the disease being analyzed
        logger.debug("Initialized DiseaseInfoGenerator")

    def generate_text(self, disease: str, structured: bool = False) -> ModelOutput:
        """Generate 3-tier comprehensive disease information."""
        if not disease or not str(disease).strip():
            raise ValueError("Disease name cannot be empty")

        self.disease = disease
        logger.info(f"Starting 3-tier disease information generation for: {disease}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug(f"[Specialist] Generating content for: {disease}")
            system_prompt = PromptBuilder.create_system_prompt()
            user_prompt = PromptBuilder.create_user_prompt(disease)
            
            spec_input = ModelInput(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=DiseaseInfoModel if structured else None,
            )
            spec_res = self.ask_llm(spec_input)
            
            if structured:
                spec_json = spec_res.data.model_dump_json(indent=2)
            else:
                spec_json = spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            logger.debug(f"[Auditor] Auditing content for: {disease}")
            audit_sys, audit_usr = PromptBuilder.get_disease_auditor_prompts(disease, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit result
            )
            audit_res = self.ask_llm(audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug(f"[Output] Synthesizing final report for: {disease}")
            out_sys, out_usr = PromptBuilder.get_output_synthesis_prompts(disease, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.ask_llm(out_input)

            logger.info("✓ Successfully generated 3-tier disease information")
            return ModelOutput(
                data=spec_res.data if structured else None, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier disease generation failed: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the disease information to a file."""
        if self.disease is None:
            raise ValueError(
                "No disease information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.disease.lower().replace(' ', '_')}"

        return save_model_response(result, output_dir / base_filename)
