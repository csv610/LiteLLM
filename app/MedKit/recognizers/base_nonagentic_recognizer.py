"""
Base Nonagentic Recognizer Module.

This module provides an abstract base class for all nonagentic recognizers.
"""

import logging
from abc import abstractmethod
from typing import Any, Optional, Type

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.websearch import WebSearchTools
from pydantic import BaseModel

from lite.config import ModelConfig

from .base_recognizer import BaseRecognizer
from .models import ModelOutput

logger = logging.getLogger(__name__)


class BaseAgenticRecognizer(BaseRecognizer):
    """Abstract base class for agentic medical entity recognizers."""

    def __init__(
        self,
        model_config: ModelConfig,
        enable_memory: bool = True,
        max_retries: int = 3,
        custom_tools: Optional[list] = None,
    ):
        super().__init__(model_config)
        self.max_retries = max_retries
        self._model = self._parse_model(model_config.model)
        self._agent = self._create_agent(
            enable_memory=enable_memory,
            custom_tools=custom_tools or [],
        )

    def _parse_model(self, model_str: str) -> Ollama:
        if "/" in model_str:
            provider, model_name = model_str.split("/", 1)
            if provider == "ollama":
                return Ollama(id=model_name)
        return Ollama(id=model_str)

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass

    @abstractmethod
    def get_input_class(self) -> Type[BaseModel]:
        pass

    @abstractmethod
    def get_response_model(self) -> Optional[Type[BaseModel]]:
        pass

    @abstractmethod
    def _get_prompt_builder(self) -> Type[Any]:
        pass

    @abstractmethod
    def _get_name_field(self) -> str:
        pass

    def _create_agent(
        self,
        enable_memory: bool = True,
        custom_tools: Optional[list] = None,
    ) -> Agent:
        tools: list = [WebSearchTools()]
        if custom_tools:
            tools.extend(custom_tools)
        return Agent(
            model=self._model,
            markdown=True,
            debug_mode=False,
            system_message=self.get_system_prompt(),
            tools=tools,
            add_history_to_context=enable_memory,
            num_history_messages=10,
            retries=self.max_retries,
        )

    def _build_prompt(self, name: str) -> str:
        InputClass = self.get_input_class()
        name_field = self._get_name_field()
        input_obj = InputClass(**{name_field: name})
        return self._get_prompt_builder().create_user_prompt(input_obj)

    def identify(self, name: str, structured: bool = False) -> ModelOutput:
        for attempt in range(self.max_retries):
            try:
                user_prompt = self._build_prompt(name)
                response = self._agent.run(user_prompt)
                return self._process_response(response, structured)
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt == self.max_retries - 1:
                    logger.error(f"All {self.max_retries} attempts failed for: {name}")
                    return ModelOutput(
                        markdown=f"Error identifying {name}: {str(e)}",
                        metadata={"error": str(e), "attempts": self.max_retries},
                    )
        return ModelOutput(
            markdown="Unknown error", metadata={"error": "max_retries_exceeded"}
        )

    def _process_response(self, response: Any, structured: bool) -> ModelOutput:
        if structured:
            response_model = self.get_response_model()
            if response_model:
                try:
                    parsed_data = response.parse(response_model)
                    return ModelOutput(data=parsed_data, markdown=response.content)
                except Exception as e:
                    logger.warning(f"Failed to parse structured output: {e}")
                    return ModelOutput(
                        markdown=response.content, metadata={"parse_error": str(e)}
                    )
        return ModelOutput(markdown=response.content)

    def identify_with_tools(self, name: str) -> ModelOutput:
        research_prompt = f"""Research and identify '{name}' using available tools."""
        response = self._agent.run(research_prompt)
        return ModelOutput(
            markdown=response.content, metadata={"method": "tools", "entity_name": name}
        )

    def compare(self, name1: str, name2: str) -> ModelOutput:
        comparison_prompt = f"""Compare '{name1}' and '{name2}'."""
        response = self._agent.run(comparison_prompt)
        return ModelOutput(
            markdown=response.content,
            metadata={"comparison": True, "entity1": name1, "entity2": name2},
        )

    def verify(self, name: str, claims: list[str]) -> ModelOutput:
        claims_text = "\n".join([f"- {claim}" for claim in claims])
        verification_prompt = (
            f"""Verify the following claims about '{name}':\n{claims_text}"""
        )
        response = self._agent.run(verification_prompt)
        return ModelOutput(
            markdown=response.content,
            metadata={"verification": True, "entity_name": name, "claims": claims},
        )

    def reset_memory(self) -> None:
        self._agent.history = []
        logger.info("Agent memory reset")

    def get_conversation_history(self) -> list[dict[str, Any]]:
        return self._agent.history if hasattr(self._agent, "history") else []
