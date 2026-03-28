import unittest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from similar_drugs import SimilarDrugsOrchestrator
from similar_drugs_models import (
    SimilarMedicinesResult,
    TriageResultModel,
    ComplianceInfoModel,
    SimilarityCategory,
    EfficacyComparison,
    SwitchingGuidance,
    SimilarMedicinesModel
)
from lite.config import ModelConfig

class TestSimilarDrugsOrchestration(unittest.TestCase):
    def setUp(self):
        self.model_config = ModelConfig(model="mock-model")
        self.orchestrator = SimilarDrugsOrchestrator(self.model_config)
        self.medicine_name = "Ibuprofen"
        self.context = "Patient age: 45 years."

    def run_async(self, coro):
        """Helper to run async coroutines in sync test."""
        return asyncio.run(coro)

    @patch("similar_drugs_agents.TriageAgent.run_async", new_callable=AsyncMock)
    @patch("similar_drugs_agents.ResearchAgent.run_async", new_callable=AsyncMock)
    @patch("similar_drugs_agents.ComplianceAgent.run_async", new_callable=AsyncMock)
    def test_full_orchestration_flow(
        self, mock_compliance, mock_research, mock_triage
    ):
        """Verify full orchestration and consolidation with triage and compliance."""
        
        # 1. Triage
        mock_triage.return_value = TriageResultModel(
            is_real_medicine=True,
            has_alternatives=True,
            initial_reasoning="Common NSAID with many alternatives.",
            suggested_focus_areas=["Naproxen", "Celecoxib"]
        )

        # 2. Research agent
        mock_research.return_value = SimilarMedicinesResult(
            original_medicine="Ibuprofen",
            original_active_ingredients="Ibuprofen",
            original_therapeutic_use="Analgesic/Antipyretic",
            total_similar_medicines_found=2,
            categorized_results=[],
            switching_guidance=SwitchingGuidance(
                switching_considerations="GI safety",
                transition_recommendations="Direct switch",
                monitoring_during_switch="Pain level",
                contraindications_for_switch="GI bleed"
            ),
            top_recommended="Naproxen",
            summary_analysis="Good alternatives available.",
            clinical_notes="None"
        )

        # 3. Compliance Review
        mock_compliance.return_value = ComplianceInfoModel(
            compliance_passed=True,
            safety_warnings=["Switching may cause GI issues"],
            disclaimers=["Consult a doctor"],
            compliance_notes="Analysis meets medical standards."
        )

        # Execute
        result = self.run_async(self.orchestrator.orchestrate_async(self.medicine_name, self.context))

        # Verify Triage was called
        mock_triage.assert_called_once()
        
        # Verify Research was called
        mock_research.assert_called_once()
        
        # Verify Compliance received the draft context
        args, kwargs = mock_compliance.call_args
        self.assertIn("DRAFT REPORT", kwargs['custom_user_prompt'])

        # Verify Consolidation
        self.assertTrue(result.compliance_info.compliance_passed)
        self.assertEqual(result.compliance_info.safety_warnings[0], "Switching may cause GI issues")
        
        # Verify Audit Log
        self.assertIsNotNone(result.audit_log)
        self.assertEqual(result.audit_log.triage_raw.is_real_medicine, True)
        self.assertEqual(result.audit_log.research_raw.original_medicine, "Ibuprofen")

        print("✓ Full Async Orchestration & Audit Log Test Passed.")

if __name__ == "__main__":
    unittest.main()
