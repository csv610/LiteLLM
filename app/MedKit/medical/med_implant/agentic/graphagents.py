"""
graphagents.py - Multi-agent implementation using LangGraph for med_implant.
"""

import asyncio
from typing import List, Optional, Any, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from app.MedKit.medical.med_implant.shared.models import ModelOutput

class AgentState(TypedDict):
    input: str
    specialist_output: str
    final_report: str

class GraphMedImplantAgents:
    def __init__(self, model_name: str = "gemini/gemini-2.5-flash"):
        self.model_name = model_name
        self.llm = self.get_model(model_name)
        workflow = StateGraph(AgentState)
        workflow.add_node("specialist", self.specialist_node)
        workflow.add_node("manager", self.manager_node)
        workflow.set_entry_point("specialist")
        workflow.add_edge("specialist", "manager")
        workflow.add_edge("manager", END)
        self.app = workflow.compile()

    def get_model(self, model_name: str):
        if "gemini" in model_name.lower(): return ChatGoogleGenerativeAI(model=model_name)
        if "gpt" in model_name.lower(): return ChatOpenAI(model=model_name)
        return ChatOllama(model=model_name)

    def specialist_node(self, state: AgentState):
        response = self.llm.invoke(f"Specialist for med_implant: {state['input']}")
        return {"specialist_output": response.content}

    def manager_node(self, state: AgentState):
        response = self.llm.invoke(f"Manager for med_implant synthesize: {state['specialist_output']}")
        return {"final_report": response.content}

    async def run(self, input_text: str) -> ModelOutput:
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(None, lambda: self.app.invoke({"input": input_text}))
        return ModelOutput(markdown=final_state["final_report"], metadata={"framework": "langgraph"})
