"""
deep_intuition.py - The Deep Intuition Storytelling Engine

Orchestrates the generation of the human story behind fundamental ideas.
"""

import logging
from typing import Optional

from lite import LiteClient, ModelConfig
from lite.config import ModelInput

from app.DeepIntuition.shared.models import DeepIntuitionStory
from app.DeepIntuition.shared.prompts import PromptBuilder
from .deep_intuition_archive import MissionArchive

logger = logging.getLogger(__name__)


class DeepIntuition:
    """The Deep Intuition Storytelling Engine."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the engine with a single, high-fidelity client."""
        self.client = LiteClient(model_config=model_config)

    def generate_story(self, topic: str, output_path: Optional[str] = None) -> DeepIntuitionStory:
        """Uncover the human story behind a fundamental discovery."""
        archive = MissionArchive(topic, output_path)

        print(f"\n✨ Uncovering the human triumph behind '{topic}'...")
        
        story_input = ModelInput(
            user_prompt=PromptBuilder.get_storytelling_prompt(topic),
            response_format=DeepIntuitionStory
        )
        
        try:
            story: DeepIntuitionStory = self.client.generate_text(story_input)
            archive.set_final_story(story)
            return story
        except Exception as e:
            logger.error(f"Failed to uncover the story for '{topic}': {e}")
            raise
