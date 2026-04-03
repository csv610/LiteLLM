"""
agno_agents.py - Multi-agent implementation using Agno framework with Pydantic models.
"""

import asyncio
from typing import Type, Optional, Any
from pydantic import BaseModel
from agno.agent import Agent
from lite import ModelOutput

from app.shared.model_factory import get_model


class AgnoAgents:
    def __init__(
        self,
        model_name: str = "gemini/gemini-2.5-flash",
        module_name: str = "Module",
        specialist_schema: Optional[Type[BaseModel]] = None,
        verifier_schema: Optional[Type[BaseModel]] = None,
    ):
        self.model_name = model_name
        self.module_name = module_name
        self.specialist_schema = specialist_schema
        self.verifier_schema = verifier_schema
        self.model = get_model(model_name, framework="agno")

        self.specialist = Agent(
            name=f"{module_name} Specialist",
            role=f"Expert in {module_name}",
            model=self.model,
            response_model=specialist_schema,
            instructions=["Provide structured analysis."],
        )
        self.verifier = Agent(
            name=f"{module_name} Verifier",
            role="Quality control",
            model=self.model,
            response_model=verifier_schema,
            instructions=["Verify findings."],
        )
        self.manager = Agent(
            name=f"{module_name} Manager",
            team=[self.specialist, self.verifier],
            model=self.model,
            instructions=[f"Synthesize for {module_name}."],
            markdown=True,
        )

    async def run(self, input_text: str) -> ModelOutput:
        loop = asyncio.get_event_loop()

        try:
            r = await loop.run_in_executor(
                None, lambda: self.specialist.run(input_text)
            )
            specialist_output = r.content if hasattr(r, "content") else str(r)
        except Exception as e:
            specialist_output = f"Error: {e}"

        try:
            r = await loop.run_in_executor(
                None, lambda: self.verifier.run(f"Verify: {specialist_output}")
            )
            verifier_output = r.content if hasattr(r, "content") else str(r)
        except Exception as e:
            verifier_output = f"Error: {e}"

        r = await loop.run_in_executor(
            None,
            lambda: self.manager.run(
                f"Input: {input_text}\nSpecialist: {specialist_output}\nVerifier: {verifier_output}"
            ),
        )
        final_report = r.content if hasattr(r, "content") else str(r)

        return ModelOutput(
            data={"specialist": specialist_output, "verifier": verifier_output},
            markdown=final_report,
            metadata={
                "framework": "agno",
                "agents": ["Specialist", "Verifier", "Manager"],
                "model": self.model_name,
            },
        )
