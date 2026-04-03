"""
agnoagents.py - Multi-agent implementation using Agno framework for med_decision_guide.
"""

import asyncio
from agno.agent import Agent
from agno.tools.pubmed import PubmedTools
from agno.tools.websearch import WebSearchTools
from agno.models.google import Gemini
from agno.models.ollama import Ollama
from app.MedKit.medical.base.models import ModelOutput

from app.MedKit.shared.model_factory import get_agno_model


class AgnoMedDecisionGuideAgents:
    def __init__(self, model_name: str = "gemini/gemini-2.5-flash"):
        self.model_name = model_name
        self.model = get_agno_model(model_name)

        self.specialist = Agent(
            name="med_decision_guide Specialist",
            role="Expert in med_decision_guide tasks",
            model=self.model,
            instructions=[
                "Provide deep analysis and structured insights for med_decision_guide."
            ],
            tools=[PubmedTools(), WebSearchTools()],
        )

        self.verifier = Agent(
            name="med_decision_guide Verifier",
            role="Quality control and verification",
            model=self.model,
            instructions=[
                "Verify the specialist's findings for accuracy and completeness."
            ],
            tools=[PubmedTools(), WebSearchTools()],
        )

        self.manager = Agent(
            name="med_decision_guide Manager",
            team=[self.specialist, self.verifier],
            model=self.model,
            instructions=[
                "Coordinate the med_decision_guide workflow.",
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
