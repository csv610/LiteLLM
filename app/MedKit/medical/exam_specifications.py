"""exam_specifications - Define comprehensive exam specifications with required questions.

This module provides detailed specifications for different types of physical exams, ensuring
complete and standardized question coverage. Each exam specification includes required inspection,
palpation, percussion, auscultation, and verbal assessment questions, along with relevant medical
history, lifestyle, and family history topics. Predefined specifications for common exams
(throat, pregnancy, neck, male genitalia) are included, with dynamic fallback generation for
other exam types.

QUICK START:
    Get specification for an exam type:

    >>> from exam_specifications import get_exam_specification
    >>> throat_spec = get_exam_specification("throat")
    >>> print(f"Min questions required: {throat_spec.min_physical_exam_questions}")

    Validate exam and gender compatibility:

    >>> from exam_specifications import validate_exam_gender_compatibility
    >>> validate_exam_gender_compatibility("pregnancy", "female")  # OK
    >>> validate_exam_gender_compatibility("pregnancy", "male")  # Raises ValueError

COMMON USES:
    1. Question generation validation - ensuring generated exams meet requirements
    2. Curriculum design - defining comprehensive exam question sets
    3. Quality assurance - verifying exam completeness before deployment
    4. Gender-appropriate exams - matching exam types to patient demographics
    5. Standardization - maintaining consistent exam structures across applications

KEY FEATURES AND COVERAGE AREAS:
    - Physical Exam Sections: inspection, palpation, percussion, auscultation questions
    - Verbal Assessment: required clinical history questions
    - Medical History Topics: relevant past medical conditions and treatments
    - Lifestyle Topics: social factors and behavioral history
    - Family History Topics: genetic and hereditary information
    - Exam Specifications Registry: predefined specs for 4+ exam types
    - Gender Compatibility: ensuring exams are appropriate for patient demographics
    - Dynamic Specification Generation: auto-create specs for unknown exam types
    - Validation Functions: enforce zero-tolerance requirements
"""

from dataclasses import dataclass
from typing import List

from medkit.utils.logging_config import setup_logger

# Configure logging
logger = setup_logger(__name__, enable_file_handler=False)

@dataclass
class ExamSpecification:
    """Defines the required questions for a specific exam type."""
    exam: str  # e.g., "throat", "cardiac", "lung"
    applicable_genders: List[str]  # e.g., ["male", "female"] or ["female"] for pregnancy exams

    # Physical exam sections that MUST be covered
    required_inspection_questions: List[str]
    required_palpation_questions: List[str]
    required_percussion_questions: List[str]  # Empty if not applicable
    required_auscultation_questions: List[str]  # Empty if not applicable
    required_verbal_assessment_questions: List[str]

    # Supporting history (only clinically relevant)
    relevant_medical_history_topics: List[str]
    relevant_lifestyle_topics: List[str]
    relevant_family_history_topics: List[str]

    # Minimum number of physical exam questions (zero tolerance if not met)
    min_physical_exam_questions: int


# ============================================================================
# THROAT EXAM SPECIFICATION
# ============================================================================

THROAT_EXAM = ExamSpecification(
    exam="throat",
    applicable_genders=["male", "female"],

    required_inspection_questions=[
        "Appearance of lips, mouth opening, and tongue - normal vs abnormal, symmetry, color",
        "Tongue color (pink, pale, coated), coating type/thickness, size (normal vs enlarged/macroglossia), bilateral symmetry",
        "Oral mucosa - intact vs ulcerated, color (pale, red, white patches), signs of inflammation, moistness vs dry",
        "Hard and soft palate - color (pink vs red), intact vs defects, exudate vs clear, normal vs abnormal",
        "Tonsillar assessment - bilateral comparison, size (1-4 scale: 1=normal, 2=mildly enlarged, 3=enlarged, 4=obstructing), color (pink vs red), exudate present vs absent, symmetry",
        "Posterior pharyngeal wall - color (pink vs red/inflamed), exudate vs clear, granular vs smooth appearance, normal vs abnormal",
        "Uvula - position (midline vs deviated), color, edema vs normal, bilateral symmetry of surrounding structures",
        "Overall pharyngeal inflammation level - none, mild, moderate, severe; document extent and location",
        "Oral cavity lesions or abnormalities - location, size, description (ulcer, vesicle, white patch), appearance, presence vs absence",
        "Lymphoid tissue - normal size vs hypertrophied, appearance, color, bilateral symmetry, presence vs absence of hyperplasia",
    ],

    required_palpation_questions=[
        "Cervical lymph nodes (anterior cervical) - bilateral comparison, size, consistency, tenderness, symmetry",
        "Cervical lymph nodes (posterior cervical) - bilateral comparison, size, consistency, tenderness, symmetry",
        "Submandibular lymph nodes - bilateral comparison, size, consistency, tenderness, normal vs abnormal",
        "Submental lymph nodes - bilateral comparison, size, consistency, palpable vs non-palpable",
        "Tonsillar size assessment by palpation - bilateral comparison, consistency, size grade (1-4 scale or descriptive)",
        "Neck muscle tenderness - bilateral assessment, muscle groups (sternocleidomastoid, trapezius), symmetry",
        "Thyroid gland palpation - size (normal vs enlarged/goiter), nodules, tenderness, symmetry, consistency",
        "Jaw and temporomandibular joint (TMJ) assessment - bilateral symmetry, tenderness, range of motion, crepitus/clicking",
    ],

    required_percussion_questions=[],  # Not typically used for throat

    required_auscultation_questions=[],  # Not typically used for standard throat exam

    required_verbal_assessment_questions=[
        "Chief complaint and primary concern description",
        "Onset, duration, and temporal pattern of symptoms",
        "Severity and character of sore throat (sharp, dull, burning, etc.)",
        "Associated symptoms (fever, cough, runny nose, body aches, rash, swollen glands)",
        "Alleviating and aggravating factors",
        "History of difficulty swallowing or dysphagia",
        "Voice changes or hoarseness",
        "Recent illness exposure or sick contacts",
        "Impact on eating, drinking, and sleep",
    ],

    relevant_medical_history_topics=[
        "Prior throat infections (frequency, type, treatment)",
        "Prior throat surgeries (tonsillectomy, adenoidectomy)",
        "Hospitalization for throat-related conditions",
        "Current medications (especially those affecting throat)",
        "Drug allergies (for treatment planning)",
        "Underlying conditions (diabetes, immunosuppression, reflux)",
        "Recent antibiotic use",
    ],

    relevant_lifestyle_topics=[
        "Tobacco use (smoking/vaping)",
        "Alcohol consumption",
        "Acid reflux or GERD symptoms",
        "Voice use/vocal strain (occupation)",
        "Allergies or seasonal triggers",
    ],

    relevant_family_history_topics=[
        "Recurrent throat infections in family",
        "Thyroid disorders in family",
        "Head/neck cancers in family",
    ],

    min_physical_exam_questions=18,  # Minimum 18 physical exam questions (inspection + palpation)
)


# ============================================================================
# PREGNANCY EXAM SPECIFICATION
# ============================================================================

PREGNANCY_EXAM = ExamSpecification(
    exam="pregnancy",
    applicable_genders=["female"],

    required_inspection_questions=[
        "Abdominal appearance - distension, striae, linea nigra, scars",
        "Abdominal skin changes - color, edema, symmetry",
        "Fundal height measurement - position relative to landmarks",
    ],

    required_palpation_questions=[
        "Abdominal palpation - tenderness, masses, organ size",
        "Fundal palpation - size, position, consistency",
        "Fetal movement assessment - presence and character",
    ],

    required_percussion_questions=[],

    required_auscultation_questions=[
        "Fetal heart rate - presence, rate, rhythm",
    ],

    required_verbal_assessment_questions=[
        "Last menstrual period and estimated due date",
        "Pregnancy symptoms and concerns",
        "Fetal movement perception",
        "Vaginal bleeding or discharge changes",
    ],

    relevant_medical_history_topics=[
        "Prior pregnancies and outcomes",
        "Current medications and supplements",
        "Pre-existing medical conditions",
        "Allergies and intolerances",
    ],

    relevant_lifestyle_topics=[
        "Alcohol and substance use",
        "Tobacco use",
        "Exercise and physical activity",
        "Nutrition and dietary concerns",
    ],

    relevant_family_history_topics=[
        "Genetic conditions in family",
        "Pregnancy complications in family",
        "Birth defects in family",
    ],

    min_physical_exam_questions=5,
)


# ============================================================================
# NECK EXAM SPECIFICATION
# ============================================================================

NECK_EXAM = ExamSpecification(
    exam="neck",
    applicable_genders=["male", "female"],

    required_inspection_questions=[
        "Neck appearance - symmetry, posture, position, skin integrity, visible masses or scars",
        "Neck skin - color, erythema, rashes, lesions, temperature, moistness vs dry",
        "Lymph nodes visible - palpable masses visible, anterior cervical vs posterior cervical, size, location",
        "Thyroid gland visible - midline location, size (normal vs enlarged/goiter), symmetry, visible masses",
        "Trachea position - midline vs deviated, symmetry",
        "Neck muscle symmetry - sternocleidomastoid, trapezius, bilateral comparison",
        "Veins - jugular venous distension (JVD), carotid pulses visible, pulsations normal vs abnormal",
    ],

    required_palpation_questions=[
        "Cervical lymph nodes (anterior cervical) - bilateral comparison, size, consistency, tenderness, mobility, matted vs mobile",
        "Cervical lymph nodes (posterior cervical) - bilateral comparison, size, consistency, tenderness, mobility",
        "Submandibular lymph nodes - bilateral comparison, size, consistency, tenderness, normal vs abnormal",
        "Submental lymph nodes - bilateral comparison, size, consistency, palpable vs non-palpable",
        "Thyroid gland palpation - size (normal vs enlarged/goiter), nodules, tenderness, symmetry, consistency, smooth vs irregular",
        "Trachea palpation - midline vs deviated, tenderness, mobility with swallowing",
        "Carotid pulses - bilateral comparison, rate, rhythm, amplitude, character (brisk vs diminished)",
        "Neck muscles (sternocleidomastoid) - bilateral symmetry, tenderness, strength assessment",
        "Neck muscles (trapezius) - bilateral symmetry, tenderness, strength assessment",
        "Neck range of motion - flexion, extension, rotation bilaterally, lateral flexion, limitation vs normal, pain vs painless",
    ],

    required_percussion_questions=[],

    required_auscultation_questions=[
        "Carotid arteries - listen for bruits bilaterally, presence vs absence of abnormal sounds",
        "Thyroid gland - listen for bruits, presence vs absence of vascular sounds",
    ],

    required_verbal_assessment_questions=[
        "Neck pain or stiffness - onset, duration, location, severity, constant vs intermittent",
        "Palpable masses or lumps - location, size, growth, tenderness",
        "Difficulty swallowing (dysphagia) - solids vs liquids, onset, associated symptoms",
        "Voice changes or hoarseness - onset, duration, severity, constant vs intermittent",
        "Recent illness or infection - sore throat, fever, sick contacts",
        "Neck trauma or injury - recent vs remote, mechanism, symptoms",
        "Lymph node swelling - location, onset, duration, tenderness",
    ],

    relevant_medical_history_topics=[
        "Prior thyroid disease or dysfunction",
        "Prior thyroid surgery or radiation",
        "Current thyroid medications",
        "Difficulty swallowing history",
        "Prior neck surgery or procedures",
        "Cancer history (any type)",
        "Lymph node disease history",
    ],

    relevant_lifestyle_topics=[
        "Tobacco use (smoking/vaping)",
        "Alcohol consumption",
        "Occupational exposure (chemicals, radiation)",
        "Voice use/vocal strain (occupation)",
        "Radiation exposure history",
    ],

    relevant_family_history_topics=[
        "Thyroid disease in family",
        "Cancer in family (especially head/neck)",
        "Autoimmune conditions in family",
    ],

    min_physical_exam_questions=16,  # Minimum 16 physical exam questions (inspection + palpation + auscultation)
)


# ============================================================================
# MALE GENITALIA EXAM SPECIFICATION
# ============================================================================

MALE_GENITALIA_EXAM = ExamSpecification(
    exam="male genitalia",
    applicable_genders=["male"],

    required_inspection_questions=[
        "Pubic hair distribution - pattern (male escutcheon), density, pigmentation, presence of lice or nits",
        "Penis appearance - circumcised vs uncircumcised, skin color, lesions, rashes, scars, ulcerations, symmetry",
        "Penile skin - erythema, edema, inflammation, discharge from urethral meatus, character (clear, cloudy, purulent, bloody)",
        "Glans appearance - color (pink vs erythematous), erosions, lesions, phimosis (tight foreskin if uncircumcised)",
        "Urethral meatus - position (ventral vs dorsal vs normal), stenosis, bleeding, discharge",
        "Scrotum appearance - symmetry, skin integrity, color, edema, masses, veins (varicose vs normal)",
        "Scrotum skin - rashes, lesions, ulcerations, inflammation, temperature assessment",
        "Inguinal area - lymph nodes visible, hernias, masses, skin integrity",
    ],

    required_palpation_questions=[
        "Penis palpation - length, diameter, consistency, tenderness, plaques (Peyronie's disease), fibrosis",
        "Testicular palpation (left) - size, consistency (firm vs soft), tenderness, nodules, masses, shape",
        "Testicular palpation (right) - size, consistency (firm vs soft), tenderness, nodules, masses, shape, bilateral comparison",
        "Epididymis palpation (left) - size, consistency, tenderness, nodules, normal vs enlarged",
        "Epididymis palpation (right) - size, consistency, tenderness, nodules, normal vs enlarged, bilateral comparison",
        "Spermatic cord palpation (left) - thickness, consistency, tenderness, nodules, varicosities",
        "Spermatic cord palpation (right) - thickness, consistency, tenderness, nodules, varicosities, bilateral comparison",
        "Inguinal lymph nodes - bilateral palpation, size, consistency, tenderness, mobility, normal vs abnormal",
        "Transillumination (if scrotal mass present) - presence of fluid vs solid, translucence assessment",
        "Cremasteric reflex - presence vs absence, symmetry (normal reflex indicates intact nerve function)",
    ],

    required_percussion_questions=[],

    required_auscultation_questions=[],

    required_verbal_assessment_questions=[
        "Chief concern and primary reason for examination",
        "Erectile dysfunction - onset, duration, frequency, partner involvement, psychological impact",
        "Ejaculatory dysfunction - premature, delayed, or painful ejaculation, timing, circumstances",
        "Penile pain or discomfort - location, character (burning, sharp, dull), frequency, triggers",
        "Testicular or scrotal pain - onset, severity, associated nausea/vomiting, radiation pattern",
        "Genital lesions or discharge - appearance, onset, duration, contagion concerns, treatment attempted",
        "History of STIs - prior infections, testing, treatments, partner notification",
        "Sexual function and satisfaction - libido, frequency of sexual activity, partner concerns",
        "Fertility concerns - desire for children, duration of infertility attempts, partner fertility status",
        "Self-examination practices - frequency, notable changes, lumps or abnormalities noted",
    ],

    relevant_medical_history_topics=[
        "Prior STI diagnoses and treatments",
        "Erectile dysfunction medications (Viagra, Cialis, etc.)",
        "Prior genitourinary surgeries (circumcision, vasectomy, hydrocelectomy)",
        "Prostate disease history",
        "Diabetes (affects erectile function)",
        "Cardiovascular disease (affects erectile function)",
        "Penile or testicular trauma history",
        "Infertility history and evaluation",
        "Testosterone replacement therapy",
    ],

    relevant_lifestyle_topics=[
        "Tobacco use (affects vascular function and ED)",
        "Alcohol consumption (affects sexual function)",
        "Recreational drug use (cocaine, methamphetamine)",
        "Exercise and physical activity",
        "Sexual practices and preferences",
        "Condom use and contraception",
        "Partner relationships and sexual satisfaction",
    ],

    relevant_family_history_topics=[
        "Erectile dysfunction in family members",
        "Infertility in family",
        "Prostate cancer in family",
        "Testicular cancer in family",
        "Early cardiovascular disease (affects erectile function)",
    ],

    min_physical_exam_questions=14,  # Minimum 14 physical exam questions (inspection + palpation + transillumination/reflex)
)


# ============================================================================
# EXAM SPECIFICATIONS REGISTRY
# ============================================================================

EXAM_SPECIFICATIONS = {
    "throat": THROAT_EXAM,
    "pregnancy": PREGNANCY_EXAM,
    "neck": NECK_EXAM,
    "male genitalia": MALE_GENITALIA_EXAM,
    # Add more exam types here as needed
}


def create_default_exam_specification(exam_type: str) -> ExamSpecification:
    """Create a default exam specification for unknown exam types.

    Args:
        exam_type: Type of exam (e.g., "legs", "cardiac")

    Returns:
        A generic ExamSpecification with reasonable defaults
    """
    return ExamSpecification(
        exam=exam_type.lower(),
        applicable_genders=["male", "female", "non-binary", "other", "prefer not to say"],

        required_inspection_questions=[
            f"Overall appearance and symmetry of the {exam_type.lower()} area",
            f"Skin condition - color, integrity, lesions, rashes, or abnormalities",
            f"Visible deformities, swelling, or asymmetry in the {exam_type.lower()}",
            f"Signs of inflammation, erythema, or discoloration",
            f"Muscle tone and bulk - normal vs atrophic or hypertrophied",
            f"Range of motion and functional ability of the {exam_type.lower()}",
        ],

        required_palpation_questions=[
            f"Palpate for tenderness, masses, or abnormal lumps in the {exam_type.lower()}",
            f"Bilateral comparison - symmetry vs asymmetry between left and right sides",
            f"Temperature assessment - normal, warm, or cold compared to contralateral side",
            f"Texture and consistency assessment",
            f"Joint assessment if applicable - stability, range of motion, crepitus",
            f"Lymph node assessment in regional areas",
        ],

        required_percussion_questions=[],

        required_auscultation_questions=[],

        required_verbal_assessment_questions=[
            f"Chief complaint and primary concern",
            f"Onset, duration, and progression of symptoms",
            f"Associated pain, swelling, weakness, or functional limitation",
            f"Recent injury, trauma, or illness affecting the {exam_type.lower()}",
            f"Impact on daily activities and functional status",
            f"Alleviating and aggravating factors",
        ],

        relevant_medical_history_topics=[
            f"Prior injuries or conditions affecting the {exam_type.lower()}",
            f"Prior surgeries related to this area",
            f"Current medications that may affect symptoms",
            f"Underlying conditions (arthritis, neuropathy, vascular disease, etc.)",
            f"Drug allergies",
        ],

        relevant_lifestyle_topics=[
            f"Physical activity level and exercise routine",
            f"Occupational demands on the {exam_type.lower()}",
            f"Recreational activities that may stress this area",
            f"Falls or trauma risk factors",
        ],

        relevant_family_history_topics=[
            f"Family history of musculoskeletal disorders",
            f"Family history of genetic conditions affecting mobility",
            f"Family history of arthritis or joint disease",
        ],

        min_physical_exam_questions=12,  # Generic minimum
    )


def get_exam_specification(exam_type: str) -> ExamSpecification:
    """Get the specification for an exam type.

    Args:
        exam_type: Type of exam (e.g., "throat")

    Returns:
        ExamSpecification for that exam type. If not found, creates a default specification.
    """
    if exam_type.lower() not in EXAM_SPECIFICATIONS:
        logger.warning(
            f"Exam type '{exam_type}' not found in specifications. "
            f"Using auto-generated default specification. "
            f"Available predefined exams: {list(EXAM_SPECIFICATIONS.keys())}"
        )
        return create_default_exam_specification(exam_type)
    return EXAM_SPECIFICATIONS[exam_type.lower()]


def validate_exam_gender_compatibility(exam_type: str, gender: str) -> None:
    """Validate that an exam is applicable for the given gender.

    Args:
        exam_type: Type of exam (e.g., "throat", "pregnancy")
        gender: Patient gender (e.g., "male", "female")

    Raises:
        ValueError: If exam is not applicable for the given gender
    """
    spec = get_exam_specification(exam_type)
    gender_normalized = gender.lower()

    if gender_normalized not in [g.lower() for g in spec.applicable_genders]:
        applicable = ", ".join(spec.applicable_genders)
        raise ValueError(
            f"{spec.exam} exam is not applicable for {gender} patients. "
            f"Applicable genders: {applicable}"
        )
