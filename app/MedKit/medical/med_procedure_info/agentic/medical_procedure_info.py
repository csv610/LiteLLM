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
    OutputPromptBuilder,
    RecoveryPromptBuilder,
    RiskPromptBuilder,
    TechnicalPromptBuilder,
)

logger = logging.getLogger(__name__)


class MedicalProcedureInfoGenerator:
    """Generate comprehensive information for medical procedures using a 3-tier multi-agent approach."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.procedure_name: Optional[str] = None
        logger.debug("Initialized 3-tier MedicalProcedureInfoGenerator")

    def generate_text(self, procedure: str, structured: bool = False) -> ModelOutput:
        """Generate and retrieve comprehensive medical procedure information."""
        if not procedure or not procedure.strip():
            raise ValueError("Procedure name cannot be empty")

        # Store the procedure for later use in save
        self.procedure_name = procedure
        logger.debug(
            f"Starting 3-tier multi-agent medical procedure information generation for: {procedure}"
        )

        # Step 1: Parallel Domain Agents (Scatter - JSON Specialists)
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
            
            response_format = output_model if structured else None
            
            model_input = ModelInput(
                system_prompt=sys_prompt,
                user_prompt=usr_prompt,
                response_format=response_format,
            )
            
            try:
                result = self.client.generate_text(model_input=model_input)
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
        final_data = None
        content_for_review = ""

        if not structured:
            content_for_review = "\n\n".join(
                [f.result().markdown or "" for name, f in futures.items() if not f.exception()]
            )
        else:
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
                content_for_review = final_data.model_dump_json(indent=2)
            except Exception as e:
                logger.error(f"✗ Error merging multi-agent results: {e}")
                raise

        # Step 3: Compliance Audit (Sequential - JSON Auditor)
        logger.debug(f"Starting compliance audit for: {procedure}")
        
        audit_sys_prompt = CompliancePromptBuilder.create_system_prompt()
        audit_usr_prompt = CompliancePromptBuilder.create_user_prompt(procedure, content_for_review)
        
        audit_input = ModelInput(
            system_prompt=audit_sys_prompt,
            user_prompt=audit_usr_prompt,
            response_format=ComplianceReport,
        )
        
        try:
            audit_result = self.client.generate_text(model_input=audit_input)
            compliance_report_json = audit_result.data.model_dump_json(indent=2)
            logger.debug("✓ Compliance audit completed (JSON)")
        except Exception as e:
            logger.error(f"✗ Compliance audit failed: {e}")
            compliance_report_json = "{}"
        
        # Step 4: Final Synthesis (Sequential - Markdown Closer)
        logger.debug(f"Starting final synthesis for: {procedure}")
        output_sys_prompt = OutputPromptBuilder.create_system_prompt()
        output_usr_prompt = OutputPromptBuilder.create_user_prompt(
            procedure, content_for_review, compliance_report_json
        )
        
        output_input = ModelInput(
            system_prompt=output_sys_prompt,
            user_prompt=output_usr_prompt,
            response_format=None,
        )
        
        try:
            final_markdown_res = self.client.generate_text(model_input=output_input)
            final_markdown = final_markdown_res.markdown if hasattr(final_markdown_res, 'markdown') else str(final_markdown_res)
            logger.debug("✓ Final synthesis completed (Markdown)")
            
            # Tier 2: Process/Audit metadata
            metadata = {}
            try:
                if 'audit_result' in locals() and audit_result and hasattr(audit_result, 'data'):
                    metadata["audit"] = audit_result.data
            except Exception as e:
                logger.debug(f"Could not attach audit metadata: {e}")

            return ModelOutput(
                data=final_data, 
                markdown=final_markdown,
                metadata=metadata
            )
        except Exception as e:
            logger.error(f"✗ Final synthesis failed: {e}")
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
