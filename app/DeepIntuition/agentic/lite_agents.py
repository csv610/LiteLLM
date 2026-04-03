"""
liteagents.py - Unified LiteClient-based agents for DeepIntuition.
"""

from app.DeepIntuition.shared.models import DeepIntuitionStory, ModelOutput
from app.DeepIntuition.shared.prompts import AgentPrompts, PromptBuilder
from app.DeepIntuition.shared.utils import save_result, print_result
from deep_intuition_models import IntuitionResponse
from dspy.teleprompt import BootstrapFewShot
from lite import LiteClient, ModelConfig
from lite.config import ModelInput
from pathlib import Path
from typing import Any, Optional, Dict, Type
import dspy
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MissionArchive:
    """Persistence manager for Deep Intuition Storytelling."""

    def __init__(self, topic: str, output_path: Optional[str] = None):
        self.topic = topic
        self.output_path = output_path
        self.story: Optional[dict] = None

        if self.output_path:
            Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)

    def set_final_story(self, story: Any):
        self.story = story.model_dump() if hasattr(story, "model_dump") else story

    def save(self):
        if self.story and self.output_path:
            with open(self.output_path, "w") as f:
                json.dump(self.story, f, indent=2)

    def load(self) -> Optional[Any]:
        if self.output_path and Path(self.output_path).exists():
            with open(self.output_path, "r") as f:
                self.story = json.load(f)
            return self.story
        return None


class IntuitionResponseOptimizer:
    """DSPy optimizer for IntuitionResponse."""

    def __init__(self, lm: Any):
        self.lm = lm
        dspy.settings.configure(lm=lm)

    def optimize(self):
        pass


def extract_text_from_response(response: Any) -> str:
    if hasattr(response, "text"):
        return response.text
    elif hasattr(response, "content"):
        return response.content
    return str(response)


class DeepIntuitionLiteAgent:
    def __init__(
        self, model_name: str = "gemma3:4b", base_url: str = "http://localhost:11434"
    ):
        self.client = LiteClient(model_name=model_name, base_url=base_url)
        self.prompts = AgentPrompts()

    def generate_story(self, topic: str) -> ModelOutput:
        prompt = self.prompts.build_story_prompt(topic)
        response = self.client.generate(prompt)
        data = extract_text_from_response(response)
        markdown = f"# {topic}\n\n{data}"
        return ModelOutput(
            data={"topic": topic, "story": data}, markdown=markdown, metadata={}
        )


__all__ = ["DeepIntuitionLiteAgent", "MissionArchive", "ModelOutput"]
