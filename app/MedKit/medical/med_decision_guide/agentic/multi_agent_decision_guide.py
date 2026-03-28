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

    def generate(self, symptom: str) -> MedicalDecisionGuideModel:
        """Orchestrates the multi-agent generation process."""
        logger.info(f"Starting multi-agent generation for: {symptom}")

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
        # Pass metadata for context
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

        # Step 5: Final Synthesis (Manual or LLM-assisted)
        # For simplicity, we assemble it manually here using the structured data from all agents.
        # But we could also pass everything to a Synthesis agent if we wanted.
        
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

        logger.info("✓ Multi-agent generation complete")
        return final_guide

    def save(self, result: MedicalDecisionGuideModel, output_path: Path) -> Path:
        """Saves the final guide."""
        model_output = ModelOutput(data=result)
        return save_model_response(model_output, output_path)
