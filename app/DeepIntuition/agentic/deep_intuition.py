"""
deep_intuition.py - The 5-Agent Deep Intuition Storytelling Engine (Refactored)

Orchestrates multiple specialized agents with a DRY, declarative approach.
"""

import logging
from typing import Optional, Dict, Any, Type

from lite import LiteClient, ModelConfig
from lite.config import ModelInput
from pydantic import BaseModel

from .deep_intuition_models import (
    DeepIntuitionStory, 
    HistoricalResearch, 
    IntuitionInsight, 
    CounterfactualAnalysis, 
    StruggleNarrative
)
from .deep_intuition_prompts import AgentPrompts
from .deep_intuition_archive import MissionArchive

logger = logging.getLogger(__name__)


class DeepIntuition:
    """The 5-Agent Deep Intuition Storytelling Engine."""

    def __init__(self, model_config: ModelConfig):
        """Initialize with a high-fidelity client."""
        self.client = LiteClient(model_config=model_config)

    def _execute_agent(self, 
                       name: str, 
                       prompt: str, 
                       response_model: Type[BaseModel], 
                       emoji: str = "🤖") -> BaseModel:
        """Helper to run a single agent and return its structured output."""
        print(f"{emoji} {name} working...")
        model_input = ModelInput(user_prompt=prompt, response_format=response_model)
        
        try:
            return self.client.generate_text(model_input)
        except Exception as e:
            logger.error(f"Agent '{name}' failed: {e}")
            raise RuntimeError(f"Mission failed during {name} phase: {e}") from e

    def generate_story(self, topic: str, output_path: Optional[str] = None) -> DeepIntuitionStory:
        """Uncover the human story through a refactored agentic pipeline."""
        archive = MissionArchive(topic, output_path)
        print(f"\n✨ Initiating Deep Intuition mission for '{topic}'...")

        # 1. Historical Researcher
        historical = self._execute_agent(
            "Historical Researcher",
            AgentPrompts.build(AgentPrompts.HISTORICAL_RESEARCHER, topic=topic),
            HistoricalResearch,
            emoji="🔍"
        )

        # 2. Intuition Specialist
        intuition = self._execute_agent(
            "Intuition Specialist",
            AgentPrompts.build(AgentPrompts.INTUITION_SPECIALIST, topic=topic),
            IntuitionInsight,
            emoji="💡"
        )

        # 3. Counterfactual Analyst
        counterfactual = self._execute_agent(
            "Counterfactual Analyst",
            AgentPrompts.build(AgentPrompts.COUNTERFACTUAL_ANALYST, topic=topic),
            CounterfactualAnalysis,
            emoji="🌍"
        )

        # 4. Human Struggle Narrator
        struggle = self._execute_agent(
            "Human Struggle Narrator",
            AgentPrompts.build(
                AgentPrompts.HUMAN_STRUGGLE_NARRATOR, 
                topic=topic, 
                historical_data=historical.archive_of_failures_details
            ),
            StruggleNarrative,
            emoji="🎭"
        )

        # 5. Lead Editor (Final Synthesis)
        story = self._execute_agent(
            "Lead Editor",
            AgentPrompts.build(
                AgentPrompts.LEAD_EDITOR_WEAVER,
                topic=topic,
                historical=historical.model_dump(),
                intuition=intuition.model_dump(),
                counterfactual=counterfactual.model_dump(),
                struggle=struggle.model_dump()
            ),
            DeepIntuitionStory,
            emoji="✍️"
        )

        archive.set_final_story(story)
        return story
