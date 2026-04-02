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
        """Analyzes drug-disease interactions using a 3-tier system."""
        self.config = config
        
        # Check cache
        cached_result = self.cache.get(config.medicine_name, config.condition_name, config.age, config.condition_severity)
        if cached_result: return cached_result

        logger.info(f"Starting 3-tier analysis for: {config.medicine_name} vs {config.condition_name}")

        try:
            # --- Tier 1: Specialists (JSON Sequential) ---
            logger.info("Tier 1: Specialists running...")
            # 1. PubMed
            real_ev = PubMedTool.get_evidence(config.medicine_name, config.condition_name)
            pubmed_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_pubmed_system_prompt(),
                user_prompt=f"Evidence for {config.medicine_name} and {config.condition_name}:\n{real_ev}"
            )).markdown

            # 2. Researcher
            researcher_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_researcher_system_prompt(),
                user_prompt=PromptBuilder.create_researcher_user_prompt(config, pubmed_res)
            )).markdown

            # 3. Pharmacologist
            pharmacologist_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_pharmacologist_system_prompt(),
                user_prompt=PromptBuilder.create_pharmacologist_user_prompt(config, researcher_res)
            )).markdown

            # 4. Clinician
            clinician_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_clinician_system_prompt(),
                user_prompt=PromptBuilder.create_clinician_user_prompt(config, pharmacologist_res, researcher_res)
            )).markdown
            if hitl: clinician_res = HITLManager.request_approval("Clinical Safety", clinician_res.markdown)
            else: clinician_res = clinician_res.markdown

            spec_data_json = f"PUBMED:\n{pubmed_res}\n\nRESEARCH:\n{researcher_res}\n\nPHARMA:\n{pharmacologist_res}\n\nCLINICAL:\n{clinician_res}"

            # --- Tier 2: Compliance Auditor (JSON Audit) ---
            logger.info("Tier 2: Compliance Auditor running...")
            audit_res = self._ask_llm(ModelInput(
                system_prompt=PromptBuilder.create_compliance_system_prompt(),
                user_prompt=PromptBuilder.create_compliance_user_prompt(clinician_res, "Patient guidance included in clinical."),
                response_format=None # Audit result
            ))
            audit_json = audit_res.markdown

            # --- Tier 3: Final Output Synthesis (Markdown Closer) ---
            logger.info("Tier 3: Output Synthesis running...")
            out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(config, spec_data_json, audit_json)
            final_res = self._ask_llm(ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None
            ))

            return ModelOutput(
                data=None, # Tier 1 data is complex here, can be added if needed
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier Analysis failed: {e}")
            raise

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
