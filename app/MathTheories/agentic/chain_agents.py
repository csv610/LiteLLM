"""
chain_agents.py - Multi-agent implementation using LangChain with Pydantic models.
"""

import asyncio
from typing import Type, Optional, Any
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from lite import ModelOutput

from app.shared.model_factory import get_model, get_structured_model


class ChainAgents:
    """LangChain-based multi-agent implementation with Pydantic structured output."""

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

        self.llm_text = get_model(model_name, framework="langchain")

        if specialist_schema:
            self.specialist_llm = get_structured_model(
                model_name, framework="langchain", response_schema=specialist_schema
            )
        if verifier_schema:
            self.verifier_llm = get_structured_model(
                model_name, framework="langchain", response_schema=verifier_schema
            )

        self.specialist_prompt = PromptTemplate.from_template(f"""You are a Specialist for {module_name}.
Analyze this input and provide structured data.

INPUT: {{input}}

Provide your analysis as structured data.""")

        self.verifier_prompt = PromptTemplate.from_template(f"""You are a Verifier for {module_name}.
Interrogate this analysis and provide structured feedback.

Specialist Analysis: {{specialist_output}}

Provide your verification as structured data.""")

        self.manager_prompt = PromptTemplate.from_template(f"""Synthesize the following into a final Markdown report for {module_name}:

Input: {{input}}
Specialist: {{specialist_output}}
Verifier: {{verifier_output}}

Final Report (Markdown):""")

    async def run(self, input_text: str) -> ModelOutput:
        if self.specialist_schema:
            try:
                specialist_result = self.specialist_llm.invoke(
                    self.specialist_prompt.format(input=input_text)
                )
                specialist_output = str(specialist_result.model_dump())
            except Exception:
                chain = self.specialist_prompt | self.llm_text
                specialist_output = (
                    await asyncio.get_event_loop().run_in_executor(
                        None, lambda: chain.invoke({"input": input_text})
                    )
                ).content
        else:
            chain = self.specialist_prompt | self.llm_text
            specialist_output = (
                await asyncio.get_event_loop().run_in_executor(
                    None, lambda: chain.invoke({"input": input_text})
                )
            ).content

        if self.verifier_schema:
            try:
                verifier_result = self.verifier_llm.invoke(
                    self.verifier_prompt.format(specialist_output=specialist_output)
                )
                verifier_output = str(verifier_result.model_dump())
            except Exception:
                chain = self.verifier_prompt | self.llm_text
                verifier_output = (
                    await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda: chain.invoke({"specialist_output": specialist_output}),
                    )
                ).content
        else:
            chain = self.verifier_prompt | self.llm_text
            verifier_output = (
                await asyncio.get_event_loop().run_in_executor(
                    None, lambda: chain.invoke({"specialist_output": specialist_output})
                )
            ).content

        chain = self.manager_prompt | self.llm_text
        final_report = (
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: chain.invoke(
                    {
                        "input": input_text,
                        "specialist_output": specialist_output,
                        "verifier_output": verifier_output,
                    }
                ),
            )
        ).content

        return ModelOutput(
            data={
                "specialist": specialist_output,
                "verifier": verifier_output,
            },
            markdown=final_report,
            metadata={
                "framework": "langchain",
                "agents": ["Specialist", "Verifier", "Manager"],
                "model": self.model_name,
            },
        )
