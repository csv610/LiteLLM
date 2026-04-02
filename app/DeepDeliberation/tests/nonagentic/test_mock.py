"""
Mock tests for DeepDeliberation class
"""

import unittest
import os
import sys
import json
from pathlib import Path
from unittest.mock import Mock, patch

# Add project root and app directory to sys.path
root = Path(__file__).resolve().parent.parent.parent.parent
app_root = root / "app"
for path in [str(root), str(app_root)]:
    if path not in sys.path:
        sys.path.insert(0, path)

from lite.config import ModelConfig
from DeepDeliberation.nonagentic.deep_deliberation import DeepDeliberation
from DeepDeliberation.nonagentic.deep_deliberation_models import (
    InitialKnowledgeMap,
    DiscoveryFAQ,
    DiscoveryInsight,
    DiscoveryCheck,
    VerificationResult,
    KnowledgeSynthesis,
    SummaryResponse,
)


class TestDeepDeliberationMock(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.model_config = ModelConfig(model="test_model", temperature=0.3)

        # Create mock responses for the LiteClient
        self.mock_initial_map = InitialKnowledgeMap(
            topic="Test Topic",
            core_pillars=["Pillar 1", "Pillar 2"],
            discovery_faqs=[
                DiscoveryFAQ(question="What is X?", rationale="To understand X"),
                DiscoveryFAQ(question="How does Y work?", rationale="To understand Y"),
            ],
        )

        self.mock_insight = DiscoveryInsight(
            analysis="This is a test analysis",
            evidence=["This is test evidence"],
            new_discovery_faq=DiscoveryFAQ(
                question="Follow-up question?", rationale="To explore further"
            ),
        )

        self.mock_check = DiscoveryCheck(
            is_novel=True, discovery_score=8, reasoning="Highly novel concept"
        )

        self.mock_verification = VerificationResult(
            is_verified=True, credibility_score=9, critique="Well-supported argument"
        )

        self.mock_summary = SummaryResponse(summary="This is a test summary")

        self.mock_synthesis = KnowledgeSynthesis(
            topic="Test Topic",
            executive_summary="High-level synthesis",
            hidden_connections=["Connection 1"],
            research_frontiers=["Frontier 1"],
        )

    @patch("DeepDeliberation.nonagentic.deep_deliberation.LiteClient")
    @patch("DeepDeliberation.nonagentic.deep_deliberation.MissionArchive")
    def test_run_method_with_mocks(self, mock_archive_class, mock_liteclient_class):
        """Test the run method with all dependencies mocked."""
        # Set up mocks
        mock_liteclient_instance = Mock()
        mock_liteclient_class.return_value = mock_liteclient_instance

        # Configure the LiteClient mock to return our predefined responses
        mock_liteclient_instance.generate_text.side_effect = [
            self.mock_initial_map,  # Wave 0: Initial map
            self.mock_summary,      # Wave 0: Summarize base
            self.mock_insight,      # Probe 1: Analyze
            self.mock_check,        # Probe 1: Novelty check
            self.mock_verification, # Probe 1: Verification
            self.mock_summary,      # Probe 1: Summarize
            self.mock_insight,      # Probe 2: Analyze
            self.mock_check,        # Probe 2: Novelty check
            self.mock_verification, # Probe 2: Verification
            self.mock_summary,      # Probe 2: Summarize
            self.mock_synthesis,    # Final synthesis
        ]

        mock_archive_instance = Mock()
        mock_archive_class.return_value = mock_archive_instance

        # Create the DeepDeliberation instance
        engine = DeepDeliberation(self.model_config)

        # Run the method under test
        result = engine.run(
            topic="Test Topic", num_rounds=1, num_faqs=2, output_path="/tmp/test_output"
        )

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result, self.mock_synthesis)

        # Verify LiteClient was instantiated with correct config
        mock_liteclient_class.assert_called_once_with(model_config=self.model_config)

        # Verify MissionArchive was instantiated
        mock_archive_class.assert_called_once_with("Test Topic", "/tmp/test_output")

        # Verify generate_text was called the expected number of times
        # 1 for initial map + 1 for base summary + (num_rounds * num_faqs * 4) for the probe cycle + 1 for synthesis
        expected_calls = 1 + 1 + (1 * 2 * 4) + 1  # 11 calls
        self.assertEqual(
            mock_liteclient_instance.generate_text.call_count, expected_calls
        )

        # Verify archive methods were called
        self.assertTrue(mock_archive_instance.record_step.called)
        self.assertTrue(mock_archive_instance.set_final_map.called)

    @patch("DeepDeliberation.nonagentic.deep_deliberation.LiteClient")
    @patch("DeepDeliberation.nonagentic.deep_deliberation.MissionArchive")
    def test_run_method_handles_rejected_probes(
        self, mock_archive_class, mock_liteclient_class
    ):
        """Test that the run method properly handles rejected probes."""
        # Set up mocks
        mock_liteclient_instance = Mock()
        mock_liteclient_class.return_value = mock_liteclient_instance

        # Create a rejected check response
        mock_rejected_check = DiscoveryCheck(
            is_novel=False, discovery_score=2, reasoning="Not novel enough"
        )

        # Configure the LiteClient mock responses
        mock_liteclient_instance.generate_text.side_effect = [
            self.mock_initial_map,  # Wave 0: Initial map
            self.mock_summary,      # Wave 0: Summarize base
            self.mock_insight,      # Probe 1: Analysis for first probe
            mock_rejected_check,    # Probe 1: Novelty check (rejected)
            self.mock_insight,      # Probe 2: Analysis for second probe
            self.mock_check,        # Probe 2: Novelty check (accepted)
            self.mock_verification, # Probe 2: Verification
            self.mock_summary,      # Probe 2: Summarize
            self.mock_synthesis,    # Final synthesis
        ]

        mock_archive_instance = Mock()
        mock_archive_class.return_value = mock_archive_instance

        # Create the DeepDeliberation instance
        engine = DeepDeliberation(self.model_config)

        # Run with 1 round (default)
        result = engine.run(
            topic="Test Topic", num_rounds=1, num_faqs=2, output_path="/tmp/test_output"
        )

        # Should still succeed and return synthesis
        self.assertIsNotNone(result)
        self.assertEqual(result, self.mock_synthesis)

        # Should have called generate_text 9 times:
        # 1 initial + 1 base summary + (probe1: analysis+check) + (probe2: analysis+check+verification+summary) + 1 synthesis
        expected_calls = 1 + 1 + 2 + 4 + 1  # 9 calls
        self.assertEqual(
            mock_liteclient_instance.generate_text.call_count, expected_calls
        )


if __name__ == "__main__":
    unittest.main()
