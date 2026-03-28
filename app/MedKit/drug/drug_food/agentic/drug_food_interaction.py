#!/usr/bin/env python3
"""
Drug-Food Interaction Analysis module.

This module provides the core DrugFoodInteraction class for analyzing
how food and beverages interact with medicines using a multi-agent orchestrated approach.
"""

import asyncio
import logging
from pathlib import Path

from lite.config import ModelConfig
from lite.utils import save_model_response

try:
    from .drug_food_agents import (
        ComplianceAgent,
        ManagementAgent,
        PatientEducationAgent,
        PharmacologyAgent,
        RiskAssessmentAgent,
        SearchAgent,
        TriageAgent,
    )
    from .drug_food_interaction_models import (
        AuditLogModel,
        ComplianceInfoModel,
        DataAvailabilityInfoModel,
        DrugFoodInteractionDetailsModel,
        DrugFoodInteractionModel,
        ModelOutput,
        PatientFriendlySummaryModel,
        TriageResultModel,
    )
    from .drug_food_interaction_prompts import DrugFoodInput, PromptBuilder
except ImportError:
    from drug_food_agents import (
        ComplianceAgent,
        ManagementAgent,
        PatientEducationAgent,
        PharmacologyAgent,
        RiskAssessmentAgent,
        SearchAgent,
        TriageAgent,
    )
    from drug_food_interaction_models import (
        AuditLogModel,
        ComplianceInfoModel,
        DataAvailabilityInfoModel,
        DrugFoodInteractionDetailsModel,
        DrugFoodInteractionModel,
        ModelOutput,
        PatientFriendlySummaryModel,
        TriageResultModel,
    )
    from drug_food_interaction_prompts import DrugFoodInput, PromptBuilder

logger = logging.getLogger(__name__)


class DrugFoodOrchestrator:
    """Orchestrates multiple agents to perform drug-food interaction analysis."""

    def __init__(self, model_config: ModelConfig):
        self.triage_agent = TriageAgent(model_config)
        self.pharmacology_agent = PharmacologyAgent(model_config)
        self.risk_agent = RiskAssessmentAgent(model_config)
        self.management_agent = ManagementAgent(model_config)
        self.patient_agent = PatientEducationAgent(model_config)
        self.search_agent = SearchAgent(model_config)
        self.compliance_agent = ComplianceAgent(model_config)

    async def orchestrate_async(self, user_input: DrugFoodInput) -> DrugFoodInteractionModel:
        """Run the multi-agent orchestration flow asynchronously with triage and audit."""
        logger.info(f"Starting orchestrated food interaction analysis for {user_input.medicine_name}")

        # Step 1: Triage
        triage_data = await self.triage_agent.run_async(
            user_input, response_format=TriageResultModel
        )

        if not triage_data.interaction_exists:
            logger.info("✓ Triage determined no clinically significant food interactions.")
            return DrugFoodInteractionModel(
                technical_summary=triage_data.initial_reasoning,
                data_availability=DataAvailabilityInfoModel(
                    data_available=False, reason=triage_data.initial_reasoning
                ),
            )

        # Step 2: Parallel Analysis
        logger.debug("Running Core Analysis agents in parallel...")
        tasks = [
            self.pharmacology_agent.run_async(user_input, DrugFoodInteractionDetailsModel),
            self.risk_agent.run_async(user_input, DrugFoodInteractionDetailsModel),
            self.management_agent.run_async(user_input, DrugFoodInteractionDetailsModel),
            self.patient_agent.run_async(user_input, PatientFriendlySummaryModel),
            self.search_agent.run_async(user_input, DrugFoodInteractionDetailsModel),
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
        # Build a draft report string for the compliance agent to review
        draft_report = (
            f"OVERALL SEVERITY: {risk_data.overall_severity}\n"
            f"MECHANISM: {pharmacology_data.mechanism_of_interaction}\n"
            f"CLINICAL EFFECTS: {pharmacology_data.clinical_effects}\n"
            f"MANAGEMENT: {management_data.management_recommendations}\n"
            f"PATIENT INFO: {patient_data.simple_explanation}\n"
            f"FOODS TO AVOID: {management_data.foods_to_avoid}\n"
        )

        compliance_user_prompt = PromptBuilder.create_compliance_review_user_prompt(
            user_input, draft_report
        )

        compliance_data = await self.compliance_agent.run_async(
            user_input,
            response_format=ComplianceInfoModel,
            custom_user_prompt=compliance_user_prompt,
        )

        # Step 4: Consolidation & Audit Log
        interaction_details = DrugFoodInteractionDetailsModel(
            medicine_name=user_input.medicine_name,
            overall_severity=risk_data.overall_severity,
            mechanism_of_interaction=pharmacology_data.mechanism_of_interaction,
            clinical_effects=pharmacology_data.clinical_effects,
            food_category_interactions=risk_data.food_category_interactions,
            management_recommendations=management_data.management_recommendations,
            foods_to_avoid=management_data.foods_to_avoid,
            foods_safe_to_consume=management_data.foods_safe_to_consume,
            confidence_level=risk_data.confidence_level,
            data_source_type=search_data.data_source_type,
            references=search_data.references,
        )

        audit_log = AuditLogModel(
            pharmacology_raw=pharmacology_data,
            risk_raw=risk_data,
            management_raw=management_data,
            patient_raw=patient_data,
            search_raw=search_data,
            compliance_raw=compliance_data,
        )

        return DrugFoodInteractionModel(
            interaction_details=interaction_details,
            technical_summary=f"Analysis for {user_input.medicine_name}: {risk_data.overall_severity} severity.",
            patient_friendly_summary=patient_data,
            data_availability=DataAvailabilityInfoModel(data_available=True),
            compliance_info=compliance_data,
            audit_log=audit_log,
        )


class DrugFoodInteraction:
    """Analyzes drug-food interactions using multi-agent orchestration."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the drug-food interaction analyzer."""
        self.model_config = model_config
        self.orchestrator = DrugFoodOrchestrator(model_config)
        self.user_input = None  # Store the configuration for later use in save
        logger.debug("Initialized DrugFoodInteraction with Orchestrator")

    def generate_text(
        self, user_input: DrugFoodInput, structured: bool = True
    ) -> ModelOutput:
        """Analyzes how food and beverages interact with a medicine (sync wrapper)."""
        self.user_input = user_input
        logger.debug(f"Starting drug-food interaction analysis for {user_input.medicine_name}")

        try:
            # Wrap the async orchestration for the existing sync API
            result = asyncio.run(self.orchestrator.orchestrate_async(user_input))
            logger.debug("✓ Successfully analyzed food interactions via orchestration")
            return ModelOutput(data=result)
        except Exception as e:
            logger.error(f"✗ Error in multi-agent orchestration: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the drug-food interaction information to a file."""
        if self.user_input is None:
            raise ValueError("No configuration available. Call generate_text first.")

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.user_input.medicine_name.lower().replace(' ', '_')}_food_interaction"

        return save_model_response(result, output_dir / base_filename)
