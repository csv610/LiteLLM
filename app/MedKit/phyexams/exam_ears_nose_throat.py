"""
Ears, Nose, and Throat (ENT) Assessment with Patient/Nurse Answer Separation

This refactored module separates ENT assessment questions into two categories:
- PatientAnswer: Questions patients can self-report (symptoms, history, subjective findings)
- NurseAnswer: Questions requiring clinical examination, measurement, or visual assessment
These are combined into a final MedicalReport for comprehensive ENT evaluation.
"""

import sys
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Fix import path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.pydantic_prompt_generator import PromptStyle


# ============================================================================
# PATIENT ANSWER CLASSES - Questions patient can directly answer
# ============================================================================

class ENTPatientHistory(BaseModel):
    """Questions patient can directly answer about ENT symptoms and history."""
    ear_pain: str = Field(description="Do you have ear pain? (yes/no, duration, severity 1-10)")
    ear_discharge: str = Field(description="Do you have any discharge from ears? (yes/no, character, duration)")
    hearing_loss: str = Field(description="Do you notice hearing loss? (yes/no, which ear, when started, progressive)")
    tinnitus: str = Field(description="Do you hear ringing, buzzing, or other sounds in ears? (yes/no, constant/intermittent, severity)")
    vertigo_dizziness: str = Field(description="Do you feel dizzy or have sensation of spinning? (yes/no, when it occurs, severity, with movements)")

    sore_throat: str = Field(description="Do you have sore throat? (yes/no, duration, severity, difficulty swallowing)")
    throat_discharge: str = Field(description="Do you cough up mucus or discharge? (yes/no, color, amount, blood-tinged)")
    hoarseness: str = Field(description="Is your voice hoarse? (yes/no, duration, constant/intermittent)")
    throat_lump_sensation: str = Field(description="Do you feel lump in throat? (yes/no, location, constant/intermittent)")
    throat_ulcers: str = Field(description="Do you have sores or ulcers in mouth/throat? (yes/no, location, painful/painless, duration)")

    nasal_congestion: str = Field(description="Do you have nasal congestion? (yes/no, unilateral/bilateral, constant/intermittent)")
    nasal_discharge: str = Field(description="Do you have nasal discharge? (yes/no, character-clear/yellow/green, amount)")
    nosebleeds: str = Field(description="Do you have nosebleeds? (yes/no, frequency, severity, which nostril)")
    nasal_obstruction: str = Field(description="Do you feel obstruction when breathing through nose? (yes/no, which side, constant/intermittent)")
    loss_of_taste_smell: str = Field(description="Have you lost sense of taste or smell? (yes/no, when started, both/one)")

    recent_illness: str = Field(description="Have you had recent cold, flu, or infection? (yes/no, duration, current status)")
    medications: str = Field(description="Are you taking any medications? (yes/no, list if yes)")
    allergies: str = Field(description="Do you have allergies? (yes/no, seasonal/year-round, triggers)")
    smoking_exposure: str = Field(description="Do you smoke or have smoking exposure? (yes/no, how much, how long)")


class ENTPatientPhysicalReportable(BaseModel):
    """Questions requiring visual assessment but can be reported by patient about themselves."""
    recent_trauma: str = Field(description="Have you had recent injury to ears, nose, or throat? (yes/no, location, when)")
    visible_lesions_self: str = Field(description="Do you notice any sores or lesions you can see? (yes/no, location, appearance)")
    facial_swelling: str = Field(description="Do you have swelling in face, cheeks, or jaw? (yes/no, location, constant/intermittent)")
    lymph_node_awareness: str = Field(description="Do you notice any lumps or swollen areas in neck? (yes/no, location, size, tender)")


# ============================================================================
# NURSE ANSWER CLASSES - Questions requiring clinical examination
# ============================================================================

class AuricleAndMastoidAssessment(BaseModel):
    """Assessment of auricles and mastoid region via inspection and palpation."""
    auricle_lateral_surface: str = Field(description="Auricle lateral surface - lesions/moles/cysts absent/present")
    auricle_medial_surface: str = Field(description="Auricle medial surface - lesions/abnormalities absent/present")
    surrounding_tissue: str = Field(description="Tissue surrounding auricle - lesions/nodules absent/present")
    auricle_color: str = Field(description="Auricle color - matches facial skin/bluish/pallor/erythema")
    auricle_size_symmetry: str = Field(description="Auricles equal size and symmetric - yes/no")
    auricle_configuration: str = Field(description="Auricle configuration - normal/cauliflower/deformity")
    darwin_tubercle: str = Field(description="Darwin tubercle visible - yes/no")
    auricle_position: str = Field(description="Auricle position - normal/low-set/high-set")
    auricle_firmness: str = Field(description="Auricle firmness on palpation - firm/soft, mobile/fixed")
    auricle_recoil: str = Field(description="Auricles recoil when folded - yes/no (immediate/delayed)")
    postauricular_tenderness: str = Field(description="Postauricular area tenderness - absent/mild/moderate/severe")
    mastoid_tenderness: str = Field(description="Mastoid area tenderness - absent/mild/moderate/severe, swelling present/absent")
    lobule_pain_on_pulling: str = Field(description="Pain when pulling lobule - absent/present (sharp/dull), severity")
    auricle_overall: str = Field(description="Overall auricle assessment - normal/abnormal (specify findings)")


class ExternalAuditoryCanal(BaseModel):
    """Assessment of external auditory canal via otoscopy."""
    canal_discharge: str = Field(description="Ear canal discharge - absent/present (serous/bloody/purulent/watery)")
    canal_odor: str = Field(description="Odor from canal - absent/foul/putrid, severity")
    canal_wall_color: str = Field(description="Canal wall color - pink/red/pale, inflammation present/absent")
    canal_wall_condition: str = Field(description="Canal wall condition - smooth/swollen/scaling/lesions/granulation")
    canal_hairs: str = Field(description="Hairs in outer third - present/absent, normal amount/excessive")
    cerumen_amount: str = Field(description="Cerumen amount - minimal/moderate/excessive, impaction yes/no")
    cerumen_color_texture: str = Field(description="Cerumen color and texture - yellow/brown/black, wet/dry/hard")
    canal_foreign_body: str = Field(description="Foreign body in canal - absent/present (type, size, location)")
    canal_lesions: str = Field(description="Canal lesions or growths - absent/present (location, description)")
    canal_overall: str = Field(description="Overall canal assessment - normal/abnormal (pathology notes)")


class TympanumAssessment(BaseModel):
    """Assessment of tympanic membrane via otoscope."""
    umbo_visibility: str = Field(description="Umbo landmark - visible/not visible")
    malleus_handle: str = Field(description="Handle of malleus - visible/obscured (by retraction/bulging)")
    light_reflex: str = Field(description="Light reflex - present/absent/distorted (location if present)")
    membrane_color: str = Field(description="Membrane color - translucent pearly gray/amber/yellow/red/white/chalky")
    membrane_opacification: str = Field(description="Opacity - clear/opaque (white flecks/plaques/air-fluid level if abnormal)")
    membrane_contour: str = Field(description="Contour - slightly conical/bulging/retracted, landmarks visible/hidden")
    membrane_perforation: str = Field(description="Perforation - absent/present (location, size, edges clean/jagged)")
    membrane_mobility: str = Field(description="Mobility with pneumatic otoscope - mobile/immobile/restricted")
    tympanum_overall: str = Field(description="Overall tympanum - normal/abnormal (pathology summary)")


class HearingAssessment(BaseModel):
    """Assessment of hearing function via clinical tests."""
    conversational_response: str = Field(description="Response to conversational speech - appropriate/delayed/requests repetition")
    speech_tone_quality: str = Field(description="Speech tone and volume - normal/monotonous/erratic/unusual")
    whispered_voice_right: str = Field(description="Right ear whispered voice - repeats >50%/unable to repeat")
    whispered_voice_left: str = Field(description="Left ear whispered voice - repeats >50%/unable to repeat")
    weber_test_result: str = Field(description="Weber test (512 Hz) - centered/lateralizes right/lateralizes left")
    rinne_test_right: str = Field(description="Rinne test right ear - air > bone/bone > air/equal")
    rinne_test_left: str = Field(description="Rinne test left ear - air > bone/bone > air/equal")
    hearing_loss_pattern: str = Field(description="Pattern if loss present - conductive/sensorineural/mixed, unilateral/bilateral")
    hearing_overall: str = Field(description="Overall hearing - normal/mild/moderate/severe/profound loss")


class NoseExternalAssessment(BaseModel):
    """Assessment of external nose via inspection and palpation."""
    nose_shape_size: str = Field(description="Nose shape and size - symmetric/swollen/depressed bridge/normal")
    nasal_bridge: str = Field(description="Nasal bridge - smooth/swelling/depression/transverse crease")
    columella_alignment: str = Field(description="Columella - midline/deviated (left/right, degree)")
    naris_width: str = Field(description="Naris width - normal/widened/narrowed")
    nose_color: str = Field(description="Nose color - matches face/erythema/cyanosis/pallor")
    nares_shape: str = Field(description="Nares shape - oval/asymmetric/narrowed/flaring")
    nares_discharge: str = Field(description="Discharge from nares - absent/present (clear/yellow/green/bloody)")
    nasal_flaring: str = Field(description="Flaring on inspiration - absent/mild/moderate/severe")
    nose_firmness: str = Field(description="Firmness on palpation - firm/soft/tender/displaced/crepitus")
    nose_masses: str = Field(description="Masses on palpation - absent/present (polyp/tumor/hematoma)")
    nares_patency: str = Field(description="Breathing through nares - clear/obstructed, bilateral/unilateral")
    nose_overall: str = Field(description="Overall nose assessment - normal/abnormal (findings summary)")


class NasalMucosaSeptumAssessment(BaseModel):
    """Assessment of nasal mucosa and septum via nasal speculum."""
    mucosa_color: str = Field(description="Mucosa color - deep pink/erythema/pallor/blue-gray")
    mucosa_condition: str = Field(description="Condition - moist/dry/bleeding/crusted/polypoid")
    turbinate_condition: str = Field(description="Turbinate status - normal size/swollen/boggy/pale/red")
    turbinate_obstruction: str = Field(description="Obstruction from turbinate - none/mild/moderate/severe")
    septum_position: str = Field(description="Septum position - midline/deviated left/deviated right/severe deviation")
    septum_straightness: str = Field(description="Septum straightness - straight/C-shaped/S-shaped")
    posterior_cavity: str = Field(description="Posterior cavities - symmetric/asymmetric/narrowed")
    turbinates_visible: str = Field(description="Inferior and middle turbinates - both visible/one hidden/both hidden")
    septal_perforation: str = Field(description="Perforation - absent/present (location, size, crusting)")
    nasal_polyps: str = Field(description="Polyps - absent/present (unilateral/bilateral, size, appearance)")
    septal_hairs: str = Field(description="Hairs in nose - absent/present (normal/excessive)")
    septal_discharge: str = Field(description="Discharge on septum - absent/present (character)")
    mucosa_overall: str = Field(description="Overall mucosa/septum assessment - normal/abnormal (summary)")


class SinusAssessment(BaseModel):
    """Assessment of paranasal sinuses via palpation and inspection."""
    forehead_swelling: str = Field(description="Forehead swelling - absent/present (location, degree)")
    frontal_sinus_palpation: str = Field(description="Frontal sinus tenderness - absent/mild/moderate/severe")
    cheek_swelling: str = Field(description="Cheek swelling - absent/present (location, degree)")
    maxillary_sinus_palpation: str = Field(description="Maxillary sinus tenderness - absent/mild/moderate/severe")
    sinus_transillumination: str = Field(description="Transillumination findings - normal/dull/opaque (location if abnormal)")
    sinus_overall: str = Field(description="Overall sinus assessment - normal/abnormal (sinusitis findings if present)")


class LipsAssessment(BaseModel):
    """Assessment of lips via inspection."""
    lips_symmetry: str = Field(description="Lips symmetry - symmetric/slight asymmetry/significant asymmetry (describe)")
    lips_color: str = Field(description="Lips color - pink/pale/erythema/cyanosis/pigmented")
    lips_border: str = Field(description="Lips border - distinct/blurred/pale/macules present")
    lips_condition: str = Field(description="Condition - smooth/dry/cracked/swollen/exfoliating")
    lips_lesions: str = Field(description="Lesions or ulceration - absent/present (location, appearance, size)")
    lips_macules: str = Field(description="Macules or spots - absent/present (Peutz-Jeghers spots, appearance)")
    lips_overall: str = Field(description="Overall lips assessment - normal/abnormal (findings)")


class TeethAssessment(BaseModel):
    """Assessment of teeth via inspection."""
    number_of_teeth: str = Field(description="Number of teeth - full set/missing teeth (which teeth, number)")
    teeth_anchoring: str = Field(description="Teeth anchoring - firmly anchored/loose/mobile (which teeth)")
    occlusion_molars: str = Field(description="Molar occlusion - normal/class I/class II/class III malocclusion")
    occlusion_premolars_canines: str = Field(description="Premolar/canine occlusion - normal/overjet/cross-bite/open-bite")
    occlusion_incisors: str = Field(description="Incisor occlusion - normal/overbite/overjet/open-bite")
    teeth_color: str = Field(description="Teeth color - white/yellow/brown/stained (smoking/coffee/tea/medication)")
    teeth_caries: str = Field(description="Caries - absent/present (location, number, severity)")
    teeth_wear: str = Field(description="Wear on teeth - absent/present (severity, grinding pattern if present)")
    teeth_overall: str = Field(description="Overall teeth assessment - normal/abnormal (dental findings summary)")


class BuccalMucosaAssessment(BaseModel):
    """Assessment of buccal mucosa via inspection and palpation."""
    buccal_color: str = Field(description="Buccal mucosa color - pink/erythema/pallor/pigmented")
    buccal_condition: str = Field(description="Condition - smooth/white patches/ulcers/lesions/bleeding")
    stenson_duct: str = Field(description="Stenson's duct appearance - normal/inflammation/discharge present")
    fordyce_spots: str = Field(description="Fordyce spots - absent/present (appearance, bilateral)")
    buccal_ulcerations: str = Field(description="Ulcerations - absent/present (location, appearance, size)")
    buccal_overall: str = Field(description="Overall buccal assessment - normal/abnormal (findings)")


class GingivalAssessment(BaseModel):
    """Assessment of gingiva (gums) via inspection and palpation."""
    gingival_color: str = Field(description="Gingival color - coral pink/erythema/cyanosis/pallor/pigmented")
    gingival_margin: str = Field(description="Gingival margin - sharp/blunt/swollen/retracted")
    gingival_inflammation: str = Field(description="Inflammation - absent/mild/moderate/severe (location)")
    gingival_bleeding: str = Field(description="Bleeding - absent/on probing/spontaneous (severity)")
    gingival_lesions: str = Field(description="Lesions - absent/present (location, type, appearance)")
    gingival_pockets: str = Field(description="Pockets on probing - absent/present (depth if present)")
    gingival_enlargement: str = Field(description="Enlargement - absent/localized/generalized (severity)")
    gingival_recession: str = Field(description="Recession - absent/present (location, degree)")
    gingival_overall: str = Field(description="Overall gingival assessment - normal/gingivitis/periodontitis (severity)")


class TongueAssessment(BaseModel):
    """Assessment of tongue via inspection and palpation."""
    tongue_position: str = Field(description="Tongue position - midline/deviated/retracted/forward")
    tongue_size: str = Field(description="Tongue size - normal/macroglossia/microglossia")
    tongue_fasciculations: str = Field(description="Fasciculations - absent/present (describe, clinical significance)")
    tongue_color: str = Field(description="Tongue color - dull red/pale/bright red/white coat/geographic")
    tongue_surface: str = Field(description="Surface - normal papillae/smooth/hairy/fissured/geographic")
    tongue_movement: str = Field(description="Movement - full range/restricted/painful (deviation on protrusion)")
    tongue_ulceration: str = Field(description="Ulceration - absent/present (location, appearance, size, character)")
    ventral_surface: str = Field(description="Ventral surface - smooth/varicosities/ranula/swelling")
    lateral_borders: str = Field(description="Lateral borders - smooth/white margins/red margins/induration")
    tongue_palpation: str = Field(description="Palpation findings - smooth/lumps/nodules/induration (location)")
    tongue_coating: str = Field(description="Coating - absent/thin white/thick white/brown/black")
    tongue_overall: str = Field(description="Overall tongue assessment - normal/abnormal (findings summary)")


class PalateUvulaAssessment(BaseModel):
    """Assessment of hard palate, soft palate, and uvula."""
    hard_palate_color: str = Field(description="Hard palate color - whitish/pink/erythema/pale/petechiae")
    hard_palate_shape: str = Field(description="Shape - dome-shaped/cleft/flat/high arch")
    hard_palate_rugae: str = Field(description="Transverse rugae - present/absent (normal)")
    hard_palate_protuberance: str = Field(description="Bony protuberance (torus) - absent/present/small/large")
    soft_palate_color: str = Field(description="Soft palate color - pink/erythema/pale/petechiae/ulcers")
    soft_palate_contiguity: str = Field(description="Soft palate contiguity - continuous/cleft/gap")
    uvula_position: str = Field(description="Uvula position - midline/deviated/bifid/absent/cleft")
    uvula_appearance: str = Field(description="Appearance - normal/bifid/cleft/edema/exudate/swollen")
    uvula_movement: str = Field(description="Movement on 'aaah' - elevates symmetrically/asymmetric/absent")
    gag_reflex: str = Field(description="Gag reflex - normal/diminished/absent/hyperactive")
    palatal_arches: str = Field(description="Palatal arches - symmetric/asymmetric/prominent/normal")
    tonsil_size: str = Field(description="Tonsil size - 0 (absent)/1+ (small)/2+ (normal)/3+ (large)/4+ (very large touching)")
    tonsil_color: str = Field(description="Tonsil color - pink/red/pale/white exudate/yellow exudate")
    tonsil_exudate: str = Field(description="Exudate - absent/patchy white/confluent white/purulent (bacterial vs viral)")
    palate_overall: str = Field(description="Overall palate/uvula assessment - normal/abnormal (pharyngitis/obstruction/findings)")


class AssessmentSummary(BaseModel):
    """Summary of findings and clinical impression."""
    ear_findings: str = Field(description="Summary of ear examination findings")
    hearing_assessment_summary: str = Field(description="Summary of hearing tests and interpretation")
    nose_findings: str = Field(description="Summary of nasal examination findings")
    sinus_findings: str = Field(description="Summary of sinus assessment")
    throat_findings: str = Field(description="Summary of throat/pharyngeal findings")
    oral_findings: str = Field(description="Summary of oral cavity and dentition findings")
    major_abnormalities: str = Field(description="List of significant abnormalities requiring follow-up")
    red_flag_findings: str = Field(description="Any red flag findings (e.g., severe sore throat, airway obstruction, sudden hearing loss)")
    clinical_impression: str = Field(description="Overall clinical impression and assessment")
    recommended_workup: str = Field(description="Recommended diagnostic workup or studies")
    specialist_referral: str = Field(description="ENT specialist referral indicated - yes/no, reason if yes")
    follow_up_plan: str = Field(description="Follow-up plan and timeline")


# ============================================================================
# COMBINED ASSESSMENT CLASSES
# ============================================================================

class ENTNurseAnswers(BaseModel):
    """All clinical examination findings from nurse assessment."""
    auricle_and_mastoid: AuricleAndMastoidAssessment
    external_auditory_canal: ExternalAuditoryCanal
    tympanum: TympanumAssessment
    hearing_assessment: HearingAssessment
    nose_external: NoseExternalAssessment
    nasal_mucosa_septum: NasalMucosaSeptumAssessment
    sinus_assessment: SinusAssessment
    lips_assessment: LipsAssessment
    teeth_assessment: TeethAssessment
    buccal_mucosa: BuccalMucosaAssessment
    gingival_assessment: GingivalAssessment
    tongue_assessment: TongueAssessment
    palate_uvula: PalateUvulaAssessment
    assessment_summary: AssessmentSummary


class ENTMedicalReport(BaseModel):
    """Complete ENT medical report combining patient history and clinical examination."""
    patient_name: str = Field(description="Name of the patient")
    examination_date: str = Field(description="Date of examination")
    patient_answers: ENTPatientHistory
    patient_physical_reportable: ENTPatientPhysicalReportable
    nurse_answers: ENTNurseAnswers


# ============================================================================
# INTERACTIVE QUESTIONING FUNCTIONS
# ============================================================================

def ask_ent_patient_questions() -> dict:
    """
    Ask patient ENT assessment questions interactively.
    These are questions patient can directly answer.
    Returns dictionary of patient responses.
    """
    print("\n" + "="*70)
    print("ENT ASSESSMENT - PATIENT QUESTIONNAIRE")
    print("="*70)
    print("\nMEASURES: Evaluates ear, nose, and throat health through assessment of:")
    print("  • Ear pain, discharge, hearing loss, tinnitus, and dizziness")
    print("  • Throat pain, discharge, hoarseness, and ulcers")
    print("  • Nasal congestion, discharge, obstruction, and nosebleeds")
    print("  • Loss of taste or smell (olfactory/gustatory function)")
    print("  • Recent infections, allergies, and medication effects")
    print("  • Clinical examination of ear canal, tympanum, throat, and nasal passages")

    print("\nTOP 10 KEY ASSESSMENT QUESTIONS:")
    print("  1. Do you have ear pain? If yes, in which ear and how severe (1-10)?")
    print("  2. Do you have hearing loss or ringing/buzzing in your ears (tinnitus)?")
    print("  3. Do you experience dizziness or vertigo, especially with movement?")
    print("  4. Do you have sore throat, difficulty swallowing, or hoarseness?")
    print("  5. Do you see any discharge (pus/blood) from your ears or throat?")
    print("  6. Do you have nasal congestion, discharge, or nosebleeds?")
    print("  7. Have you noticed recent loss of taste or smell?")
    print("  8. Have you had a recent cold, flu, or throat/ear infection?")
    print("  9. Do you have allergies? If yes, what triggers them?")
    print(" 10. Do you smoke or have exposure to secondhand smoke?")

    print("\n" + "="*70)
    print("DETAILED ENT ASSESSMENT QUESTIONNAIRE")
    print("="*70)
    print("\nPlease answer the following questions about your ear, nose, and throat symptoms.")

    responses = {}

    # EARS - SYMPTOMS
    print("\n" + "-"*70)
    print("EARS - SYMPTOMS")
    print("-"*70)

    print("💡 Hint: Common causes include ear infection, earwax impaction, allergies")
    responses['ear_pain'] = input("Do you have ear pain? (yes/no, describe severity/duration)\n→ ").strip()

    print("💡 Hint: Discharge may indicate infection, eardrum perforation, or chronic inflammation")
    responses['ear_discharge'] = input("Do you have any discharge from ears? (yes/no, describe)\n→ ").strip()

    print("💡 Hint: Can be from infection, fluid, nerve damage, or medications")
    responses['hearing_loss'] = input("Do you notice hearing loss? (yes/no, which ear, when started)\n→ ").strip()

    print("💡 Hint: Tinnitus can indicate hearing loss, infection, or circulation issues")
    responses['tinnitus'] = input("Do you hear ringing, buzzing, or other sounds? (yes/no, describe)\n→ ").strip()

    print("💡 Hint: Can indicate ear infection, BPPV, or vestibular problems")
    responses['vertigo_dizziness'] = input("Do you feel dizzy or spinning sensation? (yes/no, describe)\n→ ").strip()

    # THROAT - SYMPTOMS
    print("\n" + "-"*70)
    print("THROAT - SYMPTOMS")
    print("-"*70)

    print("💡 Hint: Most common causes: viral infection, strep throat, allergies, acid reflux")
    responses['sore_throat'] = input("Do you have sore throat? (yes/no, duration, severity, difficulty swallowing)\n→ ").strip()

    print("💡 Hint: Yellow/green suggests bacterial infection; clear suggests viral or allergies")
    responses['throat_discharge'] = input("Do you cough up discharge? (yes/no, color, amount, blood-tinged)\n→ ").strip()

    print("💡 Hint: Can be from laryngitis, overuse, smoking, acid reflux, or nodules")
    responses['hoarseness'] = input("Is your voice hoarse? (yes/no, duration, constant/intermittent)\n→ ").strip()

    print("💡 Hint: Could indicate enlarged tonsils, lymph nodes, or thyroid")
    responses['throat_lump_sensation'] = input("Do you feel lump in throat? (yes/no, describe)\n→ ").strip()

    print("💡 Hint: Painful ulcers: aphthous (benign), viral, or cancer (if >3 weeks)")
    responses['throat_ulcers'] = input("Do you have sores in mouth/throat? (yes/no, painful/painless, duration)\n→ ").strip()

    # NOSE - SYMPTOMS
    print("\n" + "-"*70)
    print("NOSE - SYMPTOMS")
    print("-"*70)

    print("💡 Hint: Common causes: allergies, infection, deviated septum, nasal polyps")
    responses['nasal_congestion'] = input("Do you have nasal congestion? (yes/no, unilateral/bilateral)\n→ ").strip()

    print("💡 Hint: Clear suggests allergies/viral; yellow/green suggests bacterial infection")
    responses['nasal_discharge'] = input("Do you have nasal discharge? (yes/no, describe - clear/yellow/green)\n→ ").strip()

    print("💡 Hint: Can be from trauma, dry air, infection, or coagulopathy. Seek help if frequent/severe")
    responses['nosebleeds'] = input("Do you have nosebleeds? (yes/no, frequency, severity)\n→ ").strip()

    print("💡 Hint: Can be from deviated septum, swollen turbinates, polyps, or mass")
    responses['nasal_obstruction'] = input("Do you feel obstruction when breathing? (yes/no, which side)\n→ ").strip()

    print("💡 Hint: Loss can be from viral infection, allergies, nasal polyps, or neurologic issues")
    responses['loss_of_taste_smell'] = input("Have you lost sense of taste/smell? (yes/no, when, both/one)\n→ ").strip()

    # GENERAL HISTORY
    print("\n" + "-"*70)
    print("GENERAL ENT HISTORY")
    print("-"*70)

    print("💡 Hint: Recent infection can predispose to secondary infections or complications")
    responses['recent_illness'] = input("Have you had recent cold, flu, or infection? (yes/no, when)\n→ ").strip()

    print("💡 Hint: Some medications can cause dry mouth, nasal congestion, or hearing loss")
    responses['medications'] = input("Are you taking any medications? (yes/no, list if yes)\n→ ").strip()

    print("💡 Hint: Environmental allergies can cause congestion, discharge, throat irritation")
    responses['allergies'] = input("Do you have allergies? (yes/no, seasonal/year-round, triggers)\n→ ").strip()

    print("💡 Hint: Smoking damages nasal/throat tissues and increases infection/cancer risk")
    responses['smoking_exposure'] = input("Do you smoke? (yes/no, how much, how long)\n→ ").strip()

    return responses


def ask_ent_patient_physical_questions() -> dict:
    """
    Ask patient about physical findings they can report about themselves.
    """
    print("\n" + "="*70)
    print("ENT ASSESSMENT - PATIENT-REPORTED PHYSICAL FINDINGS")
    print("="*70)

    responses = {}

    print("\n" + "-"*70)
    print("INJURIES AND VISIBLE FINDINGS")
    print("-"*70)

    print("💡 Hint: Trauma can cause perforation, hearing loss, or infection")
    responses['recent_trauma'] = input("Have you had recent injury to ears, nose, or throat? (yes/no, describe)\n→ ").strip()

    print("💡 Hint: Patient can see external lesions; clinician will assess internal")
    responses['visible_lesions_self'] = input("Do you notice any sores or lesions? (yes/no, describe)\n→ ").strip()

    print("💡 Hint: Swelling can indicate infection, allergies, or obstruction")
    responses['facial_swelling'] = input("Do you have swelling in face, cheeks, or jaw? (yes/no, where, constant/intermittent)\n→ ").strip()

    print("💡 Hint: Most common with infection, cancer, or metastatic disease")
    responses['lymph_node_awareness'] = input("Do you notice lumps or swelling in neck? (yes/no, where, tender, size)\n→ ").strip()

    return responses


def ask_ent_nurse_questions() -> dict:
    """
    Ask nurse clinical examination questions.
    Requires physical examination, measurement, or specialized equipment.
    """
    print("\n" + "="*70)
    print("ENT ASSESSMENT - CLINICAL EXAMINATION FINDINGS")
    print("="*70)
    print("\nClinician: Document findings from physical examination.")

    responses = {}

    # AURICLE AND MASTOID
    print("\n" + "-"*70)
    print("AURICLE AND MASTOID EXAMINATION")
    print("-"*70)

    print("💡 Hint: Look for familial variations, birthmarks, or lesions. Normal: symmetric, equal size")
    responses['auricle_lesions'] = input("Lesions/moles/cysts on auricles? (normal: absent | abnormal: describe)\n→ ").strip()

    print("💡 Hint: Normal ears match face color. Pallor=anemia; cyanosis=hypoxia; red=inflammation")
    responses['auricle_color'] = input("Auricle color? (normal: matches face | abnormal: specify)\n→ ").strip()

    print("💡 Hint: Compare both ears side-by-side for size equality")
    responses['auricle_symmetry'] = input("Auricles equal size and symmetric? (normal: yes | abnormal: no, describe)\n→ ").strip()

    print("💡 Hint: Darwin tubercle = small conical projection on posterior auricle, normal variant in ~40%")
    responses['darwin_tubercle'] = input("Darwin tubercle visible? (normal: yes/no, normal variant)\n→ ").strip()

    print("💡 Hint: Cauliflower ear = deformity from repeated trauma. Normal shape is smooth")
    responses['auricle_configuration'] = input("Auricle configuration? (normal: smooth | abnormal: cauliflower/cysts/scarring)\n→ ").strip()

    print("💡 Hint: Top of auricle should be level with or above eye-occiput line")
    responses['auricle_position'] = input("Auricle position? (normal: level with/above eye-occiput line | abnormal: low/high-set)\n→ ").strip()

    print("💡 Hint: Auricles should be firm and easily movable, NOT tender on palpation")
    responses['auricle_firmness'] = input("Auricles firm and mobile? (normal: yes | abnormal: soft/fixed/swollen)\n→ ").strip()

    print("💡 Hint: When folded forward, should spring back immediately")
    responses['auricle_recoil'] = input("Auricles recoil when folded? (normal: yes, immediate | abnormal: delayed/no)\n→ ").strip()

    print("💡 Hint: Postauricular tenderness suggests otitis media, mastoiditis, or lymphadenopathy")
    responses['postauricular_tenderness'] = input("Postauricular tenderness on palpation? (normal: no | abnormal: mild/mod/severe)\n→ ").strip()

    print("💡 Hint: Mastoid bone should NOT be tender. Tenderness = possible mastoiditis (infection)")
    responses['mastoid_tenderness'] = input("Mastoid area tenderness? (normal: no | abnormal: yes, location)\n→ ").strip()

    print("💡 Hint: Pain on pulling earlobe suggests otitis externa (swimmer's ear, external ear infection)")
    responses['lobule_pain'] = input("Pain when pulling lobule? (normal: none | abnormal: sharp pain)\n→ ").strip()

    # EXTERNAL AUDITORY CANAL
    print("\n" + "-"*70)
    print("EXTERNAL AUDITORY CANAL (Otoscopy)")
    print("-"*70)

    print("💡 Hint: Normal: pink, dry, some earwax. Discharge = infection or perforation")
    responses['canal_discharge'] = input("Canal discharge? (normal: none | abnormal: describe type)\n→ ").strip()

    print("💡 Hint: Foul odor suggests bacterial infection (otitis externa) or chronic suppuration")
    responses['canal_odor'] = input("Foul odor from canal? (normal: none | abnormal: yes, severity)\n→ ").strip()

    print("💡 Hint: Normal: pink walls. Red=inflammation/infection. Pale=atrophic")
    responses['canal_color'] = input("Canal wall color? (normal: pink | abnormal: red/pale/white)\n→ ").strip()

    print("💡 Hint: Normal: smooth. Swollen/red=otitis externa. Scaling=dermatitis or fungal infection")
    responses['canal_condition'] = input("Canal wall condition? (normal: smooth | abnormal: swollen/scaling/lesions)\n→ ").strip()

    print("💡 Hint: Hair in outer third is normal. Cerumen surrounds hairs and catches debris")
    responses['canal_hairs'] = input("Hairs in outer third of canal? (normal: yes, some present | abnormal: excessive)\n→ ").strip()

    print("💡 Hint: Cerumen varies: yellow (wet) vs brown (dry). Impaction = blocks view, causes hearing loss")
    responses['cerumen_amount'] = input("Cerumen amount? (normal: minimal-moderate | abnormal: excessive, impacted)\n→ ").strip()

    print("💡 Hint: Color varies by genetics. Yellow=wet type, brown=dry type. Both normal")
    responses['cerumen_color'] = input("Cerumen color? (normal: yellow/brown variation, genetic)\n→ ").strip()

    print("💡 Hint: Any object in canal that shouldn't be there")
    responses['canal_foreign_body'] = input("Foreign body in canal? (normal: none | abnormal: type, size, location)\n→ ").strip()

    # TYMPANIC MEMBRANE
    print("\n" + "-"*70)
    print("TYMPANIC MEMBRANE (Otoscopy)")
    print("-"*70)

    print("💡 Hint: Three normal landmarks: umbo (center), malleus handle, light reflex")
    responses['umbo_visibility'] = input("Umbo visible? (normal: yes | abnormal: hidden by fluid/bulging)\n→ ").strip()

    print("💡 Hint: Handle of malleus = vertical line from umbo toward top of eardrum")
    responses['malleus_handle'] = input("Handle of malleus visible? (normal: yes, clear | abnormal: obscured)\n→ ").strip()

    print("💡 Hint: Bright cone of light at 4-5 o'clock. Missing=retracted membrane/fluid. Distorted=bulging")
    responses['light_reflex'] = input("Light reflex on tympanum? (normal: bright, cone at 4-5 position | abnormal: absent/distorted)\n→ ").strip()

    print("💡 Hint: Normal=pearly gray, translucent. Amber=fluid. Yellow=pus. White=scarring")
    responses['membrane_color'] = input("Membrane color? (normal: translucent pearly gray | abnormal: amber/yellow/red/white)\n→ ").strip()

    print("💡 Hint: Normal=clear. White patches=scarring. Air-fluid level=otitis media. Plaques=serious infection")
    responses['membrane_opacity'] = input("Membrane opacification? (normal: clear | abnormal: opaque, flecks, plaques, bubbles)\n→ ").strip()

    print("💡 Hint: Normal=slightly conical (concave). Bulging=pressure inside. Retracted=negative pressure")
    responses['membrane_contour'] = input("Membrane contour? (normal: slightly conical | abnormal: bulging/retracted)\n→ ").strip()

    print("💡 Hint: Any hole = pathology. Size determines severity and treatment")
    responses['membrane_perforation'] = input("Membrane perforation? (normal: intact | abnormal: location, size, edges)\n→ ").strip()

    print("💡 Hint: Pneumatic otoscope test: membrane should move with air pressure")
    responses['membrane_mobility'] = input("Membrane mobility with pneumatic otoscope? (normal: mobile | abnormal: fixed/immobile)\n→ ").strip()

    # HEARING ASSESSMENT
    print("\n" + "-"*70)
    print("HEARING ASSESSMENT")
    print("-"*70)

    print("💡 Hint: Normal: patient responds appropriately. Abnormal: delayed, asks for repetition")
    responses['conversational_response'] = input("Response to conversational speech? (normal: appropriate | abnormal: delayed/requests repetition)\n→ ").strip()

    print("💡 Hint: Normal speech=varied tone/volume. Abnormal=monotone (Parkinson's) or erratic (hearing loss)")
    responses['speech_tone'] = input("Speech tone and volume? (normal: varied, appropriate | abnormal: monotone/erratic)\n→ ").strip()

    print("💡 Hint: Whisper test: 12 inches away, whisper 3 numbers. Normal: >50% correct. One ear at a time")
    responses['whispered_right'] = input("Right ear whispered voice? (normal: >50% correct | abnormal: <50%)\n→ ").strip()

    print("💡 Hint: Same whisper test left ear. Compare to determine if loss is unilateral or bilateral")
    responses['whispered_left'] = input("Left ear whispered voice? (normal: >50% correct | abnormal: <50%)\n→ ").strip()

    print("💡 Hint: Weber test: tuning fork on forehead midline. Sound should be CENTERED. Lateralizing=loss")
    responses['weber_test'] = input("Weber test (512 Hz)? (normal: centered | abnormal: lateralizes right/left)\n→ ").strip()

    print("💡 Hint: Rinne right: fork on mastoid (bone), then move to ear (air). Normal: AIR > BONE")
    responses['rinne_right'] = input("Rinne test right ear? (normal: air > bone | abnormal: bone > air-conductive loss)\n→ ").strip()

    print("💡 Hint: Rinne left: same test. Air>bone both=normal/sensorineural. Bone>air=conductive loss")
    responses['rinne_left'] = input("Rinne test left ear? (normal: air > bone | abnormal: bone > air-conductive loss)\n→ ").strip()

    # NOSE - EXTERNAL
    print("\n" + "-"*70)
    print("NOSE - EXTERNAL EXAMINATION")
    print("-"*70)

    print("💡 Hint: Normal nose is smooth, symmetric, proportionate. Swelling/depression suggests trauma/inflammation")
    responses['nose_shape'] = input("Nose shape and size? (normal: smooth, symmetric | abnormal: swollen, depressed bridge)\n→ ").strip()

    print("💡 Hint: Bridge should be smooth. Transverse crease=chronic allergy (children rubbing nose)")
    responses['nasal_bridge'] = input("Nasal bridge condition? (normal: smooth | abnormal: swelling, depression, crease)\n→ ").strip()

    print("💡 Hint: Columella should be midline. Deviation visible from front")
    responses['columella'] = input("Columella alignment? (normal: midline | abnormal: deviated left/right)\n→ ").strip()

    print("💡 Hint: Naris width should be proportionate to nostril opening")
    responses['naris_width'] = input("Naris width? (normal: proportionate | abnormal: widened/narrowed)\n→ ").strip()

    print("💡 Hint: Nose should match face. Erythema=infection/rosacea. Pallor=anemia. Cyanosis=hypoxia")
    responses['nose_color'] = input("Nose color? (normal: matches face | abnormal: erythema, cyanosis, pallor)\n→ ").strip()

    print("💡 Hint: Normal=oval, symmetric. Narrowing/flaring=obstruction or respiratory distress")
    responses['nares_shape'] = input("Nares shape? (normal: oval, symmetric | abnormal: asymmetric, narrowed, flaring)\n→ ").strip()

    print("💡 Hint: Normal=no discharge. Clear=allergies/viral. Yellow/green=bacterial. Blood=epistaxis/trauma")
    responses['nares_discharge_clinical'] = input("Discharge visible at nares? (normal: none | abnormal: clear/yellow/green/bloody)\n→ ").strip()

    print("💡 Hint: Flaring=respiratory distress. Seen in infants with difficulty or adults with severe obstruction")
    responses['nasal_flaring'] = input("Nasal flaring on inspiration? (normal: none | abnormal: mild/mod/severe)\n→ ").strip()

    print("💡 Hint: Palpate bridge and septum. Should be firm, stable, nontender. Tenderness=fracture")
    responses['nose_palpation'] = input("Nose palpation - firmness? (normal: firm, stable | abnormal: soft, displaced, tender)\n→ ").strip()

    print("💡 Hint: Masses include polyps, tumors, hematomas")
    responses['nose_masses'] = input("Masses on nasal palpation? (normal: none | abnormal: polyp, tumor, hematoma)\n→ ").strip()

    print("💡 Hint: Breathing through both nares should be silent and easy. Obstruction=stridor or wheezing")
    responses['nares_patency'] = input("Nares patency - breathing? (normal: silent, easy, bilateral | abnormal: obstructed, stridor)\n→ ").strip()

    # NOSE - INTERNAL
    print("\n" + "-"*70)
    print("NOSE - INTERNAL EXAMINATION (Nasal Speculum)")
    print("-"*70)

    print("💡 Hint: Normal mucosa=deep pink glistening (moist). Erythema=rhinitis. Pallor=allergies. Blue-gray=chronic congestion")
    responses['mucosa_color'] = input("Nasal mucosa color? (normal: deep pink | abnormal: erythema, bluish-gray, pale)\n→ ").strip()

    print("💡 Hint: Normal=moist with clear secretion. Dry=heated environment/meds. Bleeding=trauma/coagulopathy. Crust=infection")
    responses['mucosa_condition'] = input("Mucosa condition? (normal: moist | abnormal: dry, bleeding, crusted, polypoid)\n→ ").strip()

    print("💡 Hint: Normal turbinates=firm, normal size. Swollen/boggy=allergies (pale/blue). Firm red=infection")
    responses['turbinate_condition'] = input("Turbinate condition? (normal: firm, normal size | abnormal: swollen, boggy, red)\n→ ").strip()

    print("💡 Hint: Septum should be close to midline. Deviation blocks airflow on that side. Severe=may need surgery")
    responses['septum_position'] = input("Septum position? (normal: midline/slight | abnormal: marked left/right deviation)\n→ ").strip()

    print("💡 Hint: Septum should be straight. C or S-shaped=deviated. Causes obstruction and headaches")
    responses['septum_straightness'] = input("Septum straightness? (normal: straight | abnormal: C-shaped, S-shaped, severe)\n→ ").strip()

    print("💡 Hint: Posterior cavities should be symmetric. Asymmetry=deviation, mass, or hypertrophic turbinate")
    responses['posterior_cavity'] = input("Posterior nasal cavities? (normal: symmetric | abnormal: asymmetric, narrowed)\n→ ").strip()

    print("💡 Hint: Should see 2 turbinates (inferior and middle). Superior=out of normal view")
    responses['turbinates_visible'] = input("Turbinates visible? (normal: both visible | abnormal: hidden by swelling/obstruction)\n→ ").strip()

    print("💡 Hint: Septal perforation=hole in middle partition. Causes crusting, epistaxis. From trauma/cocaine/vasculitis")
    responses['septal_perforation'] = input("Septal perforation? (normal: intact | abnormal: hole, location, size)\n→ ").strip()

    print("💡 Hint: Polyps=smooth, pale, grape-like masses. Usually bilateral. Suggest allergy/chronic sinusitis")
    responses['nasal_polyps'] = input("Nasal polyps? (normal: none | abnormal: smooth, grape-like, pale masses)\n→ ").strip()

    print("💡 Hint: Hairs in nasal vestibule normal. Excessive=may trap debris")
    responses['septal_hairs'] = input("Hairs in nose? (normal: some present | abnormal: excessive, obstructive)\n→ ").strip()

    # SINUSES
    print("\n" + "-"*70)
    print("SINUS EXAMINATION (Palpation and Transillumination)")
    print("-"*70)

    print("💡 Hint: Frontal sinus swelling suggests sinusitis. Tenderness=infection")
    responses['forehead_swelling'] = input("Forehead swelling over frontal sinus? (normal: none | abnormal: location, degree)\n→ ").strip()

    print("💡 Hint: Palpate above eyebrows. Tenderness suggests frontal sinusitis")
    responses['frontal_tenderness'] = input("Frontal sinus tenderness on palpation? (normal: none | abnormal: mild/mod/severe)\n→ ").strip()

    print("💡 Hint: Maxillary sinus swelling suggests sinusitis. Check below cheekbones")
    responses['cheek_swelling'] = input("Cheek swelling over maxillary sinus? (normal: none | abnormal: location, degree)\n→ ").strip()

    print("💡 Hint: Palpate below cheekbones. Tenderness suggests maxillary sinusitis")
    responses['maxillary_tenderness'] = input("Maxillary sinus tenderness? (normal: none | abnormal: mild/mod/severe)\n→ ").strip()

    # ORAL CAVITY
    print("\n" + "-"*70)
    print("ORAL CAVITY EXAMINATION")
    print("-"*70)

    print("💡 Hint: Lips should be symmetric, pink, moist, with sharp border. Asymmetry suggests stroke")
    responses['lips_symmetry'] = input("Lips symmetry? (normal: symmetric | abnormal: asymmetric, weak)\n→ ").strip()

    print("💡 Hint: Color indicates perfusion and oxygenation. Pink=normal. Pale=anemia. Cyanosis=hypoxia")
    responses['lips_color'] = input("Lips color? (normal: pink | abnormal: pale, cyanotic, pigmented)\n→ ").strip()

    print("💡 Hint: Border should be distinct from surrounding skin")
    responses['lips_border'] = input("Lips border distinctness? (normal: distinct | abnormal: blurred, pale)\n→ ").strip()

    print("💡 Hint: Should be smooth. Cracks=dehydration or vitamin deficiency. Blisters=herpes")
    responses['lips_condition'] = input("Lips condition? (normal: smooth | abnormal: cracked, blisters, swelling)\n→ ").strip()

    print("💡 Hint: Any ulcer or lesion needs evaluation. >3 weeks=suspect cancer")
    responses['lips_lesions'] = input("Lips lesions or ulceration? (normal: none | abnormal: location, appearance, size)\n→ ").strip()

    print("💡 Hint: Macules (Peutz-Jeghers spots) = pigmented. Can be sign of syndrome")
    responses['lips_macules'] = input("Lips macules? (normal: none | abnormal: pigmented spots, extent)\n→ ").strip()

    # TEETH
    print("\n" + "-"*70)
    print("TEETH EXAMINATION")
    print("-"*70)

    print("💡 Hint: Count teeth. Adults should have 32 (including wisdom teeth)")
    responses['number_teeth'] = input("Number of teeth? (normal: 32 | abnormal: specify missing)\n→ ").strip()

    print("💡 Hint: Each tooth should be firmly anchored. Loose tooth is abnormal")
    responses['teeth_anchoring'] = input("Teeth firmly anchored? (normal: yes | abnormal: loose/mobile teeth)\n→ ").strip()

    print("💡 Hint: Molar relationship: Class I (normal), Class II (overbite), Class III (underbite)")
    responses['occlusion_molars'] = input("Molar occlusion class? (normal: Class I | abnormal: Class II or III)\n→ ").strip()

    print("💡 Hint: Assess premolar and canine alignment")
    responses['occlusion_premolars'] = input("Premolar/canine occlusion? (normal: normal overlap | abnormal: cross-bite, open-bite)\n→ ").strip()

    print("💡 Hint: Incisors should have slight overbite (2-3 mm)")
    responses['occlusion_incisors'] = input("Incisor occlusion? (normal: slight overbite | abnormal: overjet, openbite)\n→ ").strip()

    print("💡 Hint: Color from staining, aging, or medication (tetracycline). Yellow=normal with age")
    responses['teeth_color'] = input("Teeth color? (normal: white/slight yellow | abnormal: brown/gray staining)\n→ ").strip()

    print("💡 Hint: Caries=cavities. Dark spots suggest decay. Early detection allows treatment")
    responses['teeth_caries'] = input("Caries (cavities)? (normal: none | abnormal: location, number, severity)\n→ ").strip()

    print("💡 Hint: Grinding wears down cusps. Flat tooth surface suggests bruxism")
    responses['teeth_wear'] = input("Teeth wear or flattening? (normal: none | abnormal: grinding pattern)\n→ ").strip()

    # BUCCAL MUCOSA
    print("\n" + "-"*70)
    print("BUCCAL MUCOSA (Inside of Cheek)")
    print("-"*70)

    print("💡 Hint: Should be pink. Pallor=anemia. Erythema=irritation/infection")
    responses['buccal_color'] = input("Buccal mucosa color? (normal: pink | abnormal: pale, red, pigmented)\n→ ").strip()

    print("💡 Hint: Should be smooth. White patches=thrush (fungus) or cancer")
    responses['buccal_condition'] = input("Buccal condition? (normal: smooth | abnormal: white patches, ulcers, lesions)\n→ ").strip()

    print("💡 Hint: Stenson's duct=parotid duct opening opposite upper molars. Should appear normal")
    responses['stenson_duct'] = input("Stenson's duct appearance? (normal: normal opening | abnormal: inflammation, discharge)\n→ ").strip()

    print("💡 Hint: Fordyce spots=sebaceous glands. Benign yellowish spots. Normal in many people")
    responses['fordyce_spots'] = input("Fordyce spots? (normal: present/absent - benign | abnormal: only if concerning appearance)\n→ ").strip()

    # GINGIVA (Gums)
    print("\n" + "-"*70)
    print("GINGIVAL EXAMINATION (Gums)")
    print("-"*70)

    print("💡 Hint: Normal gums=coral pink. Erythema=gingivitis. Cyanosis=poor circulation")
    responses['gingival_color'] = input("Gingival color? (normal: coral pink | abnormal: red, pale, cyanosis)\n→ ").strip()

    print("💡 Hint: Margin should be sharp. Blunt/swollen=inflammation. Retracted=periodontal disease")
    responses['gingival_margin'] = input("Gingival margin? (normal: sharp | abnormal: blunt, swollen, retracted)\n→ ").strip()

    print("💡 Hint: Redness/swelling=gingivitis (inflammation of gums)")
    responses['gingival_inflammation'] = input("Gingival inflammation? (normal: none | abnormal: mild/mod/severe)\n→ ").strip()

    print("💡 Hint: Bleeding on probing=gingivitis. Spontaneous=severe inflammation")
    responses['gingival_bleeding'] = input("Gingival bleeding? (normal: none | abnormal: on probing/spontaneous)\n→ ").strip()

    print("💡 Hint: Gingival pockets=space between gum and tooth. Normal <3 mm. >4 mm=periodontal disease")
    responses['gingival_pockets'] = input("Gingival pockets on probing? (normal: <3 mm | abnormal: >4 mm-periodontitis)\n→ ").strip()

    # TONGUE
    print("\n" + "-"*70)
    print("TONGUE EXAMINATION")
    print("-"*70)

    print("💡 Hint: Tongue should be midline. Deviation=stroke or CN XII palsy")
    responses['tongue_position'] = input("Tongue position? (normal: midline | abnormal: deviated left/right)\n→ ").strip()

    print("💡 Hint: Normal size allows easy movement. Macroglossia=swelling (amyloidosis, Down syndrome)")
    responses['tongue_size'] = input("Tongue size? (normal: normal | abnormal: macroglossia, microglossia)\n→ ").strip()

    print("💡 Hint: Fasciculations=involuntary twitches=ALS or motor neuron disease. Serious sign")
    responses['tongue_fasciculations'] = input("Fasciculations on tongue? (normal: none | abnormal: twitches-ALS)\n→ ").strip()

    print("💡 Hint: Normal=dull red. Pale=anemia. Bright red=B12 deficiency. White coat=oral thrush")
    responses['tongue_color'] = input("Tongue color? (normal: dull red | abnormal: pale, bright red, white coat)\n→ ").strip()

    print("💡 Hint: Anterior=smooth papillae. Posterior=rugated (ridged). Geographic tongue=benign map pattern")
    responses['tongue_surface'] = input("Tongue surface? (normal: papillary anterior, rugated posterior | abnormal: smooth, hairy, fissured)\n→ ").strip()

    print("💡 Hint: Tongue should move freely. Restriction=tongue-tie, cancer, or surgery")
    responses['tongue_movement'] = input("Tongue movement? (normal: full range | abnormal: restricted, painful)\n→ ").strip()

    print("💡 Hint: Ulcers:aphthous (painful rim), viral (clustered), cancer (firm, fixed). >3 weeks=suspect cancer")
    responses['tongue_ulceration'] = input("Tongue ulceration? (normal: none | abnormal: aphthous, vesicles, firm ulcers-cancer)\n→ ").strip()

    print("💡 Hint: Ventral surface should be smooth, pink. Varicosities=dilated veins (benign). Ranula=cyst")
    responses['ventral_surface'] = input("Ventral surface (under tongue)? (normal: smooth, pink | abnormal: swollen, ranula-cyst)\n→ ").strip()

    print("💡 Hint: Normal=large blue veins visible. Varicosities=enlarged veins (age-related, benign)")
    responses['lateral_borders'] = input("Lateral tongue borders? (normal: smooth | abnormal: white/red margins, ulceration, induration)\n→ ").strip()

    print("💡 Hint: Palpate with gloved finger. Should be smooth. Lumps=cysts or cancer. Induration=suspicious")
    responses['tongue_palpation'] = input("Tongue palpation texture? (normal: smooth | abnormal: lumps, nodules, induration-cancer)\n→ ").strip()

    # PALATE AND UVULA
    print("\n" + "-"*70)
    print("PALATE AND UVULA EXAMINATION")
    print("-"*70)

    print("💡 Hint: Hard palate=firm front roof, whitish, rugae (normal ridges). Torus=bony bump (benign)")
    responses['hard_palate_color'] = input("Hard palate color? (normal: whitish, pink | abnormal: erythema, petechiae, ulcers)\n→ ").strip()

    print("💡 Hint: Shape=dome-shaped (normal), cleft (birth defect), or flat (variation)")
    responses['hard_palate_shape'] = input("Hard palate shape? (normal: dome-shaped | abnormal: cleft, flat, high arch)\n→ ").strip()

    print("💡 Hint: Rugae=transverse ridges on hard palate. Normal. Help with swallowing")
    responses['hard_palate_rugae'] = input("Transverse rugae on hard palate? (normal: present | abnormal: absent-unusual)\n→ ").strip()

    print("💡 Hint: Torus palatinus=hard bony bump at midline. Benign, doesn't need treatment")
    responses['palate_midline_torus'] = input("Bony protuberance (torus) at midline? (normal: absent/small | benign: firm bump)\n→ ").strip()

    print("💡 Hint: Soft palate=muscular back roof. Pink=normal. Erythema=infection/inflammation")
    responses['soft_palate_color'] = input("Soft palate color? (normal: pink | abnormal: erythema, petechiae, pale)\n→ ").strip()

    print("💡 Hint: Uvula=dangly extension from soft palate. Should be midline. Deviation=stroke/CN X palsy")
    responses['uvula_position'] = input("Uvula position? (normal: midline | abnormal: deviated, bifid-birth defect)\n→ ").strip()

    print("💡 Hint: Appearance=normal (pink), bifid (split-variant), cleft (defect), edema (swelling), exudate (pus)")
    responses['uvula_appearance'] = input("Uvula appearance? (normal: pink, single | abnormal: bifid, edema, exudate)\n→ ").strip()

    print("💡 Hint: Gag reflex: say 'aaah' - uvula should elevate symmetrically. Asymmetry=stroke. No movement=brain damage")
    responses['gag_reflex'] = input("Gag reflex/uvula movement? (normal: elevates symmetrically | abnormal: asymmetric, absent)\n→ ").strip()

    print("💡 Hint: Palatal arches=curves on sides of uvula. Should be symmetric and smooth")
    responses['palatal_arches'] = input("Palatal arches? (normal: symmetric, smooth | abnormal: prominent, asymmetric)\n→ ").strip()

    print("💡 Hint: Tonsil size grading: 0=absent, 1+=small, 2+=normal, 3+=large, 4+=very large (touching). Size matters for infection")
    responses['tonsil_size'] = input("Tonsils size - grade 0-4+? (normal: 1-2+ | abnormal: 3-4+ large-obstruction, 0 absent)\n→ ").strip()

    print("💡 Hint: Tonsil color: pink=normal, red=inflamed/infected, pale=viral, white coat=strep/viral")
    responses['tonsil_color'] = input("Tonsils color? (normal: pink | abnormal: bright red-bacterial, pale-viral, white coat)\n→ ").strip()

    print("💡 Hint: Exudate=thick coating. White/yellow=bacterial (strep). Patchy=strep. Confluent=severe. No exudate=viral")
    responses['tonsil_exudate'] = input("Tonsillar exudate? (normal: none | abnormal: white/yellow-bacterial, patchy-strep, confluent)\n→ ").strip()

    return responses


# ============================================================================
# RESPONSE AGGREGATION AND REPORT CREATION
# ============================================================================

def create_ent_medical_report(
    patient_name: str,
    patient_responses: dict,
    patient_physical_responses: dict,
    nurse_responses: dict,
    output_path: Optional[Path] = None
) -> ENTMedicalReport:
    """
    Create a comprehensive ENT medical report from patient and nurse answers.
    """
    # Create patient history from responses
    patient_history = ENTPatientHistory(
        ear_pain=patient_responses.get('ear_pain', ''),
        ear_discharge=patient_responses.get('ear_discharge', ''),
        hearing_loss=patient_responses.get('hearing_loss', ''),
        tinnitus=patient_responses.get('tinnitus', ''),
        vertigo_dizziness=patient_responses.get('vertigo_dizziness', ''),
        sore_throat=patient_responses.get('sore_throat', ''),
        throat_discharge=patient_responses.get('throat_discharge', ''),
        hoarseness=patient_responses.get('hoarseness', ''),
        throat_lump_sensation=patient_responses.get('throat_lump_sensation', ''),
        throat_ulcers=patient_responses.get('throat_ulcers', ''),
        nasal_congestion=patient_responses.get('nasal_congestion', ''),
        nasal_discharge=patient_responses.get('nasal_discharge', ''),
        nosebleeds=patient_responses.get('nosebleeds', ''),
        nasal_obstruction=patient_responses.get('nasal_obstruction', ''),
        loss_of_taste_smell=patient_responses.get('loss_of_taste_smell', ''),
        recent_illness=patient_responses.get('recent_illness', ''),
        medications=patient_responses.get('medications', ''),
        allergies=patient_responses.get('allergies', ''),
        smoking_exposure=patient_responses.get('smoking_exposure', ''),
    )

    # Create patient physical reportable from responses
    patient_physical = ENTPatientPhysicalReportable(
        recent_trauma=patient_physical_responses.get('recent_trauma', ''),
        visible_lesions_self=patient_physical_responses.get('visible_lesions_self', ''),
        facial_swelling=patient_physical_responses.get('facial_swelling', ''),
        lymph_node_awareness=patient_physical_responses.get('lymph_node_awareness', ''),
    )

    # Create nurse assessment findings
    auricle = AuricleAndMastoidAssessment(
        auricle_lateral_surface=nurse_responses.get('auricle_lesions', ''),
        auricle_medial_surface='Not assessed by patient',
        surrounding_tissue='Not assessed by patient',
        auricle_color=nurse_responses.get('auricle_color', ''),
        auricle_size_symmetry=nurse_responses.get('auricle_symmetry', ''),
        auricle_configuration=nurse_responses.get('auricle_configuration', ''),
        darwin_tubercle=nurse_responses.get('darwin_tubercle', ''),
        auricle_position=nurse_responses.get('auricle_position', ''),
        auricle_firmness=nurse_responses.get('auricle_firmness', ''),
        auricle_recoil=nurse_responses.get('auricle_recoil', ''),
        postauricular_tenderness=nurse_responses.get('postauricular_tenderness', ''),
        mastoid_tenderness=nurse_responses.get('mastoid_tenderness', ''),
        lobule_pain_on_pulling=nurse_responses.get('lobule_pain', ''),
        auricle_overall='To be determined by clinician',
    )

    canal = ExternalAuditoryCanal(
        canal_discharge=nurse_responses.get('canal_discharge', ''),
        canal_odor=nurse_responses.get('canal_odor', ''),
        canal_wall_color=nurse_responses.get('canal_color', ''),
        canal_wall_condition=nurse_responses.get('canal_condition', ''),
        canal_hairs=nurse_responses.get('canal_hairs', ''),
        cerumen_amount=nurse_responses.get('cerumen_amount', ''),
        cerumen_color_texture=nurse_responses.get('cerumen_color', ''),
        canal_foreign_body=nurse_responses.get('canal_foreign_body', ''),
        canal_lesions='To be assessed by clinician',
        canal_overall='To be determined by clinician',
    )

    tympanum = TympanumAssessment(
        umbo_visibility=nurse_responses.get('umbo_visibility', ''),
        malleus_handle=nurse_responses.get('malleus_handle', ''),
        light_reflex=nurse_responses.get('light_reflex', ''),
        membrane_color=nurse_responses.get('membrane_color', ''),
        membrane_opacification=nurse_responses.get('membrane_opacity', ''),
        membrane_contour=nurse_responses.get('membrane_contour', ''),
        membrane_perforation=nurse_responses.get('membrane_perforation', ''),
        membrane_mobility=nurse_responses.get('membrane_mobility', ''),
        tympanum_overall='To be determined by clinician',
    )

    hearing = HearingAssessment(
        conversational_response=nurse_responses.get('conversational_response', ''),
        speech_tone_quality=nurse_responses.get('speech_tone', ''),
        whispered_voice_right=nurse_responses.get('whispered_right', ''),
        whispered_voice_left=nurse_responses.get('whispered_left', ''),
        weber_test_result=nurse_responses.get('weber_test', ''),
        rinne_test_right=nurse_responses.get('rinne_right', ''),
        rinne_test_left=nurse_responses.get('rinne_left', ''),
        hearing_loss_pattern='To be determined by clinician',
        hearing_overall='To be determined by clinician',
    )

    nose_external = NoseExternalAssessment(
        nose_shape_size=nurse_responses.get('nose_shape', ''),
        nasal_bridge=nurse_responses.get('nasal_bridge', ''),
        columella_alignment=nurse_responses.get('columella', ''),
        naris_width=nurse_responses.get('naris_width', ''),
        nose_color=nurse_responses.get('nose_color', ''),
        nares_shape=nurse_responses.get('nares_shape', ''),
        nares_discharge=nurse_responses.get('nares_discharge_clinical', ''),
        nasal_flaring=nurse_responses.get('nasal_flaring', ''),
        nose_firmness=nurse_responses.get('nose_palpation', ''),
        nose_masses=nurse_responses.get('nose_masses', ''),
        nares_patency=nurse_responses.get('nares_patency', ''),
        nose_overall='To be determined by clinician',
    )

    nasal_mucosa = NasalMucosaSeptumAssessment(
        mucosa_color=nurse_responses.get('mucosa_color', ''),
        mucosa_condition=nurse_responses.get('mucosa_condition', ''),
        turbinate_condition=nurse_responses.get('turbinate_condition', ''),
        turbinate_obstruction='To be assessed by clinician',
        septum_position=nurse_responses.get('septum_position', ''),
        septum_straightness=nurse_responses.get('septum_straightness', ''),
        posterior_cavity=nurse_responses.get('posterior_cavity', ''),
        turbinates_visible=nurse_responses.get('turbinates_visible', ''),
        septal_perforation=nurse_responses.get('septal_perforation', ''),
        nasal_polyps=nurse_responses.get('nasal_polyps', ''),
        septal_hairs=nurse_responses.get('septal_hairs', ''),
        septal_discharge=nurse_responses.get('septal_discharge', ''),
        mucosa_overall='To be determined by clinician',
    )

    sinus = SinusAssessment(
        forehead_swelling=nurse_responses.get('forehead_swelling', ''),
        frontal_sinus_palpation=nurse_responses.get('frontal_tenderness', ''),
        cheek_swelling=nurse_responses.get('cheek_swelling', ''),
        maxillary_sinus_palpation=nurse_responses.get('maxillary_tenderness', ''),
        sinus_transillumination='To be assessed by clinician',
        sinus_overall='To be determined by clinician',
    )

    lips = LipsAssessment(
        lips_symmetry=nurse_responses.get('lips_symmetry', ''),
        lips_color=nurse_responses.get('lips_color', ''),
        lips_border=nurse_responses.get('lips_border', ''),
        lips_condition=nurse_responses.get('lips_condition', ''),
        lips_lesions=nurse_responses.get('lips_lesions', ''),
        lips_macules=nurse_responses.get('lips_macules', ''),
        lips_overall='To be determined by clinician',
    )

    teeth = TeethAssessment(
        number_of_teeth=nurse_responses.get('number_teeth', ''),
        teeth_anchoring=nurse_responses.get('teeth_anchoring', ''),
        occlusion_molars=nurse_responses.get('occlusion_molars', ''),
        occlusion_premolars_canines=nurse_responses.get('occlusion_premolars', ''),
        occlusion_incisors=nurse_responses.get('occlusion_incisors', ''),
        teeth_color=nurse_responses.get('teeth_color', ''),
        teeth_caries=nurse_responses.get('teeth_caries', ''),
        teeth_wear=nurse_responses.get('teeth_wear', ''),
        teeth_overall='To be determined by clinician',
    )

    buccal = BuccalMucosaAssessment(
        buccal_color=nurse_responses.get('buccal_color', ''),
        buccal_condition=nurse_responses.get('buccal_condition', ''),
        stenson_duct=nurse_responses.get('stenson_duct', ''),
        fordyce_spots=nurse_responses.get('fordyce_spots', ''),
        buccal_ulcerations=nurse_responses.get('buccal_condition', ''),
        buccal_overall='To be determined by clinician',
    )

    gingival = GingivalAssessment(
        gingival_color=nurse_responses.get('gingival_color', ''),
        gingival_margin=nurse_responses.get('gingival_margin', ''),
        gingival_inflammation=nurse_responses.get('gingival_inflammation', ''),
        gingival_bleeding=nurse_responses.get('gingival_bleeding', ''),
        gingival_lesions='To be assessed by clinician',
        gingival_pockets=nurse_responses.get('gingival_pockets', ''),
        gingival_enlargement='To be assessed by clinician',
        gingival_recession='To be assessed by clinician',
        gingival_overall='To be determined by clinician',
    )

    tongue = TongueAssessment(
        tongue_position=nurse_responses.get('tongue_position', ''),
        tongue_size=nurse_responses.get('tongue_size', ''),
        tongue_fasciculations=nurse_responses.get('tongue_fasciculations', ''),
        tongue_color=nurse_responses.get('tongue_color', ''),
        tongue_surface=nurse_responses.get('tongue_surface', ''),
        tongue_movement=nurse_responses.get('tongue_movement', ''),
        tongue_ulceration=nurse_responses.get('tongue_ulceration', ''),
        ventral_surface=nurse_responses.get('ventral_surface', ''),
        lateral_borders=nurse_responses.get('lateral_borders', ''),
        tongue_palpation=nurse_responses.get('tongue_palpation', ''),
        tongue_coating=nurse_responses.get('tongue_color', ''),
        tongue_overall='To be determined by clinician',
    )

    palate = PalateUvulaAssessment(
        hard_palate_color=nurse_responses.get('hard_palate_color', ''),
        hard_palate_shape=nurse_responses.get('hard_palate_shape', ''),
        hard_palate_rugae=nurse_responses.get('hard_palate_rugae', ''),
        hard_palate_protuberance=nurse_responses.get('palate_midline_torus', ''),
        soft_palate_color=nurse_responses.get('soft_palate_color', ''),
        soft_palate_contiguity='To be assessed by clinician',
        uvula_position=nurse_responses.get('uvula_position', ''),
        uvula_appearance=nurse_responses.get('uvula_appearance', ''),
        uvula_movement=nurse_responses.get('gag_reflex', ''),
        gag_reflex=nurse_responses.get('gag_reflex', ''),
        palatal_arches=nurse_responses.get('palatal_arches', ''),
        tonsil_size=nurse_responses.get('tonsil_size', ''),
        tonsil_color=nurse_responses.get('tonsil_color', ''),
        tonsil_exudate=nurse_responses.get('tonsil_exudate', ''),
        palate_overall='To be determined by clinician',
    )

    summary = AssessmentSummary(
        ear_findings='Summary of ear findings to be determined',
        hearing_assessment_summary=f"Weber: {nurse_responses.get('weber_test', '')}, Rinne R: {nurse_responses.get('rinne_right', '')}, Rinne L: {nurse_responses.get('rinne_left', '')}",
        nose_findings=f"Septum: {nurse_responses.get('septum_position', '')}, Turbinates: {nurse_responses.get('turbinate_condition', '')}, Polyps: {nurse_responses.get('nasal_polyps', '')}",
        sinus_findings=f"Frontal: {nurse_responses.get('forehead_swelling', '')}, Maxillary: {nurse_responses.get('cheek_swelling', '')}",
        throat_findings=f"Tonsils: {nurse_responses.get('tonsil_size', '')}, Exudate: {nurse_responses.get('tonsil_exudate', '')}, Uvula: {nurse_responses.get('uvula_position', '')}",
        oral_findings=f"Teeth: {nurse_responses.get('number_teeth', '')}, Caries: {nurse_responses.get('teeth_caries', '')}, Tongue: {nurse_responses.get('tongue_position', '')}",
        major_abnormalities='To be identified by clinician',
        red_flag_findings='To be determined - severe sore throat, airway obstruction, sudden hearing loss',
        clinical_impression='To be completed by clinician',
        recommended_workup='Audiometry, imaging, cultures if indicated',
        specialist_referral='To be determined based on findings',
        follow_up_plan='Routine monitoring with specialist evaluation if indicated',
    )

    nurse_answers = ENTNurseAnswers(
        auricle_and_mastoid=auricle,
        external_auditory_canal=canal,
        tympanum=tympanum,
        hearing_assessment=hearing,
        nose_external=nose_external,
        nasal_mucosa_septum=nasal_mucosa,
        sinus_assessment=sinus,
        lips_assessment=lips,
        teeth_assessment=teeth,
        buccal_mucosa=buccal,
        gingival_assessment=gingival,
        tongue_assessment=tongue,
        palate_uvula=palate,
        assessment_summary=summary,
    )

    # Create final medical report
    report = ENTMedicalReport(
        patient_name=patient_name,
        examination_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        patient_answers=patient_history,
        patient_physical_reportable=patient_physical,
        nurse_answers=nurse_answers,
    )

    # Save to file if path provided
    if output_path is None:
        output_path = Path("outputs") / f"{patient_name.lower().replace(' ', '_')}_ent_report.json"

    # Create outputs directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save report as JSON
    with open(output_path, 'w') as f:
        json.dump(json.loads(report.model_dump_json()), f, indent=2)

    print(f"\n✓ ENT Medical Report saved to: {output_path}")

    return report


if __name__ == "__main__":
    print("ENT Assessment Module - Patient/Nurse Answer Separation")
    print("\nTo use this module:")
    print("1. Call ask_ent_patient_questions() - Patient answers their own questions")
    print("2. Call ask_ent_patient_physical_questions() - Patient reports visible findings")
    print("3. Call ask_ent_nurse_questions() - Clinician/nurse performs examination")
    print("4. Call create_ent_medical_report() - Combine all answers into report")
    print("\nExample:")
    print("  patient_resp = ask_ent_patient_questions()")
    print("  patient_phys = ask_ent_patient_physical_questions()")
    print("  nurse_resp = ask_ent_nurse_questions()")
    print("  report = create_ent_medical_report('John Doe', patient_resp, patient_phys, nurse_resp)")
