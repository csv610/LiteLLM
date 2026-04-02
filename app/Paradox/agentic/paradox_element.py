"""
paradox_element.py - ParadoxExplainer class for paradox explanations

Contains the ParadoxExplainer class for fetching and managing
paradox explanations with a 3-tier artifact-based approach.
"""

import json
import logging
from typing import Optional, List, Dict, Any

from lite import LiteClient, ModelConfig
from lite.config import ModelInput

from app.Paradox.shared.models import (
    Paradox, ParadoxResponse, AudienceLevel, 
    ResearchData, LogicData, DomainData, ParadoxExplanation, 
    ParadoxResolution, ModelOutput
)


class ParadoxExplainer:
    """Class for fetching and managing paradox explanations using a 3-tier multi-agent system."""
    
    def __init__(self, model_config: ModelConfig):
        """Initialize the explainer with a ModelConfig."""
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)
        self.logger = logging.getLogger(__name__)

    def _researcher_agent(self, paradox_name: str, level: AudienceLevel) -> Optional[ResearchData]:
        """Researcher Agent (Tier 1 Specialist)."""
        prompt = f"As a Historical Researcher, investigate the paradox '{paradox_name}' for a {level.value} audience."
        model_input = ModelInput(user_prompt=prompt, response_format=ResearchData)
        res = self.client.generate_text(model_input=model_input)
        return res.data

    def _logical_analyst_agent(self, paradox_name: str, level: AudienceLevel) -> Optional[LogicData]:
        """Logical Analyst Agent (Tier 1 Specialist)."""
        prompt = f"As a Logical Analyst, deconstruct the paradox '{paradox_name}' for a {level.value} audience."
        model_input = ModelInput(user_prompt=prompt, response_format=LogicData)
        res = self.client.generate_text(model_input=model_input)
        return res.data

    def _domain_specialist_agent(self, paradox_name: str, level: AudienceLevel) -> Optional[DomainData]:
        """Domain Specialist Agent (Tier 1 Specialist)."""
        prompt = f"As a Domain Specialist, analyze the scientific/mathematical side of '{paradox_name}' for a {level.value} audience."
        model_input = ModelInput(user_prompt=prompt, response_format=DomainData)
        res = self.client.generate_text(model_input=model_input)
        return res.data

    def _orchestrator_agent(
        self, 
        paradox_name: str, 
        level: AudienceLevel, 
        research: ResearchData, 
        logic: LogicData, 
        domain: DomainData
    ) -> Optional[ParadoxExplanation]:
        """Orchestrator Agent (Tier 2 Auditor/Refiner)."""
        prompt = (
            f"As an Orchestrator, synthesize the findings for the paradox '{paradox_name}' for a {level.value} audience.\n\n"
            f"RESEARCH: {research.model_dump_json()}\n"
            f"LOGIC: {logic.model_dump_json()}\n"
            f"DOMAIN: {domain.model_dump_json()}"
        )
        model_input = ModelInput(user_prompt=prompt, response_format=ParadoxExplanation)
        res = self.client.generate_text(model_input=model_input)
        return res.data
    
    def generate_text(self, paradox_name: str, audience_levels: List[AudienceLevel] = None) -> Optional[ModelOutput]:
        """Fetch explanations and return a standardized ModelOutput artifact."""
        if audience_levels is None:
            audience_levels = [AudienceLevel.UNDERGRAD]
            
        explanations = {}
        all_metadata = []
        
        for level in audience_levels:
            self.logger.info(f"Tier 1/2: Processing '{paradox_name}' for {level.value} level...")
            
            research = self._researcher_agent(paradox_name, level)
            logic = self._logical_analyst_agent(paradox_name, level)
            domain = self._domain_specialist_agent(paradox_name, level)
            
            if research and logic and domain:
                final_explanation = self._orchestrator_agent(paradox_name, level, research, logic, domain)
                if final_explanation:
                    explanations[level] = final_explanation
                    all_metadata.append({
                        "level": level.value,
                        "research": research.model_dump(),
                        "logic": logic.model_dump(),
                        "domain": domain.model_dump()
                    })

        if not explanations:
            return None

        # Assemble Final Data Object
        paradox_data = Paradox(paradox_name=paradox_name, explanations=explanations)

        # Tier 3: Output Synthesis (Markdown Closer)
        logger.info("Tier 3: Output synthesis starting...")
        synth_prompt = (
            f"Synthesize a final scholarly Markdown report for the paradox: '{paradox_name}'.\n\n"
            f"EXPLANATIONS BY LEVEL:\n"
            + "\n\n".join([f"### For {l.value}:\n{e.introduction}\n\n**Contradiction:** {e.the_contradiction}" for l, e in explanations.items()])
        )
        
        final_markdown_res = self.client.generate_text(ModelInput(
            system_prompt="You are a Lead Philosophical Editor. Synthesize raw paradox deconstructions into a beautiful Markdown report with historical context and logical resolution sections.",
            user_prompt=synth_prompt,
            response_format=None
        ))
        final_markdown = final_markdown_res.markdown

        return ModelOutput(
            data=paradox_data,
            markdown=final_markdown,
            metadata={"audience_missions": all_metadata}
        )
