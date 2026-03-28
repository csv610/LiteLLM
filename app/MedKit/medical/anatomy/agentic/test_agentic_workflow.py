#!/usr/bin/env python3
"""
Mock tests for the Agentic Anatomy Workflow.
Verifies the interaction between Generator and Evaluator.
"""

import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
import sys

# Add the project root to sys.path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from medical.anatomy.agentic.medical_anatomy_agentic_cli import AgenticAnatomyWorkflow
from medical.anatomy.agentic.evaluate_anatomy_report import AnatomyEvaluationResult, AccuracyRating, TerminologyRating, EmbryologyRating, ClinicalReliabilityRating, StructuralOrganizationRating, ReadabilityRating
from medical.anatomy.agentic.medical_anatomy_models import FactCheckModel, FactClaimModel

class TestAgenticAnatomyWorkflow(unittest.TestCase):
    """Test cases for the AgenticAnatomyWorkflow class."""

    def setUp(self):
        """Set up test fixtures."""
        self.output_dir = Path("test_output")
        # We'll mock the internal components in the tests
        with patch('medical.anatomy.agentic.medical_anatomy_agentic_cli.MedicalAnatomyGenerator'), \
             patch('medical.anatomy.agentic.medical_anatomy_agentic_cli.AnatomyReportEvaluator'):
            self.workflow = AgenticAnatomyWorkflow(
                generator_model="mock-gen",
                evaluator_model="mock-eval",
                output_dir=self.output_dir
            )

    @patch('medical.anatomy.agentic.medical_anatomy_agentic_cli.Path.mkdir')
    def test_run_workflow_success(self, mock_mkdir):
        """Test a successful generation and evaluation run."""
        body_part = "Test Structure"
        
        # Mock Generator
        mock_gen_result = MagicMock()
        self.workflow.generator.generate_text.return_value = mock_gen_result
        self.workflow.generator.save.return_value = Path("test_output/test.md")
        
        # Mock Evaluator
        mock_eval_result = AnatomyEvaluationResult(
            structure_name=body_part,
            anatomical_accuracy=(AccuracyRating.EXCELLENT, []),
            terminology_precision=(TerminologyRating.ACCURATE, []),
            embryology=(EmbryologyRating.CORRECT, []),
            clinical_reliability=(ClinicalReliabilityRating.SAFE_RELIABLE, []),
            structural_organization=(StructuralOrganizationRating.EXCELLENT, []),
            general_accessibility=(ReadabilityRating.EXCELLENT, []),
            overall_quality_score=100.0,
            pass_fail_status="PASS",
            critical_issues=[],
            recommendations=[]
        )
        self.workflow.evaluator.evaluate_file.return_value = mock_eval_result
        
        # Run workflow
        result = self.workflow.run_workflow(body_part)
        
        # Assertions
        self.workflow.generator.generate_text.assert_called_once_with(body_part, structured=False)
        self.workflow.evaluator.evaluate_file.assert_called_once()
        self.assertEqual(result.pass_fail_status, "PASS")
        self.assertEqual(result.overall_quality_score, 100.0)

    @patch('medical.anatomy.agentic.medical_anatomy_agentic_cli.Path.mkdir')
    def test_run_workflow_with_fact_check(self, mock_mkdir):
        """Test workflow with fact-checking step."""
        body_part = "Radial Artery"
        
        # Mock Generator
        mock_gen_result = MagicMock()
        mock_gen_result.markdown = "SECTION 1: Technical info --- SECTION 2: Layperson info"
        self.workflow.generator.generate_text.return_value = mock_gen_result
        self.workflow.generator.save.return_value = Path("test_output/radial.md")
        
        # Mock Fact-Checker
        mock_fact_check = FactCheckModel(
            claims=[FactClaimModel(claim="Claim 1", category="Origin", status="Verified", correction=None, evidence="Evidence 1")],
            summary="All clear",
            accuracy_score=100.0
        )
        self.workflow._run_fact_checker = MagicMock(return_value=mock_fact_check)
        
        # Mock Evaluator
        mock_eval_result = AnatomyEvaluationResult(
            structure_name=body_part,
            anatomical_accuracy=(AccuracyRating.EXCELLENT, []),
            terminology_precision=(TerminologyRating.ACCURATE, []),
            embryology=(EmbryologyRating.CORRECT, []),
            clinical_reliability=(ClinicalReliabilityRating.SAFE_RELIABLE, []),
            structural_organization=(StructuralOrganizationRating.EXCELLENT, []),
            general_accessibility=(ReadabilityRating.EXCELLENT, []),
            overall_quality_score=100.0,
            pass_fail_status="PASS",
            critical_issues=[],
            recommendations=[]
        )
        self.workflow.evaluator.evaluate_file.return_value = mock_eval_result
        
        # Run workflow
        result = self.workflow.run_workflow(body_part)
        
        # Assertions
        self.workflow._run_fact_checker.assert_called_once()
        self.assertEqual(result.pass_fail_status, "PASS")

    def test_run_workflow_generation_failure(self):
        """Test workflow when generation fails."""
        body_part = "Test Structure"
        self.workflow.generator.generate_text.side_effect = Exception("Generation error")
        
        result = self.workflow.run_workflow(body_part)
        
        self.assertIsNone(result)
        self.workflow.evaluator.evaluate_file.assert_not_called()

if __name__ == "__main__":
    unittest.main()
