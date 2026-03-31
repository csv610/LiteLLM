"""
deep_deliberation_agents.py - Reusable Discovery Agents

Encapsulates the specialized LLM logic for Inquiry, Analysis, and Verification.
"""

from lite import LiteClient
from lite.config import ModelInput
from .deep_deliberation_models import (
    DiscoveryFAQ, DiscoveryInsight, DiscoveryCheck, VerificationResult, SummaryResponse
)
from .deep_deliberation_prompts import PromptBuilder


class DiscoveryAgent:
    """Agent responsible for processing a single knowledge probe."""

    def __init__(self, client: LiteClient):
        self.client = client

    def analyze(self, topic: str, faq: DiscoveryFAQ, context_history: str) -> DiscoveryInsight:
        """Step 1: Perform adversarial analysis of a probe."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_iteration_prompt(topic, faq.question, faq.rationale, context_history),
            response_format=DiscoveryInsight
        )
        return self.client.generate_text(model_input)

    def check_novelty(self, topic: str, analysis: str) -> DiscoveryCheck:
        """Step 2: Adversarial Novelty Gate."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_discovery_check_prompt(topic, analysis),
            response_format=DiscoveryCheck
        )
        return self.client.generate_text(model_input)

    def verify(self, topic: str, insight: DiscoveryInsight) -> VerificationResult:
        """Step 3: Adversarial Skeptic Verifier."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_verification_prompt(topic, insight.analysis, insight.evidence),
            response_format=VerificationResult
        )
        return self.client.generate_text(model_input)

    def summarize(self, topic: str, analysis: str) -> str:
        """Step 4: Contextual Distillation."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_summary_prompt(topic, analysis),
            response_format=SummaryResponse
        )
        try:
            result = self.client.generate_text(model_input)
            return result.summary
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to summarize: {e}")
            return analysis[:200] + "..."
