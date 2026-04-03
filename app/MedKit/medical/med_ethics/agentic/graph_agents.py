"""
graphagents.py - Multi-agent implementation using LangGraph for med_ethics.
"""

import asyncio
from typing import List, Optional, Any, TypedDict
from langgraph.graph import StateGraph, END
from app.MedKit.medical.med_ethics.shared.models import ModelOutput
from app.MedKit.shared.model_factory import get_chain_model


class AgentState(TypedDict):
    input: str
    specialist_output: str
    final_report: str


class GraphMedEthicsAgents:
    def __init__(self, model_name: str = "gemini/gemini-2.5-flash"):
        self.model_name = model_name
        self.llm = get_chain_model(model_name)
        workflow = StateGraph(AgentState)
        workflow.add_node("specialist", self.specialist_node)
        workflow.add_node("manager", self.manager_node)
        workflow.set_entry_point("specialist")
        workflow.add_edge("specialist", "manager")
        workflow.add_edge("manager", END)
        self.app = workflow.compile()

    def specialist_node(self, state: AgentState):
        response = self.llm.invoke(f"Specialist for med_ethics: {state['input']}")
        return {"specialist_output": response.content}

    def manager_node(self, state: AgentState):
        response = self.llm.invoke(
            f"Manager for med_ethics synthesize: {state['specialist_output']}"
        )
        return {"final_report": response.content}

    async def run(self, input_text: str) -> ModelOutput:
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(
            None, lambda: self.app.invoke({"input": input_text})
        )
        return ModelOutput(
            markdown=final_state["final_report"], metadata={"framework": "langgraph"}
        )
