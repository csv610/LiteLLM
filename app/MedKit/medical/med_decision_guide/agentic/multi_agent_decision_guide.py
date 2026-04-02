#!/usr/bin/env python3
"""
Multi-agent Medical Decision Guide Analysis module.
"""

import logging
from pathlib import Path
from typing import List, Optional

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.utils import save_model_response

from .medical_decision_guide_models import (
    MedicalDecisionGuideModel,
    ModelOutput,
    SymptomMetadataModel,
    EmergencyTriageModel,
    DecisionLogicModel,
    OutcomeListModel,
    ComplianceReportModel,
    DecisionNode,
    Outcome
)
from .medical_decision_guide_multi_agent_prompts import MultiAgentPrompts

logger = logging.getLogger(__name__)


class Agent:
    """Base class for specialized medical agents."""

    def __init__(self, client: LiteClient, name: str):
        self.client = client
        self.name = name

    def run(self, system_prompt: str, user_prompt: str, response_format) -> any:
        logger.info(f"[{self.name}] Running...")
        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )
        result = self.client.generate_text(model_input=model_input)
        return result.data


class MultiAgentMedicalDecisionGuideGenerator:
    """Orchestrates multiple agents to generate a medical decision guide."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        
        # Initialize agents
        self.analyzer = Agent(self.client, "SymptomAnalyzer")
        self.triage = Agent(self.client, "EmergencyTriage")
        self.architect = Agent(self.client, "LogicArchitect")
        self.outcomes = Agent(self.client, "OutcomeSpecialist")
        self.synthesizer = Agent(self.client, "SynthesisCoordinator")
        self.compliance_officer = Agent(self.client, "ComplianceOfficer")

    def generate(self, symptom: str) -> ModelOutput:
        """Orchestrates the 3-tier multi-agent generation process."""
        logger.info(f"Starting 3-tier multi-agent generation for: {symptom}")

        # --- Tier 1: Specialist Stages (JSON) ---
        # Step 1: Analyze symptom metadata
        metadata: SymptomMetadataModel = self.analyzer.run(
            MultiAgentPrompts.get_analyzer_system_prompt(),
            MultiAgentPrompts.get_analyzer_user_prompt(symptom),
            SymptomMetadataModel
        )

        # Step 2: Identify emergency triage indicators
        triage_info: EmergencyTriageModel = self.triage.run(
            MultiAgentPrompts.get_triage_system_prompt(),
            MultiAgentPrompts.get_triage_user_prompt(symptom),
            EmergencyTriageModel
        )

        # Step 3: Design decision tree logic
        logic_context = f"Symptom: {metadata.primary_symptom}, Scope: {metadata.scope}"
        tree_logic: DecisionLogicModel = self.architect.run(
            MultiAgentPrompts.get_logic_architect_system_prompt(),
            MultiAgentPrompts.get_logic_architect_user_prompt(symptom, logic_context),
            DecisionLogicModel
        )

        # Step 4: Define outcomes for the logic
        tree_summary = f"Nodes: {[n.node_id for n in tree_logic.decision_nodes]}"
        outcomes_info: OutcomeListModel = self.outcomes.run(
            MultiAgentPrompts.get_outcome_specialist_system_prompt(),
            MultiAgentPrompts.get_outcome_specialist_user_prompt(symptom, tree_summary),
            OutcomeListModel
        )

        final_guide = MedicalDecisionGuideModel(
            guide_name=metadata.guide_name,
            primary_symptom=metadata.primary_symptom,
            secondary_symptoms=metadata.secondary_symptoms,
            age_groups_covered=metadata.age_groups_covered,
            scope=metadata.scope,
            start_node_id=tree_logic.start_node_id,
            decision_nodes=tree_logic.decision_nodes,
            outcomes=outcomes_info.outcomes,
            warning_signs=triage_info.warning_signs,
            emergency_indicators=triage_info.emergency_indicators
        )
        specialist_json = final_guide.model_dump_json(indent=2)

        # --- Tier 2: Compliance Audit Stage (JSON Audit) ---
        audit_report: ComplianceReportModel = self.compliance_officer.run(
            MultiAgentPrompts.get_compliance_system_prompt(),
            MultiAgentPrompts.get_compliance_user_prompt(specialist_json),
            ComplianceReportModel
        )
        compliance_json = audit_report.model_dump_json(indent=2)

        # --- Tier 3: Final Output Synthesis (Markdown Closer) ---
        logger.info("Agent: Output synthesis starting...")
        out_sys, out_usr = MultiAgentPrompts.get_output_synthesis_prompts(
            symptom, specialist_json, compliance_json
        )
        
        output_input = ModelInput(
            system_prompt=out_sys,
            user_prompt=out_usr,
            response_format=None,
        )
        final_markdown = self.client.generate_text(model_input=output_input).markdown

        logger.info("✓ 3-tier multi-agent generation complete")
        return ModelOutput(
            data=final_guide, 
            markdown=final_markdown,
            metadata={"audit": compliance_json}
        )

    def save(self, result: ModelOutput, output_path: Path) -> Path:
        """Saves the final guide."""
        return save_model_response(result, output_path)
