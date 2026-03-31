#!/usr/bin/env python3
"""
Medical Ethics module.

This module provides the core MedEthicsGenerator class for generating
comprehensive medical ethics analysis based on provided configuration.
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
    from .med_ethics_models import EthicalAnalysisModel, ModelOutput
    from .med_ethics_prompts import PromptBuilder
except (ImportError, ValueError):
    from medical.med_ethics.nonagentic.med_ethics_models import EthicalAnalysisModel, ModelOutput
    from medical.med_ethics.nonagentic.med_ethics_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedEthicalQA:
    """Generates comprehensive medical ethics analysis."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.question = None  # Store the ethics question being analyzed
        logger.debug("Initialized MedEthicalQA")

    def generate_text(self, question: str, structured: bool = False) -> ModelOutput:
        """Generate comprehensive medical ethics analysis."""
        if not question or not str(question).strip():
            raise ValueError("Medical ethics question or scenario cannot be empty")

        # Store the question for later use in save
        self.question = question
        logger.debug(f"Starting medical ethics analysis for: {question[:50]}...")

        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(question)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = EthicalAnalysisModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            logger.debug("✓ Successfully generated medical ethics analysis")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating medical ethics analysis: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        response = self.client.generate_text(model_input=model_input)

        if isinstance(response, ModelOutput):
            return response
        elif isinstance(response, EthicalAnalysisModel):
            return ModelOutput(data=response)
        elif isinstance(response, str):
            return ModelOutput(markdown=response)
        else:
            # Handle cases where it might be some other type
            return ModelOutput(markdown=str(response))

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical ethics analysis to a file (JSON if structured, Markdown otherwise)."""
        if self.question is None:
            raise ValueError(
                "No medical ethics question available. Call generate_text first."
            )

        import re

        if result.data:
            # Structured output - Save as JSON using the title for filename
            title = result.data.case_title or self.question[:50]
            sanitized_title = (
                re.sub(r"[^\w\s-]", "", title).strip().lower().replace(" ", "_")
            )
            logger.info(
                f"✓ Saving structured analysis to {output_dir / sanitized_title}.json"
            )
            return save_model_response(result, output_dir / sanitized_title)

        # Markdown output
        md_content = result.markdown
        if not md_content:
            raise ValueError("No content to save.")

        first_line = md_content.split("\n")[0].strip("*# ")
        sanitized_title = (
            re.sub(r"[^\w\s-]", "", first_line).strip().lower().replace(" ", "_")
        )

        filename = f"{sanitized_title}.md"
        file_path = output_dir / filename

        with open(file_path, "w") as f:
            f.write(md_content)

        logger.info(f"✓ Saved markdown analysis to {file_path}")
        return file_path
