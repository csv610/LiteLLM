#!/usr/bin/env python3
"""
Drug-Disease Interaction Analysis module.

This module provides the core DrugDiseaseInteraction class for analyzing
how medical conditions affect drug efficacy, safety, and metabolism.
"""

import logging
from pathlib import Path

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

try:
    from .drug_disease_interaction_models import (
        DrugDiseaseInteractionModel,
        ModelOutput,
    )
    from .drug_disease_interaction_prompts import DrugDiseaseInput, PromptBuilder
    from .pubmed_utils import PubMedTool
    from .cache_utils import InteractionCache
    from .hitl_utils import HITLManager
except ImportError:
    from drug_disease_interaction_models import DrugDiseaseInteractionModel, ModelOutput
    from drug_disease_interaction_prompts import DrugDiseaseInput, PromptBuilder
    from pubmed_utils import PubMedTool
    from cache_utils import InteractionCache
    from hitl_utils import HITLManager

logger = logging.getLogger(__name__)


class DrugDiseaseInteraction:
    """Analyzes drug-disease interactions based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.cache = InteractionCache()
        self.config = None  # Store the configuration for later use in save
        logger.debug("Initialized DrugDiseaseInteraction with Caching and HITL support")

    def generate_text(
        self, config: DrugDiseaseInput, structured: bool = False, hitl: bool = False
    ) -> ModelOutput:
        """
        Analyzes how a medical condition affects drug efficacy, safety, and metabolism using multiple specialized agents.

        Args:
            config: Configuration and input for analysis
            structured: Whether to use structured output

        Returns:
            ModelOutput: The analysis result
        """
        # Store the configuration for later use in save
        self.config = config
        
        # Check cache first
        cached_result = self.cache.get(
            config.medicine_name, 
            config.condition_name, 
            config.age, 
            config.condition_severity
        )
        if cached_result:
            logger.info("✓ Cache Hit: Returning cached analysis result")
            return cached_result

        logger.debug("Starting multi-agent drug-disease interaction analysis")
        logger.debug(f"Medicine: {config.medicine_name}")
        logger.debug(f"Condition: {config.condition_name}")

        # 1. PubMed Agent
        logger.info("Agent 1/8: Running PubMed Literature Specialist...")
        real_evidence = PubMedTool.get_evidence(config.medicine_name, config.condition_name)

        pubmed_input = ModelInput(
            system_prompt=PromptBuilder.create_pubmed_system_prompt(),
            user_prompt=f"Summarize these real PubMed literature results for {config.medicine_name} and {config.condition_name}:\n{real_evidence}",
        )
        pubmed_out = self._ask_llm(pubmed_input).markdown


        # 2. Researcher Agent
        logger.info("Agent 2/8: Running Medical Researcher...")
        researcher_input = ModelInput(
            system_prompt=PromptBuilder.create_researcher_system_prompt(),
            user_prompt=PromptBuilder.create_researcher_user_prompt(config, pubmed_out),
        )
        researcher_out = self._ask_llm(researcher_input).markdown

        # 3. Pharmacologist Agent
        logger.info("Agent 3/8: Running Pharmacology Analyst...")
        pharmacologist_input = ModelInput(
            system_prompt=PromptBuilder.create_pharmacologist_system_prompt(),
            user_prompt=PromptBuilder.create_pharmacologist_user_prompt(config, researcher_out),
        )
        pharmacologist_out = self._ask_llm(pharmacologist_input).markdown

        # 4. DDI Agent
        logger.info("Agent 4/8: Running DDI Specialist...")
        ddi_input = ModelInput(
            system_prompt=PromptBuilder.create_ddi_system_prompt(),
            user_prompt=PromptBuilder.create_ddi_user_prompt(config, pharmacologist_out),
        )
        ddi_out = self._ask_llm(ddi_input).markdown

        # 5. Clinician Agent
        logger.info("Agent 5/8: Running Clinical Safety Expert...")
        clinician_input = ModelInput(
            system_prompt=PromptBuilder.create_clinician_system_prompt(),
            user_prompt=PromptBuilder.create_clinician_user_prompt(config, pharmacologist_out, researcher_out),
        )
        clinician_out = self._ask_llm(clinician_input).markdown
        
        # HITL Hook
        if hitl:
            clinician_out = HITLManager.request_approval("Clinical Safety Agent", clinician_out)

        # 6. Educator Agent
        logger.info("Agent 6/8: Running Patient Education Specialist...")
        educator_input = ModelInput(
            system_prompt=PromptBuilder.create_educator_system_prompt(),
            user_prompt=PromptBuilder.create_educator_user_prompt(clinician_out, pharmacologist_out),
        )
        educator_out = self._ask_llm(educator_input).markdown

        # 7. Compliance Agent
        logger.info("Agent 7/8: Running Medical Compliance Officer...")
        compliance_input = ModelInput(
            system_prompt=PromptBuilder.create_compliance_system_prompt(),
            user_prompt=PromptBuilder.create_compliance_user_prompt(clinician_out, educator_out),
        )
        compliance_out = self._ask_llm(compliance_input).markdown

        # 8. Orchestrator Agent
        logger.info("Agent 8/8: Running Orchestrator & Synthesizer...")
        response_format = None
        if structured:
            response_format = DrugDiseaseInteractionModel

        orchestrator_input = ModelInput(
            system_prompt=PromptBuilder.create_orchestrator_system_prompt(),
            user_prompt=PromptBuilder.create_orchestrator_user_prompt(
                config, researcher_out, pharmacologist_out, clinician_out, educator_out, compliance_out, ddi_out
            ),
            response_format=response_format,
        )
        result = self._ask_llm(orchestrator_input)

        # Save to cache
        self.cache.set(
            config.medicine_name, 
            config.condition_name, 
            config.age, 
            config.condition_severity, 
            result
        )

        logger.debug("✓ Successfully analyzed disease interaction using multi-agent system")
        return result

    def _ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Helper to call LiteClient with error handling and normalization."""
        logger.debug("Calling LiteClient...")
        try:
            response = self.client.generate_text(model_input=model_input)
            
            # Normalize response to ModelOutput
            if isinstance(response, ModelOutput):
                return response
            elif hasattr(response, "markdown"):
                return response
            else:
                # Handle string or other unexpected types
                return ModelOutput(markdown=str(response))
                
        except Exception as e:
            logger.error(f"✗ Error during LLM analysis: {e}")
            logger.exception("Full exception details:")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the drug-disease interaction analysis to a file."""
        if self.config is None:
            raise ValueError(
                "No configuration information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        medicine_safe = self.config.medicine_name.lower().replace(" ", "_")
        condition_safe = self.config.condition_name.lower().replace(" ", "_")
        base_filename = f"{medicine_safe}_{condition_safe}_interaction"

        return save_model_response(result, output_dir / base_filename)
