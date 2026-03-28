#!/usr/bin/env python3
"""
Medical Procedure Information module.

This module provides the core MedicalProcedureInfoGenerator class for generating
comprehensive medical procedure information based on provided configuration using
a multi-agent approach, including parallel domain agents and a sequential compliance auditor.
"""

import concurrent.futures
import logging
from pathlib import Path
from typing import Optional

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

from .medical_procedure_info_models import (
    AdminAgentOutput,
    ClinicalAgentOutput,
    ComplianceReport,
    MedicalProcedureInfoModel,
    ModelOutput,
    RecoveryAgentOutput,
    RiskAgentOutput,
    TechnicalAgentOutput,
)
from .medical_procedure_info_prompts import (
    AdminPromptBuilder,
    ClinicalPromptBuilder,
    CompliancePromptBuilder,
    RecoveryPromptBuilder,
    RiskPromptBuilder,
    TechnicalPromptBuilder,
)

logger = logging.getLogger(__name__)


class MedicalProcedureInfoGenerator:
    """Generate comprehensive information for medical procedures using a multi-agent approach."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.procedure_name: Optional[str] = None
        logger.debug("Initialized MedicalProcedureInfoGenerator")

    def generate_text(self, procedure: str, structured: bool = False) -> ModelOutput:
        """Generate and retrieve comprehensive medical procedure information."""
        if not procedure or not procedure.strip():
            raise ValueError("Procedure name cannot be empty")

        # Store the procedure for later use in save
        self.procedure_name = procedure
        logger.debug(
            f"Starting multi-agent medical procedure information generation for: {procedure}"
        )

        # Step 1: Parallel Domain Agents (Scatter)
        agents = [
            ("Clinical", ClinicalPromptBuilder, ClinicalAgentOutput),
            ("Technical", TechnicalPromptBuilder, TechnicalAgentOutput),
            ("Risk", RiskPromptBuilder, RiskAgentOutput),
            ("Recovery", RecoveryPromptBuilder, RecoveryAgentOutput),
            ("Admin", AdminPromptBuilder, AdminAgentOutput),
        ]

        def call_agent(agent_name, prompt_builder, output_model) -> ModelOutput:
            sys_prompt = prompt_builder.create_system_prompt()
            usr_prompt = prompt_builder.create_user_prompt(procedure)
            
            logger.debug(f"[{agent_name} Agent] System Prompt: {sys_prompt}")
            logger.debug(f"[{agent_name} Agent] User Prompt: {usr_prompt}")
            
            response_format = output_model if structured else None
            
            model_input = ModelInput(
                system_prompt=sys_prompt,
                user_prompt=usr_prompt,
                response_format=response_format,
            )
            
            logger.debug(f"[{agent_name} Agent] Calling LiteClient.generate_text()...")
            try:
                result = self.client.generate_text(model_input=model_input)
                logger.debug(f"[{agent_name} Agent] ✓ Successfully generated information")
                return result
            except Exception as e:
                logger.error(f"[{agent_name} Agent] ✗ Error generating information: {e}")
                raise

        futures = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for name, builder, model in agents:
                futures[name] = executor.submit(call_agent, name, builder, model)
            
            concurrent.futures.wait(futures.values())

        # Step 2: Gather Results
        if not structured:
            combined_markdown = "\n\n".join(
                [f.result().markdown or "" for name, f in futures.items() if not f.exception()]
            )
            return ModelOutput(data=None, markdown=combined_markdown)

        # Merge structured results
        try:
            clinical_data = futures["Clinical"].result().data
            technical_data = futures["Technical"].result().data
            risk_data = futures["Risk"].result().data
            recovery_data = futures["Recovery"].result().data
            admin_data = futures["Admin"].result().data
            
            final_data = MedicalProcedureInfoModel(
                metadata=clinical_data.metadata,
                purpose=clinical_data.purpose,
                indications=clinical_data.indications,
                preparation=recovery_data.preparation,
                details=technical_data.details,
                risks=risk_data.risks,
                recovery=recovery_data.recovery,
                outcomes=recovery_data.outcomes,
                follow_up=recovery_data.follow_up,
                alternatives=clinical_data.alternatives,
                technical=technical_data.technical,
                evidence=technical_data.evidence,
                cost_and_insurance=admin_data.cost_and_insurance,
                education=admin_data.education,
            )
            
            combined_markdown = "\n\n".join(
                [f.result().markdown or "" for name, f in futures.items() if not f.exception() and f.result().markdown]
            )

            # Step 3: Compliance Audit (Sequential)
            logger.debug(f"Starting compliance audit for: {procedure}")
            audit_content = final_data.model_dump_json(indent=2)
            
            audit_sys_prompt = CompliancePromptBuilder.create_system_prompt()
            audit_usr_prompt = CompliancePromptBuilder.create_user_prompt(procedure, audit_content)
            
            audit_input = ModelInput(
                system_prompt=audit_sys_prompt,
                user_prompt=audit_usr_prompt,
                response_format=ComplianceReport,
            )
            
            compliance_report = None
            try:
                audit_result = self.client.generate_text(model_input=audit_input)
                compliance_report = audit_result.data
                logger.debug("✓ Compliance audit completed")
            except Exception as e:
                logger.error(f"✗ Compliance audit failed: {e}")
            
            return ModelOutput(
                data=final_data, 
                markdown=combined_markdown,
                compliance_report=compliance_report
            )
        except Exception as e:
            logger.error(f"✗ Error merging multi-agent results: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the medical procedure information to a file."""
        if self.procedure_name is None:
            raise ValueError(
                "No procedure information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.procedure_name.lower().replace(' ', '_')}"

        return save_model_response(result, output_dir / base_filename)
