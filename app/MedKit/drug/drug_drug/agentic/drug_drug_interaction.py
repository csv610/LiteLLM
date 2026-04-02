#!/usr/bin/env python3
"""
Drug-Drug Interaction Analysis module.

This module provides the core DrugDrugInteractionGenerator class for analyzing
interactions between two medicines.
"""

import logging
from pathlib import Path

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

try:
    from .drug_drug_agents import (
        ComplianceAgent,
        ManagementAgent,
        PatientEducationAgent,
        PharmacologyAgent,
        RiskAssessmentAgent,
        SearchAgent,
        TriageAgent,
    )
    from .drug_drug_interaction_models import (
        AuditLogModel,
        ComplianceInfoModel,
        DataAvailabilityInfoModel,
        DrugInteractionDetailsModel,
        DrugInteractionModel,
        ModelOutput,
        PatientFriendlySummaryModel,
        TriageResultModel,
    )
    from .drug_drug_interaction_prompts import DrugDrugInput, DrugDrugPromptBuilder
except ImportError:
    from drug_drug_agents import (
        ComplianceAgent,
        ManagementAgent,
        PatientEducationAgent,
        PharmacologyAgent,
        RiskAssessmentAgent,
        SearchAgent,
        TriageAgent,
    )
    from drug_drug_interaction_models import (
        AuditLogModel,
        ComplianceInfoModel,
        DataAvailabilityInfoModel,
        DrugInteractionDetailsModel,
        DrugInteractionModel,
        ModelOutput,
        PatientFriendlySummaryModel,
        TriageResultModel,
    )
    from drug_drug_interaction_prompts import DrugDrugInput, DrugDrugPromptBuilder

logger = logging.getLogger(__name__)


class DrugDrugOrchestrator:
    """Orchestrates multiple agents to perform drug-drug interaction analysis."""

    def __init__(self, model_config: ModelConfig):
        self.triage_agent = TriageAgent(model_config)
        self.pharmacology_agent = PharmacologyAgent(model_config)
        self.risk_agent = RiskAssessmentAgent(model_config)
        self.management_agent = ManagementAgent(model_config)
        self.patient_agent = PatientEducationAgent(model_config)
        self.search_agent = SearchAgent(model_config)
        self.compliance_agent = ComplianceAgent(model_config)

    async def orchestrate_async(self, user_input: DrugDrugInput) -> ModelOutput:
        """Run the 3-tier multi-agent orchestration flow (Specialists -> Auditor -> Closer)."""
        logger.info(f"Starting 3-tier analysis for {user_input.medicine1} + {user_input.medicine2}")

        # Tier 1: Triage
        triage_data = await self.triage_agent.run_async(
            user_input, response_format=TriageResultModel
        )

        if not triage_data.interaction_exists:
            logger.info("✓ Triage determined no clinically significant interaction.")
            return ModelOutput(markdown=f"No clinically significant interaction found between {user_input.medicine1} and {user_input.medicine2}. {triage_data.initial_reasoning}")

        # Tier 1: Parallel Specialists
        import asyncio
        logger.debug("Tier 1: Running Specialists in parallel...")
        tasks = [
            self.pharmacology_agent.run_async(user_input, DrugInteractionDetailsModel),
            self.risk_agent.run_async(user_input, DrugInteractionDetailsModel),
            self.management_agent.run_async(user_input, DrugInteractionDetailsModel),
            self.patient_agent.run_async(user_input, PatientFriendlySummaryModel),
            self.search_agent.run_async(user_input, DrugInteractionDetailsModel),
        ]
        spec_results = await asyncio.gather(*tasks)
        
        spec_data_json = "\n\n".join([
            f"SPECIALIST {i}: {res.model_dump_json(indent=2) if hasattr(res, 'model_dump_json') else str(res)}"
            for i, res in enumerate(spec_results)
        ])

        # Tier 2: Compliance Auditor (JSON Audit)
        logger.debug("Tier 2: Compliance Auditor performing safety review...")
        compliance_user_prompt = DrugDrugPromptBuilder.create_compliance_review_user_prompt(
            user_input, spec_data_json
        )
        compliance_data = await self.compliance_agent.run_async(
            user_input,
            response_format=ComplianceInfoModel,
            custom_user_prompt=compliance_user_prompt,
        )
        audit_json = compliance_data.model_dump_json(indent=2)

        # Tier 3: Final Output Synthesis (Markdown Closer)
        logger.debug("Tier 3: Output Agent synthesizing final report...")
        out_sys, out_usr = DrugDrugPromptBuilder.create_output_synthesis_prompts(
            user_input, spec_data_json, audit_json
        )
        
        final_markdown = await self.pharmacology_agent.client.generate_text_async(ModelInput(
            system_prompt=out_sys,
            user_prompt=out_usr,
            response_format=None
        ))

        logger.info("✓ Successfully generated 3-tier orchestrated drug-drug report")
        return ModelOutput(
            data=spec_results[0] if structured else None, 
            markdown=final_markdown.markdown,
            metadata={"audit": audit_json}
        )


class DrugDrugInteractionGenerator:
    """Generates drug-drug interaction analysis using multi-agent orchestration."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator with an orchestrator."""
        self.model_config = model_config
        self.orchestrator = DrugDrugOrchestrator(model_config)
        self.user_input = None
        logger.debug("Initialized DrugDrugInteractionGenerator with Orchestrator")

    def generate_text(
        self, user_input: DrugDrugInput, structured: bool = True
    ) -> ModelOutput:
        """Generate drug-drug interaction analysis through orchestration (sync wrapper)."""
        import asyncio

        try:
            # Wrap the async orchestration for the existing sync API
            result = asyncio.run(self.orchestrator.orchestrate_async(user_input))
            logger.debug("✓ Successfully analyzed drug-drug interaction via async orchestration")
            return ModelOutput(data=result)
        except Exception as e:
            logger.error(f"✗ Error in multi-agent orchestration: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the drug-drug interaction information to a file."""
        if self.user_input is None:
            raise ValueError("No configuration available. Call generate_text first.")

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.user_input.medicine1.lower().replace(' ', '_')}_{self.user_input.medicine2.lower().replace(' ', '_')}_interaction"

        return save_model_response(result, output_dir / base_filename)
