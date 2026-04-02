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
    StruggleNarrative,
    ModelOutput
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
                       response_model: Optional[Type[BaseModel]], 
                       emoji: str = "🤖") -> Any:
        """Helper to run a single agent and return its output (structured or string)."""
        print(f"{emoji} {name} working...")
        model_input = ModelInput(user_prompt=prompt, response_format=response_model)
        
        try:
            res = self.client.generate_text(model_input)
            if response_model:
                return res.data
            return res.markdown
        except Exception as e:
            logger.error(f"Agent '{name}' failed: {e}")
            raise RuntimeError(f"Mission failed during {name} phase: {e}") from e

    def generate_story(self, topic: str, output_path: Optional[str] = None) -> ModelOutput:
        """Uncover the human story through a 3-tier artifact-based pipeline."""
        archive = MissionArchive(topic, output_path)
        print(f"\n✨ Initiating Deep Intuition mission for '{topic}'...")

        # --- Tier 1: Specialists (JSON) ---
        # 1. Historical Researcher
        historical: HistoricalResearch = self._execute_agent(
            "Historical Researcher",
            AgentPrompts.build(AgentPrompts.HISTORICAL_RESEARCHER, topic=topic),
            HistoricalResearch,
            emoji="🔍"
        )

        # 2. Intuition Specialist
        intuition: IntuitionInsight = self._execute_agent(
            "Intuition Specialist",
            AgentPrompts.build(AgentPrompts.INTUITION_SPECIALIST, topic=topic),
            IntuitionInsight,
            emoji="💡"
        )

        # 3. Counterfactual Analyst
        counterfactual: CounterfactualAnalysis = self._execute_agent(
            "Counterfactual Analyst",
            AgentPrompts.build(AgentPrompts.COUNTERFACTUAL_ANALYST, topic=topic),
            CounterfactualAnalysis,
            emoji="🌍"
        )

        # 4. Human Struggle Narrator
        struggle: StruggleNarrative = self._execute_agent(
            "Human Struggle Narrator",
            AgentPrompts.build(
                AgentPrompts.HUMAN_STRUGGLE_NARRATOR, 
                topic=topic, 
                historical_data=historical.archive_of_failures_details
            ),
            StruggleNarrative,
            emoji="🎭"
        )

        # --- Tier 3: Lead Editor (Final Synthesis - Markdown Closer) ---
        story_markdown: str = self._execute_agent(
            "Lead Editor",
            AgentPrompts.build(
                AgentPrompts.LEAD_EDITOR_WEAVER,
                topic=topic,
                historical=historical.model_dump(),
                intuition=intuition.model_dump(),
                counterfactual=counterfactual.model_dump(),
                struggle=struggle.model_dump()
            ) + "\n\nFINAL INSTRUCTION: Weave these insights into a powerful Markdown story. Use headers, quotes, and emphasized key insights.",
            None,
            emoji="✍️"
        )

        # Create structured data for the .data member
        final_data = DeepIntuitionStory(
            topic=topic,
            the_human_struggle=struggle.the_human_struggle,
            the_aha_moment=intuition.the_aha_moment,
            human_triumph_rationale=struggle.human_triumph_rationale,
            counterfactual_world=counterfactual.counterfactual_world,
            modern_resonance=counterfactual.modern_resonance,
            key_historical_anchors=historical.key_historical_anchors
        )

        archive.set_final_story(story_markdown)
        
        return ModelOutput(
            data=final_data,
            markdown=story_markdown,
            metadata={
                "historical": historical.model_dump(),
                "intuition": intuition.model_dump(),
                "counterfactual": counterfactual.model_dump(),
                "struggle": struggle.model_dump()
            }
        )
