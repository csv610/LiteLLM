import unittest
from unittest.mock import MagicMock
from app.DeepDeliberation.deep_deliberation_agents import DiscoveryAgent
from app.DeepDeliberation.deep_deliberation_models import (
    DiscoveryFAQ, DiscoveryInsight, DiscoveryCheck, VerificationResult, SummaryResponse
)

class TestDiscoveryAgent(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.agent = DiscoveryAgent(self.mock_client)
        self.topic = "Quantum Computing"

    def test_analyze(self):
        faq = DiscoveryFAQ(question="What is entanglement?", rationale="Core concept")
        expected_insight = DiscoveryInsight(
            analysis="Analysis",
            evidence=["evidence1"],
            new_discovery_faq=DiscoveryFAQ(question="Next Q?", rationale="Next R")
        )
        self.mock_client.generate_text.return_value = expected_insight

        result = self.agent.analyze(self.topic, faq, "history")
        
        self.assertEqual(result, expected_insight)
        self.mock_client.generate_text.assert_called_once()

    def test_check_novelty(self):
        expected_check = DiscoveryCheck(is_novel=True, discovery_score=8, reasoning="Good")
        self.mock_client.generate_text.return_value = expected_check

        result = self.agent.check_novelty(self.topic, "analysis")
        
        self.assertEqual(result, expected_check)
        self.mock_client.generate_text.assert_called_once()

    def test_verify(self):
        insight = DiscoveryInsight(
            analysis="Analysis",
            evidence=["evidence1"],
            new_discovery_faq=DiscoveryFAQ(question="Next Q?", rationale="Next R")
        )
        expected_verification = VerificationResult(is_verified=True, credibility_score=9, critique="Solid")
        self.mock_client.generate_text.return_value = expected_verification

        result = self.agent.verify(self.topic, insight)
        
        self.assertEqual(result, expected_verification)
        self.mock_client.generate_text.assert_called_once()

    def test_summarize(self):
        expected_summary = SummaryResponse(summary="Short summary")
        self.mock_client.generate_text.return_value = expected_summary

        result = self.agent.summarize(self.topic, "analysis")
        
        self.assertEqual(result, "Short summary")
        self.mock_client.generate_text.assert_called_once()

    def test_summarize_failure(self):
        # Test the fallback logic in summarize
        self.mock_client.generate_text.side_effect = Exception("API error")
        
        analysis = "This is a very long analysis " * 20
        result = self.agent.summarize(self.topic, analysis)
        
        self.assertTrue(result.startswith("This is a very long analysis"))
        self.assertTrue(result.endswith("..."))

if __name__ == "__main__":
    unittest.main()
