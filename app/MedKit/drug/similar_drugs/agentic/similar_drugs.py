"""Similar Drugs Finder.

This module contains the core logic for finding similar medicines based on
active ingredients, therapeutic classes, and mechanisms of action.
"""

import logging
from pathlib import Path
from typing import Optional, Union

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.logging_config import configure_logging

try:
    from .similar_drugs_agents import ComplianceAgent, ResearchAgent, TriageAgent
    from .similar_drugs_models import (
        AuditLogModel,
        ComplianceInfoModel,
        SimilarDrugsConfig,
        SimilarMedicinesModel,
        SimilarMedicinesResult,
        TriageResultModel,
    )
    from .similar_drugs_prompts import PromptBuilder
except ImportError:
    from similar_drugs_agents import ComplianceAgent, ResearchAgent, TriageAgent
    from similar_drugs_models import (
        AuditLogModel,
        ComplianceInfoModel,
        SimilarDrugsConfig,
        SimilarMedicinesModel,
        SimilarMedicinesResult,
        TriageResultModel,
    )
    from similar_drugs_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class SimilarDrugsOrchestrator:
    """Orchestrates multiple agents to find similar medicines."""

    def __init__(self, model_config: ModelConfig):
        self.triage_agent = TriageAgent(model_config)
        self.research_agent = ResearchAgent(model_config)
        self.compliance_agent = ComplianceAgent(model_config)

    async def orchestrate_async(
        self,
        medicine_name: str,
        context: str,
    ) -> SimilarMedicinesModel:
        """Run the multi-agent orchestration flow."""
        logger.info(f"Starting orchestrated search for medicines similar to {medicine_name}")

        # Step 1: Triage
        triage_data = await self.triage_agent.run_async(
            medicine_name, context, response_format=TriageResultModel
        )

        if not triage_data.is_real_medicine:
            logger.warning(f"Triage determined '{medicine_name}' may not be a valid medicine.")

        # Step 2: Detailed Research
        research_data = await self.research_agent.run_async(
            medicine_name, context, response_format=SimilarMedicinesResult
        )

        # Step 3: Compliance Review
        draft_report = research_data.model_dump_json(indent=2)
        compliance_user_prompt = PromptBuilder.create_compliance_review_user_prompt(
            medicine_name, draft_report
        )

        compliance_data = await self.compliance_agent.run_async(
            medicine_name,
            context,
            response_format=ComplianceInfoModel,
            custom_user_prompt=compliance_user_prompt,
        )

        # Step 4: Consolidation
        audit_log = AuditLogModel(
            triage_raw=triage_data,
            research_raw=research_data,
            compliance_raw=compliance_data,
        )

        return SimilarMedicinesModel(
            main_result=research_data,
            compliance_info=compliance_data,
            audit_log=audit_log,
        )


class SimilarDrugs:
    """Finds similar drugs based on provided configuration."""

    def __init__(self, config: "SimilarDrugsConfig", model_config: ModelConfig):
        self.config = config
        self.orchestrator = SimilarDrugsOrchestrator(model_config)

        # Apply verbosity level using centralized logging configuration
        configure_logging(
            log_file=str(Path(__file__).parent / "logs" / "similar_drugs.log"),
            verbosity=self.config.verbosity,
            enable_console=True,
        )

    def find(
        self,
        medicine_name: str,
        include_generics: bool = True,
        patient_age: Optional[int] = None,
        patient_conditions: Optional[str] = None,
        structured: bool = False,
    ) -> Union[SimilarMedicinesResult, SimilarMedicinesModel, str]:
        """
        Finds top 10-15 medicines similar to a given medicine.
        """
        # Validate inputs
        if not medicine_name or not medicine_name.strip():
            raise ValueError("Medicine name cannot be empty")
        if patient_age is not None and (patient_age < 0 or patient_age > 150):
            raise ValueError("Age must be between 0 and 150 years")

        context_parts = []
        if include_generics:
            context_parts.append("Include generic formulations")
        if patient_age is not None:
            context_parts.append(f"Patient age: {patient_age} years")
        if patient_conditions:
            context_parts.append(f"Patient conditions: {patient_conditions}")

        context = ". ".join(context_parts) + "." if context_parts else ""

        import asyncio

        try:
            result = asyncio.run(self.orchestrator.orchestrate_async(medicine_name, context))
            if structured:
                return result
            return result.main_result.model_dump_json(indent=2)
        except Exception as e:
            logger.error(f"Error in multi-agent orchestration: {e}")
            raise
