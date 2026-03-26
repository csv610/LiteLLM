"""
paradox_element.py - ParadoxExplainer class for paradox explanations

Contains the ParadoxExplainer class for fetching and managing
paradox explanations with high academic rigor.
"""

import json
import logging
from typing import Optional, List

from lite import LiteClient, ModelConfig
from lite.config import ModelInput

from paradox_models import (
    Paradox, ParadoxResponse, AudienceLevel, 
    ResearchData, LogicData, DomainData, ParadoxExplanation, ParadoxResolution
)


class ParadoxExplainer:
    """Class for fetching and managing paradox explanations using a 4-agent system."""
    
    def __init__(self, model_config: ModelConfig):
        """Initialize the explainer with a ModelConfig.
        
        Args:
            model_config: Configured ModelConfig for API calls
        """
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.logger = logging.getLogger(__name__)

    def _researcher_agent(self, paradox_name: str, level: AudienceLevel) -> Optional[ResearchData]:
        """Researcher Agent: Historical context and status."""
        prompt = (
            f"As a Historical Researcher, investigate the paradox '{paradox_name}' for a {level.value} audience.\n"
            f"Focus on:\n"
            f"1. HISTORICAL ACCURACY: Reference key philosophers/scientists and their schools of thought.\n"
            f"2. STATUS: Determine if it's Solved, Unsolved, Under Debate, or Partially Solved.\n"
            f"3. WHO SOLVED IT: Identify the primary figures (e.g., Aristotle, Russell, etc.).\n"
            f"Provide historical motivation and context."
        )
        model_input = ModelInput(user_prompt=prompt, response_format=ResearchData)
        return self.client.generate_text(model_input=model_input)

    def _logical_analyst_agent(self, paradox_name: str, level: AudienceLevel) -> Optional[LogicData]:
        """Logical Analyst Agent: Root cause and core contradiction."""
        prompt = (
            f"As a Logical Analyst, deconstruct the paradox '{paradox_name}' for a {level.value} audience.\n"
            f"Focus on:\n"
            f"1. ROOT CAUSE: Identify the exact 'hidden assumptions' or category errors in the underlying theories.\n"
            f"2. THE CONTRADICTION: Explain the core counter-intuitive nature with airtight logic.\n"
            f"3. IMPACT ON THOUGHT: How this paradox forced the evolution of human logic or scientific knowledge."
        )
        model_input = ModelInput(user_prompt=prompt, response_format=LogicData)
        return self.client.generate_text(model_input=model_input)

    def _domain_specialist_agent(self, paradox_name: str, level: AudienceLevel) -> Optional[DomainData]:
        """Domain Specialist Agent: Scientific/Mathematical details and modern relevance."""
        prompt = (
            f"As a Domain Specialist (Math/Science), analyze the paradox '{paradox_name}' for a {level.value} audience.\n"
            f"Focus on:\n"
            f"1. KEY CONCEPTS: List fundamental concepts with precise definitions.\n"
            f"2. MODERN RELEVANCE: Connection to modern physics, logic, or computer science.\n"
            f"3. RESOLUTION BREAKTHROUGH: The exact method/realization (e.g., Real Analysis, Set Theory).\n"
            f"4. RESOLUTION DETAILS: Provide both logical and mathematical/scientific details."
        )
        model_input = ModelInput(user_prompt=prompt, response_format=DomainData)
        return self.client.generate_text(model_input=model_input)

    def _orchestrator_agent(
        self, 
        paradox_name: str, 
        level: AudienceLevel, 
        research: ResearchData, 
        logic: LogicData, 
        domain: DomainData
    ) -> Optional[ParadoxExplanation]:
        """Orchestrator Agent: Final assembly and audience-level adaptation."""
        prompt = (
            f"As an Orchestrator and Senior Editor, synthesize the findings for the paradox '{paradox_name}' for a {level.value} audience.\n"
            f"YOU MUST ADAPT THE FOLLOWING RAW DATA TO THE '{level.value.upper()}' AUDIENCE LEVEL:\n\n"
            f"RESEARCH DATA:\n{research.json()}\n\n"
            f"LOGIC DATA:\n{logic.json()}\n\n"
            f"DOMAIN DATA:\n{domain.json()}\n\n"
            f"TASKS:\n"
            f"1. Write a clear, engaging INTRODUCTION.\n"
            f"2. Summarize the CURRENT DEBATES or persistent open questions.\n"
            f"3. Refine and polish all other fields (historical context, root cause, contradiction, impact, modern relevance, key concepts, resolutions) "
            f"to ensure the tone is scholarly, the logic is airtight, and the depth matches the {level.value} level."
        )
        model_input = ModelInput(user_prompt=prompt, response_format=ParadoxExplanation)
        return self.client.generate_text(model_input=model_input)
    
    def fetch_paradox_explanation(self, paradox_name: str, audience_levels: List[AudienceLevel] = None) -> Optional[Paradox]:
        """Fetch explanations for a paradox across specified audience levels using 4 agents.
        
        Args:
            paradox_name: Name of the paradox
            audience_levels: List of AudienceLevel enums to fetch for. Defaults to all levels.
            
        Returns:
            Paradox object with detailed explanations, or None if failed
        """
        if audience_levels is None:
            audience_levels = [AudienceLevel.UNDERGRAD]
            
        explanations = {}
        
        for level in audience_levels:
            self.logger.info(f"Processing '{paradox_name}' for {level.value} level...")
            
            # 1. Researcher Agent
            research = self._researcher_agent(paradox_name, level)
            if not research: continue
            
            # 2. Logical Analyst Agent
            logic = self._logical_analyst_agent(paradox_name, level)
            if not logic: continue
            
            # 3. Domain Specialist Agent
            domain = self._domain_specialist_agent(paradox_name, level)
            if not domain: continue
            
            # 4. Orchestrator Agent
            final_explanation = self._orchestrator_agent(paradox_name, level, research, logic, domain)
            if final_explanation:
                explanations[level] = final_explanation

        if explanations:
            return Paradox(paradox_name=paradox_name, explanations=explanations)
        return None
