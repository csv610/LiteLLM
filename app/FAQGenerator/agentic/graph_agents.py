"""
graph_agents.py - Multi-agent implementation using LangGraph with Pydantic models.
"""

import asyncio
from typing import Type, Optional, Any, TypedDict
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from lite import ModelOutput

from app.shared.model_factory import get_structured_model, get_model


class AgentState(TypedDict):
    input: str
    specialist_data: str
    verifier_data: str
    final_report: str


class GraphAgents:
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

        self.llm_text = get_model(model_name, framework="langgraph")

        if specialist_schema:
            self.specialist_llm = get_structured_model(
                model_name, framework="langgraph", response_schema=specialist_schema
            )
        if verifier_schema:
            self.verifier_llm = get_structured_model(
                model_name, framework="langgraph", response_schema=verifier_schema
            )

        workflow = StateGraph(AgentState)
        workflow.add_node("specialist", self.specialist_node)
        workflow.add_node("verifier", self.verifier_node)
        workflow.add_node("manager", self.manager_node)
        workflow.set_entry_point("specialist")
        workflow.add_edge("specialist", "verifier")
        workflow.add_edge("verifier", "manager")
        workflow.add_edge("manager", END)
        self.app = workflow.compile()

    def specialist_node(self, state: AgentState):
        prompt = (
            f"You are a Specialist for {self.module_name}. Analyze: {state['input']}"
        )
        if self.specialist_schema:
            try:
                result = self.specialist_llm.invoke(prompt)
                return {"specialist_data": str(result.model_dump())}
            except:
                pass
        response = self.llm_text.invoke(prompt)
        return {
            "specialist_data": response.content
            if hasattr(response, "content")
            else str(response)
        }

    def verifier_node(self, state: AgentState):
        prompt = f"You are a Verifier for {self.module_name}. Interrogate: {state['specialist_data']}"
        if self.verifier_schema:
            try:
                result = self.verifier_llm.invoke(prompt)
                return {"verifier_data": str(result.model_dump())}
            except:
                pass
        response = self.llm_text.invoke(prompt)
        return {
            "verifier_data": response.content
            if hasattr(response, "content")
            else str(response)
        }

    def manager_node(self, state: AgentState):
        prompt = f"Synthesize for {self.module_name}: Input={state['input']}, Specialist={state['specialist_data']}, Verifier={state['verifier_data']}"
        response = self.llm_text.invoke(prompt)
        return {
            "final_report": response.content
            if hasattr(response, "content")
            else str(response)
        }

    async def run(self, input_text: str) -> ModelOutput:
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(
            None, lambda: self.app.invoke({"input": input_text})
        )
        return ModelOutput(
            data={
                "specialist": final_state.get("specialist_data"),
                "verifier": final_state.get("verifier_data"),
            },
            markdown=final_state["final_report"],
            metadata={
                "framework": "langgraph",
                "agents": ["Specialist", "Verifier", "Manager"],
                "model": self.model_name,
            },
        )
