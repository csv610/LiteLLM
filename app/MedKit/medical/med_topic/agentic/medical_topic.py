#!/usr/bin/env python3
"""
Medical Topic module.

This module provides the core MedicalTopicGenerator class for generating
comprehensive medical topic information based on provided configuration.
"""

import logging
from pathlib import Path

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

from .medical_topic_models import MedicalTopicModel, ModelOutput
from .medical_topic_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalTopicGenerator:
    """Generates comprehensive medical topic information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.topic = None  # Store the topic being analyzed
        logger.debug("Initialized MedicalTopicGenerator")

    def generate_text(self, topic: str, structured: bool = False) -> ModelOutput:
        """Generates 3-tier medical topic information: Specialist -> Auditor -> Output."""
        if not topic or not str(topic).strip():
            raise ValueError("Topic name cannot be empty")

        self.topic = topic
        logger.info(f"Starting 3-tier topic generation for: {topic}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug(f"[Specialist] Generating content for: {topic}")
            system_prompt = PromptBuilder.create_system_prompt()
            user_prompt = PromptBuilder.create_user_prompt(topic)

            spec_input = ModelInput(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=MedicalTopicModel if structured else None,
            )
            spec_res = self.ask_llm(spec_input)
            
            if structured:
                spec_json = spec_res.data.model_dump_json(indent=2)
            else:
                spec_json = spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            logger.debug(f"[Auditor] Auditing content for: {topic}")
            audit_sys, audit_usr = PromptBuilder.get_topic_auditor_prompts(topic, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit is markdown/json
            )
            audit_res = self.ask_llm(audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown Closer)
            logger.debug(f"[Output] Synthesizing final report for: {topic}")
            out_sys, out_usr = PromptBuilder.get_output_synthesis_prompts(topic, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.ask_llm(out_input)

            logger.info("✓ Successfully generated 3-tier medical topic information")
            return ModelOutput(
                data=spec_res.data, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier Topic generation failed: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical topic information to a file."""
        if self.topic is None:
            raise ValueError(
                "No topic information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.topic.lower().replace(' ', '_')}"

        return save_model_response(result, output_dir / base_filename)
