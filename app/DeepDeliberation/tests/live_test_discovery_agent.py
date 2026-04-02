"""
live_test_discovery_agent.py - Live tests for DiscoveryAgent using real LLM.
"""

import unittest
import os
from DeepDeliberation.noagentic.deep_deliberation_agents import DiscoveryAgent
from DeepDeliberation.noagentic.deep_deliberation_models import DiscoveryFAQ
from lite import LiteClient, ModelConfig

class LiveTestDiscoveryAgent(unittest.TestCase):
    def setUp(self):
        self.model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3")
        self.model_config = ModelConfig(model=self.model, temperature=0.7)
        self.client = LiteClient(model_config=self.model_config)
        self.agent = DiscoveryAgent(self.client)
        self.topic = "The physics of black holes"

    def test_live_analyze(self):
        """Test DiscoveryAgent.analyze with real LLM."""
        faq = DiscoveryFAQ(
            question="How does Hawking radiation affect black hole evaporation?",
            rationale="To understand the long-term lifecycle of a black hole."
        )
        insight = self.agent.analyze(self.topic, faq, "Previous context: Black holes have mass and charge.")
        
        self.assertTrue(len(insight.analysis) > 50)
        self.assertTrue(len(insight.evidence) > 0)
        self.assertIsNotNone(insight.new_discovery_faq)
        print(f"\nLive Analysis: {insight.analysis[:100]}...")

    def test_live_check_novelty(self):
        """Test DiscoveryAgent.check_novelty with real LLM."""
        analysis = "Hawking radiation is predicted to release energy, reducing the mass of the black hole over time."
        check = self.agent.check_novelty(self.topic, analysis)
        
        self.assertIsInstance(check.is_novel, bool)
        self.assertGreaterEqual(check.discovery_score, 0)
        self.assertLessEqual(check.discovery_score, 10)
        print(f"\nLive Novelty Check: score={check.discovery_score}, is_novel={check.is_novel}")

    def test_live_verify(self):
        """Test DiscoveryAgent.verify with real LLM."""
        from DeepDeliberation.noagentic.deep_deliberation_models import DiscoveryInsight
        insight = DiscoveryInsight(
            analysis="Hawking radiation causes black holes to lose mass.",
            evidence=["Hawking, S. W. (1974). Black hole explosions?. Nature, 248(5443), 30-31."],
            new_discovery_faq=DiscoveryFAQ(question="What happens at the end?", rationale="Curiosity")
        )
        verification = self.agent.verify(self.topic, insight)
        
        self.assertIsInstance(verification.is_verified, bool)
        self.assertGreaterEqual(verification.credibility_score, 0)
        self.assertLessEqual(verification.credibility_score, 10)
        print(f"\nLive Verification: score={verification.credibility_score}, is_verified={verification.is_verified}")

    def test_live_summarize(self):
        """Test DiscoveryAgent.summarize with real LLM."""
        analysis = "A detailed analysis of how quantum fluctuations at the event horizon lead to the emission of particles."
        summary = self.agent.summarize(self.topic, analysis)
        
        self.assertTrue(len(summary) > 0)
        self.assertTrue(len(summary) < len(analysis) or "API error" in summary)
        print(f"\nLive Summary: {summary}")

if __name__ == "__main__":
    unittest.main()
