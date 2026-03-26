import os
import json
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput

try:
    from .riemann_problems_models import (
        RiemannTheoryModel,
        RiemannOverviewModel,
        RiemannTechnicalModel,
        RiemannAppliedImpactModel,
    )
    from .riemann_problems_prompts import AgentPersonas, PromptBuilder
except ImportError:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from riemann_problems_models import (
        RiemannTheoryModel,
        RiemannOverviewModel,
        RiemannTechnicalModel,
        RiemannAppliedImpactModel,
    )
    from riemann_problems_prompts import AgentPersonas, PromptBuilder

class MultiAgentRiemannGuide:
    """
    Orchestrates 5 specialized agents:
    1. Researcher (History)
    2. Overview (Pedagogical Narrative)
    3. Technical (Mathematical Formalism)
    4. Application Expert (Real-world Impact)
    5. Critic (Integration & Quality Control)
    """

    def __init__(self, model: str = "ollama/gemma3"):
        self.config = ModelConfig(model=model, temperature=0.1)
        self.client = LiteClient(self.config)

    async def researcher_agent(self, theory_name: str) -> str:
        print(f"🕵️  Researcher Agent: Fact-checking {theory_name}...")
        model_input = ModelInput(
            system_prompt=AgentPersonas.get_researcher_prompt(),
            user_prompt=f"Provide a research brief for: '{theory_name}'."
        )
        return self.client.generate_text(model_input)

    async def overview_agent(self, theory_name: str, brief: str) -> RiemannOverviewModel:
        print(f"🏫 Overview Agent (Teacher): Drafting narrative for {theory_name}...")
        model_input = ModelInput(
            system_prompt=AgentPersonas.get_overview_prompt(),
            user_prompt=f"Create a pedagogical overview for '{theory_name}' based on this brief:\n{brief}",
            response_format=RiemannOverviewModel
        )
        return self.client.generate_text(model_input)

    async def technical_agent(self, theory_name: str, brief: str) -> RiemannTechnicalModel:
        print(f"🎓 Technical Agent (Professor): Drafting formal math for {theory_name}...")
        model_input = ModelInput(
            system_prompt=AgentPersonas.get_technical_prompt(),
            user_prompt=f"Create a rigorous mathematical core for '{theory_name}' based on this brief:\n{brief}",
            response_format=RiemannTechnicalModel
        )
        return self.client.generate_text(model_input)

    async def app_expert_agent(self, theory_name: str, tech_report: RiemannTechnicalModel) -> RiemannAppliedImpactModel:
        print(f"🚀 Application Expert: Analyzing impact of {theory_name}...")
        tech_data = tech_report.model_dump_json()
        model_input = ModelInput(
            system_prompt=AgentPersonas.get_app_expert_prompt(),
            user_prompt=f"Explain applications for '{theory_name}' given this math:\n{tech_data}",
            response_format=RiemannAppliedImpactModel
        )
        return self.client.generate_text(model_input)

    async def critic_agent(self, report: RiemannTheoryModel) -> str:
        print(f"🧐 Critic Agent: Reviewing integrated dossier...")
        model_input = ModelInput(
            system_prompt=AgentPersonas.get_critic_prompt(),
            user_prompt=f"Review this dossier:\n{report.model_dump_json(indent=2)}"
        )
        return self.client.generate_text(model_input)

    def _merge(self, ov: RiemannOverviewModel, tech: RiemannTechnicalModel, app: RiemannAppliedImpactModel) -> RiemannTheoryModel:
        merged = {**ov.model_dump(), **tech.model_dump(), **app.model_dump()}
        return RiemannTheoryModel.model_validate(merged)

    async def run_pipeline(self, theory_name: str) -> RiemannTheoryModel:
        # 1. Fact-finding
        brief = await self.researcher_agent(theory_name)
        
        # 2. Parallelizable Creation (though we run sequentially for CLI logs)
        overview = await self.overview_agent(theory_name, brief)
        technical = await self.technical_agent(theory_name, brief)
        
        # 3. Contextual Application Analysis
        applied = await self.app_expert_agent(theory_name, technical)
        
        # 4. Integration
        final_report = self._merge(overview, technical, applied)
        
        # 5. Peer Review
        review = await self.critic_agent(final_report)
        if "PASS" not in review.upper():
            print(f"⚠️  Critic Feedback: {review[:100]}...")
            
        print(f"✅ 5-Agent dossier complete for '{theory_name}'.")
        return final_report

async def run_riemann_agent(theory_name: str, model: str = "ollama/gemma3") -> RiemannTheoryModel:
    orchestrator = MultiAgentRiemannGuide(model=model)
    return await orchestrator.run_pipeline(theory_name)
