"""
chainagents.py - Multi-agent implementation using LangChain for tests.
"""

import asyncio
from typing import List, Optional, Any
from langchain_core.prompts import PromptTemplate
from lite import ModelOutput

from app.MedKit.shared.model_factory import get_chain_model


class ChainTestsAgents:
    def __init__(self, model_name: str = "gemini/gemini-2.5-flash"):
        self.model_name = model_name
        self.llm = get_chain_model(model_name)
        self.prompt = PromptTemplate.from_template("""
        You are a multi-agent system for tests.
        SPECIALIST ROLE: Expert in tests tasks.
        VERIFIER ROLE: Quality control and verification.
        MISSION: Specialist analyzes, Verifier interrogates, Manager synthesizes.
        INPUT: {input}
        Final Report (Markdown):
        """)

    async def run(self, input_text: str) -> ModelOutput:
        chain = self.prompt | self.llm
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, lambda: chain.invoke({"input": input_text})
        )
        content = response.content if hasattr(response, "content") else str(response)
        return ModelOutput(
            markdown=content,
            metadata={"framework": "langchain", "model": self.model_name},
        )
