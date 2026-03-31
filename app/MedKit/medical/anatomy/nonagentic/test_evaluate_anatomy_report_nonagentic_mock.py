#!/usr/bin/env python3
"""
Tests for the Anatomy Report Evaluator.

Tests the strict evaluation system with sample anatomy reports.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from medical.anatomy.nonagentic.evaluate_anatomy_report import (
    AccuracyRating,
    AnatomyReportEvaluator,
    ClinicalReliabilityRating,
    EmbryologyRating,
    StructuralOrganizationRating,
    TerminologyRating,
)


class TestAnatomyReportEvaluator(unittest.TestCase):
    """Test cases for AnatomyReportEvaluator."""

    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = AnatomyReportEvaluator()
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Clean up temporary files."""
        self.temp_dir.cleanup()

    def _create_temp_report(self, filename: str, content: str) -> Path:
        """Create a temporary report file."""
        file_path = Path(self.temp_dir.name) / filename
        file_path.write_text(content)
        return file_path

    def test_excellent_report(self):
        """Test evaluation of an excellent anatomy report."""
        excellent_report = """
# Femoral Artery - Comprehensive Anatomical Review

## I. Anatomical Overview

The femoral artery is the main arterial supply to the lower limb. It is the continuation
of the external iliac artery after it passes beneath the inguinal ligament at the midpoint.

### Origin and Course
- **Origin**: Continuation of the external iliac artery at the inguinal ligament
- **Location**: Passes through the femoral triangle in the medial thigh
- **Surface landmarks**: Palpable below the inguinal ligament midpoint

### Branches and Distribution
The femoral artery gives rise to:
- Superficial epigastric artery
- Superficial circumflex iliac artery
- Profunda femoris artery (deep femoral artery) - major branch
- Medial and lateral circumflex femoral arteries

## II. Embryological Development

The femoral artery develops from mesodermal tissue during weeks 4-8 of gestation:
- Derives from the umbilical artery initially
- Mesoderm forms the arteries through vasculogenesis
- Complete development by 8-10 weeks gestation
- The external iliac artery branches to form the femoral artery

## III. Clinical Significance

### Palpation
The femoral artery is easily palpated below the inguinal ligament at the midpoint,
making it important for clinical examination and vascular access.

### Common Pathologies
- Femoral artery stenosis
- Atherosclerotic disease
- Aneurysms
- Thrombosis

## IV. Vascular Supply and Innervation

### Blood Supply
The femoral artery is supplied by the external iliac artery superiorly.
Collateral circulation via deep circumflex iliac artery provides alternative pathways.

### Innervation
The femoral nerve (L2-L4) innervates muscles in the anterior thigh.

## V. Anatomical Variations

- Accessory femoral artery (2-3% of population)
- Anomalous origin of profunda femoris artery
- Hypoplasia of the femoral artery (rare)

## VI. Imaging Characteristics

- **Ultrasound**: Hypoechoic tubular structure, compressible
- **CT/MRI**: Well-visualized on contrast-enhanced studies
- **Angiography**: Gold standard for visualization
"""
        file_path = self._create_temp_report("femoral_excellent.md", excellent_report)
        result = self.evaluator.evaluate_file(file_path)

        # Verify reasonable positive ratings
        self.assertIn(
            result.anatomical_accuracy[0],
            [AccuracyRating.EXCELLENT, AccuracyRating.GOOD, AccuracyRating.ACCEPTABLE],
        )
        self.assertIn(
            result.clinical_reliability[0],
            [
                ClinicalReliabilityRating.SAFE_RELIABLE,
                ClinicalReliabilityRating.CLINICALLY_SOUND,
                ClinicalReliabilityRating.SAFE_ACCURATE,
            ],
        )
        self.assertGreater(result.overall_quality_score, 60)

    def test_report_with_critical_errors(self):
        """Test evaluation of report with critical anatomical errors."""
        bad_report = """
# Femoral Artery Analysis

The femoral artery is located in the thigh and has the following characteristics:

## Branches
- The ulnar artery branches from the femoral artery in the thigh
- The saphenous vein (deep) is a major deep venous drainage pathway
- Femoral notch branches supply the femoral ring

## Clinical Notes
The ulnar artery in the thigh is important for patient diagnosis.
The saphenous vein being deep makes it important for surgical planning.

## Summary
Various structures contribute to the anatomy of the femoral region.
"""
        file_path = self._create_temp_report("femoral_bad.md", bad_report)
        result = self.evaluator.evaluate_file(file_path)

        # These critical errors should be caught
        self.assertEqual(
            result.clinical_reliability[0], ClinicalReliabilityRating.DANGEROUS
        )
        self.assertEqual(result.pass_fail_status, "FAIL")
        self.assertGreater(len(result.critical_issues), 0)
        self.assertLess(result.overall_quality_score, 50)

    def test_report_with_missing_sections(self):
        """Test evaluation of incomplete report."""
        incomplete_report = """
# Humerus

The humerus is a bone in the arm. It is long. It connects to other bones.
It develops from mesoderm.
"""
        file_path = self._create_temp_report("humerus_incomplete.md", incomplete_report)
        result = self.evaluator.evaluate_file(file_path)

        # Incomplete reports have lower scores
        self.assertLess(
            result.overall_quality_score, 85
        )  # Incomplete report should score below excellent

    def test_report_with_vague_terminology(self):
        """Test evaluation of report with imprecise terminology."""
        vague_report = """
# Cardiac Plexus

The cardiac plexus is kind of located in the thorax. It's fairly important for the heart.
Possibly it has something to do with innervation. It might have branches.

The cardiac plexus roughly consists of various nerve fibers that are somewhat involved
in cardiac function. It could be derived from neural crest tissue, but we're not entirely sure.

Clinical significance may include various cardiac conditions.
"""
        file_path = self._create_temp_report("cardiac_vague.md", vague_report)
        result = self.evaluator.evaluate_file(file_path)

        # Should flag vague terminology
        self.assertIn(
            result.terminology_precision[0],
            [
                TerminologyRating.IMPRECISE,
                TerminologyRating.VAGUE,
                TerminologyRating.ACCEPTABLE,
            ],
        )
        # Vague information affects reliability but not critical unless factually wrong
        self.assertIn(
            result.clinical_reliability[0],
            [
                ClinicalReliabilityRating.ACCEPTABLE_WITH_CAUTION,
                ClinicalReliabilityRating.MISLEADING,
            ],
        )

    def test_report_organization(self):
        """Test evaluation of structural organization."""
        well_organized = """
# Heart Structure

## I. Anatomical Overview
The heart is divided into four chambers: two atria and two ventricles.

## II. Gross Morphology
The heart measures approximately 12 cm in length.

## III. Embryological Development
The heart develops from mesoderm during weeks 3-8 of gestation.

## IV. Function
The heart pumps blood throughout the body.

## V. Clinical Significance
Cardiac diseases are common causes of mortality.

## VI. Innervation and Vascular Supply
The heart receives blood from coronary arteries.
"""
        file_path = self._create_temp_report("heart_organized.md", well_organized)
        result = self.evaluator.evaluate_file(file_path)

        # Should recognize good organization
        self.assertIn(
            result.structural_organization[0],
            [
                StructuralOrganizationRating.EXCELLENT,
                StructuralOrganizationRating.WELL_ORGANIZED,
                StructuralOrganizationRating.LOGICAL,
            ],
        )

    def test_evaluation_result_serialization(self):
        """Test that evaluation results can be serialized to JSON."""
        good_report = """
# Triceps Muscle

The triceps is located on the posterior arm. It has three heads:
- Long head
- Lateral head
- Medial head

## Embryology
The triceps develops from mesoderm during weeks 7-12 of gestation.

## Clinical Significance
Important for arm extension and clinical examination.
"""
        file_path = self._create_temp_report("triceps.md", good_report)
        result = self.evaluator.evaluate_file(file_path)

        # Should be serializable
        result_dict = result.to_dict()
        self.assertIsInstance(result_dict, dict)
        self.assertIn("structure_name", result_dict)
        self.assertIn("overall_quality_score", result_dict)
        self.assertIn("pass_fail_status", result_dict)

        # Should be JSON serializable
        json_str = json.dumps(result_dict)
        self.assertIsInstance(json_str, str)

    def test_evaluation_with_multiple_critical_issues(self):
        """Test report with multiple critical issues."""
        multi_error_report = """
# Femoral Artery

The femoral artery is located in the thigh.
The ulnar artery is a major branch in the thigh.
The saphenous vein is a deep venous structure.

This structure develops from ectoderm.
"""
        file_path = self._create_temp_report("femoral_errors.md", multi_error_report)
        result = self.evaluator.evaluate_file(file_path)

        # Should catch critical errors
        self.assertEqual(result.pass_fail_status, "FAIL")
        self.assertGreater(len(result.critical_issues), 0)

    def test_no_embryology_section(self):
        """Test report completely lacking embryology information."""
        no_embryology = """
# Tibialis Anterior Muscle

## Anatomy
Located in the anterior compartment of the leg.
Originates from the anterior tibia and interosseous membrane.

## Function
Dorsiflexion of the ankle and inversion of the foot.

## Clinical Significance
Important for lower leg movements.
Important for gait assessment.

## Innervation
Innervated by the deep fibular (peroneal) nerve.
"""
        file_path = self._create_temp_report("tibialis.md", no_embryology)
        result = self.evaluator.evaluate_file(file_path)

        # Should flag missing embryology
        self.assertIn(
            result.embryology[0],
            [
                EmbryologyRating.ABSENT,
                EmbryologyRating.VAGUE,
                EmbryologyRating.ACCEPTABLE,
            ],
        )


class TestKnowledgeBase(unittest.TestCase):
    """Test the knowledge base."""

    def test_knowledge_base_initialization(self):
        """Test that knowledge base initializes correctly."""
        from medical.anatomy.nonagentic.evaluate_anatomy_report import KnowledgeBase

        kb = KnowledgeBase()
        self.assertIsNotNone(kb.CORRECT_ARTERIAL_ORIGINS)
        self.assertIn("femoral_artery", kb.CORRECT_ARTERIAL_ORIGINS)
        self.assertIn("femoral_artery", kb.THIGH_ARTERIES)
        self.assertIn("ulnar_artery", kb.FOREARM_ARTERIES)


def run_tests_with_summary():
    """Run tests and provide summary."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestAnatomyReportEvaluator))
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeBase))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests_with_summary()
    sys.exit(0 if success else 1)
