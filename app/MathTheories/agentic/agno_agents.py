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
    """Agno-based multi-agent implementation with Pydantic structured output."""

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
            role=f"Expert in {module_name} tasks",
            model=self.model,
            response_model=specialist_schema,
            instructions=[
                f"Provide deep analysis and structured insights for {module_name}. "
                "Return structured data in your response."
            ],
        )

        self.verifier = Agent(
            name=f"{module_name} Verifier",
            role="Quality control and verification",
            model=self.model,
            response_model=verifier_schema,
            instructions=[
                "Verify the specialist's findings for accuracy and completeness. "
                "Return structured verification data."
            ],
        )

        self.manager = Agent(
            name=f"{module_name} Manager",
            team=[self.specialist, self.verifier],
            model=self.model,
            instructions=[
                f"Coordinate the {module_name} workflow.",
                "Synthesize specialist and verifier outputs into a final Markdown report.",
            ],
            markdown=True,
        )

    async def run(self, input_text: str) -> ModelOutput:
        loop = asyncio.get_event_loop()

        try:
            if self.specialist_schema:
                specialist_response = await loop.run_in_executor(
                    None, lambda: self.specialist.run(input_text)
                )
                specialist_output = (
                    str(specialist_response.content)
                    if hasattr(specialist_response, "content")
                    else str(specialist_response)
                )
            else:
                specialist_response = await loop.run_in_executor(
                    None, lambda: self.specialist.run(input_text)
                )
                specialist_output = (
                    specialist_response.content
                    if hasattr(specialist_response, "content")
                    else str(specialist_response)
                )
        except Exception as e:
            specialist_output = f"Error: {str(e)}"

        try:
            if self.verifier_schema:
                verifier_response = await loop.run_in_executor(
                    None,
                    lambda: self.verifier.run(
                        f"Verify this analysis: {specialist_output}"
                    ),
                )
                verifier_output = (
                    str(verifier_response.content)
                    if hasattr(verifier_response, "content")
                    else str(verifier_response)
                )
            else:
                verifier_response = await loop.run_in_executor(
                    None,
                    lambda: self.verifier.run(
                        f"Verify this analysis: {specialist_output}"
                    ),
                )
                verifier_output = (
                    verifier_response.content
                    if hasattr(verifier_response, "content")
                    else str(verifier_response)
                )
        except Exception as e:
            verifier_output = f"Error: {str(e)}"

        manager_response = await loop.run_in_executor(
            None,
            lambda: self.manager.run(f"""Synthesize the following into a Markdown report:

Input: {input_text}
Specialist: {specialist_output}
Verifier: {verifier_output}"""),
        )

        final_report = (
            manager_response.content
            if hasattr(manager_response, "content")
            else str(manager_response)
        )

        return ModelOutput(
            data={
                "specialist": specialist_output,
                "verifier": verifier_output,
            },
            markdown=final_report,
            metadata={
                "framework": "agno",
                "agents": ["Specialist", "Verifier", "Manager"],
                "model": self.model_name,
            },
        )
