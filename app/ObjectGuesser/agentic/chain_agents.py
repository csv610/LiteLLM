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

        self.specialist_prompt = PromptTemplate.from_template(
            f"You are a Specialist for {module_name}. INPUT: {{input}}"
        )
        self.verifier_prompt = PromptTemplate.from_template(
            f"You are a Verifier for {module_name}. Specialist: {{specialist_output}}"
        )
        self.manager_prompt = PromptTemplate.from_template(
            f"Synthesize for {module_name}: Input={{input}}, Specialist={{specialist_output}}, Verifier={{verifier_output}}"
        )

    async def run(self, input_text: str) -> ModelOutput:
        loop = asyncio.get_event_loop()

        if self.specialist_schema:
            try:
                r = self.specialist_llm.invoke(
                    self.specialist_prompt.format(input=input_text)
                )
                specialist_output = str(r.model_dump())
            except:
                r = await loop.run_in_executor(
                    None,
                    lambda: (self.specialist_prompt | self.llm_text).invoke(
                        {"input": input_text}
                    ),
                )
                specialist_output = r.content if hasattr(r, "content") else str(r)
        else:
            r = await loop.run_in_executor(
                None,
                lambda: (self.specialist_prompt | self.llm_text).invoke(
                    {"input": input_text}
                ),
            )
            specialist_output = r.content if hasattr(r, "content") else str(r)

        if self.verifier_schema:
            try:
                r = self.verifier_llm.invoke(
                    self.verifier_prompt.format(specialist_output=specialist_output)
                )
                verifier_output = str(r.model_dump())
            except:
                r = await loop.run_in_executor(
                    None,
                    lambda: (self.verifier_prompt | self.llm_text).invoke(
                        {"specialist_output": specialist_output}
                    ),
                )
                verifier_output = r.content if hasattr(r, "content") else str(r)
        else:
            r = await loop.run_in_executor(
                None,
                lambda: (self.verifier_prompt | self.llm_text).invoke(
                    {"specialist_output": specialist_output}
                ),
            )
            verifier_output = r.content if hasattr(r, "content") else str(r)

        r = await loop.run_in_executor(
            None,
            lambda: (self.manager_prompt | self.llm_text).invoke(
                {
                    "input": input_text,
                    "specialist_output": specialist_output,
                    "verifier_output": verifier_output,
                }
            ),
        )
        final_report = r.content if hasattr(r, "content") else str(r)

        return ModelOutput(
            data={"specialist": specialist_output, "verifier": verifier_output},
            markdown=final_report,
            metadata={
                "framework": "langchain",
                "agents": ["Specialist", "Verifier", "Manager"],
                "model": self.model_name,
            },
        )
