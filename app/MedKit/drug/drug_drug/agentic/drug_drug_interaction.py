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

    async def orchestrate_async(self, user_input: DrugDrugInput) -> DrugInteractionModel:
        """Run the multi-agent orchestration flow asynchronously with triage and audit."""
        logger.info(
            f"Starting orchestrated analysis for {user_input.medicine1} + {user_input.medicine2}"
        )

        # Step 1: Triage
        triage_data = await self.triage_agent.run_async(
            user_input, response_format=TriageResultModel
        )

        if not triage_data.interaction_exists:
            logger.info("✓ Triage determined no clinically significant interaction.")
            return DrugInteractionModel(
                technical_summary=triage_data.initial_reasoning,
                data_availability=DataAvailabilityInfoModel(
                    data_available=False, reason=triage_data.initial_reasoning
                ),
            )

        # Step 2: Parallel Analysis
        import asyncio

        logger.debug("Running Core Analysis agents in parallel...")
        tasks = [
            self.pharmacology_agent.run_async(user_input, DrugInteractionDetailsModel),
            self.risk_agent.run_async(user_input, DrugInteractionDetailsModel),
            self.management_agent.run_async(user_input, DrugInteractionDetailsModel),
            self.patient_agent.run_async(user_input, PatientFriendlySummaryModel),
            self.search_agent.run_async(user_input, DrugInteractionDetailsModel),
        ]

        results = await asyncio.gather(*tasks)
        (
            pharmacology_data,
            risk_data,
            management_data,
            patient_data,
            search_data,
        ) = results

        # Step 3: Contextual Compliance Review
        # We build a draft report string for the compliance agent to review
        draft_report = (
            f"SEVERITY: {risk_data.severity_level}\n"
            f"MECHANISM: {pharmacology_data.mechanism_of_interaction}\n"
            f"CLINICAL EFFECTS: {pharmacology_data.clinical_effects}\n"
            f"MANAGEMENT: {management_data.management_recommendations}\n"
            f"PATIENT INFO: {patient_data.simple_explanation}\n"
        )

        compliance_user_prompt = DrugDrugPromptBuilder.create_compliance_review_user_prompt(
            user_input, draft_report
        )

        compliance_data = await self.compliance_agent.run_async(
            user_input,
            response_format=ComplianceInfoModel,
            custom_user_prompt=compliance_user_prompt,
        )

        # Step 4: Consolidation & Audit Log
        interaction_details = DrugInteractionDetailsModel(
            drug1_name=user_input.medicine1,
            drug2_name=user_input.medicine2,
            severity_level=risk_data.severity_level,
            mechanism_of_interaction=pharmacology_data.mechanism_of_interaction,
            clinical_effects=pharmacology_data.clinical_effects,
            management_recommendations=management_data.management_recommendations,
            alternative_medicines=management_data.alternative_medicines,
            confidence_level=risk_data.confidence_level,
            data_source_type=search_data.data_source_type,
            references=search_data.references,
            technical_summary=risk_data.technical_summary,
        )

        audit_log = AuditLogModel(
            pharmacology_raw=pharmacology_data,
            risk_raw=risk_data,
            management_raw=management_data,
            patient_raw=patient_data,
            search_raw=search_data,
            compliance_raw=compliance_data,
        )

        return DrugInteractionModel(
            interaction_details=interaction_details,
            technical_summary=risk_data.technical_summary,
            patient_friendly_summary=patient_data,
            data_availability=DataAvailabilityInfoModel(data_available=True),
            compliance_info=compliance_data,
            audit_log=audit_log,
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
