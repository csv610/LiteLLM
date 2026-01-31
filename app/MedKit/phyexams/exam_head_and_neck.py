"""
Head and Neck Assessment

Evaluate patient head and neck health through clinical examination including
scalp, hair, temporal arteries, facial features, skull, neck anatomy, trachea,
thyroid, and lymph nodes using BaseModel definitions and interactive patient questioning.
"""

import sys
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional

from lite.utils import save_model_response

# Fix import path
from utils.pydantic_prompt_generator import PromptStyle


class ScalpAssessment(BaseModel):
    """Assessment of scalp palpation findings."""
    scalp_symmetry: str = Field(description="Scalp palpation for symmetry - symmetric/asymmetric, smooth bones")
    scalp_bone_abnormalities: str = Field(description="Bone abnormalities on palpation - none/indentations/depressions/irregular contours")
    scalp_lesions: str = Field(description="Scalp lesions or abnormalities - absent/present (describe: location, type, size)")
    scalp_tenderness: str = Field(description="Scalp tenderness - absent/present, areas affected")
    scalp_parasites: str = Field(description="Evidence of parasites or nits - absent/present, location")
    scalp_scabs_crusting: str = Field(description="Scabs or crusting - absent/present, extent")
    scalp_scaliness: str = Field(description="Scaliness or flaking - absent/present, severity")
    scalp_condition_overall: str = Field(description="Overall scalp condition assessment - normal/abnormal, summary")


class HairAssessment(BaseModel):
    """Assessment of hair characteristics and distribution."""
    hair_texture: str = Field(description="Hair texture - smooth/coarse/dry/brittle/fine/silky/other, overall quality")
    hair_color: str = Field(description="Hair color - natural/gray/pigmentation abnormalities, distribution of color")
    hair_distribution: str = Field(description="Hair distribution - symmetric/asymmetric, pattern (temporal/parietal/occipital)")
    hair_thickness: str = Field(description="Hair thickness - normal/fine/thick/variable")
    hair_splitting_ends: str = Field(description="Splitting or cracked ends - absent/present, extent")
    hair_breakage: str = Field(description="Hair breakage - absent/present, severity")
    hair_loss_pattern: str = Field(description="Hair loss pattern - none/bitemporal recession/balding/random alopecia/alopecia totalis, distribution")
    hair_overall_appearance: str = Field(description="Overall hair appearance - healthy/unhealthy/abnormal findings")


class TemporalArteriesAssessment(BaseModel):
    """Assessment of temporal arteries."""
    temporal_artery_course: str = Field(description="Temporal artery course palpation - normal/prominent, location clarity")
    temporal_artery_thickening: str = Field(description="Temporal artery thickening - absent/present, degree")
    temporal_artery_hardness: str = Field(description="Temporal artery hardness or stiffness - absent/present, severity")
    temporal_artery_tenderness: str = Field(description="Temporal artery tenderness - absent/present, severity, bilateral/unilateral")
    temporal_artery_pulsation: str = Field(description="Temporal artery pulsation quality - normal/bounding/weak/absent")
    bruits_skull_eye_auscultation: str = Field(description="Bruits on auscultation over skull/eyes/temporal regions - absent/present (describe location, character)")
    temporal_artery_overall: str = Field(description="Overall temporal artery assessment - normal/abnormal, clinical significance")


class SalivaryGlandsAssessment(BaseModel):
    """Assessment of salivary glands."""
    parotid_gland_symmetry: str = Field(description="Parotid gland symmetry - symmetric/asymmetric, if asymmetric describe")
    parotid_gland_size: str = Field(description="Parotid gland size - normal/enlarged, extent")
    submandibular_gland_symmetry: str = Field(description="Submandibular gland symmetry - symmetric/asymmetric")
    submandibular_gland_size: str = Field(description="Submandibular gland size - normal/enlarged")
    salivary_gland_tenderness: str = Field(description="Salivary gland tenderness - absent/present, location")
    salivary_gland_nodules: str = Field(description="Discrete nodules in salivary glands - absent/present, location, size")
    salivary_duct_expression: str = Field(description="Salivary material expression from ducts - normal/purulent/scanty/thick/other")
    salivary_gland_overall: str = Field(description="Overall salivary gland assessment - normal/abnormal, findings summary")


class FacialFeaturesAssessment(BaseModel):
    """Assessment of facial features and appearance."""
    head_position: str = Field(description="Head position - upright/midline/tilted/forward/other")
    head_movement: str = Field(description="Head movement and control - still/tremor/involuntary movements/dystonia")
    facial_symmetry: str = Field(description="Facial symmetry - symmetric/slight asymmetry/significant asymmetry, describe")
    facial_shape: str = Field(description="Facial shape variations - normal/round/square/oblong/other, describe")
    facial_edema: str = Field(description="Facial edema or puffiness - absent/mild/moderate/severe, distribution (periorbital/generalized/unilateral)")
    facial_features_coarsening: str = Field(description="Coarsened facial features - absent/present, description")
    prominent_eyes: str = Field(description="Prominence of eyes/exophthalmos - absent/mild/moderate/severe, bilateral/unilateral")
    hirsutism: str = Field(description="Hirsutism (excessive hair growth) - absent/present, distribution (facial/body)")
    facial_expression: str = Field(description="Facial expression - normal/masklike/flat/lack of expression/other")
    excessive_perspiration: str = Field(description="Excessive perspiration on face - absent/present, localized/generalized")
    skin_pigmentation: str = Field(description="Skin pigmentation abnormalities - normal/pallor/flushing/cyanosis/jaundice/hyperpigmentation")
    facial_features_overall: str = Field(description="Overall facial features assessment - normal/abnormal, clinical significance")


class SkullAndScalpAssessment(BaseModel):
    """Assessment of skull and scalp inspection."""
    skull_size: str = Field(description="Skull size - normal/microcephaly/macrocephaly")
    skull_shape: str = Field(description="Skull shape - symmetric/asymmetric, describe deformities if present")
    skull_bone_symmetry: str = Field(description="Skull bone symmetry - symmetric/asymmetric, smooth vs irregular")
    skull_bone_abnormalities: str = Field(description="Bony abnormalities (frontal bossing, occipital prominence) - absent/present")
    scalp_lesions_inspection: str = Field(description="Scalp lesions - absent/present (describe: location, type, distribution)")
    scalp_scabs_inspection: str = Field(description="Scalp scabs - absent/present, extent, healing status")
    scalp_tenderness_inspection: str = Field(description="Scalp tenderness on inspection/palpation - absent/present, areas")
    scalp_parasites_inspection: str = Field(description="Parasites or nits visible - absent/present, location")
    scalp_scaliness_inspection: str = Field(description="Scaliness or dandruff - absent/present, severity")
    skull_scalp_overall: str = Field(description="Overall skull and scalp assessment - normal/abnormal, summary")


class HairPatternAssessment(BaseModel):
    """Assessment of hair distribution patterns."""
    male_pattern_baldness: str = Field(description="Male pattern baldness or bitemporal recession - absent/present, stage/extent")
    female_pattern_baldness: str = Field(description="Female pattern hair loss - absent/present, pattern (vertex/crown/diffuse)")
    alopecia_areata: str = Field(description="Random alopecia or alopecia areata - absent/present, location, extent")
    alopecia_totalis: str = Field(description="Alopecia totalis (complete hair loss on scalp) - absent/present")
    hair_distribution_pattern: str = Field(description="Hair distribution pattern - normal/abnormal, describe pattern")
    hair_loss_progression: str = Field(description="Hair loss progression - stable/progressive/improving, timeline")
    hair_pattern_overall: str = Field(description="Overall hair pattern assessment - normal/abnormal, clinical significance")


class NeckInspectionAssessment(BaseModel):
    """Assessment of neck inspection findings."""
    neck_position: str = Field(description="Neck position in usual posture - midline/tilted/forward/posterior positioning")
    neck_symmetry: str = Field(description="Neck symmetry bilateral inspection - symmetric/asymmetric, describe")
    sternocleidomastoid_muscle_symmetry: str = Field(description="Sternocleidomastoid muscles symmetry and size - symmetric/asymmetric")
    trapezius_muscle_symmetry: str = Field(description="Trapezius muscles symmetry and size - symmetric/asymmetric")
    torticollis_present: str = Field(description="Torticollis (wryneck) - absent/present, degree")
    neck_webbing: str = Field(description="Neck webbing (pterygium colli) - absent/present, extent")
    posterior_skinfolds: str = Field(description="Excessive posterior skinfolds - absent/present, describe")
    neck_shortness: str = Field(description="Unusually short neck - absent/present, estimate length")
    jugular_vein_distention: str = Field(description="Jugular vein distention (JVD) - absent/mild/moderate/severe, bilateral/unilateral")
    carotid_artery_prominence: str = Field(description="Prominence of carotid arteries - absent/normal/prominent/hyperpulsatile")
    neck_edema: str = Field(description="Neck edema - absent/present, distribution, severity")
    neck_inspection_overall: str = Field(description="Overall neck inspection findings - normal/abnormal, summary")


class TrachealAssessment(BaseModel):
    """Assessment of trachea position and findings."""
    trachea_position_midline: str = Field(description="Trachea position in midline - midline/deviated left/deviated right, degree")
    trachea_masses: str = Field(description="Tracheal masses or swelling - absent/present, location, size")
    trachea_deviation_swallowing: str = Field(description="Trachea deviation during swallowing - absent/present, describe")
    trachea_appearance: str = Field(description="Trachea appearance - normal/prominent/tender/other findings")
    tracheal_tugging: str = Field(description="Tracheal tug (tugging synchronous with pulse) - absent/present")
    trachea_overall: str = Field(description="Overall tracheal assessment - normal/abnormal, clinical significance")


class RangeOfMotionAssessment(BaseModel):
    """Assessment of head and neck range of motion."""
    neck_flexion: str = Field(description="Neck flexion (chin to chest) - normal/limited, degree, pain/discomfort")
    neck_extension: str = Field(description="Neck extension (looking up) - normal/limited, degree, pain/discomfort")
    neck_rotation: str = Field(description="Neck rotation (turning head side to side) - normal/limited bilaterally, degree, pain")
    lateral_flexion: str = Field(description="Lateral flexion (bending ear to shoulder) - normal/limited bilaterally, degree")
    rom_smoothness: str = Field(description="Smoothness of motion - smooth/jerky/restricted/guarded")
    rom_pain: str = Field(description="Pain with range of motion - absent/present (describe location, severity)")
    rom_dizziness: str = Field(description="Dizziness or vertigo with motion - absent/present")
    rom_overall: str = Field(description="Overall range of motion assessment - normal/abnormal, limitations")


class NeckPalpationAssessment(BaseModel):
    """Assessment of palpable structures in the neck."""
    trachea_palpation: str = Field(description="Trachea palpation for midline position - midline/deviated, tenderness")
    hyoid_bone: str = Field(description="Hyoid bone palpation - palpable/not palpable, smooth, tenderness")
    thyroid_cartilage: str = Field(description="Thyroid cartilage palpation - smooth/tender/irregular, movement with swallowing")
    cricoid_cartilage: str = Field(description="Cricoid cartilage palpation - smooth/tender/prominent, movement")
    tracheal_rings: str = Field(description="Cartilaginous tracheal rings palpation while swallowing - distinct/tender/prominent")
    neck_lymph_nodes: str = Field(description="Neck lymph nodes palpation - absent/present, size, consistency, mobility, tenderness, location")
    lymph_node_matting: str = Field(description="Lymph node matting or fixation - absent/present, extent")
    lymph_node_warmth: str = Field(description="Warmth over lymph nodes - absent/present, suggests infection")
    neck_palpation_overall: str = Field(description="Overall neck palpation findings - normal/abnormal, summary")


class ThyroidAssessment(BaseModel):
    """Comprehensive thyroid gland assessment."""
    thyroid_visibility: str = Field(description="Thyroid visibility on inspection - not visible/slightly visible/prominent")
    thyroid_symmetry: str = Field(description="Thyroid symmetry - symmetric/asymmetric, if asymmetric describe lobes")
    thyroid_size: str = Field(description="Thyroid size - normal (not palpable or <2cm)/mildly enlarged/moderately enlarged/severely enlarged")
    thyroid_shape: str = Field(description="Thyroid shape - normal/irregular/asymmetric nodules")
    thyroid_configuration: str = Field(description="Thyroid configuration - smooth/nodular/multinodular")
    thyroid_consistency: str = Field(description="Thyroid consistency - pliable/firm/hard/gritty sensation/tender")
    thyroid_mobility: str = Field(description="Thyroid mobility with swallowing - moves freely/restricted/fixed")
    thyroid_nodules: str = Field(description="Thyroid nodules - absent/present, location, size, firm/soft/hard, tender/non-tender")
    thyroid_bruit: str = Field(description="Auscultation for vascular sounds/bruit - absent/present, character, bilateral/unilateral")
    thyroid_tenderness: str = Field(description="Thyroid tenderness - absent/mild/moderate/severe, focal/diffuse")
    thyroid_lower_border: str = Field(description="Lower border of thyroid - at sternal notch/below sternal notch/not palpable")
    thyroid_overall: str = Field(description="Overall thyroid assessment - normal/abnormal, clinical significance, recommendations")


class AssessmentSummary(BaseModel):
    """Overall head and neck assessment summary and clinical recommendations."""
    head_findings_summary: str = Field(description="Summary of significant head findings - normal/abnormal, describe major findings")
    scalp_hair_findings: str = Field(description="Scalp and hair findings - normal/abnormal, describe pathology if present")
    facial_features_findings: str = Field(description="Facial features findings - normal/abnormal, note asymmetry or unusual features")
    vascular_findings: str = Field(description="Temporal artery and vascular findings - normal/abnormal, bruits, tenderness")
    neck_anatomy_findings: str = Field(description="Neck anatomy findings - normal/abnormal, note asymmetry, masses, or deformities")
    trachea_findings: str = Field(description="Trachea findings - normal/midline/deviated, masses absent/present")
    thyroid_findings: str = Field(description="Thyroid findings - normal/enlarged (size)/nodular, consistency, mobility")
    lymph_node_findings: str = Field(description="Lymph node findings - normal/enlarged, location, characteristics, concerning features")
    range_of_motion_status: str = Field(description="Range of motion status - normal/limited, restrictions noted")
    major_abnormalities: str = Field(description="Major abnormalities requiring clinical attention - list all significant findings")
    recommended_workup: str = Field(description="Recommended diagnostic workup if abnormalities noted - imaging/ultrasound/fine needle aspiration/other")
    specialist_referral: str = Field(description="Specialist referral recommendations - ENT/endocrinology/neurology/vascular/oncology and rationale")
    follow_up_plan: str = Field(description="Follow-up plan - routine monitoring/focused re-exam/imaging follow-up/specialist evaluation")


class HeadAndNeckAssessment(BaseModel):
    """
    Comprehensive head and neck assessment.

    Organized as a collection of BaseModel sections representing distinct aspects
    of head and neck examination. Includes assessment of scalp, hair, facial features,
    skull, neck anatomy, trachea, thyroid, lymph nodes, temporal arteries, and
    salivary glands.
    """
    # Scalp assessment
    scalp_assessment: ScalpAssessment

    # Hair assessment
    hair_assessment: HairAssessment

    # Temporal arteries assessment
    temporal_arteries_assessment: TemporalArteriesAssessment

    # Salivary glands assessment
    salivary_glands_assessment: SalivaryGlandsAssessment

    # Facial features assessment
    facial_features_assessment: FacialFeaturesAssessment

    # Skull and scalp inspection
    skull_and_scalp_assessment: SkullAndScalpAssessment

    # Hair pattern assessment
    hair_pattern_assessment: HairPatternAssessment

    # Neck inspection assessment
    neck_inspection_assessment: NeckInspectionAssessment

    # Trachea assessment
    trachea_assessment: TrachealAssessment

    # Range of motion assessment
    range_of_motion_assessment: RangeOfMotionAssessment

    # Neck palpation assessment
    neck_palpation_assessment: NeckPalpationAssessment

    # Thyroid assessment
    thyroid_assessment: ThyroidAssessment

    # Final assessment
    assessment_summary: AssessmentSummary


def ask_head_and_neck_questions() -> dict:
    """
    Ask patient head and neck assessment questions interactively.
    Returns a dictionary of patient responses to be used in assessment.
    """
    print("\n" + "="*60)
    print("HEAD AND NECK ASSESSMENT")
    print("="*60)
    print("\nMEASURES: Evaluates head and neck health through assessment of:")
    print("  • Scalp condition, hair texture, and hair loss patterns")
    print("  • Temporal arteries (pulsation, thickening, tenderness)")
    print("  • Facial features, symmetry, and skin characteristics")
    print("  • Skull size, shape, and bone abnormalities")
    print("  • Neck position, symmetry, and muscle function")
    print("  • Trachea position and movement")
    print("  • Thyroid size, nodules, and function")
    print("  • Range of motion (flexion, extension, rotation)")

    print("\nTOP 10 KEY ASSESSMENT QUESTIONS:")
    print("  1. Do you have any scalp lesions, tenderness, or parasites (lice)?")
    print("  2. Have you noticed hair loss patterns (bitemporal, balding, patchy)?")
    print("  3. Do your temporal arteries feel thickened, hard, or tender?")
    print("  4. Is your face symmetric with normal features, or do you notice asymmetry?")
    print("  5. Do you have facial puffiness, coarsened features, or excessive sweating?")
    print("  6. Is your skull symmetrical and free of bumps or deformities?")
    print("  7. Is your neck positioned midline and symmetric bilaterally?")
    print("  8. Do you have fullness in the neck, tracheal deviation, or masses?")
    print("  9. Do you have a palpable thyroid, nodules, or thyroid symptoms?")
    print(" 10. Can you move your neck freely (flexion, extension, rotation)?")

    print("\n" + "="*60)
    print("HEAD AND NECK ASSESSMENT QUESTIONNAIRE")
    print("="*60)

    responses = {}

    # SCALP ASSESSMENT
    print("\n--- SCALP ASSESSMENT ---")
    print("Examining scalp through inspection and palpation")
    responses['scalp_symmetry'] = input("Is the scalp symmetric with smooth, distinguishable bones? (yes/no): ").strip()
    responses['scalp_abnormalities'] = input("Any indentations, depressions, or bone irregularities? (no/yes, describe): ").strip()
    responses['scalp_lesions'] = input("Scalp lesions, sores, or abnormalities? (no/yes, location/type/size): ").strip()
    responses['scalp_tenderness'] = input("Scalp tenderness when touched? (no/yes, where): ").strip()
    responses['scalp_parasites'] = input("Evidence of parasites or nits (lice)? (no/yes): ").strip()
    responses['scalp_scabs'] = input("Scabs or crusting on scalp? (no/yes, extent): ").strip()
    responses['scalp_flaking'] = input("Scaliness, flaking, or dandruff? (no/yes, severity): ").strip()

    # HAIR ASSESSMENT
    print("\n--- HAIR ASSESSMENT ---")
    print("Examining hair texture, color, and distribution")
    responses['hair_texture'] = input("Hair texture - smooth/coarse/dry/brittle/fine/silky? (describe): ").strip()
    responses['hair_color'] = input("Hair color - natural/gray/other discoloration? (describe): ").strip()
    responses['hair_distribution'] = input("Hair distribution - symmetric or asymmetric? (describe): ").strip()
    responses['hair_thickness'] = input("Hair thickness - normal/fine/thick/variable? (describe): ").strip()
    responses['hair_splitting'] = input("Splitting or cracked ends? (no/yes, extent): ").strip()
    responses['hair_breakage'] = input("Hair breakage - absent/present? (severity): ").strip()
    responses['hair_loss_pattern'] = input("Hair loss pattern - none/bitemporal/balding/random/alopecia totalis? (describe): ").strip()

    # TEMPORAL ARTERIES ASSESSMENT
    print("\n--- TEMPORAL ARTERIES ---")
    print("Examining temporal arteries by palpation and auscultation")
    responses['temporal_artery_course'] = input("Temporal artery course on palpation - normal/prominent? (describe): ").strip()
    responses['temporal_artery_thickening'] = input("Temporal artery thickening? (no/yes, degree): ").strip()
    responses['temporal_artery_hardness'] = input("Temporal artery hardness or stiffness? (no/yes): ").strip()
    responses['temporal_artery_tenderness'] = input("Temporal artery tenderness? (no/yes, bilateral/unilateral, severity): ").strip()
    responses['temporal_pulsation'] = input("Temporal artery pulsation quality? (normal/bounding/weak/absent): ").strip()
    responses['bruits_auscultation'] = input("Bruits on auscultation over skull/eyes/temples? (no/yes, describe): ").strip()

    # SALIVARY GLANDS ASSESSMENT
    print("\n--- SALIVARY GLANDS ---")
    print("Examining parotid and submandibular glands")
    responses['parotid_symmetry'] = input("Parotid glands symmetric? (yes/no, if no describe): ").strip()
    responses['parotid_size'] = input("Parotid gland size - normal/enlarged? (describe): ").strip()
    responses['submandibular_symmetry'] = input("Submandibular glands symmetric? (yes/no): ").strip()
    responses['submandibular_size'] = input("Submandibular gland size - normal/enlarged? (describe): ").strip()
    responses['salivary_tenderness'] = input("Salivary gland tenderness? (no/yes, location): ").strip()
    responses['salivary_nodules'] = input("Discrete nodules in salivary glands? (no/yes, location/size): ").strip()
    responses['salivary_duct_expression'] = input("Salivary material expression from ducts - normal/purulent/scanty/thick? (describe): ").strip()

    # FACIAL FEATURES ASSESSMENT
    print("\n--- FACIAL FEATURES ---")
    print("Examining facial appearance, symmetry, and features")
    responses['head_position'] = input("Head position - upright and midline? (yes/no, describe if abnormal): ").strip()
    responses['head_movement'] = input("Head movement - still and controlled? (yes/no, any tremor/involuntary movements): ").strip()
    responses['facial_symmetry'] = input("Facial symmetry - symmetric or asymmetric? (describe): ").strip()
    responses['facial_shape'] = input("Facial shape - normal/round/square/oblong/other? (describe): ").strip()
    responses['facial_edema'] = input("Facial edema or puffiness? (no/yes, severity, distribution): ").strip()
    responses['facial_coarsening'] = input("Coarsened facial features? (no/yes, describe): ").strip()
    responses['prominent_eyes'] = input("Prominent eyes or bulging? (no/yes, degree, bilateral/unilateral): ").strip()
    responses['hirsutism'] = input("Excessive facial or body hair (hirsutism)? (no/yes, distribution): ").strip()
    responses['facial_expression'] = input("Facial expression - normal/masklike/flat/lack of expression? (describe): ").strip()
    responses['perspiration'] = input("Excessive perspiration on face? (no/yes, localized/generalized): ").strip()
    responses['skin_pigmentation'] = input("Skin pigmentation abnormalities - normal/pallor/flushing/cyanosis/jaundice? (describe): ").strip()

    # SKULL AND SCALP INSPECTION
    print("\n--- SKULL AND SCALP INSPECTION ---")
    responses['skull_size'] = input("Skull size - normal/microcephaly/macrocephaly? (describe): ").strip()
    responses['skull_shape'] = input("Skull shape - symmetric or deformities? (describe): ").strip()
    responses['skull_bone_symmetry'] = input("Skull bones symmetric and smooth? (yes/no, describe if abnormal): ").strip()
    responses['skull_bony_abnormalities'] = input("Bony abnormalities (frontal bossing, occipital prominence)? (no/yes, describe): ").strip()

    # HAIR PATTERN ASSESSMENT
    print("\n--- HAIR PATTERN ---")
    responses['male_pattern_baldness'] = input("Male pattern baldness or bitemporal recession? (no/yes, stage): ").strip()
    responses['female_pattern_loss'] = input("Female pattern hair loss? (no/yes, describe pattern): ").strip()
    responses['alopecia_areata'] = input("Random alopecia (patchy hair loss)? (no/yes, location): ").strip()
    responses['alopecia_totalis'] = input("Complete hair loss on scalp (alopecia totalis)? (no/yes): ").strip()

    # NECK INSPECTION
    print("\n--- NECK INSPECTION ---")
    print("Examining neck position, muscles, and symmetry")
    responses['neck_position'] = input("Neck position - upright, midline, and still? (yes/no, describe if abnormal): ").strip()
    responses['neck_symmetry'] = input("Neck symmetric bilaterally? (yes/no, describe if asymmetric): ").strip()
    responses['sternocleidomastoid'] = input("Sternocleidomastoid muscles symmetric? (yes/no, describe): ").strip()
    responses['trapezius_muscles'] = input("Trapezius muscles symmetric? (yes/no, describe): ").strip()
    responses['torticollis'] = input("Torticollis (wryneck) present? (no/yes, degree): ").strip()
    responses['neck_webbing'] = input("Neck webbing (pterygium colli)? (no/yes, extent): ").strip()
    responses['posterior_skinfolds'] = input("Excessive posterior skinfolds? (no/yes, describe): ").strip()
    responses['neck_shortness'] = input("Unusually short neck? (no/yes, estimate): ").strip()
    responses['jugular_vein_distention'] = input("Jugular vein distention (JVD)? (no/yes, severity, bilateral/unilateral): ").strip()
    responses['carotid_prominence'] = input("Prominent carotid arteries? (no/yes, hyperpulsatile): ").strip()
    responses['neck_edema'] = input("Neck edema? (no/yes, distribution, severity): ").strip()

    # TRACHEA ASSESSMENT
    print("\n--- TRACHEA ---")
    print("Examining trachea position and movement")
    responses['trachea_position'] = input("Trachea midline or deviated? (midline/left/right, degree): ").strip()
    responses['trachea_masses'] = input("Tracheal masses or swelling? (no/yes, location/size): ").strip()
    responses['trachea_deviation_swallowing'] = input("Trachea deviates during swallowing? (no/yes, describe): ").strip()
    responses['tracheal_tug'] = input("Tracheal tug synchronous with pulse? (no/yes): ").strip()

    # RANGE OF MOTION
    print("\n--- RANGE OF MOTION ---")
    print("Evaluating head and neck flexibility")
    responses['neck_flexion'] = input("Neck flexion (chin to chest) - normal/limited? (describe, pain/discomfort): ").strip()
    responses['neck_extension'] = input("Neck extension (looking up) - normal/limited? (describe, pain): ").strip()
    responses['neck_rotation'] = input("Neck rotation (turning head) - normal/limited bilaterally? (describe, pain): ").strip()
    responses['lateral_flexion'] = input("Lateral flexion (ear to shoulder) - normal/limited? (describe): ").strip()
    responses['rom_smoothness'] = input("Motion smooth or jerky/restricted? (smooth/jerky/guarded): ").strip()
    responses['rom_dizziness'] = input("Dizziness or vertigo with motion? (no/yes): ").strip()

    # NECK PALPATION
    print("\n--- NECK PALPATION ---")
    print("Palpating neck structures")
    responses['trachea_palpation'] = input("Trachea palpation - midline or deviated? (midline/deviated, tenderness): ").strip()
    responses['hyoid_bone'] = input("Hyoid bone palpable? (yes/no, smooth, tender): ").strip()
    responses['thyroid_cartilage'] = input("Thyroid cartilage - smooth/tender/moves with swallowing? (describe): ").strip()
    responses['cricoid_cartilage'] = input("Cricoid cartilage palpable? (yes/no, tender/normal): ").strip()
    responses['tracheal_rings'] = input("Cartilaginous tracheal rings distinct? (yes/no, tender): ").strip()
    responses['neck_lymph_nodes'] = input("Neck lymph nodes palpable? (no/yes, location, size, consistency, mobility, tenderness): ").strip()
    responses['lymph_node_matting'] = input("Lymph node matting or fixation? (no/yes, extent): ").strip()
    responses['lymph_node_warmth'] = input("Warmth over lymph nodes? (no/yes, suggests infection): ").strip()

    # THYROID ASSESSMENT
    print("\n--- THYROID GLAND ---")
    print("Comprehensive thyroid examination")
    responses['thyroid_visibility'] = input("Thyroid visible on inspection? (not visible/slightly visible/prominent, describe): ").strip()
    responses['thyroid_symmetry'] = input("Thyroid symmetric? (yes/no, if asymmetric describe lobes): ").strip()
    responses['thyroid_size'] = input("Thyroid size - normal/mildly enlarged/moderately enlarged/severely enlarged? (estimate): ").strip()
    responses['thyroid_shape'] = input("Thyroid shape - normal/irregular/nodules? (describe): ").strip()
    responses['thyroid_configuration'] = input("Thyroid configuration - smooth/nodular/multinodular? (describe): ").strip()
    responses['thyroid_consistency'] = input("Thyroid consistency - pliable/firm/hard/gritty/tender? (describe): ").strip()
    responses['thyroid_mobility'] = input("Thyroid moves freely with swallowing? (yes/no, describe): ").strip()
    responses['thyroid_nodules'] = input("Thyroid nodules present? (no/yes, location, size, firm/soft/hard, tender): ").strip()
    responses['thyroid_bruit'] = input("Bruit on auscultation over thyroid? (no/yes, character): ").strip()
    responses['thyroid_tenderness'] = input("Thyroid tenderness? (no/yes, focal/diffuse, severity): ").strip()
    responses['thyroid_lower_border'] = input("Lower border of thyroid at sternal notch or below? (at notch/below/not palpable): ").strip()

    return responses


def create_head_and_neck_assessment_from_responses(patient_name: str, responses: dict, output_path: Optional[Path] = None) -> HeadAndNeckAssessment:
    """
    Create a structured head and neck assessment object from collected patient responses.

    Args:
        patient_name: Name of the patient
        responses: Dictionary of patient responses from questions
        output_path: Optional path to save JSON output

    Returns:
        HeadAndNeckAssessment: Validated assessment object
    """
    # Create assessment object from responses
    assessment_data = {
        "scalp_assessment": {
            "scalp_symmetry": responses.get('scalp_symmetry', ''),
            "scalp_bone_abnormalities": responses.get('scalp_abnormalities', ''),
            "scalp_lesions": responses.get('scalp_lesions', ''),
            "scalp_tenderness": responses.get('scalp_tenderness', ''),
            "scalp_parasites": responses.get('scalp_parasites', ''),
            "scalp_scabs_crusting": responses.get('scalp_scabs', ''),
            "scalp_scaliness": responses.get('scalp_flaking', ''),
            "scalp_condition_overall": "To be determined by clinician"
        },
        "hair_assessment": {
            "hair_texture": responses.get('hair_texture', ''),
            "hair_color": responses.get('hair_color', ''),
            "hair_distribution": responses.get('hair_distribution', ''),
            "hair_thickness": responses.get('hair_thickness', ''),
            "hair_splitting_ends": responses.get('hair_splitting', ''),
            "hair_breakage": responses.get('hair_breakage', ''),
            "hair_loss_pattern": responses.get('hair_loss_pattern', ''),
            "hair_overall_appearance": "To be determined by clinician"
        },
        "temporal_arteries_assessment": {
            "temporal_artery_course": responses.get('temporal_artery_course', ''),
            "temporal_artery_thickening": responses.get('temporal_artery_thickening', ''),
            "temporal_artery_hardness": responses.get('temporal_artery_hardness', ''),
            "temporal_artery_tenderness": responses.get('temporal_artery_tenderness', ''),
            "temporal_artery_pulsation": responses.get('temporal_pulsation', ''),
            "bruits_skull_eye_auscultation": responses.get('bruits_auscultation', ''),
            "temporal_artery_overall": "To be determined by clinician"
        },
        "salivary_glands_assessment": {
            "parotid_gland_symmetry": responses.get('parotid_symmetry', ''),
            "parotid_gland_size": responses.get('parotid_size', ''),
            "submandibular_gland_symmetry": responses.get('submandibular_symmetry', ''),
            "submandibular_gland_size": responses.get('submandibular_size', ''),
            "salivary_gland_tenderness": responses.get('salivary_tenderness', ''),
            "salivary_gland_nodules": responses.get('salivary_nodules', ''),
            "salivary_duct_expression": responses.get('salivary_duct_expression', ''),
            "salivary_gland_overall": "To be determined by clinician"
        },
        "facial_features_assessment": {
            "head_position": responses.get('head_position', ''),
            "head_movement": responses.get('head_movement', ''),
            "facial_symmetry": responses.get('facial_symmetry', ''),
            "facial_shape": responses.get('facial_shape', ''),
            "facial_edema": responses.get('facial_edema', ''),
            "facial_features_coarsening": responses.get('facial_coarsening', ''),
            "prominent_eyes": responses.get('prominent_eyes', ''),
            "hirsutism": responses.get('hirsutism', ''),
            "facial_expression": responses.get('facial_expression', ''),
            "excessive_perspiration": responses.get('perspiration', ''),
            "skin_pigmentation": responses.get('skin_pigmentation', ''),
            "facial_features_overall": "To be determined by clinician"
        },
        "skull_and_scalp_assessment": {
            "skull_size": responses.get('skull_size', ''),
            "skull_shape": responses.get('skull_shape', ''),
            "skull_bone_symmetry": responses.get('skull_bone_symmetry', ''),
            "skull_bone_abnormalities": responses.get('skull_bony_abnormalities', ''),
            "scalp_lesions_inspection": "Assessed in scalp section",
            "scalp_scabs_inspection": "Assessed in scalp section",
            "scalp_tenderness_inspection": "Assessed in scalp section",
            "scalp_parasites_inspection": "Assessed in scalp section",
            "scalp_scaliness_inspection": "Assessed in scalp section",
            "skull_scalp_overall": "To be determined by clinician"
        },
        "hair_pattern_assessment": {
            "male_pattern_baldness": responses.get('male_pattern_baldness', ''),
            "female_pattern_baldness": responses.get('female_pattern_loss', ''),
            "alopecia_areata": responses.get('alopecia_areata', ''),
            "alopecia_totalis": responses.get('alopecia_totalis', ''),
            "hair_distribution_pattern": responses.get('hair_distribution', ''),
            "hair_loss_progression": "To be assessed on follow-up",
            "hair_pattern_overall": "To be determined by clinician"
        },
        "neck_inspection_assessment": {
            "neck_position": responses.get('neck_position', ''),
            "neck_symmetry": responses.get('neck_symmetry', ''),
            "sternocleidomastoid_muscle_symmetry": responses.get('sternocleidomastoid', ''),
            "trapezius_muscle_symmetry": responses.get('trapezius_muscles', ''),
            "torticollis_present": responses.get('torticollis', ''),
            "neck_webbing": responses.get('neck_webbing', ''),
            "posterior_skinfolds": responses.get('posterior_skinfolds', ''),
            "neck_shortness": responses.get('neck_shortness', ''),
            "jugular_vein_distention": responses.get('jugular_vein_distention', ''),
            "carotid_artery_prominence": responses.get('carotid_prominence', ''),
            "neck_edema": responses.get('neck_edema', ''),
            "neck_inspection_overall": "To be determined by clinician"
        },
        "trachea_assessment": {
            "trachea_position_midline": responses.get('trachea_position', ''),
            "trachea_masses": responses.get('trachea_masses', ''),
            "trachea_deviation_swallowing": responses.get('trachea_deviation_swallowing', ''),
            "trachea_appearance": "To be assessed",
            "tracheal_tugging": responses.get('tracheal_tug', ''),
            "trachea_overall": "To be determined by clinician"
        },
        "range_of_motion_assessment": {
            "neck_flexion": responses.get('neck_flexion', ''),
            "neck_extension": responses.get('neck_extension', ''),
            "neck_rotation": responses.get('neck_rotation', ''),
            "lateral_flexion": responses.get('lateral_flexion', ''),
            "rom_smoothness": responses.get('rom_smoothness', ''),
            "rom_pain": "To be assessed by clinician",
            "rom_dizziness": responses.get('rom_dizziness', ''),
            "rom_overall": "To be determined by clinician"
        },
        "neck_palpation_assessment": {
            "trachea_palpation": responses.get('trachea_palpation', ''),
            "hyoid_bone": responses.get('hyoid_bone', ''),
            "thyroid_cartilage": responses.get('thyroid_cartilage', ''),
            "cricoid_cartilage": responses.get('cricoid_cartilage', ''),
            "tracheal_rings": responses.get('tracheal_rings', ''),
            "neck_lymph_nodes": responses.get('neck_lymph_nodes', ''),
            "lymph_node_matting": responses.get('lymph_node_matting', ''),
            "lymph_node_warmth": responses.get('lymph_node_warmth', ''),
            "neck_palpation_overall": "To be determined by clinician"
        },
        "thyroid_assessment": {
            "thyroid_visibility": responses.get('thyroid_visibility', ''),
            "thyroid_symmetry": responses.get('thyroid_symmetry', ''),
            "thyroid_size": responses.get('thyroid_size', ''),
            "thyroid_shape": responses.get('thyroid_shape', ''),
            "thyroid_configuration": responses.get('thyroid_configuration', ''),
            "thyroid_consistency": responses.get('thyroid_consistency', ''),
            "thyroid_mobility": responses.get('thyroid_mobility', ''),
            "thyroid_nodules": responses.get('thyroid_nodules', ''),
            "thyroid_bruit": responses.get('thyroid_bruit', ''),
            "thyroid_tenderness": responses.get('thyroid_tenderness', ''),
            "thyroid_lower_border": responses.get('thyroid_lower_border', ''),
            "thyroid_overall": "To be determined by clinician"
        },
        "assessment_summary": {
            "head_findings_summary": "To be determined by clinician",
            "scalp_hair_findings": "To be determined by clinician",
            "facial_features_findings": "To be determined by clinician",
            "vascular_findings": "To be determined by clinician",
            "neck_anatomy_findings": "To be determined by clinician",
            "trachea_findings": "To be determined by clinician",
            "thyroid_findings": "To be determined by clinician",
            "lymph_node_findings": "To be determined by clinician",
            "range_of_motion_status": "To be determined by clinician",
            "major_abnormalities": "None noted on initial assessment",
            "recommended_workup": "Routine assessment - additional imaging if abnormalities noted",
            "specialist_referral": "Not indicated at this time",
            "follow_up_plan": "Routine follow-up as indicated by clinical findings"
        }
    }

    # Create assessment object
    assessment = HeadAndNeckAssessment(**assessment_data)

    # Save to file if path provided
    if output_path is None:
        output_path = Path("outputs") / f"{patient_name.lower().replace(' ', '_')}_head_and_neck.json"

    # Create outputs directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save assessment as JSON
    save_model_response(assessment, output_path)

    print(f"\n✓ Assessment saved to: {output_path}")

    return assessment


def evaluate_head_and_neck(
    patient_name: str,
    output_path: Optional[Path] = None,
    use_schema_prompt: bool = True,
    prompt_style: PromptStyle = PromptStyle.DETAILED,
) -> HeadAndNeckAssessment:
    """
    Evaluate patient head and neck health through interactive questionnaire.

    Args:
        patient_name: Name or identifier of the patient
        output_path: Optional path to save JSON output. Defaults to outputs/{patient_name}_head_and_neck.json
        use_schema_prompt: Whether to use PydanticPromptGenerator for schema
        prompt_style: Style of schema prompt (DETAILED, CONCISE, TECHNICAL)

    Returns:
        HeadAndNeckAssessment: Validated head and neck assessment object
    """
    if not patient_name or not patient_name.strip():
        raise ValueError("Patient name cannot be empty")

    # Ask patient questions interactively
    print(f"\nStarting head and neck assessment for: {patient_name}")
    responses = ask_head_and_neck_questions()

    # Create assessment from responses
    assessment = create_head_and_neck_assessment_from_responses(patient_name, responses, output_path)

    return assessment


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate patient head and neck health through structured assessment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default - saves to outputs/patient_head_and_neck.json
  python exam_head_and_neck.py "John Doe"

  # Custom output path
  python exam_head_and_neck.py "John Doe" -o custom_assessment.json

  # With concise prompting
  python exam_head_and_neck.py "John Doe" --concise

Head and Neck Assessment Protocol:
  1. SCALP ASSESSMENT: Palpate for symmetry, smooth bones, lesions, parasites
     - Document any indentations, depressions, scabs, tenderness
     - Check for scalp condition (normal/abnormal)

  2. HAIR ASSESSMENT: Evaluate texture, color, thickness, and distribution
     - Assess for splitting/cracking, breakage, hair loss patterns
     - Note male/female pattern baldness or alopecia

  3. FACIAL FEATURES: Inspect head position, symmetry, and facial appearance
     - Note any edema, coarsening, prominent eyes, hirsutism
     - Evaluate facial expression and skin pigmentation

  4. TEMPORAL ARTERIES: Palpate for course, thickening, hardness, tenderness
     - Auscultate for bruits over skull, eyes, and temporal regions
     - Document any abnormalities concerning for temporal arteritis

  5. SALIVARY GLANDS: Inspect and palpate for symmetry, enlargement, tenderness
     - Express salivary ducts to assess material quality
     - Note any discrete nodules or asymmetry

  6. NECK INSPECTION: Assess position, symmetry, and muscle development
     - Note JVD, carotid prominence, webbing, short neck, edema
     - Check for torticollis or other abnormalities

  7. TRACHEA: Inspect position (midline/deviated) and movement with swallowing
     - Assess for masses, deviation, or tracheal tug
     - Document any abnormalities

  8. THYROID: Palpate for size, symmetry, consistency, mobility, nodules
     - Auscultate for bruits if enlarged
     - Document nodule characteristics and lower border position

  9. LYMPH NODES: Palpate neck nodes for size, consistency, mobility, tenderness
     - Note any matting, fixation, warmth, or concerning characteristics
     - Assess regional distribution and characteristics
        """
    )
    parser.add_argument("patient", nargs='+', help="Name or identifier of the patient")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Path to save JSON output. Defaults to outputs/{patient_name}_head_and_neck.json"
    )
    parser.add_argument(
        "--concise",
        action="store_true",
        help="Use concise prompt style (faster generation)"
    )

    args = parser.parse_args()

    try:
        patient_name = " ".join(args.patient)
        prompt_style = PromptStyle.CONCISE if args.concise else PromptStyle.DETAILED

        result = evaluate_head_and_neck(
            patient_name=patient_name,
            output_path=args.output,
            prompt_style=prompt_style,
        )
        print("✓ Success!")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
