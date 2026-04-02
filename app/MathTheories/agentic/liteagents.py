"""
liteagents.py - Unified LiteClient-based agents for MathTheories.
"""

from app.MathTheories.shared.models import (
from app.MathTheories.shared.models import *
from app.MathTheories.shared.utils import *
from lite.config import ModelConfig, ModelInput
from typing import Optional, List, Dict, Any
import json
import logging

"""
math_theory_element.py - Multi-agent system for mathematical theory explanations

Implements a 3-tier artifact-based approach (Specialists -> Auditor -> Closer)
for fetching and managing high-quality mathematical theory information.
"""

    MathTheory,
    TheoryExplanation,
    AudienceLevel,
    ResearchData,
    ReviewFeedback,
    AgenticLiteClient,
    ModelOutput
)

class ResearcherAgent:
    """Agent responsible for gathering deep technical and historical mathematical data."""

    def __init__(self, client: AgenticLiteClient):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def research(self, theory_name: str) -> Optional[ResearchData]:
        prompt = (
            f"Conduct exhaustive research on the mathematical theory: '{theory_name}'.\n"
            "Provide highly detailed information including historical context, fundamental axioms, "
            "key theorems, modern applications, and current research frontiers.\n"
            "This data will be used by other agents to create audience-specific explanations, "
            "so be as technically thorough as possible."
        )
        return self.client.generate_json(prompt=prompt, schema=ResearchData)

class WriterAgent:
    """Agent responsible for adapting technical research into audience-specific content."""

    def __init__(self, client: AgenticLiteClient):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def write_explanation(
        self,
        research: ResearchData,
        level: AudienceLevel,
        feedback: Optional[ReviewFeedback] = None,
    ) -> Optional[TheoryExplanation]:
        if not isinstance(research, ResearchData):
            self.logger.error(
                f"Expected ResearchData but got {type(research).__name__}. Research parsing may have failed."
            )
            return None

        level_descriptions = {
            AudienceLevel.GENERAL: "No mathematical background. Use analogies, avoid jargon, focus on the 'big idea'.",
            AudienceLevel.HIGH_SCHOOL: "Basic algebra/geometry knowledge. Introduce formal concepts gently.",
            AudienceLevel.UNDERGRAD: "Math/Science major. Use formal notation, proofs-sketches, and rigorous definitions.",
            AudienceLevel.MASTER: "Graduate student. Deep dive into complex structures and theoretical implications.",
            AudienceLevel.PHD: "Expert level. Focus on nuance, recent papers, and advanced abstract connections.",
            AudienceLevel.RESEARCHER: "Peer level. Focus on the cutting edge, open conjectures, and cross-disciplinary utility.",
        }

        prompt = (
            f"You are a world-class mathematical educator. Using the following research data, "
            f"write a comprehensive explanation of '{research.theory_name}' for a '{level.value}' audience.\n\n"
            f"Audience Guidelines: {level_descriptions.get(level, '')}\n\n"
            f"Research Data:\n{research.model_dump_json(indent=2)}\n\n"
        )

        if feedback:
            prompt += (
                f"\nIMPORTANT: A reviewer has provided the following critique of your previous draft. "
                f"You MUST address these points in this updated version:\n"
                f"Critique: {feedback.critique}\n"
                f"Required Corrections: {feedback.required_corrections}\n"
            )

        prompt += "\nEnsure the output is lengthy, engaging, and perfectly matches the audience's mathematical maturity."

        return self.client.generate_json(prompt=prompt, schema=TheoryExplanation)

class ReviewerAgent:
    """Agent responsible for auditing explanations for accuracy and audience fit."""

    def __init__(self, client: AgenticLiteClient):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def review(
        self, research: ResearchData, explanation: TheoryExplanation
    ) -> Optional[ReviewFeedback]:
        prompt = (
            f"You are a critical reviewer for a prestigious mathematical journal. "
            f"Audit the following explanation of '{research.theory_name}' intended for a '{explanation.audience.value}' audience.\n\n"
            f"Original Research Data (Ground Truth):\n{research.model_dump_json(indent=2)}\n\n"
            f"Proposed Explanation:\n{explanation.model_dump_json(indent=2)}\n\n"
            "Check for:\n"
            "1. Mathematical accuracy (does it deviate from the truth?)\n"
            "2. Audience appropriateness (is it too hard or too easy?)\n"
            "3. Completeness (did it miss key facts from the research?)\n"
        )
        return self.client.generate_json(prompt=prompt, schema=ReviewFeedback)

class MathTheoryExplainer:
    """Orchestrates the 3-tier pipeline to generate high-quality ModelOutput artifacts."""

    def __init__(self, model_config: ModelConfig, max_refinements: int = 2):
        self.client = AgenticLiteClient(model_config=model_config)
        self.researcher = ResearcherAgent(self.client)
        self.writer = WriterAgent(self.client)
        self.reviewer = ReviewerAgent(self.client)
        self.max_refinements = max_refinements
        self.logger = logging.getLogger(__name__)

    def generate_text(
        self, theory_name: str, audience_levels: List[AudienceLevel] = None
    ) -> Optional[ModelOutput]:
        """Fetch explanation and return standardized ModelOutput artifact."""
        if audience_levels is None:
            audience_levels = [AudienceLevel.UNDERGRAD]

        self.logger.info(f"Starting 3-tier process for theory: '{theory_name}'...")
        
        # Tier 1: Specialist Research (JSON)
        research_data = self.researcher.research(theory_name)
        if not research_data:
            self.logger.error("Research phase failed.")
            return None

        explanations: Dict[AudienceLevel, TheoryExplanation] = {}
        all_feedback = []

        for level in audience_levels:
            self.logger.info(f"Generating Tier 1/2 explanation for audience: {level.value}")

            # Initial Specialist Draft (JSON)
            explanation = self.writer.write_explanation(research_data, level)
            if not explanation: continue

            # Tier 2: Auditor Stage (JSON Audit & Refinement)
            attempt = 0
            while attempt < self.max_refinements:
                feedback = self.reviewer.review(research_data, explanation)
                all_feedback.append({
                    "level": level.value,
                    "attempt": attempt + 1,
                    "feedback": feedback.model_dump() if feedback else "Error"
                })

                if feedback and feedback.is_accurate and feedback.is_audience_appropriate:
                    break

                attempt += 1
                refined = self.writer.write_explanation(research_data, level, feedback)
                if refined: explanation = refined
                else: break

            explanations[level] = explanation

        # Assemble Final Data Object
        math_theory_data = MathTheory(theory_name=theory_name, explanations=explanations)

        # Tier 3: Output Synthesis (Markdown Closer)
        # Convert the complex MathTheory object into a beautiful Markdown report
        synth_prompt = (
            f"Synthesize a final professional Markdown report for the mathematical theory: '{theory_name}'.\n\n"
            f"RESEARCH SUMMARY: {research_data.fundamental_axioms}\n\n"
            f"AUDIENCE EXPLANATIONS:\n"
            + "\n\n".join([f"### For {l.value}:\n{e.explanation_text}" for l, e in explanations.items()])
        )
        
        final_markdown = self.client.generate_text(
            prompt=synth_prompt + "\n\nFINAL INSTRUCTION: Create a master Markdown document with a history section, technical depth, and clear educational paths for different levels.",
            response_format=None
        )

        return ModelOutput(
            data=math_theory_data,
            markdown=final_markdown,
            metadata={
                "research": research_data.model_dump(),
                "audit_history": all_feedback
            }
        )

