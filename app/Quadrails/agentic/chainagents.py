"""
chainagents.py - Multi-agent implementation using LangChain.
"""

import asyncio
from typing import List, Optional, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from app.Quadrails.shared.models import ModelOutput

def get_chain_model(model_name: str):
    if "gemini" in model_name.lower():
        return ChatGoogleGenerativeAI(model=model_name)
    elif "gpt" in model_name.lower() or "claude" in model_name.lower():
        return ChatOpenAI(model=model_name)
    else:
        # Default to Ollama for local models
        return ChatOllama(model=model_name)

class ChainQuadrailsAgents:
    """LangChain-based multi-agent implementation for Quadrails."""
    
    def __init__(self, model_name: str = "gemini/gemini-2.5-flash"):
        self.model_name = model_name
        self.llm = get_chain_model(model_name)
        
        # In LangChain, we often use chains or specialized agents.
        # For simplicity in this batch implementation, we'll use a 
        # structured prompt approach that mimics the multi-agent flow.
        
        self.prompt = PromptTemplate.from_template("""
        You are a multi-agent system for Quadrails.
        
        SPECIALIST ROLE: Expert in Quadrails tasks.
        VERIFIER ROLE: Quality control and verification.
        
        MISSION:
        1. Specialist: Analyze the input and provide deep insights.
        2. Verifier: Interrogate the specialist's findings for accuracy.
        3. Manager: Synthesize everything into a final Markdown report.
        
        INPUT: {input}
        
        Final Report (Markdown):
        """)

    async def run(self, input_text: str) -> ModelOutput:
        # Simple chain execution
        chain = self.prompt | self.llm
        
        # Run in executor to handle sync LLM calls if needed
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: chain.invoke({"input": input_text})
        )
        
        # response.content for ChatModels
        content = response.content if hasattr(response, 'content') else str(response)
        
        return ModelOutput(
            markdown=content,
            metadata={
                "framework": "langchain",
                "agents": ["Specialist", "Verifier"],
                "model": self.model_name
            }
        )
