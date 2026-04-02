"""
liteagents.py - Unified for anatomy
"""
from typing import List, Optional\nfrom lite.config import ModelConfig\nimport json\nfrom lite.logging_config import configure_logging\nimport sys\nfrom typing import Dict, List, Optional, Tuple\nfrom typing import Optional\nfrom tqdm import tqdm\nfrom pydantic import BaseModel\nimport unittest\nfrom lite.config import ModelConfig, ModelInput\nimport logging\nfrom pathlib import Path\nfrom unittest.mock import MagicMock, patch\nfrom app.MedKit.medical.anatomy.shared.models import *\nfrom lite.utils import save_model_response\nfrom enum import Enum\nfrom lite.lite_client import LiteClient\nimport argparse\nimport tempfile\n\n#!/usr/bin/env python3
"""
Tests for the Anatomy Report Evaluator.

Tests the strict evaluation system with sample anatomy reports.
"""


# Add the project root to sys.path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

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
        from medical.anatomy.agentic.evaluate_anatomy_report import KnowledgeBase

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

#!/usr/bin/env python3
"""
Strict Anatomy Report Evaluator.

This module evaluates anatomical reports against rigorous medical and scientific standards.
Zero tolerance for inaccuracies in clinical reliability and anatomical accuracy.
"""



# Add the project root to sys.path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


logger = logging.getLogger(__name__)


class AccuracyRating(Enum):
    """Anatomical accuracy ratings."""

    EXCELLENT = "✓ Excellent"
    GOOD = "✓ Good"
    ACCEPTABLE = "⚠️ Acceptable"
    SUPERFICIAL = "⚠️ Superficially organized but conceptually flawed"
    POOR = "❌ Poor"
    VERY_POOR = "❌ Very Poor"
    INCORRECT = "❌ Incorrect"
    UNSAFE = "❌ Unsafe"


class TerminologyRating(Enum):
    """Terminology precision ratings."""

    EXCELLENT = "✓ Excellent"
    ACCURATE = "✓ Accurate"
    ACCEPTABLE = "⚠️ Acceptable with minor issues"
    IMPRECISE = "⚠️ Imprecise terminology"
    POOR = "❌ Poor"
    VAGUE = "❌ Vague/Non-standard"
    INCORRECT = "❌ Incorrect terminology used"


class EmbryologyRating(Enum):
    """Embryology accuracy ratings."""

    CORRECT = "✓ Correct"
    ACCURATE = "✓ Accurate"
    ACCEPTABLE = "⚠️ Acceptable but incomplete"
    VAGUE = "⚠️ Vague or oversimplified"
    PARTIALLY_INCORRECT = "⚠️ Partially incorrect"
    INCORRECT = "❌ Incorrect"
    ABSENT = "❌ Absent or severely flawed"


class ClinicalReliabilityRating(Enum):
    """Clinical reliability ratings - ZERO TOLERANCE for unsafe info."""

    SAFE_RELIABLE = "✓ Safe and reliable"
    SAFE_ACCURATE = "✓ Safe and accurate"
    CLINICALLY_SOUND = "✓ Clinically sound"
    ACCEPTABLE_WITH_CAUTION = "⚠️ Acceptable with caution"
    MISLEADING = "⚠️ Misleading or potentially problematic"
    UNSAFE_CLINICAL = "❌ Unsafe for clinical use"
    CONTRADICTS_STANDARDS = "❌ Contradicts established clinical standards"
    DANGEROUS = "❌ Dangerous/High-risk information"


class StructuralOrganizationRating(Enum):
    """Structural organization ratings."""

    EXCELLENT = "✓ Excellent organization"
    WELL_ORGANIZED = "✓ Well-organized"
    LOGICAL = "✓ Logically structured"
    ACCEPTABLE = "⚠️ Acceptable but needs improvement"
    FLAWED = "⚠️ Superficially organized but conceptually flawed"
    POOR = "❌ Poor organization"
    INCOHERENT = "❌ Incoherent/Disorganized"


class ReadabilityRating(Enum):
    """Readability and patient education ratings."""

    EXCELLENT = "✓ Excellent clarity for laypeople"
    CLEAR = "✓ Clear and accessible"
    MODERATE = "⚠️ Moderate jargon used"
    TOO_TECHNICAL = "⚠️ Too technical for general audience"
    POOR = "❌ Poor clarity"
    INACCURATE_SIMPLIFICATION = "❌ Inaccurate simplification"


class AnatomyEvaluationResult(BaseModel):
    """Comprehensive evaluation result for an anatomy report."""

    structure_name: str
    anatomical_accuracy: Tuple[AccuracyRating, List[str]]
    terminology_precision: Tuple[TerminologyRating, List[str]]
    embryology: Tuple[EmbryologyRating, List[str]]
    clinical_reliability: Tuple[ClinicalReliabilityRating, List[str]]
    structural_organization: Tuple[StructuralOrganizationRating, List[str]]
    
    # Dual-stream additions
    general_accessibility: Tuple[ReadabilityRating, List[str]]

    overall_quality_score: float
    pass_fail_status: str  # "PASS", "FAIL", or "CONDITIONAL_PASS"
    critical_issues: List[str]
    recommendations: List[str]

    def to_dict(self) -> Dict:
        """Convert result to dictionary."""
        return {
            "structure_name": self.structure_name,
            "anatomical_accuracy": {
                "rating": self.anatomical_accuracy[0].value,
                "issues": self.anatomical_accuracy[1],
            },
            "terminology_precision": {
                "rating": self.terminology_precision[0].value,
                "issues": self.terminology_precision[1],
            },
            "embryology": {
                "rating": self.embryology[0].value,
                "issues": self.embryology[1],
            },
            "clinical_reliability": {
                "rating": self.clinical_reliability[0].value,
                "issues": self.clinical_reliability[1],
            },
            "structural_organization": {
                "rating": self.structural_organization[0].value,
                "issues": self.structural_organization[1],
            },
            "general_accessibility": {
                "rating": self.general_accessibility[0].value,
                "issues": self.general_accessibility[1],
            },
            "overall_quality_score": self.overall_quality_score,
            "pass_fail_status": self.pass_fail_status,
            "critical_issues": self.critical_issues,
            "recommendations": self.recommendations,
        }


class KnowledgeBase:
    """Knowledge base for anatomical validation."""

    # Anatomical structure validation rules
    CORRECT_ARTERIAL_ORIGINS = {
        "femoral_artery": ["external_iliac_artery"],
        "ulnar_artery": ["brachial_artery"],
        "radial_artery": ["brachial_artery"],
        "popliteal_artery": ["femoral_artery"],
        "anterior_tibial_artery": ["popliteal_artery"],
        "posterior_tibial_artery": ["popliteal_artery"],
    }

    # Regional artery branches (prevent misplacement)
    FOREARM_ARTERIES = {"ulnar_artery", "radial_artery", "anterior_interosseous_artery"}
    THIGH_ARTERIES = {
        "femoral_artery",
        "profunda_femoris_artery",
        "superficial_femoral_artery",
    }
    LEG_ARTERIES = {
        "popliteal_artery",
        "anterior_tibial_artery",
        "posterior_tibial_artery",
    }

    # Vein characteristics
    SUPERFICIAL_VEINS = {"saphenous_vein", "cephalic_vein", "basilic_vein"}
    DEEP_VEINS = {"femoral_vein", "popliteal_vein", "tibial_vein"}

    # Embryological origins (germ layers)
    MESODERM_DERIVATIVES = {
        "musculoskeletal": [
            "skeletal_muscle",
            "bone",
            "cartilage",
            "connective_tissue",
        ],
        "vascular": ["arteries", "veins", "lymphatics"],
        "blood": ["blood_cells", "blood_vessels"],
    }

    NEURAL_CREST_DERIVATIVES = {
        "peripheral_nerves",
        "sensory_neurons",
        "sympathetic_neurons",
        "cranial_nerve_ganglia",
    }

    # Common anatomical errors
    COMMON_ERRORS = {
        "ulnar_artery": {
            "error": "Mistakenly placing in thigh instead of forearm",
            "location": "Forearm (formed from brachial artery)",
            "severity": "CRITICAL",
        },
        "saphenous_vein": {
            "error": "Described as deep when it is superficial",
            "location": "Superficial (between skin and fascia)",
            "severity": "CRITICAL",
        },
        "radial_artery": {
            "error": "Mistakenly placing outside forearm",
            "location": "Forearm (formed from brachial artery)",
            "severity": "CRITICAL",
        },
    }


class AnatomyReportEvaluator:
    """Strict evaluator for anatomical reports."""

    def __init__(self, model: Optional[str] = None):
        self.model = model
        self.kb = KnowledgeBase()
        self.issues = []
        self.critical_issues = []
        self.client = None

        if model:
            config = ModelConfig(model=model, temperature=0.0)
            self.client = LiteClient(config)

        logger.debug(f"Initialized AnatomyReportEvaluator (model: {model})")

    def evaluate_file(self, file_path: Path) -> AnatomyEvaluationResult:
        """Evaluate an anatomy report file."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read file content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract structure name from filename or content
        structure_name = file_path.stem.replace("_", " ").title()

        if self.client:
            logger.info(f"Evaluating {structure_name} using LLM ({self.model})")
            return self._evaluate_with_llm(content, structure_name)
        else:
            logger.info(f"Evaluating {structure_name} using rule-based system")
            return self._evaluate_with_rules(content, structure_name)

    def _evaluate_with_rules(
        self, content: str, structure_name: str
    ) -> AnatomyEvaluationResult:
        """Evaluate an anatomy report using rule-based system."""
        # Reset issues
        self.issues = []
        self.critical_issues = []

        logger.debug(f"Evaluating anatomy report with rules for: {structure_name}")

        # Evaluate all dimensions
        accuracy = self._evaluate_anatomical_accuracy(content, structure_name)
        terminology = self._evaluate_terminology_precision(content, structure_name)
        embryology = self._evaluate_embryology(content, structure_name)
        clinical = self._evaluate_clinical_reliability(content, structure_name)
        organization = self._evaluate_structural_organization(content)
        accessibility = self._evaluate_general_accessibility(content)

        # Calculate overall score
        overall_score = self._calculate_overall_score(
            accuracy, terminology, embryology, clinical, organization, accessibility
        )

        # Determine pass/fail status
        pass_fail = self._determine_pass_fail(
            accuracy, terminology, embryology, clinical, organization, accessibility
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            accuracy, terminology, embryology, clinical, organization, accessibility
        )

        result = AnatomyEvaluationResult(
            structure_name=structure_name,
            anatomical_accuracy=accuracy,
            terminology_precision=terminology,
            embryology=embryology,
            clinical_reliability=clinical,
            structural_organization=organization,
            general_accessibility=accessibility,
            overall_quality_score=overall_score,
            pass_fail_status=pass_fail,
            critical_issues=self.critical_issues,
            recommendations=recommendations,
        )

        return result

    def _evaluate_with_llm(
        self, content: str, structure_name: str
    ) -> AnatomyEvaluationResult:
        """Evaluate an anatomy report using an LLM."""
        logger.debug(f"Evaluating anatomy report with LLM for: {structure_name}")

        system_prompt = """You are a Strict Anatomy Report Evaluator with zero tolerance for inaccuracies.
You must evaluate anatomical reports against rigorous medical and scientific standards.

Key Dimensions to Evaluate:
1. Anatomical Accuracy: Zero tolerance for incorrect placements or descriptions.
2. Terminology Precision: Must use standard Terminologia Anatomica.
3. Embryology: Must include germ layer origins and developmental timeline.
4. Clinical Reliability: Must be safe and accurate for clinical reference.
5. Structural Organization: Must be logically structured with clear sections.
6. General Accessibility: Check the plain English section for clarity and avoidance of jargon.

CRITICAL FAILURE CONDITIONS:
- Any anatomical inaccuracy (e.g., ulnar artery in thigh).
- Any clinical safety issue or dangerous misinformation.
- Contradictory anatomical statements.
- Inaccurate simplification in the layperson section that leads to medical misunderstanding.

Evaluation Ratings (USE THESE EXACT STRINGS):
Accuracy: "✓ Excellent", "✓ Good", "⚠️ Acceptable", "⚠️ Superficially organized but conceptually flawed", "❌ Poor", "❌ Very Poor", "❌ Incorrect", "❌ Unsafe"
Terminology: "✓ Excellent", "✓ Accurate", "⚠️ Acceptable with minor issues", "⚠️ Imprecise terminology", "❌ Poor", "❌ Vague/Non-standard", "❌ Incorrect terminology used"
Embryology: "✓ Correct", "✓ Accurate", "⚠️ Acceptable but incomplete", "⚠️ Vague or oversimplified", "⚠️ Partially incorrect", "❌ Incorrect", "❌ Absent or severely flawed"
Clinical: "✓ Safe and reliable", "✓ Safe and accurate", "✓ Clinically sound", "⚠️ Acceptable with caution", "⚠️ Misleading or potentially problematic", "❌ Unsafe for clinical use", "❌ Contradicts established clinical standards", "❌ Dangerous/High-risk information"
Organization: "✓ Excellent organization", "✓ Well-organized", "✓ Logically structured", "⚠️ Acceptable but needs improvement", "⚠️ Superficially organized but conceptually flawed", "❌ Poor organization", "❌ Incoherent/Disorganized"
Accessibility: "✓ Excellent clarity for laypeople", "✓ Clear and accessible", "⚠️ Moderate jargon used", "⚠️ Too technical for general audience", "❌ Poor clarity", "❌ Inaccurate simplification"

Output format MUST be a structured object matching AnatomyEvaluationResult:
- anatomical_accuracy: [Rating, Issues]
- terminology_precision: [Rating, Issues]
- embryology: [Rating, Issues]
- clinical_reliability: [Rating, Issues]
- structural_organization: [Rating, Issues]
- general_accessibility: [Rating, Issues]
- structure_name: Name of the structure (string).
- overall_quality_score: float (0-100).
- pass_fail_status: string ("PASS", "FAIL", or "CONDITIONAL_PASS").
- critical_issues: list of strings.
- recommendations: list of strings.
"""

        user_prompt = f"Evaluate the following anatomy report for '{structure_name}':\n\n{content}"

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=AnatomyEvaluationResult,
        )

        try:
            result_output = self.client.generate_text(model_input=model_input)
            if result_output:
                return result_output
            else:
                raise ValueError("LLM returned empty data")
        except Exception as e:
            logger.error(f"Error during LLM evaluation: {e}")
            raise

    def _evaluate_anatomical_accuracy(
        self, content: str, structure_name: str
    ) -> Tuple[AccuracyRating, List[str]]:
        """Evaluate anatomical accuracy with ZERO tolerance for errors."""
        issues = []
        severity_count = {"critical": 0, "major": 0, "minor": 0}

        # Check for common anatomical errors
        if "femoral" in structure_name.lower():
            # Check for incorrect artery placements
            if "ulnar_artery" in content.lower() and "thigh" in content.lower():
                issues.append(
                    "CRITICAL: Ulnar artery incorrectly placed in thigh (should be in forearm)"
                )
                severity_count["critical"] += 1
                self.critical_issues.append(
                    "Ulnar artery mislocalization in femoral artery report"
                )

            if "saphenous vein" in content.lower() and "deep" in content.lower():
                issues.append(
                    "CRITICAL: Saphenous vein described as deep (should be superficial)"
                )
                severity_count["critical"] += 1
                self.critical_issues.append("Saphenous vein mischaracterization")

        # Check for vague anatomical descriptions
        vague_terms = ["approximately", "roughly", "somewhat", "fairly", "kind of"]
        vague_count = sum(1 for term in vague_terms if f" {term} " in content.lower())
        if vague_count > 5:
            issues.append(
                f"Multiple vague anatomical descriptions detected ({vague_count} instances)"
            )
            severity_count["major"] += 1

        # Check for missing critical anatomical details

        # Determine overall rating
        if severity_count["critical"] > 0:
            rating = AccuracyRating.UNSAFE
            self.critical_issues.extend(issues)
        elif severity_count["major"] > 2:
            rating = AccuracyRating.VERY_POOR
        elif severity_count["major"] > 0:
            rating = AccuracyRating.POOR
        elif severity_count["minor"] > 3:
            rating = AccuracyRating.ACCEPTABLE
        else:
            rating = AccuracyRating.EXCELLENT

        logger.debug(f"Anatomical accuracy: {rating.value}")
        return (rating, issues)

    def _evaluate_terminology_precision(
        self, content: str, structure_name: str
    ) -> Tuple[TerminologyRating, List[str]]:
        """Evaluate terminology precision and correctness."""
        issues = []
        severity_count = {"critical": 0, "major": 0, "minor": 0}

        # Check for non-standard terminology
        non_standard_terms = {
            "femoral notch": "Should be 'femoral ring' or 'pectineal ligament'",
            "deep saphenous": "Should be 'great saphenous vein' or 'long saphenous vein'",
            "superficial epigastric": "Should be 'superficial epigastric artery'",
        }

        for wrong, correct in non_standard_terms.items():
            if wrong.lower() in content.lower():
                issues.append(f"Non-standard terminology: '{wrong}' → {correct}")
                severity_count["major"] += 1

        # Check for vague qualifiers that indicate imprecise language
        vague_qualifiers = [
            " kind of ",
            " fairly ",
            " possibly ",
            " might ",
            " roughly ",
            " somewhat ",
            " could be ",
            " not entirely sure",
        ]
        vague_count = sum(1 for q in vague_qualifiers if q in content.lower())
        if vague_count > 3:
            issues.append(
                f"Excessive vague qualifiers detected ({vague_count} instances)"
            )
            severity_count["major"] += 1

        # Check for anatomical position terminology
        position_terms = [
            "anterior",
            "posterior",
            "medial",
            "lateral",
            "superior",
            "inferior",
            "deep",
            "superficial",
        ]
        position_count = sum(1 for term in position_terms if term in content.lower())

        if position_count < 3:
            issues.append("Insufficient anatomical position terminology used")
            severity_count["minor"] += 1

        # Check for incorrect anatomical planes
        if "sagittal plane" in content.lower() or "coronal plane" in content.lower():
            pass  # Good usage of planes
        else:
            issues.append("Limited reference to anatomical planes")
            severity_count["minor"] += 1

        # Determine rating
        if severity_count["critical"] > 0:
            rating = TerminologyRating.INCORRECT
            self.critical_issues.extend(issues)
        elif severity_count["major"] > 2:
            rating = TerminologyRating.POOR
        elif severity_count["major"] > 0:
            rating = TerminologyRating.IMPRECISE
        elif severity_count["minor"] > 2:
            rating = TerminologyRating.ACCEPTABLE
        else:
            rating = TerminologyRating.ACCURATE

        logger.debug(f"Terminology precision: {rating.value}")
        return (rating, issues)

    def _evaluate_embryology(
        self, content: str, structure_name: str
    ) -> Tuple[EmbryologyRating, List[str]]:
        """Evaluate embryological information accuracy."""
        issues = []
        severity_count = {"critical": 0, "major": 0, "minor": 0}

        # Check if embryology section exists
        has_embryology = any(
            term in content.lower()
            for term in ["embryological", "embryology", "development", "origin", "germ"]
        )

        if not has_embryology:
            issues.append("Missing embryological information")
            severity_count["major"] += 1
        else:
            # Check for correct germ layer origins
            if (
                "femoral" in structure_name.lower()
                and "artery" in structure_name.lower()
            ):
                # Arteries come from mesoderm
                if "mesoderm" not in content.lower():
                    issues.append("Missing mesoderm origin for arterial structure")
                    severity_count["major"] += 1

            # Check for vague embryological statements
            vague_embryo = ["develops from", "comes from", "arises from"]
            if any(term in content.lower() for term in vague_embryo):
                if (
                    "germ layer" not in content.lower()
                    and "mesoderm" not in content.lower()
                ):
                    issues.append(
                        "Embryological description lacks specific germ layer information"
                    )
                    severity_count["minor"] += 1

        # Check for specific developmental timeline
        timeline_keywords = ["week", "weeks", "gestation", "embryonic", "fetal"]
        if not any(term in content.lower() for term in timeline_keywords):
            issues.append("Missing developmental timeline information")
            severity_count["minor"] += 1

        # Determine rating
        if severity_count["critical"] > 0:
            rating = EmbryologyRating.INCORRECT
            self.critical_issues.extend(issues)
        elif severity_count["major"] > 1:
            rating = EmbryologyRating.ABSENT
        elif severity_count["major"] > 0:
            rating = EmbryologyRating.PARTIALLY_INCORRECT
        elif severity_count["minor"] > 1:
            rating = EmbryologyRating.VAGUE
        elif severity_count["minor"] > 0:
            rating = EmbryologyRating.ACCEPTABLE
        else:
            rating = EmbryologyRating.CORRECT

        logger.debug(f"Embryology: {rating.value}")
        return (rating, issues)

    def _evaluate_clinical_reliability(
        self, content: str, structure_name: str
    ) -> Tuple[ClinicalReliabilityRating, List[str]]:
        """Evaluate clinical reliability - ZERO TOLERANCE for unsafe information."""
        issues = []
        severity_count = {"critical": 0, "major": 0, "minor": 0}

        # Check for potentially dangerous misinformation

        # Check for critical anatomical errors that could lead to clinical harm
        if "femoral" in structure_name.lower():
            if "ulnar artery" in content and "thigh" in content:
                issues.append(
                    "UNSAFE: Ulnar artery misplacement could lead to clinical misidentification"
                )
                severity_count["critical"] += 1
                self.critical_issues.append(
                    "Clinical safety issue: Arterial mislocalization"
                )

        # Check for unclear clinical descriptions
        vague_clinical = ["may", "might", "could", "possibly"]
        vague_count = sum(
            1 for term in vague_clinical if f" {term} " in content.lower()
        )
        if vague_count > 5:
            issues.append(
                f"Excessive clinical uncertainty ('{' '.join(vague_clinical)}' used {vague_count} times)"
            )
            severity_count["major"] += 1

        # Check for presence of clinical significance section
        has_clinical_section = any(
            term in content.lower()
            for term in [
                "clinical significance",
                "clinical importance",
                "clinical application",
            ]
        )
        if not has_clinical_section:
            issues.append("Missing clinical significance information")
            severity_count["minor"] += 1

        # Check for warnings about variations
        has_variation_warning = any(
            term in content.lower()
            for term in ["variation", "variant", "anatomical variation"]
        )
        if not has_variation_warning:
            issues.append("Missing information about anatomical variations")
            severity_count["minor"] += 1

        # Determine rating - ZERO TOLERANCE for critical issues
        if severity_count["critical"] > 0:
            rating = ClinicalReliabilityRating.DANGEROUS
            self.critical_issues.extend(issues)
        elif severity_count["major"] > 2:
            rating = ClinicalReliabilityRating.CONTRADICTS_STANDARDS
        elif severity_count["major"] > 0:
            rating = ClinicalReliabilityRating.UNSAFE_CLINICAL
        elif severity_count["minor"] > 2:
            rating = ClinicalReliabilityRating.MISLEADING
        elif severity_count["minor"] > 0:
            rating = ClinicalReliabilityRating.ACCEPTABLE_WITH_CAUTION
        else:
            rating = ClinicalReliabilityRating.SAFE_RELIABLE

        logger.debug(f"Clinical reliability: {rating.value}")
        return (rating, issues)

    def _evaluate_structural_organization(
        self, content: str
    ) -> Tuple[StructuralOrganizationRating, List[str]]:
        """Evaluate structural organization and logical flow."""
        issues = []
        severity_count = {"critical": 0, "major": 0, "minor": 0}

        # Check for proper section organization
        expected_sections = {
            "anatomical": ["origin", "course", "location", "structure"],
            "functional": ["function", "role", "mechanism"],
            "clinical": ["clinical", "pathology", "significance"],
            "embryological": ["embryo", "development"],
            "relationships": [
                "branch",
                "connection",
                "relationship",
                "innervation",
                "supply",
            ],
        }

        found_sections = 0
        for category, keywords in expected_sections.items():
            if any(keyword in content.lower() for keyword in keywords):
                found_sections += 1

        if found_sections < 3:
            issues.append(
                f"Incomplete organizational structure (only {found_sections} out of {len(expected_sections)} major sections)"
            )
            severity_count["major"] += 1

        # Check for logical flow indicators
        flow_words = [
            "then",
            "therefore",
            "consequently",
            "as a result",
            "furthermore",
            "in addition",
        ]
        flow_count = sum(1 for word in flow_words if word in content.lower())

        if flow_count < 2:
            issues.append("Limited logical flow and transitions between concepts")
            severity_count["minor"] += 1

        # Check for proper heading usage
        heading_count = content.count("#") + content.count("**")
        if heading_count < 5:
            issues.append("Insufficient use of organizational headings/formatting")
            severity_count["minor"] += 1

        # Check for bullet points or lists (good for organization)
        if "*" not in content and "-" not in content:
            issues.append("No use of lists or bullet points for organization")
            severity_count["minor"] += 1

        # Determine rating
        if severity_count["critical"] > 0:
            rating = StructuralOrganizationRating.INCOHERENT
            self.critical_issues.extend(issues)
        elif severity_count["major"] > 0:
            rating = StructuralOrganizationRating.FLAWED
        elif severity_count["minor"] > 2:
            rating = StructuralOrganizationRating.ACCEPTABLE
        elif severity_count["minor"] > 0:
            rating = StructuralOrganizationRating.LOGICAL
        else:
            rating = StructuralOrganizationRating.EXCELLENT

        logger.debug(f"Structural organization: {rating.value}")
        return (rating, issues)

    def _evaluate_general_accessibility(
        self, content: str
    ) -> Tuple[ReadabilityRating, List[str]]:
        """Evaluate readability for general audience."""
        issues = []
        severity_count = {"major": 0, "minor": 0}

        # Check for plain English section
        if "GENERAL AUDIENCE" not in content.upper() and "PLAIN ENGLISH" not in content.upper():
            issues.append("Missing dedicated plain English section")
            return (ReadabilityRating.POOR, issues)

        # Extract the layperson section
        lay_section = content.split("SECTION 2")[-1] if "SECTION 2" in content else content
        
        # Check for excessive jargon in lay section
        jargon = ["innervation", "morphology", "histological", "embryology", "vasculature"]
        found_jargon = [j for j in jargon if j in lay_section.lower()]
        
        if len(found_jargon) > 2:
            issues.append(f"Excessive jargon in lay section: {', '.join(found_jargon)}")
            severity_count["major"] += 1
            
        # Check for analogies (good for laypeople)
        analogies = ["like a", "similar to", "acts as a", "think of it as"]
        if not any(a in lay_section.lower() for a in analogies):
            issues.append("Lack of helpful analogies for general audience")
            severity_count["minor"] += 1

        # Determine rating
        if severity_count["major"] > 0:
            rating = ReadabilityRating.TOO_TECHNICAL
        elif severity_count["minor"] > 0:
            rating = ReadabilityRating.MODERATE
        else:
            rating = ReadabilityRating.EXCELLENT
            
        return (rating, issues)

    def _calculate_overall_score(
        self,
        accuracy: Tuple[AccuracyRating, List[str]],
        terminology: Tuple[TerminologyRating, List[str]],
        embryology: Tuple[EmbryologyRating, List[str]],
        clinical: Tuple[ClinicalReliabilityRating, List[str]],
        organization: Tuple[StructuralOrganizationRating, List[str]],
        accessibility: Tuple[ReadabilityRating, List[str]],
    ) -> float:
        """Calculate overall quality score (0-100)."""

        # Rating score mappings (higher is better)
        rating_scores = {
            # ... (previous scores)
            AccuracyRating.EXCELLENT: 100, AccuracyRating.GOOD: 90, AccuracyRating.ACCEPTABLE: 70,
            AccuracyRating.SUPERFICIAL: 40, AccuracyRating.POOR: 20, AccuracyRating.VERY_POOR: 10,
            AccuracyRating.INCORRECT: 0, AccuracyRating.UNSAFE: 0,
            TerminologyRating.EXCELLENT: 100, TerminologyRating.ACCURATE: 95, TerminologyRating.ACCEPTABLE: 75,
            TerminologyRating.IMPRECISE: 50, TerminologyRating.POOR: 20, TerminologyRating.VAGUE: 10, TerminologyRating.INCORRECT: 0,
            EmbryologyRating.CORRECT: 100, EmbryologyRating.ACCURATE: 95, EmbryologyRating.ACCEPTABLE: 75,
            EmbryologyRating.VAGUE: 50, EmbryologyRating.PARTIALLY_INCORRECT: 25, EmbryologyRating.INCORRECT: 0, EmbryologyRating.ABSENT: 10,
            ClinicalReliabilityRating.SAFE_RELIABLE: 100, ClinicalReliabilityRating.SAFE_ACCURATE: 100,
            ClinicalReliabilityRating.CLINICALLY_SOUND: 95, ClinicalReliabilityRating.ACCEPTABLE_WITH_CAUTION: 70,
            ClinicalReliabilityRating.MISLEADING: 40, ClinicalReliabilityRating.UNSAFE_CLINICAL: 10,
            ClinicalReliabilityRating.CONTRADICTS_STANDARDS: 5, ClinicalReliabilityRating.DANGEROUS: 0,
            StructuralOrganizationRating.EXCELLENT: 100, StructuralOrganizationRating.WELL_ORGANIZED: 90,
            StructuralOrganizationRating.LOGICAL: 85, StructuralOrganizationRating.ACCEPTABLE: 70,
            StructuralOrganizationRating.FLAWED: 40, StructuralOrganizationRating.POOR: 20, StructuralOrganizationRating.INCOHERENT: 0,
            # Accessibility
            ReadabilityRating.EXCELLENT: 100, ReadabilityRating.CLEAR: 90, ReadabilityRating.MODERATE: 70,
            ReadabilityRating.TOO_TECHNICAL: 40, ReadabilityRating.POOR: 10, ReadabilityRating.INACCURATE_SIMPLIFICATION: 0
        }

        # Weights: Clinical (40%), Accuracy (20%), Accessibility (15%), Terminology (10%), Embryology (10%), Organization (5%)
        scores = [
            rating_scores[accuracy[0]] * 0.20,
            rating_scores[terminology[0]] * 0.10,
            rating_scores[embryology[0]] * 0.10,
            rating_scores[clinical[0]] * 0.40,
            rating_scores[organization[0]] * 0.05,
            rating_scores[accessibility[0]] * 0.15,
        ]

        overall = sum(scores)
        return round(overall, 1)

    def _determine_pass_fail(
        self,
        accuracy: Tuple[AccuracyRating, List[str]],
        terminology: Tuple[TerminologyRating, List[str]],
        embryology: Tuple[EmbryologyRating, List[str]],
        clinical: Tuple[ClinicalReliabilityRating, List[str]],
        organization: Tuple[StructuralOrganizationRating, List[str]],
        accessibility: Tuple[ReadabilityRating, List[str]],
    ) -> str:
        """Determine pass/fail status with ZERO tolerance for critical issues."""

        # FAIL conditions (zero tolerance)
        fail_conditions = [
            clinical[0]
            in [
                ClinicalReliabilityRating.DANGEROUS,
                ClinicalReliabilityRating.CONTRADICTS_STANDARDS,
            ],
            accuracy[0] in [AccuracyRating.UNSAFE, AccuracyRating.INCORRECT],
            accessibility[0] == ReadabilityRating.INACCURATE_SIMPLIFICATION,
            len(self.critical_issues) > 0,
        ]

        if any(fail_conditions):
            return "FAIL"

        # PASS conditions - must meet minimum standards
        pass_conditions = [
            clinical[0]
            in [
                ClinicalReliabilityRating.SAFE_RELIABLE,
                ClinicalReliabilityRating.CLINICALLY_SOUND,
                ClinicalReliabilityRating.SAFE_ACCURATE,
            ],
            accuracy[0]
            in [
                AccuracyRating.EXCELLENT,
                AccuracyRating.GOOD,
                AccuracyRating.ACCEPTABLE,
            ],
            accessibility[0] in [ReadabilityRating.EXCELLENT, ReadabilityRating.CLEAR],
        ]

        if all(pass_conditions):
            return "PASS"

        return "CONDITIONAL_PASS"

    def _generate_recommendations(
        self,
        accuracy: Tuple[AccuracyRating, List[str]],
        terminology: Tuple[TerminologyRating, List[str]],
        embryology: Tuple[EmbryologyRating, List[str]],
        clinical: Tuple[ClinicalReliabilityRating, List[str]],
        organization: Tuple[StructuralOrganizationRating, List[str]],
        accessibility: Tuple[ReadabilityRating, List[str]],
    ) -> List[str]:
        """Generate recommendations for improvement."""
        recommendations = []

        # Accuracy recommendations
        if accuracy[0] in [
            AccuracyRating.UNSAFE,
            AccuracyRating.INCORRECT,
            AccuracyRating.VERY_POOR,
            AccuracyRating.POOR,
        ]:
            recommendations.append(
                "CRITICAL: Verify all anatomical information against Gray's Anatomy and standard references"
            )
            recommendations.extend(accuracy[1][:2])

        # Accessibility recommendations
        if accessibility[0] in [
            ReadabilityRating.POOR,
            ReadabilityRating.TOO_TECHNICAL,
            ReadabilityRating.INACCURATE_SIMPLIFICATION,
        ]:
            recommendations.append(
                "Improve the plain English section by removing jargon and using more analogies"
            )
            recommendations.extend(accessibility[1][:2])

        # Clinical recommendations
        if clinical[0] in [
            ClinicalReliabilityRating.DANGEROUS,
            ClinicalReliabilityRating.UNSAFE_CLINICAL,
            ClinicalReliabilityRating.CONTRADICTS_STANDARDS,
            ClinicalReliabilityRating.MISLEADING,
        ]:
            recommendations.append(
                "CRITICAL: Review clinical information for accuracy and safety before publication"
            )
            recommendations.extend(clinical[1][:2])

        # Terminology recommendations
        if terminology[0] in [
            TerminologyRating.INCORRECT,
            TerminologyRating.POOR,
            TerminologyRating.IMPRECISE,
            TerminologyRating.VAGUE,
        ]:
            recommendations.append(
                "Standardize terminology using Terminologia Anatomica (TA) and proper anatomical nomenclature"
            )
            recommendations.extend(terminology[1][:2])

        # Embryology recommendations
        if embryology[0] in [
            EmbryologyRating.ABSENT,
            EmbryologyRating.INCORRECT,
            EmbryologyRating.VAGUE,
            EmbryologyRating.PARTIALLY_INCORRECT,
        ]:
            recommendations.append(
                "Add comprehensive embryological information with specific germ layer origins and developmental timeline"
            )
            recommendations.extend(embryology[1][:1])

        # Organization recommendations
        if organization[0] in [
            StructuralOrganizationRating.INCOHERENT,
            StructuralOrganizationRating.POOR,
            StructuralOrganizationRating.FLAWED,
        ]:
            recommendations.append(
                "Reorganize content with clear sections: Anatomy → Embryology → Function → Clinical Significance"
            )

        return recommendations


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Strict Anatomy Report Evaluator with Zero Tolerance for Inaccuracies"
    )
    parser.add_argument(
        "input_file", type=Path, help="Path to anatomy report file (.md or .txt)"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output JSON file for evaluation results",
    )
    parser.add_argument(
        "-m", "--model", type=str, default=None, help="Model to use for evaluation"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Configure logging
    configure_logging(
        log_file="evaluate_anatomy_report.log",
        verbosity=4 if args.verbose else 3,
        enable_console=args.verbose,
    )

    # Evaluate report
    evaluator = AnatomyReportEvaluator(model=args.model)
    result = evaluator.evaluate_file(args.input_file)

    # Display results
    if args.verbose:
        print("\n" + "=" * 80)
        print(f"ANATOMY REPORT EVALUATION: {result.structure_name.upper()}")
        print("=" * 80)
        print(f"\nAnatomical Accuracy: {result.anatomical_accuracy[0].value}")
        if result.anatomical_accuracy[1]:
            for issue in result.anatomical_accuracy[1]:
                print(f"  • {issue}")

        print(f"\nTerminology Precision: {result.terminology_precision[0].value}")
        if result.terminology_precision[1]:
            for issue in result.terminology_precision[1]:
                print(f"  • {issue}")

        print(f"\nEmbryology: {result.embryology[0].value}")
        if result.embryology[1]:
            for issue in result.embryology[1]:
                print(f"  • {issue}")

        print(f"\nClinical Reliability: {result.clinical_reliability[0].value}")
        if result.clinical_reliability[1]:
            for issue in result.clinical_reliability[1]:
                print(f"  • {issue}")

        print(f"\nStructural Organization: {result.structural_organization[0].value}")
        if result.structural_organization[1]:
            for issue in result.structural_organization[1]:
                print(f"  • {issue}")

        print(f"\n{'=' * 80}")
        print(f"Overall Quality Score: {result.overall_quality_score}/100")
        print(f"Status: {result.pass_fail_status}")
        print(f"{'=' * 80}")

        if result.critical_issues:
            print("\nCRITICAL ISSUES (MUST FIX):")
            for issue in result.critical_issues:
                print(f"  ❌ {issue}")

        if result.recommendations:
            print("\nRECOMMENDATIONS:")
            for rec in result.recommendations:
                print(f"  → {rec}")

    # Save to JSON if output specified
    if args.output:
        with open(args.output, "w") as f:
            json.dump(result.to_dict(), f, indent=2)
        if args.verbose:
            print(f"\n✓ Results saved to: {args.output}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Orchestrator for the Medical Anatomy Generator-Evaluator (Maker-Checker) workflow.

This script coordinates the MedicalAnatomyGenerator (Maker) and the
AnatomyReportEvaluator (Checker) to produce high-quality, verified anatomical reports.
"""



# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


try:
    from .medical_anatomy import MedicalAnatomyGenerator
    from .evaluate_anatomy_report import AnatomyReportEvaluator, AnatomyEvaluationResult
    from .medical_anatomy_models import FactCheckModel
    from .medical_anatomy_prompts import PromptBuilder
except (ImportError, ValueError):
    from medical.anatomy.agentic.medical_anatomy import MedicalAnatomyGenerator
    from medical.anatomy.agentic.evaluate_anatomy_report import AnatomyReportEvaluator, AnatomyEvaluationResult
    from medical.anatomy.agentic.medical_anatomy_models import FactCheckModel
    from medical.anatomy.agentic.medical_anatomy_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class AgenticAnatomyWorkflow:
    """Orchestrates the Generator-Evaluator workflow."""

    def __init__(
        self,
        generator_model: str,
        evaluator_model: str,
        output_dir: Path,
        structured: bool = False,
    ):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.structured = structured

        # Initialize Generator Agent
        gen_config = ModelConfig(model=generator_model, temperature=0.2)
        self.generator = MedicalAnatomyGenerator(gen_config)

        # Initialize Evaluator Agent
        # If evaluator_model is the same as generator_model, we still create a separate instance
        # although they might share the same underlying LiteClient logic if needed.
        self.evaluator = AnatomyReportEvaluator(model=evaluator_model)

        # Initialize Fact-Checker Auditor
        self.auditor_client = LiteClient(ModelConfig(model=evaluator_model, temperature=0.0))

        logger.info(f"Workflow initialized: Generator={generator_model}, Evaluator={evaluator_model}")

    def run_workflow(self, body_part: str) -> Optional[AnatomyEvaluationResult]:
        """Runs the generation then evaluation for a single body part."""
        logger.info(f"--- Processing: {body_part} ---")

        # 1. Generation Phase (Maker)
        print(f"  [Maker] Generating anatomical report for {body_part}...")
        try:
            gen_result = self.generator.generate_text(body_part, structured=self.structured)
            report_path = self.generator.save(gen_result, self.output_dir)
            print(f"  ✓ [Maker] Report saved to {report_path}")
        except Exception as e:
            logger.error(f"  ❌ [Maker] Generation failed: {e}")
            return None

        # Extract technical section for fact-checking
        report_md = gen_result.markdown
        if "SECTION 1" in report_md:
            technical_content = report_md.split("SECTION 1:")[1].split("---")[0].strip()
        else:
            technical_content = report_md

        # 2. Fact-Checking Phase (Auditor)
        print(f"  [Auditor] Verifying anatomical claims for {body_part}...")
        try:
            fact_check = self._run_fact_checker(technical_content)
            self._print_fact_check_summary(fact_check)
        except Exception as e:
            logger.error(f"  ❌ [Auditor] Fact-check failed: {e}")
            fact_check = None

        # 3. Evaluation Phase (Checker)
        print(f"  [Checker] Evaluating report for {body_part}...")
        try:
            eval_result = self.evaluator.evaluate_file(report_path)
            self._print_evaluation_summary(eval_result)
            return eval_result
        except Exception as e:
            logger.error(f"  ❌ [Checker] Evaluation failed: {e}")
            return None

    def _run_fact_checker(self, technical_report: str) -> FactCheckModel:
        """Run the Fact-Checker agent."""
        system_prompt = PromptBuilder.create_fact_checker_system_prompt()
        user_prompt = PromptBuilder.create_fact_checker_user_prompt(technical_report)

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=FactCheckModel,
        )

        return self.auditor_client.generate_text(model_input=model_input)

    def _print_fact_check_summary(self, result: FactCheckModel):
        """Prints a summary of the fact-check results."""
        print(f"\n  🔍 Fact-Check Summary (Accuracy: {result.accuracy_score}%)")
        
        incorrect_claims = [c for c in result.claims if c.status.lower() == 'incorrect']
        if incorrect_claims:
            print(f"  🔴 Found {len(incorrect_claims)} incorrect claims:")
            for c in incorrect_claims:
                print(f"    - Claim: {c.claim}")
                print(f"      Correction: {c.correction}")
        else:
            print("  ✅ All anatomical claims verified successfully.")
        
        print(f"  Summary: {result.summary}")
        print("-" * 50)

    def _print_evaluation_summary(self, result: AnatomyEvaluationResult):
        """Prints a concise summary of the evaluation."""
        status_color = {
            "PASS": "✅",
            "CONDITIONAL_PASS": "⚠️",
            "FAIL": "❌"
        }.get(result.pass_fail_status, "❓")

        print(f"\n  {status_color} Evaluation Result: {result.pass_fail_status}")
        print(f"  Quality Score: {result.overall_quality_score}/100")
        
        # Display key ratings
        print(f"  Accuracy:      {result.anatomical_accuracy[0].value}")
        print(f"  Clinical:      {result.clinical_reliability[0].value}")
        print(f"  Accessibility: {result.general_accessibility[0].value}")
        
        if result.critical_issues:
            print(f"  🔴 Critical Issues ({len(result.critical_issues)}):")
            for issue in result.critical_issues[:3]:
                print(f"    - {issue}")
        
        if result.pass_fail_status == "FAIL":
            print("  ❌ Report failed clinical safety, accuracy, or simplification checks.")
        elif result.pass_fail_status == "CONDITIONAL_PASS":
            print("  ⚠️ Report has minor issues that should be addressed.")
        else:
            print("  ✅ Report passed all strict anatomical and accessibility standards.")
        print("-" * 50)


def get_args():
    parser = argparse.ArgumentParser(
        description="Agentic Medical Anatomy Workflow (Maker-Checker)"
    )
    parser.add_argument(
        "body_part", help="Anatomical part to analyze (or file with list of parts)."
    )
    parser.add_argument(
        "-d", "--output-dir", default="agentic_outputs", help="Output directory."
    )
    parser.add_argument(
        "-gm", "--gen-model", default="ollama/gemma3", help="Model for Generator Agent."
    )
    parser.add_argument(
        "-em", "--eval-model", default="ollama/gemma3", help="Model for Evaluator Agent."
    )
    parser.add_argument(
        "-s", "--structured", action="store_true", help="Use structured output for generation."
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging."
    )
    return parser.parse_args()


def main():
    args = get_args()
    configure_logging(
        log_file="anatomy_workflow.log", 
        verbosity=4 if args.verbose else 3, 
        enable_console=args.verbose
    )

    input_path = Path(args.body_part)
    if input_path.is_file():
        with open(input_path, "r") as f:
            items = [line.strip() for line in f if line.strip()]
    else:
        items = [args.body_part]

    workflow = AgenticAnatomyWorkflow(
        generator_model=args.gen_model,
        evaluator_model=args.eval_model,
        output_dir=Path(args.output_dir),
        structured=args.structured
    )

    print(f"\n🚀 Starting Agentic Anatomy Workflow on {len(items)} item(s)\n")
    
    results = []
    for item in items:
        res = workflow.run_workflow(item)
        if res:
            results.append(res)

    # Final summary
    if len(items) > 1:
        print("\n" + "=" * 50)
        print("WORKFLOW BATCH SUMMARY")
        print("=" * 50)
        passed = sum(1 for r in results if r.pass_fail_status == "PASS")
        failed = sum(1 for r in results if r.pass_fail_status == "FAIL")
        conditional = sum(1 for r in results if r.pass_fail_status == "CONDITIONAL_PASS")
        
        print(f"Total processed: {len(results)}")
        print(f"✅ PASSED: {passed}")
        print(f"⚠️  CONDITIONAL: {conditional}")
        print(f"❌ FAILED: {failed}")
        print("=" * 50)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Medical Anatomy module.

This module provides the core MedicalAnatomyGenerator class for generating
comprehensive anatomical information based on provided configuration.
"""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


try:
    from .medical_anatomy_models import MedicalAnatomyModel, ModelOutput
    from .medical_anatomy_prompts import PromptBuilder
except (ImportError, ValueError):
    from medical.anatomy.agentic.medical_anatomy_models import MedicalAnatomyModel, ModelOutput
    from medical.anatomy.agentic.medical_anatomy_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class MedicalAnatomyGenerator:
    """Generates comprehensive anatomical information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.body_part = None  # Store the body part being analyzed
        logger.debug("Initialized MedicalAnatomyGenerator")

    def generate_text(self, body_part: str, structured: bool = False) -> ModelOutput:
        """Generates 3-tier anatomical information: Specialist -> Auditor -> Output."""
        if not body_part or not str(body_part).strip():
            raise ValueError("Body part name cannot be empty")

        self.body_part = body_part
        logger.info(f"Starting 3-tier anatomical generation for: {body_part}")

        # 1. Technical Specialist Pass (JSON Specialist)
        logger.debug(f"[Specialist] Generating content for: {body_part}")
        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(body_part)

        response_format = MedicalAnatomyModel if structured else None
        tech_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        tech_result = self.ask_llm(tech_input)
        if structured:
            tech_content = tech_result.data.model_dump_json(indent=2)
        else:
            tech_content = tech_result.markdown
        
        # 2. Compliance Auditor Pass (JSON Auditor)
        logger.debug(f"[Auditor] Auditing content for: {body_part}")
        audit_system = PromptBuilder.create_fact_checker_system_prompt()
        audit_user = PromptBuilder.create_fact_checker_user_prompt(tech_content)

        audit_input = ModelInput(
            system_prompt=audit_system,
            user_prompt=audit_user,
            response_format=None, # For simplicity, can be JSON if a model exists
        )

        audit_result = self.ask_llm(audit_input)
        audit_content = audit_result.markdown # Usually JSON string in markdown
        
        # 3. Final Output Synthesis (Markdown Closer)
        logger.debug(f"[Output] Synthesizing final report for: {body_part}")
        out_sys, out_user = PromptBuilder.create_output_synthesis_prompts(
            body_part, tech_content, audit_content
        )

        output_input = ModelInput(
            system_prompt=out_sys,
            user_prompt=out_user,
            response_format=None,
        )

        output_result = self.ask_llm(output_input)
        final_markdown = output_result.markdown

        logger.info("✓ Successfully generated 3-tier anatomical information")
        
        return ModelOutput(
            data=tech_result.data if structured else None,
            markdown=final_markdown,
            metadata={"audit": audit_content}
        )

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate content."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the anatomical information to a file."""
        if self.body_part is None:
            raise ValueError(
                "No body part information available. Call generate_text first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.body_part.lower().replace(' ', '_')}"

        return save_model_response(result, output_dir / base_filename)

"""Medical Anatomy Information Generator CLI."""



# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


try:
    from .medical_anatomy import MedicalAnatomyGenerator
except (ImportError, ValueError):
    from medical.anatomy.agentic.medical_anatomy import MedicalAnatomyGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical anatomy information."
    )
    parser.add_argument(
        "body_part", help="Anatomical part or file path containing parts."
    )
    parser.add_argument(
        "-d", "--output-dir", default="outputs", help="Output directory."
    )
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Verbosity level.",
    )
    parser.add_argument(
        "-s", "--structured", action="store_true", help="Use structured output."
    )
    return parser.parse_args()


def main():
    args = get_user_arguments()
    configure_logging(
        log_file="medical_anatomy.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.body_part)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.body_part]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)
        generator = MedicalAnatomyGenerator(model_config)

        for item in tqdm(items, desc="Processing"):
            result = generator.generate_text(body_part=item, structured=args.structured)
            if result:
                generator.save(result, output_dir)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

#!/usr/bin/env python3
"""
Mock tests for the Agentic Anatomy Workflow.
Verifies the interaction between Generator and Evaluator.
"""


# Add the project root to sys.path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


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

#!/usr/bin/env python3
"""
CLI interface for Anatomy Report Evaluator.

Provides command-line access to evaluate anatomy reports with strict quality standards.
"""


# Add the project root to sys.path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

try:
    from .evaluate_anatomy_report import AnatomyEvaluationResult, AnatomyReportEvaluator
except (ImportError, ValueError):
    from evaluate_anatomy_report import AnatomyEvaluationResult, AnatomyReportEvaluator


logger = logging.getLogger(__name__)


class EvaluationCLI:
    """Command-line interface for anatomy report evaluation."""

    def __init__(self, model: str = "ollama/gemma3", verbose: bool = False):
        self.evaluator = AnatomyReportEvaluator(model=model)
        self.verbose = verbose
        logger.debug("Initialized EvaluationCLI")

    def evaluate_single(
        self, file_path: Path, output_json: Optional[Path] = None
    ) -> AnatomyEvaluationResult:
        """Evaluate a single anatomy report file."""
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        logger.info(f"Evaluating: {file_path}")
        result = self.evaluator.evaluate_file(file_path)

        # Display results
        if self.verbose:
            self._display_results(result)

        # Save JSON output if specified
        if output_json:
            self._save_json_results(result, output_json)

        return result

    def evaluate_directory(
        self, directory: Path, output_dir: Optional[Path] = None
    ) -> dict:
        """Evaluate all anatomy report files in a directory."""
        if not directory.is_dir():
            logger.error(f"Directory not found: {directory}")
            raise NotADirectoryError(f"Directory not found: {directory}")

        logger.info(f"Scanning directory: {directory}")

        # Find all markdown and text files
        files = list(directory.glob("*.md")) + list(directory.glob("*.txt"))
        if not files:
            logger.warning(f"No .md or .txt files found in {directory}")
            return {}

        results = {}
        logger.info(f"Found {len(files)} files to evaluate")

        for file_path in sorted(files):
            logger.info(f"Processing: {file_path.name}")
            try:
                result = self.evaluator.evaluate_file(file_path)
                results[file_path.name] = result.to_dict()
            except Exception as e:
                logger.error(f"Error evaluating {file_path.name}: {e}")
                results[file_path.name] = {"error": str(e)}

        # Summary report
        if self.verbose:
            self._display_batch_summary(results)

        # Save results if output directory specified
        if output_dir:
            self._save_batch_results(results, output_dir)

        return results

    def _display_results(self, result: AnatomyEvaluationResult) -> None:
        """Display evaluation results in formatted output."""
        border = "=" * 90
        print(f"\n{border}")
        print(f"ANATOMY REPORT EVALUATION: {result.structure_name.upper()}")
        print(border)

        # Anatomical Accuracy
        print("\n📋 ANATOMICAL ACCURACY")
        print(f"   {result.anatomical_accuracy[0].value}")
        if result.anatomical_accuracy[1]:
            for issue in result.anatomical_accuracy[1]:
                prefix = "   ❌" if "CRITICAL" in issue else "   ⚠️"
                print(f"{prefix} {issue}")

        # Terminology Precision
        print("\n📚 TERMINOLOGY PRECISION")
        print(f"   {result.terminology_precision[0].value}")
        if result.terminology_precision[1]:
            for issue in result.terminology_precision[1]:
                print(f"   ⚠️ {issue}")

        # Embryology
        print("\n🧬 EMBRYOLOGY")
        print(f"   {result.embryology[0].value}")
        if result.embryology[1]:
            for issue in result.embryology[1]:
                print(f"   ⚠️ {issue}")

        # Clinical Reliability
        print("\n⚕️ CLINICAL RELIABILITY")
        print(f"   {result.clinical_reliability[0].value}")
        if result.clinical_reliability[1]:
            for issue in result.clinical_reliability[1]:
                prefix = "   ❌" if "UNSAFE" in issue or "CRITICAL" in issue else "   ⚠️"
                print(f"{prefix} {issue}")

        # Structural Organization
        print("\n🏗️ STRUCTURAL ORGANIZATION")
        print(f"   {result.structural_organization[0].value}")
        if result.structural_organization[1]:
            for issue in result.structural_organization[1]:
                print(f"   ⚠️ {issue}")

        # General Accessibility
        print("\n🌍 GENERAL ACCESSIBILITY")
        print(f"   {result.general_accessibility[0].value}")
        if result.general_accessibility[1]:
            for issue in result.general_accessibility[1]:
                print(f"   ⚠️ {issue}")

        # Summary
        print(f"\n{border}")
        print(f"Overall Quality Score: {result.overall_quality_score}/100")
        print(
            f"Status: {self._status_emoji(result.pass_fail_status)} {result.pass_fail_status}"
        )
        print(border)

        # Critical Issues
        if result.critical_issues:
            print("\n🔴 CRITICAL ISSUES (MUST FIX):")
            for issue in result.critical_issues:
                print(f"   ❌ {issue}")

        # Recommendations
        if result.recommendations:
            print("\n💡 RECOMMENDATIONS:")
            for rec in result.recommendations:
                print(f"   → {rec}")

        print()

    def _display_batch_summary(self, results: dict) -> None:
        """Display summary of batch evaluation results."""
        if not results:
            print("No results to display")
            return

        print("\n" + "=" * 90)
        print("BATCH EVALUATION SUMMARY")
        print("=" * 90)

        # Count results
        passed = sum(
            1
            for r in results.values()
            if isinstance(r, dict) and r.get("pass_fail_status") == "PASS"
        )
        failed = sum(
            1
            for r in results.values()
            if isinstance(r, dict) and r.get("pass_fail_status") == "FAIL"
        )
        conditional = sum(
            1
            for r in results.values()
            if isinstance(r, dict) and r.get("pass_fail_status") == "CONDITIONAL_PASS"
        )
        errors = sum(
            1 for r in results.values() if isinstance(r, dict) and "error" in r
        )

        print(f"\nTotal Files: {len(results)}")
        print(f"  ✓ PASSED: {passed}")
        print(f"  ⚠️  CONDITIONAL: {conditional}")
        print(f"  ❌ FAILED: {failed}")
        print(f"  🔴 ERRORS: {errors}")

        # Score distribution
        scores = [
            r["overall_quality_score"]
            for r in results.values()
            if isinstance(r, dict) and "overall_quality_score" in r
        ]
        if scores:
            avg_score = sum(scores) / len(scores)
            max_score = max(scores)
            min_score = min(scores)
            print("\nScore Statistics:")
            print(f"  Average: {avg_score:.1f}/100")
            print(f"  Highest: {max_score:.1f}/100")
            print(f"  Lowest: {min_score:.1f}/100")

        # Details by file
        print("\nDetailed Results:")
        print("-" * 90)
        for filename, result in sorted(results.items()):
            if isinstance(result, dict) and "overall_quality_score" in result:
                status = self._status_emoji(result["pass_fail_status"])
                print(
                    f"{status} {filename:40s} {result['overall_quality_score']:6.1f}/100 {result['pass_fail_status']}"
                )
            else:
                print(f"🔴 {filename:40s} ERROR")

    def _save_json_results(
        self, result: AnatomyEvaluationResult, output_path: Path
    ) -> None:
        """Save evaluation results to JSON file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(result.to_dict(), f, indent=2)

        logger.info(f"Results saved to: {output_path}")
        print(f"✓ JSON results saved to: {output_path}")

    def _save_batch_results(self, results: dict, output_dir: Path) -> None:
        """Save batch evaluation results to directory."""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save individual results
        for filename, result in results.items():
            if isinstance(result, dict) and "overall_quality_score" in result:
                output_file = output_dir / f"{Path(filename).stem}_evaluation.json"
                with open(output_file, "w") as f:
                    json.dump(result, f, indent=2)

        # Save summary report
        summary = {"total_files": len(results), "results": results}
        summary_file = output_dir / "evaluation_summary.json"
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Batch results saved to: {output_dir}")
        print(f"✓ Batch results saved to: {output_dir}")

    @staticmethod
    def _status_emoji(status: str) -> str:
        """Return emoji for status."""
        status_map = {"PASS": "✅", "CONDITIONAL_PASS": "⚠️", "FAIL": "❌"}
        return status_map.get(status, "❓")


def main():
    """Main CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Strict Anatomy Report Evaluator - Zero Tolerance for Inaccuracies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Evaluate single file
  python evaluate_anatomy_cli.py path/to/report.md

  # Evaluate with JSON output
  python evaluate_anatomy_cli.py path/to/report.md -o output.json

  # Evaluate entire directory
  python evaluate_anatomy_cli.py path/to/reports/ -b -o output_dir/

  # Verbose output
  python evaluate_anatomy_cli.py path/to/report.md -v
        """,
    )

    parser.add_argument("path", type=Path, help="File or directory to evaluate")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output file/directory for results (JSON format)",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="ollama/gemma3",
        help="Model to use for evaluation",
    )
    parser.add_argument(
        "-b",
        "--batch",
        action="store_true",
        help="Evaluate all files in directory (if path is directory)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Configure logging
    configure_logging(
        log_file="evaluate_anatomy.log",
        verbosity=4 if args.verbose else 3,
        enable_console=args.verbose,
    )

    try:
        cli = EvaluationCLI(model=args.model, verbose=args.verbose)

        if args.path.is_dir() and args.batch:
            cli.evaluate_directory(args.path, args.output)
        elif args.path.is_file():
            cli.evaluate_single(args.path, args.output)
        else:
            print(f"Error: {args.path} is not a valid file or directory")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.verbose)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

