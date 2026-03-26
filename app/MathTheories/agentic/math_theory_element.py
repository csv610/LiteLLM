"""
math_theory_element.py - Multi-agent system for mathematical theory explanations

Implements a 3-agent pipeline (Researcher, Writer, Reviewer) for fetching 
and managing high-quality mathematical theory information.
"""

import logging
from typing import Optional, List, Dict

from lite import LiteClient, ModelConfig
from lite.config import ModelInput

from math_theory_models import (
    MathTheory, TheoryExplanation, AudienceLevel, 
    ResearchData, ReviewFeedback
)


class ResearcherAgent:
    """Agent responsible for gathering deep technical and historical mathematical data."""
    
    def __init__(self, client: LiteClient):
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
        model_input = ModelInput(user_prompt=prompt, response_format=ResearchData)
        return self.client.generate_text(model_input=model_input)


class WriterAgent:
    """Agent responsible for adapting technical research into audience-specific content."""
    
    def __init__(self, client: LiteClient):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def write_explanation(self, research: ResearchData, level: AudienceLevel, feedback: Optional[ReviewFeedback] = None) -> Optional[TheoryExplanation]:
        level_descriptions = {
            AudienceLevel.GENERAL: "No mathematical background. Use analogies, avoid jargon, focus on the 'big idea'.",
            AudienceLevel.HIGH_SCHOOL: "Basic algebra/geometry knowledge. Introduce formal concepts gently.",
            AudienceLevel.UNDERGRAD: "Math/Science major. Use formal notation, proofs-sketches, and rigorous definitions.",
            AudienceLevel.MASTER: "Graduate student. Deep dive into complex structures and theoretical implications.",
            AudienceLevel.PHD: "Expert level. Focus on nuance, recent papers, and advanced abstract connections.",
            AudienceLevel.RESEARCHER: "Peer level. Focus on the cutting edge, open conjectures, and cross-disciplinary utility."
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
        
        model_input = ModelInput(user_prompt=prompt, response_format=TheoryExplanation)
        return self.client.generate_text(model_input=model_input)


class ReviewerAgent:
    """Agent responsible for auditing explanations for accuracy and audience fit."""
    
    def __init__(self, client: LiteClient):
        self.client = client
        self.logger = logging.getLogger(__name__)

    def review(self, research: ResearchData, explanation: TheoryExplanation) -> Optional[ReviewFeedback]:
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
        model_input = ModelInput(user_prompt=prompt, response_format=ReviewFeedback)
        return self.client.generate_text(model_input=model_input)


class MathTheoryExplainer:
    """Orchestrates the 3-agent pipeline to generate high-quality theory explanations."""
    
    def __init__(self, model_config: ModelConfig, max_refinements: int = 3):
        self.client = LiteClient(model_config=model_config)
        self.researcher = ResearcherAgent(self.client)
        self.writer = WriterAgent(self.client)
        self.reviewer = ReviewerAgent(self.client)
        self.max_refinements = max_refinements
        self.logger = logging.getLogger(__name__)
    
    def fetch_theory_explanation(self, theory_name: str, audience_levels: List[AudienceLevel] = None) -> Optional[MathTheory]:
        if audience_levels is None:
            audience_levels = [AudienceLevel.UNDERGRAD]
            
        self.logger.info(f"Starting research phase for '{theory_name}'...")
        research_data = self.researcher.research(theory_name)
        
        if not research_data:
            self.logger.error("Research phase failed.")
            return None

        explanations: Dict[AudienceLevel, TheoryExplanation] = {}
        
        for level in audience_levels:
            self.logger.info(f"Generating explanation for audience: {level.value}")
            
            # Initial Draft
            explanation = self.writer.write_explanation(research_data, level)
            if not explanation:
                continue
                
            # Iterative Refinement Loop
            attempt = 0
            while attempt < self.max_refinements:
                self.logger.info(f"Reviewing explanation for audience: {level.value} (Attempt {attempt + 1})")
                feedback = self.reviewer.review(research_data, explanation)
                
                if feedback and feedback.is_accurate and feedback.is_audience_appropriate:
                    self.logger.info(f"Review passed for {level.value} after {attempt + 1} attempt(s).")
                    break
                
                attempt += 1
                if attempt < self.max_refinements:
                    critique_msg = feedback.critique if feedback else "Unknown error during review"
                    self.logger.warning(
                        f"Refinement required for {level.value} (Attempt {attempt}): {critique_msg}"
                    )
                    refined_explanation = self.writer.write_explanation(research_data, level, feedback)
                    if refined_explanation:
                        explanation = refined_explanation
                    else:
                        self.logger.error(f"Failed to generate refined draft on attempt {attempt}.")
                        break
                else:
                    self.logger.error(f"Reached max refinements ({self.max_refinements}) for {level.value}. Using last draft.")
            
            explanations[level] = explanation
            
        return MathTheory(theory_name=theory_name, explanations=explanations)
