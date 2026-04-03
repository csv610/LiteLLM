"""
agnoagents.py - Multi-agent implementation using Agno framework for med_myths_checker.
"""

import asyncio
from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.ollama import Ollama
from agno.tools.pubmed import PubmedTools
from agno.tools.websearch import WebSearchTools
from app.MedKit.medical.base.models import ModelOutput

from app.MedKit.shared.model_factory import get_agno_model


class AgnoMedMythsCheckerAgents:
    def __init__(self, model_name: str = "gemini/gemini-2.5-flash"):
        self.model_name = model_name
        self.model = get_agno_model(model_name)

        self.specialist = Agent(
            name="med_myths_checker Specialist",
            role="Expert in med_myths_checker tasks",
            model=self.model,
            instructions=[
                "Provide deep analysis and structured insights for med_myths_checker."
            ],
            tools=[PubmedTools(), WebSearchTools()],
        )

        self.verifier = Agent(
            name="med_myths_checker Verifier",
            role="Quality control and verification",
            model=self.model,
            instructions=[
                "Verify the specialist's findings for accuracy and completeness."
            ],
            tools=[PubmedTools(), WebSearchTools()],
        )

        self.manager = Agent(
            name="med_myths_checker Manager",
            team=[self.specialist, self.verifier],
            model=self.model,
            instructions=[
                "Coordinate the med_myths_checker workflow.",
                "Synthesize specialist and verifier outputs into a final Markdown report.",
            ],
            tools=[PubmedTools(), WebSearchTools()],
            markdown=True,
        )

    async def run(self, input_text: str) -> ModelOutput:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, lambda: self.manager.run(input_text)
        )
        return ModelOutput(
            markdown=response.content,
            metadata={
                "framework": "agno",
                "agents": ["Specialist", "Verifier"],
                "model": self.model_name,
            },
        )
