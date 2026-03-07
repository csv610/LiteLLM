import unittest
from unittest.mock import MagicMock, patch
from deep_deliberation import DeepDeliberation
from deep_deliberation_models import (
    InitialKnowledgeMap, DiscoveryFAQ, DiscoveryInsight, DiscoveryCheck, 
    VerificationResult, KnowledgeSynthesis, SummaryResponse
)
from lite import ModelConfig

class TestDeepDeliberation(unittest.TestCase):
    def setUp(self):
        self.model_config = ModelConfig(model="test-model")
        with patch('deep_deliberation.LiteClient'), patch('deep_deliberation.DiscoveryAgent'):
            self.orchestrator = DeepDeliberation(self.model_config)
            self.orchestrator.client = MagicMock()
            self.orchestrator.agent = MagicMock()

    def test_execute_single_probe_success(self):
        topic = "topic"
        faq = DiscoveryFAQ(question="Q", rationale="R")
        
        insight = DiscoveryInsight(
            analysis="Analysis",
            evidence=["E"],
            new_discovery_faq=DiscoveryFAQ(question="Next Q", rationale="Next R")
        )
        check = DiscoveryCheck(is_novel=True, discovery_score=9, reasoning="Good")
        verification = VerificationResult(is_verified=True, credibility_score=9, critique="Solid")
        summary = "Summary"

        self.orchestrator.agent.analyze.return_value = insight
        self.orchestrator.agent.check_novelty.return_value = check
        self.orchestrator.agent.verify.return_value = verification
        self.orchestrator.agent.summarize.return_value = summary

        res = self.orchestrator._execute_single_probe(topic, faq, ["H"])

        self.assertEqual(res["insight"], insight)
        self.assertEqual(res["summary"], summary)
        self.assertNotIn("rejected", res)

    def test_execute_single_probe_novelty_fail(self):
        topic = "topic"
        faq = DiscoveryFAQ(question="Q", rationale="R")
        
        insight = DiscoveryInsight(
            analysis="Analysis",
            evidence=["E"],
            new_discovery_faq=DiscoveryFAQ(question="Next Q", rationale="Next R")
        )
        check = DiscoveryCheck(is_novel=False, discovery_score=2, reasoning="Old")

        self.orchestrator.agent.analyze.return_value = insight
        self.orchestrator.agent.check_novelty.return_value = check

        res = self.orchestrator._execute_single_probe(topic, faq, ["H"])

        self.assertTrue(res["rejected"])
        self.assertIn("Low Novelty", res["reason"])

    def test_run_integration(self):
        # Mocking the whole flow
        topic = "topic"
        
        # Wave 0 initialization
        initial_map = InitialKnowledgeMap(
            topic=topic,
            core_pillars=["P1"],
            discovery_faqs=[DiscoveryFAQ(question="Q1", rationale="R1")]
        )
        self.orchestrator.client.generate_text.side_effect = [
            initial_map, # Wave 0
            KnowledgeSynthesis( # Final synthesis
                topic=topic,
                executive_summary="Final Summary",
                hidden_connections=["C1"],
                research_frontiers=["F1"]
            )
        ]
        
        # Wave 1 execution
        insight = DiscoveryInsight(
            analysis="A1",
            evidence=["E1"],
            new_discovery_faq=DiscoveryFAQ(question="Q2", rationale="R2")
        )
        self.orchestrator.agent.analyze.return_value = insight
        self.orchestrator.agent.check_novelty.return_value = DiscoveryCheck(is_novel=True, discovery_score=9, reasoning="Good")
        self.orchestrator.agent.verify.return_value = VerificationResult(is_verified=True, credibility_score=9, critique="Solid")
        self.orchestrator.agent.summarize.return_value = "S1"

        with patch('deep_deliberation.MissionArchive') as mock_archive:
             res = self.orchestrator.run(topic, num_rounds=1, num_faqs=1)
             
             self.assertEqual(res.topic, topic)
             self.assertEqual(res.executive_summary, "Final Summary")
             self.orchestrator.client.generate_text.assert_called()

if __name__ == "__main__":
    unittest.main()
