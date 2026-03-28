#!/usr/bin/env python3
"""
Strict Anatomy Report Evaluator.

This module evaluates anatomical reports against rigorous medical and scientific standards.
Zero tolerance for inaccuracies in clinical reliability and anatomical accuracy.
"""

import json
import logging
import sys
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel

# Add the project root to sys.path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from lite.logging_config import configure_logging

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


class AnatomyEvaluationResult(BaseModel):
    """Comprehensive evaluation result for an anatomy report."""

    structure_name: str
    anatomical_accuracy: Tuple[AccuracyRating, List[str]]
    terminology_precision: Tuple[TerminologyRating, List[str]]
    embryology: Tuple[EmbryologyRating, List[str]]
    clinical_reliability: Tuple[ClinicalReliabilityRating, List[str]]
    structural_organization: Tuple[StructuralOrganizationRating, List[str]]

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

        # Calculate overall score
        overall_score = self._calculate_overall_score(
            accuracy, terminology, embryology, clinical, organization
        )

        # Determine pass/fail status
        pass_fail = self._determine_pass_fail(
            accuracy, terminology, embryology, clinical, organization
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            accuracy, terminology, embryology, clinical, organization
        )

        result = AnatomyEvaluationResult(
            structure_name=structure_name,
            anatomical_accuracy=accuracy,
            terminology_precision=terminology,
            embryology=embryology,
            clinical_reliability=clinical,
            structural_organization=organization,
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

CRITICAL FAILURE CONDITIONS:
- Any anatomical inaccuracy (e.g., ulnar artery in thigh).
- Any clinical safety issue or dangerous misinformation.
- Contradictory anatomical statements.

Evaluation Ratings (USE THESE EXACT STRINGS):
Accuracy: "✓ Excellent", "✓ Good", "⚠️ Acceptable", "⚠️ Superficially organized but conceptually flawed", "❌ Poor", "❌ Very Poor", "❌ Incorrect", "❌ Unsafe"
Terminology: "✓ Excellent", "✓ Accurate", "⚠️ Acceptable with minor issues", "⚠️ Imprecise terminology", "❌ Poor", "❌ Vague/Non-standard", "❌ Incorrect terminology used"
Embryology: "✓ Correct", "✓ Accurate", "⚠️ Acceptable but incomplete", "⚠️ Vague or oversimplified", "⚠️ Partially incorrect", "❌ Incorrect", "❌ Absent or severely flawed"
Clinical: "✓ Safe and reliable", "✓ Safe and accurate", "✓ Clinically sound", "⚠️ Acceptable with caution", "⚠️ Misleading or potentially problematic", "❌ Unsafe for clinical use", "❌ Contradicts established clinical standards", "❌ Dangerous/High-risk information"
Organization: "✓ Excellent organization", "✓ Well-organized", "✓ Logically structured", "⚠️ Acceptable but needs improvement", "⚠️ Superficially organized but conceptually flawed", "❌ Poor organization", "❌ Incoherent/Disorganized"

Output format MUST be a structured object matching AnatomyEvaluationResult:
- anatomical_accuracy: [Rating, Issues] where Rating is one of Accuracy strings and Issues is a list of strings.
- terminology_precision: [Rating, Issues] where Rating is one of Terminology strings and Issues is a list of strings.
- embryology: [Rating, Issues] where Rating is one of Embryology strings and Issues is a list of strings.
- clinical_reliability: [Rating, Issues] where Rating is one of Clinical strings and Issues is a list of strings.
- structural_organization: [Rating, Issues] where Rating is one of Organization strings and Issues is a list of strings.
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

    def _calculate_overall_score(
        self,
        accuracy: Tuple[AccuracyRating, List[str]],
        terminology: Tuple[TerminologyRating, List[str]],
        embryology: Tuple[EmbryologyRating, List[str]],
        clinical: Tuple[ClinicalReliabilityRating, List[str]],
        organization: Tuple[StructuralOrganizationRating, List[str]],
    ) -> float:
        """Calculate overall quality score (0-100)."""

        # Rating score mappings (higher is better)
        rating_scores = {
            # Accuracy
            AccuracyRating.EXCELLENT: 100,
            AccuracyRating.GOOD: 90,
            AccuracyRating.ACCEPTABLE: 70,
            AccuracyRating.SUPERFICIAL: 40,
            AccuracyRating.POOR: 20,
            AccuracyRating.VERY_POOR: 10,
            AccuracyRating.INCORRECT: 0,
            AccuracyRating.UNSAFE: 0,
            # Terminology
            TerminologyRating.EXCELLENT: 100,
            TerminologyRating.ACCURATE: 95,
            TerminologyRating.ACCEPTABLE: 75,
            TerminologyRating.IMPRECISE: 50,
            TerminologyRating.POOR: 20,
            TerminologyRating.VAGUE: 10,
            TerminologyRating.INCORRECT: 0,
            # Embryology
            EmbryologyRating.CORRECT: 100,
            EmbryologyRating.ACCURATE: 95,
            EmbryologyRating.ACCEPTABLE: 75,
            EmbryologyRating.VAGUE: 50,
            EmbryologyRating.PARTIALLY_INCORRECT: 25,
            EmbryologyRating.INCORRECT: 0,
            EmbryologyRating.ABSENT: 10,
            # Clinical
            ClinicalReliabilityRating.SAFE_RELIABLE: 100,
            ClinicalReliabilityRating.SAFE_ACCURATE: 100,
            ClinicalReliabilityRating.CLINICALLY_SOUND: 95,
            ClinicalReliabilityRating.ACCEPTABLE_WITH_CAUTION: 70,
            ClinicalReliabilityRating.MISLEADING: 40,
            ClinicalReliabilityRating.UNSAFE_CLINICAL: 10,
            ClinicalReliabilityRating.CONTRADICTS_STANDARDS: 5,
            ClinicalReliabilityRating.DANGEROUS: 0,
            # Organization
            StructuralOrganizationRating.EXCELLENT: 100,
            StructuralOrganizationRating.WELL_ORGANIZED: 90,
            StructuralOrganizationRating.LOGICAL: 85,
            StructuralOrganizationRating.ACCEPTABLE: 70,
            StructuralOrganizationRating.FLAWED: 40,
            StructuralOrganizationRating.POOR: 20,
            StructuralOrganizationRating.INCOHERENT: 0,
        }

        # Weights: Clinical reliability is most critical (50%), then accuracy (25%), rest (25%)
        scores = [
            rating_scores[accuracy[0]] * 0.25,  # Accuracy: 25%
            rating_scores[terminology[0]] * 0.10,  # Terminology: 10%
            rating_scores[embryology[0]] * 0.10,  # Embryology: 10%
            rating_scores[clinical[0]] * 0.50,  # Clinical: 50% (CRITICAL)
            rating_scores[organization[0]] * 0.05,  # Organization: 5%
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
            terminology[0]
            in [
                TerminologyRating.ACCURATE,
                TerminologyRating.EXCELLENT,
                TerminologyRating.ACCEPTABLE,
            ],
            organization[0]
            in [
                StructuralOrganizationRating.LOGICAL,
                StructuralOrganizationRating.WELL_ORGANIZED,
                StructuralOrganizationRating.EXCELLENT,
            ],
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
            recommendations.extend(accuracy[1][:2])  # Add up to 2 specific issues

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
            recommendations.extend(terminology[1][:2])  # Add up to 2 specific issues

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
            recommendations.extend(embryology[1][:1])  # Add specific issue

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
            recommendations.extend(clinical[1][:2])  # Add up to 2 specific issues

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
