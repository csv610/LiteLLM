import unittest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from drug_drug_interaction import DrugDrugOrchestrator
from drug_drug_interaction_prompts import DrugDrugInput
from drug_drug_interaction_models import (
    DrugInteractionDetailsModel,
    PatientFriendlySummaryModel,
    DrugInteractionSeverity,
    ConfidenceLevel,
    DataSourceType,
    TriageResultModel,
    ComplianceInfoModel
)
from lite.config import ModelConfig

class TestAsyncDrugDrugOrchestration(unittest.TestCase):
    def setUp(self):
        self.model_config = ModelConfig(model="mock-model")
        self.orchestrator = DrugDrugOrchestrator(self.model_config)
        self.user_input = DrugDrugInput(
            medicine1="Warfarin",
            medicine2="Aspirin",
            age=65
        )

    def run_async(self, coro):
        """Helper to run async coroutines in sync test."""
        return asyncio.run(coro)

    @patch("drug_drug_agents.TriageAgent.run_async", new_callable=AsyncMock)
    def test_triage_no_interaction(self, mock_triage):
        """Verify that orchestration stops if triage says no interaction."""
        mock_triage.return_value = TriageResultModel(
            interaction_exists=False,
            initial_reasoning="No clinically significant interaction expected between Vitamin C and Water."
        )
        
        result = self.run_async(self.orchestrator.orchestrate_async(self.user_input))
        
        self.assertFalse(result.data_availability.data_available)
        self.assertEqual(result.technical_summary, "No clinically significant interaction expected between Vitamin C and Water.")
        self.assertIsNone(result.interaction_details)
        print("✓ Triage 'No Interaction' Test Passed.")

    @patch("drug_drug_agents.TriageAgent.run_async", new_callable=AsyncMock)
    @patch("drug_drug_agents.PharmacologyAgent.run_async", new_callable=AsyncMock)
    @patch("drug_drug_agents.RiskAssessmentAgent.run_async", new_callable=AsyncMock)
    @patch("drug_drug_agents.ManagementAgent.run_async", new_callable=AsyncMock)
    @patch("drug_drug_agents.PatientEducationAgent.run_async", new_callable=AsyncMock)
    @patch("drug_drug_agents.SearchAgent.run_async", new_callable=AsyncMock)
    @patch("drug_drug_agents.ComplianceAgent.run_async", new_callable=AsyncMock)
    def test_full_orchestration_flow(
        self, mock_compliance, mock_search, mock_patient, mock_management, mock_risk, mock_pharma, mock_triage
    ):
        """Verify full parallel orchestration and consolidation with triage and compliance."""
        
        # 1. Triage exists
        mock_triage.return_value = TriageResultModel(
            interaction_exists=True,
            initial_reasoning="High-risk combination detected."
        )

        # 2. Expert agents
        mock_pharma.return_value = DrugInteractionDetailsModel(
            drug1_name="Warfarin", drug2_name="Aspirin",
            severity_level=DrugInteractionSeverity.SIGNIFICANT,
            mechanism_of_interaction="Synergistic inhibition of hemostasis.",
            clinical_effects="Increased bleeding risk.",
            management_recommendations="", alternative_medicines="",
            confidence_level=ConfidenceLevel.HIGH, data_source_type=DataSourceType.CLINICAL_STUDIES
        )
        
        mock_risk.return_value = DrugInteractionDetailsModel(
            drug1_name="Warfarin", drug2_name="Aspirin",
            severity_level=DrugInteractionSeverity.SIGNIFICANT,
            mechanism_of_interaction="", clinical_effects="",
            management_recommendations="", alternative_medicines="",
            confidence_level=ConfidenceLevel.HIGH, data_source_type=DataSourceType.CLINICAL_STUDIES,
            technical_summary="High risk of major hemorrhage."
        )

        mock_management.return_value = DrugInteractionDetailsModel(
            drug1_name="Warfarin", drug2_name="Aspirin",
            severity_level=DrugInteractionSeverity.SIGNIFICANT,
            mechanism_of_interaction="", clinical_effects="",
            management_recommendations="Monitor INR closely.",
            alternative_medicines="Acetaminophen.",
            confidence_level=ConfidenceLevel.HIGH, data_source_type=DataSourceType.CLINICAL_STUDIES
        )

        mock_patient.return_value = PatientFriendlySummaryModel(
            simple_explanation="Both medicines thin your blood.",
            what_patient_should_do="Inform your doctor.",
            warning_signs="Bruising.",
            when_to_seek_help="Seek help for heavy bleeding."
        )

        mock_search.return_value = DrugInteractionDetailsModel(
            drug1_name="Warfarin", drug2_name="Aspirin",
            severity_level=DrugInteractionSeverity.SIGNIFICANT,
            mechanism_of_interaction="", clinical_effects="",
            management_recommendations="", alternative_medicines="",
            confidence_level=ConfidenceLevel.HIGH, data_source_type=DataSourceType.REGULATORY_DATA,
            references="FDA Label"
        )

        # 3. Compliance Review
        mock_compliance.return_value = ComplianceInfoModel(
            compliance_passed=True,
            safety_warnings="PRIORITY: Bleeding risk",
            compliance_notes="Analysis meets medical standards."
        )

        # Execute
        result = self.run_async(self.orchestrator.orchestrate_async(self.user_input))

        # Verify Triage was called
        mock_triage.assert_called_once()
        
        # Verify Parallelism (Expert agents called before compliance)
        mock_pharma.assert_called_once()
        mock_risk.assert_called_once()
        
        # Verify Compliance received the draft context
        args, kwargs = mock_compliance.call_args
        self.assertIn("DRAFT REPORT", kwargs['custom_user_prompt'])
        self.assertIn("SEVERITY: DrugInteractionSeverity.SIGNIFICANT", kwargs['custom_user_prompt'])

        # Verify Consolidation
        self.assertTrue(result.data_availability.data_available)
        self.assertTrue(result.compliance_info.compliance_passed)
        self.assertEqual(result.compliance_info.safety_warnings, "PRIORITY: Bleeding risk")
        
        # Verify Audit Log
        self.assertIsNotNone(result.audit_log)
        self.assertEqual(result.audit_log.pharmacology_raw.mechanism_of_interaction, "Synergistic inhibition of hemostasis.")
        self.assertEqual(result.audit_log.compliance_raw.compliance_notes, "Analysis meets medical standards.")

        print("✓ Full Async Orchestration & Audit Log Test Passed.")

if __name__ == "__main__":
    unittest.main()
