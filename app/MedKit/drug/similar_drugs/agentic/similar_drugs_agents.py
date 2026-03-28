"""
similar_drugs_agents.py - Specialized agents for finding similar medicines.
"""

import logging
from typing import Type, TypeVar

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from pydantic import BaseModel

try:
    from .similar_drugs_prompts import PromptBuilder
except ImportError:
    from similar_drugs_prompts import PromptBuilder

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class BaseAgent:
    """Base class for specialized similar medicine search agents."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config=model_config)

    def run(self, medicine_name: str, context: str, response_format: Type[T]) -> T:
        """Run the agent with the given input and expected response format."""
        system_prompt = self.get_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(medicine_name, context)

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug(f"Running {self.__class__.__name__}...")
        return self.client.generate_text(model_input=model_input)

    async def run_async(
        self,
        medicine_name: str,
        context: str,
        response_format: Type[T],
        custom_user_prompt: str | None = None,
    ) -> T:
        """Run the agent asynchronously with the given input."""
        system_prompt = self.get_system_prompt()
        user_prompt = (
            custom_user_prompt
            if custom_user_prompt
            else PromptBuilder.create_user_prompt(medicine_name, context)
        )

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug(f"Running {self.__class__.__name__} (async)...")
        import asyncio
        from functools import partial

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, partial(self.client.generate_text, model_input=model_input)
        )

    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent. Must be overridden."""
        raise NotImplementedError


class TriageAgent(BaseAgent):
    """Agent specializing in initial triage of medicines."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_triage_system_prompt()


class ResearchAgent(BaseAgent):
    """Agent specializing in medical research and comparison."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_research_system_prompt()


class ComplianceAgent(BaseAgent):
    """Agent specializing in medical compliance and safety review."""

    def get_system_prompt(self) -> str:
        return PromptBuilder.create_compliance_system_prompt()
