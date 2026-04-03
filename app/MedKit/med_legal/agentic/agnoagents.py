#!/usr/bin/env python3
"""
Agno Agents module for Patient Legal Rights.

This module implements Agno agents to generate comprehensive patient legal rights
information, leveraging the Agno framework for agentic workflows.
"""

import logging
from typing import Optional

from agno.agent import Agent
from agno.models.ollama import Ollama
from agno.tools.pubmed import PubmedTools
from agno.tools.websearch import WebSearchTools

try:
    from med_legal.legal_rights_models import LegalRightsModel, ModelOutput
    from med_legal.legal_rights_prompts import PromptBuilder
except (ImportError, ValueError):
    from legal_rights_models import LegalRightsModel, ModelOutput
    from legal_rights_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class LegalRightsAgnoAgent:
    """
    Agno-based agent for generating patient legal rights information using Ollama.
    """

    def __init__(self, model_id: str = "llama3.2"):
        self.model_id = model_id
        self.system_prompt = PromptBuilder.create_system_prompt()
        self.host = "http://localhost:11434"

        # Initialize the Agno Agent with Ollama
        self.agent = Agent(
            model=Ollama(id=self.model_id, host=self.host),
            description="You are a legal expert specializing in patient rights and healthcare law.",
            instructions=[
                self.system_prompt,
                "Ensure the output strictly follows the requested structure and jurisdictional focus.",
            ],
            markdown=True,
            tools=[PubmedTools(), WebSearchTools()],
        )
        logger.debug(
            f"Initialized LegalRightsAgnoAgent with Ollama model: {self.model_id} at {self.host}"
        )

    def generate(
        self, topic: str, country: str, structured: bool = False
    ) -> ModelOutput:
        """
        Generates comprehensive patient legal rights information using Agno Agent.
        """
        if not topic or not str(topic).strip():
            raise ValueError("Topic name cannot be empty")
        if not country or not str(country).strip():
            raise ValueError("Country cannot be empty")

        user_prompt = PromptBuilder.create_user_prompt(topic, country)

        logger.debug(
            f"Generating legal rights for: {topic} in {country} (structured={structured})"
        )

        if structured:
            # For structured output, we use the output_schema feature of Agno
            structured_agent = Agent(
                model=Ollama(id=self.model_id, host=self.host),
                description="You are a legal expert specializing in patient rights and healthcare law.",
                instructions=[self.system_prompt],
                output_schema=LegalRightsModel,
                structured_outputs=True,
                tools=[PubmedTools(), WebSearchTools()],
            )
            response = structured_agent.run(user_prompt)
            return ModelOutput(
                data=response.content,
                markdown=None,
                metadata={"model": self.model_id, "agent": "agno_ollama_structured"},
            )
        else:
            # For regular markdown output
            response = self.agent.run(user_prompt)
            return ModelOutput(
                data=None,
                markdown=response.content,
                metadata={"model": self.model_id, "agent": "agno_ollama_markdown"},
            )


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    agent = LegalRightsAgnoAgent()

    # Test generation
    try:
        print("Testing Agno Agent (Markdown)...")
        result = agent.generate("Informed Consent", "USA", structured=False)
        print("\nMarkdown Result Preview:")
        print(result.markdown[:500] + "...")

        print("\nTesting Agno Agent (Structured)...")
        result_structured = agent.generate(
            "Medical Records Access", "India", structured=True
        )
        print("\nStructured Result (Data Type):", type(result_structured.data))
        if result_structured.data:
            print("Topic Name:", result_structured.data.overview.topic_name)
    except Exception as e:
        print(f"Error during test: {e}")
