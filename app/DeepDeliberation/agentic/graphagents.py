"""
graphagents.py - Multi-agent implementation using LangGraph.
"""

import asyncio
from typing import List, Optional, Any, TypedDict, Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from app.DeepDeliberation.shared.models import ModelOutput

class AgentState(TypedDict):
    input: str
    specialist_output: str
    verifier_output: str
    final_report: str

def get_graph_model(model_name: str):
    if "gemini" in model_name.lower():
        return ChatGoogleGenerativeAI(model=model_name)
    elif "gpt" in model_name.lower() or "claude" in model_name.lower():
        return ChatOpenAI(model=model_name)
    else:
        return ChatOllama(model=model_name)

class GraphDeepDeliberationAgents:
    """LangGraph-based multi-agent implementation for DeepDeliberation."""
    
    def __init__(self, model_name: str = "gemini/gemini-2.5-flash"):
        self.model_name = model_name
        self.llm = get_graph_model(model_name)
        
        # Build the graph
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
        prompt = f"You are a Specialist for DeepDeliberation. Analyze this input: {state['input']}"
        response = self.llm.invoke(prompt)
        return {"specialist_output": response.content}

    def verifier_node(self, state: AgentState):
        prompt = f"You are a Verifier for DeepDeliberation. Interrogate this analysis: {state['specialist_output']}"
        response = self.llm.invoke(prompt)
        return {"verifier_output": response.content}

    def manager_node(self, state: AgentState):
        prompt = f"""Synthesize the following into a final Markdown report for DeepDeliberation:
        Input: {state['input']}
        Specialist: {state['specialist_output']}
        Verifier: {state['verifier_output']}
        """
        response = self.llm.invoke(prompt)
        return {"final_report": response.content}

    async def run(self, input_text: str) -> ModelOutput:
        initial_state = {"input": input_text}
        
        # Run the graph
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(
            None, 
            lambda: self.app.invoke(initial_state)
        )
        
        return ModelOutput(
            markdown=final_state["final_report"],
            metadata={
                "framework": "langgraph",
                "agents": ["Specialist", "Verifier", "Manager"],
                "model": self.model_name
            }
        )
