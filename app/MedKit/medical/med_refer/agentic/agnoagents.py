"""
agnoagents.py - Multi-agent implementation using Agno framework for med_refer.
"""

import asyncio
from typing import List, Optional, Any
from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.ollama import Ollama
from app.MedKit.medical.med_refer.shared.models import ModelOutput

def get_agno_model(model_name: str):
    if "gemini" in model_name.lower():
        return Gemini(id=model_name)
    else:
        return Ollama(id=model_name)

class AgnoMedReferAgents:
    def __init__(self, model_name: str = "gemini/gemini-2.5-flash"):
        self.model_name = model_name
        self.model = get_agno_model(model_name)
        
        self.specialist = Agent(
            name="med_refer Specialist",
            role="Expert in med_refer tasks",
            model=self.model,
            instructions=["Provide deep analysis and structured insights for med_refer."],
        )

        self.verifier = Agent(
            name="med_refer Verifier",
            role="Quality control and verification",
            model=self.model,
            instructions=["Verify the specialist's findings for accuracy and completeness."],
        )

        self.manager = Agent(
            name="med_refer Manager",
            team=[self.specialist, self.verifier],
            model=self.model,
            instructions=[
                "Coordinate the med_refer workflow.",
                "Synthesize specialist and verifier outputs into a final Markdown report."
            ],
            markdown=True
        )

    async def run(self, input_text: str) -> ModelOutput:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: self.manager.run(input_text)
        )
        return ModelOutput(
            markdown=response.content,
            metadata={
                "framework": "agno",
                "agents": ["Specialist", "Verifier"],
                "model": self.model_name
            }
        )
