"""
Lymphatic System Assessment

Evaluate patient lymphatic system health through clinical examination of lymph nodes,
edema, lymphatic drainage, and related symptoms using BaseModel definitions and
interactive patient questioning.
"""

import sys
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.utils import save_model_response

# Fix import path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.pydantic_prompt_generator import PromptStyle


class LymphNodeAssessment(BaseModel):
    """Assessment of palpable lymph nodes in different body regions."""
    cervical_nodes: str = Field(description="Cervical lymph nodes (neck) - present/absent/palpable. Size in cm if present, consistency (firm/soft/matted), mobility, tenderness")
    supraclavicular_nodes: str = Field(description="Supraclavicular nodes - present/absent. Location (left/right/bilateral), size, consistency, mobility")
    axillary_nodes: str = Field(description="Axillary nodes (armpit) - present/absent. Size, number if multiple, consistency, tenderness, mobility")
    inguinal_nodes: str = Field(description="Inguinal nodes (groin) - present/absent. Size, consistency, mobility, number of nodes, tenderness")
    epitrochlear_nodes: str = Field(description="Epitrochlear nodes (elbow) - present/absent. Size, consistency, tenderness")
    abdominal_nodes: str = Field(description="Abdominal/mesenteric nodes - assessment if palpable. Size, consistency, tenderness, location")
    mediastinal_nodes: str = Field(description="Mediastinal nodes - if identified on imaging. Size, location, clinical significance")
    other_nodes: str = Field(description="Any other enlarged or palpable nodes in other locations - describe location, size, characteristics")
    generalized_lymphadenopathy: str = Field(description="Generalized lymphadenopathy (nodes >1cm in multiple non-contiguous sites) - present/absent/focal")
    node_characteristics: str = Field(description="Overall characteristics of palpable nodes - mobile/fixed, tender/non-tender, soft/firm/hard, matted/discrete")


class Edema(BaseModel):
    """Assessment of lymphedema and other forms of edema."""
    peripheral_edema_upper_extremity: str = Field(description="Upper extremity edema - present/absent. If present: which arm (right/left/bilateral), location (hand/forearm/arm/shoulder), pitting/non-pitting, grade (1-4), circumference difference if bilateral")
    peripheral_edema_lower_extremity: str = Field(description="Lower extremity edema - present/absent. Which leg (right/left/bilateral), location (foot/calf/thigh), pitting/non-pitting, grade (1-4), circumference measurements")
    facial_edema: str = Field(description="Facial edema - present/absent. If present: distribution (periorbital/generalized/asymmetric), severity, associated symptoms")
    genital_edema: str = Field(description="Genital edema - present/absent. If present: location, severity, skin changes")
    lymphedema_staging: str = Field(description="Lymphedema staging if present - Stage 0 (latency)/Stage 1 (spontaneously reversible)/Stage 2 (lymphostatic fibrosis)/Stage 3 (lymphostatic elephantiasis)")
    skin_changes_from_edema: str = Field(description="Skin changes associated with edema - fibrosis, hyperkeratosis, papillomatosis, color changes, infection signs")
    edema_pitting_response: str = Field(description="Pitting response - immediate/delayed return/no return after pressing. Indicates severity")
    circumference_measurements: str = Field(description="Limb circumference measurements at standardized points for comparison and monitoring")


class LymphaticDrainage(BaseModel):
    """Assessment of lymphatic drainage patterns and function."""
    unilateral_drainage: str = Field(description="Unilateral lymph drainage - which side (right/left). Asymmetric findings suggesting obstruction")
    drainage_obstruction_signs: str = Field(description="Signs of lymphatic obstruction - dilated veins, collateral circulation, skin changes indicating blocked drainage")
    venous_assessment: str = Field(description="Associated venous findings - varicose veins, spider veins, venous insufficiency signs")
    lymphatic_vessel_visibility: str = Field(description="Visible lymphatic vessels or dilated veins - present/absent. Pattern and distribution")
    lymphatic_malfunction_indicators: str = Field(description="Indicators of lymphatic malfunction - poor wound healing, recurrent infections, chronic edema, skin thickening")


class SystemicSymptoms(BaseModel):
    """Patient-reported symptoms related to lymphatic system."""
    swelling_location: str = Field(description="Location of swelling or puffiness - arms/legs/face/neck/generalized/other. Duration (acute/chronic)")
    swelling_onset: str = Field(description="Onset of swelling - sudden/gradual. Precipitating factors (trauma/surgery/infection/unknown)")
    swelling_progression: str = Field(description="How swelling has progressed - stable/worsening/improving/intermittent/cyclical")
    pain_heaviness: str = Field(description="Associated pain or heaviness in affected areas - yes/no. Severity (mild/moderate/severe), constant/intermittent")
    fatigue: str = Field(description="Fatigue or systemic symptoms - present/absent. Associated with swelling or independent")
    fever_night_sweats: str = Field(description="Fever or night sweats - yes/no. Frequency, severity, associated with node enlargement")
    recurrent_infections: str = Field(description="Recurrent infections in affected limb/area - yes/no. Type, frequency, treatment response")
    constitutional_symptoms: str = Field(description="Weight loss, loss of appetite, general malaise - yes/no. Timeline, severity")


class MedicalHistory(BaseModel):
    """Relevant medical history affecting lymphatic system."""
    cancer_history: str = Field(description="History of cancer - yes/no. Type, treatment (surgery/radiation/chemotherapy), location, time since treatment")
    cancer_ongoing: str = Field(description="Ongoing cancer or active treatment - yes/no. Currently receiving chemotherapy/radiation that could affect lymphatics")
    surgery_history: str = Field(description="Previous surgery with lymph node removal/dissection - yes/no. Type, location, date, extent of lymph node removal")
    trauma_injury: str = Field(description="Previous trauma or injury to areas with lymph node removal - yes/no. Location, severity, treatment")
    infection_history: str = Field(description="History of serious infections (cellulitis, sepsis) - yes/no. Location, treatment, recurrence")
    venous_insufficiency: str = Field(description="Known venous insufficiency or DVT - yes/no. Location, treatment, duration")
    autoimmune_conditions: str = Field(description="Autoimmune or rheumatologic conditions - yes/no. Type (lupus, rheumatoid arthritis, etc.), treatment")
    radiation_therapy_history: str = Field(description="History of radiation therapy - yes/no. Site, dates, dose, distance from assessment area")
    congenital_abnormalities: str = Field(description="Congenital lymphatic abnormalities - yes/no. Type (hypoplasia, dysplasia, functional abnormality)")
    vascular_surgery: str = Field(description="Previous vascular surgery or interventions - yes/no. Type, location, impact on lymphatic drainage")


class CurrentMedications(BaseModel):
    """Current medications affecting lymphatic function or assessment."""
    diuretics: str = Field(description="Diuretic use - yes/no. Type, dose, duration, effect on edema/swelling")
    anticoagulants: str = Field(description="Anticoagulants (warfarin, DOACs) - yes/no. Reason, duration, affects bruising assessment")
    corticosteroids: str = Field(description="Corticosteroid use - yes/no. Dose, duration, effect on immune/lymphatic function")
    immunosuppressants: str = Field(description="Immunosuppressant medications - yes/no. Type, reason, duration")
    anti_inflammatory: str = Field(description="NSAIDs or other anti-inflammatory agents - yes/no. Frequency, indication")
    other_medications: str = Field(description="Other medications affecting lymphatic/vascular function - describe")
    supplements_herbs: str = Field(description="Supplements or herbal remedies - yes/no. Type, reason for use")


class LymphedemaRiskFactors(BaseModel):
    """Assessment of risk factors for lymphedema development."""
    cancer_related_risk: str = Field(description="Cancer-related risk - current/history of cancer, node removal, radiation. Risk level (low/moderate/high)")
    BMI: str = Field(description="Body Mass Index - value. Obesity increases lymphedema risk")
    infection_risk: str = Field(description="Infection risk - recurrent cellulitis, immunocompromise. Triggers for infection")
    venous_insufficiency_risk: str = Field(description="Concurrent venous insufficiency - yes/no. Compounds lymphatic dysfunction")
    immobility: str = Field(description="Immobility or sedentary lifestyle - yes/no. Activity level, ability to exercise")
    limb_use_demands: str = Field(description="Limb use demands and occupational risk - physically demanding job, repetitive strain")
    psychosocial_factors: str = Field(description="Psychosocial factors - depression, poor compliance with treatment/compression, body image concerns")


class FunctionalImpact(BaseModel):
    """Impact of lymphatic dysfunction on daily function."""
    activities_of_daily_living: str = Field(description="Impact on ADLs - unaffected/mild impact/moderate impact/severe impact. Examples (dressing, bathing, etc.)")
    work_impact: str = Field(description="Impact on work or occupational function - no impact/modified duties/unable to work/on disability")
    social_impact: str = Field(description="Social impact - normal interaction/withdrawal/isolation/relationship changes")
    mental_health_impact: str = Field(description="Mental health impact - anxiety/depression/body image distress/other psychological effects")
    mobility_impact: str = Field(description="Impact on mobility - normal gait/modified gait/assistive device use/severe limitation")
    exercise_tolerance: str = Field(description="Exercise tolerance - normal/limited/unable. Specific limitations")
    sleep_quality: str = Field(description="Sleep quality affected - yes/no. How (pain/position changes/night sweats/discomfort)")


class AssessmentSummary(BaseModel):
    """Overall lymphatic system assessment summary and clinical recommendations."""
    lymphatic_function_status: str = Field(description="Lymphatic function status - normal/mildly impaired/moderately impaired/severely impaired")
    lymph_node_findings: str = Field(description="Summary of lymph node findings - normal/reactive enlargement/abnormal/concerning for malignancy/other")
    edema_status: str = Field(description="Edema status - none/mild/moderate/severe, pitting/non-pitting, localized/generalized")
    lymphedema_presence: str = Field(description="Lymphedema present - yes/no. If yes: type (primary/secondary), stage, location")
    identified_complications: str = Field(description="Identified complications - infection risk/cellulitis history/fibrosis/functional impairment/other")
    contributing_factors: str = Field(description="Contributing factors to lymphatic dysfunction - cancer treatment/surgery/trauma/immobility/obesity/venous disease/infection/other, comma-separated")
    major_findings: str = Field(description="Major clinical findings requiring attention, comma-separated")
    risk_stratification: str = Field(description="Risk level - low/moderate/high. Justification based on findings")
    recommendations: str = Field(description="Recommendations for management - conservative/compression therapy/lymphatic drainage/exercise/weight management/infection prevention/specialist referral, comma-separated")
    specialist_referral: str = Field(description="Specialist referral recommendations - lymphedema specialist/vascular surgeon/oncologist/dermatologist/other and rationale")
    follow_up_plan: str = Field(description="Recommended follow-up - routine monitoring/1 month follow-up/3 month follow-up/before/after surgery/based on progression")


class AcuteLymphangitis(BaseModel):
    """Assessment for acute lymphangitis (inflammation of lymphatic vessels)."""
    red_streaks_present: str = Field(description="Red streaks or red lines on skin from infection site towards nodes - present/absent. Location and pattern")
    painful_cords: str = Field(description="Tender, painful cord-like structures indicating inflamed lymph vessels - present/absent. Location")
    lymphatic_vessel_inflammation: str = Field(description="Visible inflammation along lymphatic vessels/drainage lines - present/absent")
    associated_cellulitis: str = Field(description="Associated cellulitis (area red, swollen, warm, tender) - present/absent. Location")
    systemic_signs: str = Field(description="Systemic infection signs (fever, chills, malaise, weakness) - present/absent")
    entry_wound: str = Field(description="Known entry wound/skin break (cut, bite, fungal infection) - present/absent. Description")
    symptom_duration: str = Field(description="Duration of symptoms - hours/days/timeline")
    progression: str = Field(description="Progression status - stable/worsening/rapidly worsening/spreading")
    lymphangitis_diagnosis: str = Field(description="Acute lymphangitis indicated - yes/no/possible/probable. Clinical urgency assessment")


class LymphomaScreening(BaseModel):
    """Screening for Hodgkin Lymphoma and Non-Hodgkin Lymphoma."""
    persistent_lymphadenopathy: str = Field(description="Persistently enlarged lymph nodes >3 months - present/absent. Location and duration")
    b_symptoms: str = Field(description="B-symptoms (fever, night sweats, weight loss) - present/absent. Which symptoms present")
    weight_loss_significant: str = Field(description="Unintentional weight loss >10% body weight in past 6 months - present/absent. Amount")
    night_sweats_severity: str = Field(description="Night sweats severe enough to soak clothing/sheets - present/absent. Frequency")
    unexplained_fever: str = Field(description="Unexplained fever pattern - absent/low-grade/high, intermittent/persistent")
    lymph_node_distribution: str = Field(description="Lymph node distribution pattern - localized/generalized/mediastinal/abdominal/mixed")
    node_characteristics_malignancy: str = Field(description="Node characteristics concerning for malignancy (hard/fixed/matted/rubbery) - present/absent")
    pruritus: str = Field(description="Unexplained itching/pruritus (especially post-warm shower) - absent/mild/moderate/severe")
    fatigue_disproportionate: str = Field(description="Excessive fatigue/weakness out of proportion - present/absent")
    family_history_lymphoma: str = Field(description="Family history of lymphoma or hematologic malignancy - none/yes (specify relative/age)")
    lymphoma_risk_assessment: str = Field(description="Lymphoma risk assessment - low/moderate/high. Red flags present/absent")


class EBVMononucleosisScreening(BaseModel):
    """Screening for Epstein-Barr Virus (EBV) infection and infectious mononucleosis."""
    pharyngitis: str = Field(description="Sore throat or pharyngitis - absent/mild/moderate/severe, duration")
    throat_examination: str = Field(description="Throat appearance - normal/red/swollen/exudative, describe findings")
    tonsillar_enlargement: str = Field(description="Tonsillar enlargement - absent/present, bilateral/unilateral, size")
    tonsillar_exudate: str = Field(description="White or gray exudate on tonsils - absent/present, extent")
    cervical_lymphadenopathy_ebv: str = Field(description="Cervical lymphadenopathy - absent/present, bilateral/unilateral, tenderness")
    splenomegaly: str = Field(description="Hepatosplenomegaly - splenic enlargement absent/present, tenderness")
    hepatomegaly: str = Field(description="Hepatic enlargement - absent/present, tenderness")
    jaundice: str = Field(description="Jaundice or yellowing of skin/eyes - absent/present")
    recent_ebv_exposure: str = Field(description="Recent EBV exposure (kissing, shared drinks, close contact) - none/yes (describe)")
    atypical_lymphocytes_noted: str = Field(description="Blood work with atypical lymphocytes or abnormal WBC - not done/normal/abnormal (specify)")
    monospot_ebv_serology: str = Field(description="Monospot test or EBV serology - not done/negative/positive (IgM/IgG)")
    symptom_timeline: str = Field(description="Symptom timeline - acute onset/gradual/ongoing, describe pattern")
    ebv_diagnosis_likelihood: str = Field(description="EBV/mononucleosis likelihood - unlikely/possible/probable/consistent with diagnosis")


class StreptococcalPharyngitisScreening(BaseModel):
    """Screening for Streptococcal pharyngitis (Group A Streptococcus infection)."""
    sore_throat_strep: str = Field(description="Sore throat - absent/mild/moderate/severe, duration")
    runny_nose: str = Field(description="Runny nose or nasal congestion - absent/mild/moderate/present")
    headache_strep: str = Field(description="Headache - absent/mild/moderate/severe")
    fatigue_strep: str = Field(description="Fatigue or general malaise - absent/present")
    abdominal_pain_strep: str = Field(description="Abdominal pain or nausea - absent/mild/moderate/severe")
    throat_appearance_strep: str = Field(description="Throat appearance on examination - normal/red/swollen/exudate")
    anterior_cervical_nodes_strep: str = Field(description="Anterior cervical lymph nodes - absent/present, size, firm/discrete/tender")
    fever_strep: str = Field(description="Fever present - absent/yes, temperature if known")
    rash_scarlet_fever: str = Field(description="Rash present (sandpaper-like, characteristic of scarlet fever) - absent/present")
    streptococcal_pharyngitis_likelihood: str = Field(description="Streptococcal pharyngitis likelihood - unlikely/possible/probable/consistent with diagnosis")


class HerpesSimplexScreening(BaseModel):
    """Screening for Herpes Simplex Virus (HSV) infection."""
    burning_itching_lesions: str = Field(description="Burning or itching lesions - absent/present, duration, severity")
    lesion_location_oral: str = Field(description="Lesions location on lips or around mouth - absent/present, describe")
    lesion_location_gingival: str = Field(description="Discrete labial and/or gingival ulcers/vesicles - absent/present, number, appearance")
    fever_hsv: str = Field(description="High fever - absent/present, temperature if known")
    anterior_cervical_nodes_hsv: str = Field(description="Anterior cervical lymph node enlargement - absent/present, bilateral/unilateral, size")
    submandibular_nodes_hsv: str = Field(description="Submandibular lymph node enlargement - absent/present, bilateral/unilateral, size")
    node_characteristics_hsv: str = Field(description="Node characteristics (firm/discrete/movable/tender) - describe")
    vesicle_progression: str = Field(description="Progression of lesions (clear vesicles -> pustules -> ulcers -> crusts) - describe stage")
    systemic_symptoms_hsv: str = Field(description="Systemic symptoms (malaise, myalgia, headache) - absent/present")
    primary_vs_recurrent: str = Field(description="Primary HSV infection vs recurrent episode - primary/recurrent/unknown")
    hsv_diagnosis_likelihood: str = Field(description="Herpes simplex likelihood - unlikely/possible/probable/consistent with diagnosis")


class HIVAIDSScreening(BaseModel):
    """Screening for Human Immunodeficiency Virus (HIV) and Acquired Immunodeficiency Syndrome (AIDS)."""
    generalized_lymphadenopathy_hiv: str = Field(description="Generalized lymphadenopathy (>1cm in multiple non-contiguous sites, >3 months) - absent/present")
    lymph_node_sites_affected: str = Field(description="Lymph node sites affected - cervical/axillary/inguinal/abdominal/other, describe pattern")
    lymph_node_consistency_hiv: str = Field(description="Node consistency - firm/soft/mobile/fixed, size range")
    fever_prolonged_hiv: str = Field(description="Prolonged fever (>1 month) - absent/present, pattern")
    night_sweats_hiv: str = Field(description="Night sweats - absent/present, severity, soaking clothes/sheets")
    weight_loss_hiv: str = Field(description="Unintentional weight loss >10% - absent/present, timeline, amount")
    opportunistic_infection_history: str = Field(description="History of opportunistic infections (PCP, candida, CMV, toxoplasmosis) - none/yes (specify)")
    oral_candidiasis: str = Field(description="Oral candidiasis (thrush) - absent/present")
    herpes_infections_hiv: str = Field(description="Recurrent or severe herpes infections (HSV, VZV) - none/occasional/frequent/severe")
    respiratory_symptoms_hiv: str = Field(description="Respiratory symptoms (persistent cough, shortness of breath) - absent/present")
    gi_symptoms_hiv: str = Field(description="GI symptoms (diarrhea, esophageal discomfort) - absent/present")
    skin_findings_hiv: str = Field(description="Skin findings (seborrheic dermatitis, psoriasis, Kaposi sarcoma, molluscum) - absent/present (describe)")
    neurological_symptoms_hiv: str = Field(description="Neurological symptoms (headache, cognitive changes, peripheral neuropathy) - absent/present")
    cd4_count: str = Field(description="CD4 count if known - value, date of test, interpretation")
    viral_load: str = Field(description="Viral load if known - value, date of test")
    hiv_testing_history: str = Field(description="Prior HIV testing - never tested/tested negative (when)/tested positive (when/confirmation)")
    risk_exposure: str = Field(description="Risk exposure history - none/sexual/injection drug use/occupational needle stick/transfusion/other (describe)")
    antiretroviral_therapy: str = Field(description="Antiretroviral therapy - none/yes (regimen, adherence, duration)")
    hiv_aids_likelihood: str = Field(description="HIV/AIDS likelihood - unlikely/possible/probable/confirmed")


class LymphaticSystemAssessment(BaseModel):
    """
    Comprehensive lymphatic system assessment.

    Organized as a collection of BaseModel sections representing distinct aspects
    of lymphatic system evaluation. Includes assessment of lymph nodes, edema,
    lymphatic drainage, symptoms, medical history, functional impact, and
    acute lymphangitis screening.
    """
    # Lymph node assessment
    lymph_node_assessment: LymphNodeAssessment

    # Edema assessment
    edema: Edema

    # Lymphatic drainage patterns
    lymphatic_drainage: LymphaticDrainage

    # Patient-reported symptoms
    systemic_symptoms: SystemicSymptoms

    # Relevant medical history
    medical_history: MedicalHistory

    # Current medications
    current_medications: CurrentMedications

    # Lymphedema risk factors
    lymphedema_risk_factors: LymphedemaRiskFactors

    # Acute lymphangitis assessment
    acute_lymphangitis: AcuteLymphangitis

    # Lymphoma screening (Hodgkin & Non-Hodgkin)
    lymphoma_screening: LymphomaScreening

    # EBV/Mononucleosis screening
    ebv_mononucleosis_screening: EBVMononucleosisScreening

    # Streptococcal pharyngitis screening
    streptococcal_pharyngitis_screening: StreptococcalPharyngitisScreening

    # Herpes simplex screening
    herpes_simplex_screening: HerpesSimplexScreening

    # HIV/AIDS screening
    hiv_aids_screening: HIVAIDSScreening

    # Functional impact
    functional_impact: FunctionalImpact

    # Final assessment
    assessment_summary: AssessmentSummary


def ask_lymphatic_questions() -> dict:
    """
    Ask patient lymphatic system assessment questions interactively.
    Returns a dictionary of patient responses to be used in assessment.
    """
    print("\n" + "="*60)
    print("LYMPHATIC SYSTEM ASSESSMENT")
    print("="*60)
    print("\nMEASURES: Evaluates lymphatic system function through assessment of:")
    print("  • Lymph node size, consistency, mobility, and tenderness")
    print("  • Edema (swelling) in extremities and face")
    print("  • Lymphatic drainage patterns and obstruction signs")
    print("  • Systemic symptoms (fever, fatigue, weight loss)")
    print("  • History of cancer, surgery, trauma, infection")
    print("  • Risk factors for lymphedema development")
    print("  • Screening for lymphoma, infections, and HIV")

    print("\nTOP 10 KEY ASSESSMENT QUESTIONS:")
    print("  1. Are you aware of any lumps, bumps, or swelling anywhere on your body?")
    print("  2. Do you have swelling in your arms, legs, face, or neck? Is it new or chronic?")
    print("  3. Do you experience pain or heaviness in swollen areas?")
    print("  4. Have you had cancer surgery, radiation, or lymph node removal?")
    print("  5. Do you have fever, night sweats, or unintentional weight loss?")
    print("  6. Have you experienced recent infections or cellulitis?")
    print("  7. Do you have red streaks, painful cords, or signs of infection in the swollen areas?")
    print("  8. What is your current activity level, and how does swelling affect your daily life?")
    print("  9. Are you on any medications (diuretics, anticoagulants, corticosteroids)?")
    print(" 10. Do you have a family history of lymphoma or hematologic conditions?")

    print("\n" + "="*60)
    print("LYMPHATIC SYSTEM ASSESSMENT QUESTIONNAIRE")
    print("="*60)

    responses = {}

    # LYMPH NODE ASSESSMENT
    print("\n--- LYMPH NODE ASSESSMENT ---")
    print("Clinical examination of lymph nodes by palpation.")
    print("Nodes are palpated for: size, consistency, mobility, tenderness, warmth")
    print()

    # Direct question about lumps awareness
    responses['aware_of_lumps'] = input("Are you aware of any lumps or bumps anywhere on your body? (no/yes, describe location/size/when noticed): ").strip()

    # CERVICAL NODES (neck)
    print("\n--- Cervical Nodes (Neck) ---")
    print("Palpation technique: Systematically palpate both sides of neck moving hand in circular fashion")
    responses['cervical_palpable'] = input("Are nodes palpable/enlarged in neck? (no/yes, describe location - anterior/posterior/chain): ").strip()
    responses['cervical_size'] = input("If palpable, size in cm or compared to object (pea/bean/grape/etc.): ").strip()
    responses['cervical_consistency'] = input("Consistency? (soft/firm/hard/rubbery/irregular): ").strip()
    responses['cervical_mobility'] = input("Mobility? (mobile/freely movable/fixed/matted): ").strip()
    responses['cervical_tenderness'] = input("Tenderness? (non-tender/mildly tender/very tender): ").strip()
    responses['cervical_warmth'] = input("Warmth over nodes? (normal/warm/hot/inflamed appearance): ").strip()
    responses['cervical_findings'] = input("UNEXPECTED findings? (enlarged/tender/red/discolored/fixed/matted/inflamed/warm): ").strip()

    # AXILLARY NODES (armpits)
    print("\n--- Axillary Nodes (Armpits) ---")
    print("Palpation technique: Support arm with one hand while probing axilla with other hand")
    responses['axillary_palpable'] = input("Are nodes palpable/enlarged in armpits? (no/yes, which side/both): ").strip()
    responses['axillary_size'] = input("If palpable, size and number: ").strip()
    responses['axillary_consistency'] = input("Consistency? (soft/firm/hard/rubbery): ").strip()
    responses['axillary_mobility'] = input("Mobility? (mobile/fixed/matted): ").strip()
    responses['axillary_tenderness'] = input("Tenderness? (non-tender/mildly tender/very tender): ").strip()
    responses['axillary_warmth'] = input("Warmth or redness? (no/yes, describe): ").strip()
    responses['axillary_findings'] = input("UNEXPECTED findings observed? (enlarged/tender/discolored/fixed/matted): ").strip()

    # INGUINAL NODES (groin)
    print("\n--- Inguinal Nodes (Groin) ---")
    print("Palpation technique: Palpate both horizontal and vertical chains in groin area")
    responses['inguinal_palpable'] = input("Are nodes palpable/enlarged in groin? (no/yes, which side/both): ").strip()
    responses['inguinal_size'] = input("If palpable, size and number: ").strip()
    responses['inguinal_consistency'] = input("Consistency? (soft/firm/hard): ").strip()
    responses['inguinal_mobility'] = input("Mobility? (mobile/fixed): ").strip()
    responses['inguinal_tenderness'] = input("Tenderness? (no/yes, severity): ").strip()
    responses['inguinal_warmth'] = input("Warmth or signs of infection? (no/yes): ").strip()
    responses['inguinal_findings'] = input("UNEXPECTED findings? (enlarged/tender/red/fixed/matted): ").strip()

    # SUPRACLAVICULAR NODES
    print("\n--- Supraclavicular Nodes (Above Collarbone) ---")
    responses['supraclavicular_palpable'] = input("Are supraclavicular nodes palpable? (no/yes, left/right/both): ").strip()
    responses['supraclavicular_characteristics'] = input("If palpable, characteristics (size/consistency/mobility/tenderness): ").strip()

    # EPITROCHLEAR NODES (elbow)
    print("\n--- Epitrochlear Nodes (Inner Elbow) ---")
    responses['epitrochlear_palpable'] = input("Are epitrochlear nodes palpable? (no/yes): ").strip()
    responses['epitrochlear_characteristics'] = input("If palpable, characteristics: ").strip()

    # OTHER LOCATIONS
    print("\n--- Other Body Locations ---")
    responses['other_palpable'] = input("Any other lumps or nodules palpable elsewhere on body? (no/yes, where/size): ").strip()

    # LUMP CHARACTERISTICS
    print("\n--- Lump Characteristics ---")
    responses['lump_characteristics'] = input("Are the lumps you noticed firm/hard, or soft and squishy? Movable or fixed? (describe): ").strip()
    responses['node_pain'] = input("Do the lumps/nodes hurt when you press on them or are they tender? (no/yes/sometimes): ").strip()
    responses['lump_changes'] = input("Have the lumps changed in size or number? (no/yes, how/timeline): ").strip()

    # SYSTEMIC SIGNS RELATED TO LYMPH NODES
    print("\n--- Associated Signs ---")
    responses['node_erythema'] = input("Any redness or discoloration over nodes? (no/yes): ").strip()
    responses['node_drainage'] = input("Any drainage, pus, or discharge from nodes? (no/yes): ").strip()
    responses['increased_vascularity'] = input("Increased redness/vascularity in areas with nodes? (no/yes): ").strip()

    # ACUTE LYMPHANGITIS ASSESSMENT
    print("\n--- ACUTE LYMPHANGITIS SCREENING ---")
    print("Lymphangitis: Inflammation of lymphatic vessels (red streaks/lines from infection source)")
    responses['red_streaks'] = input("Red streaks or red lines on skin (from infection site towards nodes)? (no/yes, describe location/pattern): ").strip()
    responses['painful_cords'] = input("Tender, painful cord-like structures (inflamed lymph vessels)? (no/yes, location): ").strip()
    responses['lymphatic_inflammation'] = input("Visible inflammation along lymphatic vessels/drainage lines? (no/yes): ").strip()
    responses['cellulitis_signs'] = input("Associated cellulitis (local area red, swollen, warm, tender)? (no/yes, location): ").strip()
    responses['systemic_infection_signs'] = input("Systemic infection signs (fever, chills, malaise, weakness)? (no/yes): ").strip()
    responses['entry_wound'] = input("Known entry wound or skin break (cut, bite, fungal infection, etc.)? (no/yes, describe): ").strip()
    responses['lymphangitis_timeline'] = input("How long have these symptoms been present? (hours/days): ").strip()
    responses['lymphangitis_progression'] = input("Has it been getting worse/spreading? (no/yes/rapidly worsening): ").strip()

    # LYMPHOMA SCREENING (Hodgkin & Non-Hodgkin)
    print("\n--- LYMPHOMA SCREENING ---")
    print("Questions to screen for Hodgkin Lymphoma and Non-Hodgkin Lymphoma")
    responses['persistent_lymphadenopathy'] = input("Persistently enlarged lymph nodes for >3 months? (no/yes, location/duration): ").strip()
    responses['b_symptoms'] = input("B-symptoms present (unexplained fever, night sweats, unintentional weight loss)? (no/yes, describe): ").strip()
    responses['weight_loss'] = input("Unintentional weight loss >10% body weight in past 6 months? (no/yes, amount): ").strip()
    responses['night_sweats_severity'] = input("Night sweats severe enough to soak clothing/sheets? (no/yes, frequency): ").strip()
    responses['fever_pattern'] = input("Unexplained fever (low-grade/high, intermittent/persistent)? (describe pattern): ").strip()
    responses['lymph_node_pattern'] = input("Lymph node pattern: localized/generalized/mediastinal/abdominal? (describe): ").strip()
    responses['node_characteristics_malignancy'] = input("Node characteristics concerning for malignancy (hard/fixed/matted/rubbery)? (yes/no): ").strip()
    responses['pruritus'] = input("Unexplained itching/pruritus (especially after warm shower/bath)? (no/yes, severity): ").strip()
    responses['fatigue_weakness'] = input("Excessive fatigue or weakness out of proportion to activity? (no/yes): ").strip()
    responses['lymphoma_family_history'] = input("Family history of lymphoma or hematologic malignancy? (no/yes, who/age): ").strip()

    # EPSTEIN-BARR VIRUS (EBV) / INFECTIOUS MONONUCLEOSIS SCREENING
    print("\n--- EPSTEIN-BARR VIRUS (EBV) / INFECTIOUS MONONUCLEOSIS SCREENING ---")
    print("Questions to assess for EBV infection and infectious mononucleosis")
    responses['sore_throat'] = input("Sore throat or pharyngitis? (no/yes, duration/severity): ").strip()
    responses['throat_appearance'] = input("Throat appearance: normal/red/swollen/white coating/exudate? (describe): ").strip()
    responses['tonsillar_enlargement'] = input("Enlarged tonsils? (no/yes, bilateral/unilateral, size): ").strip()
    responses['tonsillar_exudate'] = input("White/gray exudate on tonsils? (no/yes): ").strip()
    responses['cervical_lymphadenopathy'] = input("Cervical lymphadenopathy (swollen neck nodes)? (no/yes, bilateral/unilateral): ").strip()
    responses['splenomegaly'] = input("Enlarged spleen? (no/yes, tenderness): ").strip()
    responses['hepatomegaly'] = input("Enlarged liver? (no/yes, tenderness): ").strip()
    responses['jaundice'] = input("Jaundice or yellowing of skin/eyes? (no/yes): ").strip()
    responses['ebv_exposure'] = input("Recent exposure to EBV (kissing, shared drinks, close contact)? (no/yes, describe): ").strip()
    responses['atypical_lymphocytes'] = input("Any blood work showing atypical lymphocytes/abnormal WBC? (no/yes, results if known): ").strip()
    responses['monospot_test'] = input("Monospot test or EBV serology done? (no/yes, results): ").strip()
    responses['ebv_timeline'] = input("Timeline of symptoms (acute onset/gradual/ongoing)? (describe): ").strip()

    # STREPTOCOCCAL PHARYNGITIS SCREENING
    print("\n--- STREPTOCOCCAL PHARYNGITIS (GROUP A STREPTOCOCCUS) SCREENING ---")
    print("Questions to assess for Streptococcal pharyngitis (Strep throat)")
    responses['sore_throat_strep'] = input("Sore throat? (no/yes, severity, duration): ").strip()
    responses['runny_nose'] = input("Runny nose or nasal congestion? (no/yes): ").strip()
    responses['headache_strep'] = input("Headache? (no/yes, severity): ").strip()
    responses['fatigue_strep'] = input("Fatigue or general malaise? (no/yes): ").strip()
    responses['abdominal_pain_strep'] = input("Abdominal pain or nausea? (no/yes, severity): ").strip()
    responses['throat_appearance_strep'] = input("Throat appearance on exam (normal/red/swollen/exudate)? (describe): ").strip()
    responses['anterior_cervical_nodes_strep'] = input("Anterior cervical lymph nodes present? (no/yes, size, firm/discrete/tender): ").strip()
    responses['fever_strep'] = input("Fever? (no/yes, temperature if known): ").strip()
    responses['rash_scarlet_fever'] = input("Rash present (sandpaper-like, characteristic of scarlet fever)? (no/yes): ").strip()

    # HERPES SIMPLEX SCREENING
    print("\n--- HERPES SIMPLEX VIRUS (HSV) SCREENING ---")
    print("Questions to assess for Herpes Simplex Virus infection")
    responses['burning_itching_lesions'] = input("Burning or itching lesions on lips/mouth? (no/yes, duration, severity): ").strip()
    responses['lesion_location_oral'] = input("Lesions on lips or around mouth area? (no/yes, describe): ").strip()
    responses['lesion_location_gingival'] = input("Discrete ulcers or vesicles on lips/gums? (no/yes, number, appearance): ").strip()
    responses['fever_hsv'] = input("High fever present? (no/yes, temperature if known): ").strip()
    responses['anterior_cervical_nodes_hsv'] = input("Anterior cervical lymph node enlargement? (no/yes, bilateral/unilateral, size): ").strip()
    responses['submandibular_nodes_hsv'] = input("Submandibular lymph node enlargement? (no/yes, bilateral/unilateral, size): ").strip()
    responses['node_characteristics_hsv'] = input("Node characteristics? (firm/discrete/movable/tender): ").strip()
    responses['vesicle_progression'] = input("Progression of lesions (clear vesicles -> pustules -> ulcers -> crusts)? (describe current stage): ").strip()
    responses['systemic_symptoms_hsv'] = input("Systemic symptoms (malaise, body aches, headache)? (no/yes): ").strip()
    responses['primary_vs_recurrent'] = input("Is this a primary infection or recurrent episode? (primary/recurrent/unknown): ").strip()

    # HIV/AIDS SCREENING
    print("\n--- HIV/AIDS SCREENING ---")
    print("Questions to assess for HIV and AIDS")
    responses['generalized_lymphadenopathy_hiv'] = input("Generalized swollen lymph nodes (>1cm in multiple areas, >3 months)? (no/yes, describe): ").strip()
    responses['lymph_node_sites_affected'] = input("Lymph node sites affected (neck/armpits/groin/abdomen/other)? (describe pattern): ").strip()
    responses['lymph_node_consistency_hiv'] = input("Node consistency (firm/soft/mobile/fixed)? Size range? (describe): ").strip()
    responses['fever_prolonged_hiv'] = input("Prolonged fever (>1 month) with no clear cause? (no/yes, pattern): ").strip()
    responses['night_sweats_hiv'] = input("Night sweats soaking clothing/sheets? (no/yes, frequency, severity): ").strip()
    responses['weight_loss_hiv'] = input("Unintentional weight loss >10% body weight? (no/yes, amount, timeline): ").strip()
    responses['opportunistic_infection_history'] = input("History of opportunistic infections (PCP, candida, CMV, toxo)? (no/yes, specify): ").strip()
    responses['oral_candidiasis'] = input("Oral candidiasis (white coating/thrush in mouth)? (no/yes): ").strip()
    responses['herpes_infections_hiv'] = input("Recurrent or severe herpes infections? (none/occasional/frequent/severe): ").strip()
    responses['respiratory_symptoms_hiv'] = input("Respiratory symptoms (persistent cough, shortness of breath)? (no/yes): ").strip()
    responses['gi_symptoms_hiv'] = input("GI symptoms (chronic diarrhea, esophageal discomfort)? (no/yes): ").strip()
    responses['skin_findings_hiv'] = input("Skin findings (seborrheic dermatitis, psoriasis, unusual lesions)? (no/yes, describe): ").strip()
    responses['neurological_symptoms_hiv'] = input("Neurological symptoms (headache, cognitive changes, neuropathy)? (no/yes): ").strip()
    responses['cd4_count'] = input("CD4 count if known? (value, date): ").strip()
    responses['viral_load'] = input("Viral load if known? (value, date): ").strip()
    responses['hiv_testing_history'] = input("Prior HIV testing? (never/negative-when/positive-when): ").strip()
    responses['risk_exposure'] = input("Risk exposure history? (none/sexual/injection drug use/occupational/transfusion/other): ").strip()
    responses['antiretroviral_therapy'] = input("Currently on antiretroviral therapy? (no/yes, regimen if known): ").strip()

    # EDEMA AND SWELLING
    print("\n--- EDEMA AND SWELLING ---")
    responses['arm_swelling'] = input("Do you have swelling in your arms? (no/yes, which arm/both, location): ").strip()
    responses['leg_swelling'] = input("Do you have swelling in your legs? (no/yes, which leg/both, how severe): ").strip()
    responses['face_swelling'] = input("Any facial puffiness or swelling? (no/yes, around eyes/general/other): ").strip()
    responses['swelling_pitting'] = input("When you press on the swelling, does it leave an indent? (yes/no/not applicable): ").strip()
    responses['swelling_timeline'] = input("How long have you had this swelling? (days/weeks/months/years): ").strip()

    # SYMPTOMS
    print("\n--- SYMPTOMS ---")
    responses['heaviness'] = input("Do you feel heaviness or fullness in affected areas? (no/yes, how much): ").strip()
    responses['pain_swelling'] = input("Pain or discomfort associated with swelling? (no/yes, severity 1-10): ").strip()
    responses['infections'] = input("Have you had frequent infections in swollen areas? (no/yes, how often): ").strip()
    responses['fever_sweats'] = input("Fever or night sweats? (no/yes, frequency): ").strip()
    responses['fatigue'] = input("Unusual fatigue? (no/yes, when did it start): ").strip()

    # MEDICAL HISTORY
    print("\n--- MEDICAL HISTORY ---")
    responses['cancer_history'] = input("History of cancer? (no/yes, type and when): ").strip()
    responses['cancer_treatment'] = input("Cancer treatment received? (none/surgery/radiation/chemotherapy/combinations): ").strip()
    responses['node_removal'] = input("Have you had lymph nodes removed? (no/yes, how many, from where): ").strip()
    responses['surgery_history'] = input("Other surgeries affecting your arms or legs? (no/yes, describe): ").strip()
    responses['injury_history'] = input("Significant injury or trauma to arms/legs? (no/yes, when and severity): ").strip()
    responses['venous_problems'] = input("History of blood clots or varicose veins? (no/yes): ").strip()
    responses['autoimmune'] = input("Autoimmune conditions (lupus, rheumatoid arthritis)? (no/yes, which): ").strip()

    # LIFESTYLE AND RISK FACTORS
    print("\n--- LIFESTYLE AND RISK FACTORS ---")
    responses['weight'] = input("Current weight (kg) and height (cm) for BMI calculation: ").strip()
    responses['activity_level'] = input("Activity level (sedentary/light/moderate/active): ").strip()
    responses['occupation'] = input("Do you have a physically demanding job? (no/yes, describe): ").strip()
    responses['compression_use'] = input("Currently using compression garments? (no/yes, type): ").strip()
    responses['elevation'] = input("Do you elevate your legs/arms when they swell? (no/yes, how often): ").strip()

    # MEDICATIONS
    print("\n--- MEDICATIONS ---")
    responses['diuretics'] = input("Taking water pills/diuretics? (no/yes): ").strip()
    responses['blood_pressure_meds'] = input("Taking blood pressure or heart medications? (no/yes, which): ").strip()
    responses['hormones'] = input("Hormone therapy or birth control? (no/yes): ").strip()
    responses['corticosteroids'] = input("Corticosteroids? (no/yes): ").strip()

    # FUNCTIONAL IMPACT
    print("\n--- FUNCTIONAL IMPACT ---")
    responses['work_impact'] = input("Impact on work/daily activities? (none/mild/moderate/severe): ").strip()
    responses['clothing_fit'] = input("Difficulty fitting into clothing due to swelling? (no/yes): ").strip()
    responses['sleep_impact'] = input("Sleep affected by swelling or discomfort? (no/yes, how): ").strip()
    responses['emotional_impact'] = input("Emotional/psychological impact of swelling? (none/mild/moderate/significant): ").strip()
    responses['exercise_tolerance'] = input("Can you exercise normally? (yes/limited/no): ").strip()

    # PREVIOUS TREATMENT
    print("\n--- PREVIOUS TREATMENT ---")
    responses['previous_treatment'] = input("Previous treatment for swelling/lymphedema? (none/physical therapy/compression/medication/surgery): ").strip()
    responses['treatment_response'] = input("How did you respond to treatment? (improved/stable/worsened/not applicable): ").strip()

    return responses


def create_lymphatic_assessment_from_responses(patient_name: str, responses: dict, output_path: Optional[Path] = None) -> LymphaticSystemAssessment:
    """
    Create a structured lymphatic system assessment object from collected patient responses.

    Args:
        patient_name: Name of the patient
        responses: Dictionary of patient responses from questions
        output_path: Optional path to save JSON output

    Returns:
        LymphaticSystemAssessment: Validated assessment object
    """
    # Create assessment object from responses
    assessment_data = {
        "lymph_node_assessment": {
            "cervical_nodes": f"Palpable: {responses.get('cervical_palpable', '')}. Size: {responses.get('cervical_size', '')}. Consistency: {responses.get('cervical_consistency', '')}. Mobility: {responses.get('cervical_mobility', '')}. Tenderness: {responses.get('cervical_tenderness', '')}. Warmth: {responses.get('cervical_warmth', '')}. Unexpected findings: {responses.get('cervical_findings', 'None')}",
            "supraclavicular_nodes": f"Palpable: {responses.get('supraclavicular_palpable', '')}. {responses.get('supraclavicular_characteristics', '')}",
            "axillary_nodes": f"Palpable: {responses.get('axillary_palpable', '')}. Size: {responses.get('axillary_size', '')}. Consistency: {responses.get('axillary_consistency', '')}. Mobility: {responses.get('axillary_mobility', '')}. Tenderness: {responses.get('axillary_tenderness', '')}. Warmth: {responses.get('axillary_warmth', '')}. Unexpected findings: {responses.get('axillary_findings', 'None')}",
            "inguinal_nodes": f"Palpable: {responses.get('inguinal_palpable', '')}. Size: {responses.get('inguinal_size', '')}. Consistency: {responses.get('inguinal_consistency', '')}. Mobility: {responses.get('inguinal_mobility', '')}. Tenderness: {responses.get('inguinal_tenderness', '')}. Warmth/infection signs: {responses.get('inguinal_warmth', '')}. Unexpected findings: {responses.get('inguinal_findings', 'None')}",
            "epitrochlear_nodes": f"Palpable: {responses.get('epitrochlear_palpable', '')}. {responses.get('epitrochlear_characteristics', '')}",
            "abdominal_nodes": "To be assessed by clinician during abdominal examination",
            "mediastinal_nodes": "Not assessed on physical exam - would require imaging",
            "other_nodes": f"Other body locations: {responses.get('other_palpable', '')}",
            "generalized_lymphadenopathy": "To be determined - assess if nodes >1cm in multiple non-contiguous sites",
            "node_characteristics": f"Firmness: {responses.get('lump_characteristics', '')}. Changes: {responses.get('lump_changes', '')}. Erythema: {responses.get('node_erythema', '')}. Drainage: {responses.get('node_drainage', '')}. Vascularity: {responses.get('increased_vascularity', '')}"
        },
        "edema": {
            "peripheral_edema_upper_extremity": responses.get('arm_swelling', ''),
            "peripheral_edema_lower_extremity": responses.get('leg_swelling', ''),
            "facial_edema": responses.get('face_swelling', ''),
            "genital_edema": "Not reported",
            "lymphedema_staging": "To be determined by clinician",
            "skin_changes_from_edema": "To be assessed",
            "edema_pitting_response": responses.get('swelling_pitting', ''),
            "circumference_measurements": "To be measured by clinician"
        },
        "lymphatic_drainage": {
            "unilateral_drainage": "To be assessed",
            "drainage_obstruction_signs": "To be assessed",
            "venous_assessment": responses.get('venous_problems', ''),
            "lymphatic_vessel_visibility": "Not visible",
            "lymphatic_malfunction_indicators": f"Duration: {responses.get('swelling_timeline', '')}"
        },
        "systemic_symptoms": {
            "swelling_location": f"Aware of lumps: {responses.get('aware_of_lumps', '')}. Patient-reported swelling",
            "swelling_onset": responses.get('swelling_timeline', ''),
            "swelling_progression": responses.get('lump_changes', ''),
            "pain_heaviness": responses.get('heaviness', ''),
            "fatigue": responses.get('fatigue', ''),
            "fever_night_sweats": responses.get('fever_sweats', ''),
            "recurrent_infections": responses.get('infections', ''),
            "constitutional_symptoms": "To be assessed"
        },
        "medical_history": {
            "cancer_history": responses.get('cancer_history', ''),
            "cancer_ongoing": "To be verified",
            "surgery_history": responses.get('surgery_history', ''),
            "trauma_injury": responses.get('injury_history', ''),
            "infection_history": "To be assessed",
            "venous_insufficiency": responses.get('venous_problems', ''),
            "autoimmune_conditions": responses.get('autoimmune', ''),
            "radiation_therapy_history": "To be assessed",
            "congenital_abnormalities": "Not reported",
            "vascular_surgery": "To be assessed"
        },
        "current_medications": {
            "diuretics": responses.get('diuretics', ''),
            "anticoagulants": "To be assessed",
            "corticosteroids": responses.get('corticosteroids', ''),
            "immunosuppressants": "To be assessed",
            "anti_inflammatory": "To be assessed",
            "other_medications": responses.get('blood_pressure_meds', ''),
            "supplements_herbs": "Not addressed"
        },
        "lymphedema_risk_factors": {
            "cancer_related_risk": responses.get('cancer_treatment', ''),
            "BMI": responses.get('weight', ''),
            "infection_risk": responses.get('infections', ''),
            "venous_insufficiency_risk": responses.get('venous_problems', ''),
            "immobility": responses.get('activity_level', ''),
            "limb_use_demands": responses.get('occupation', ''),
            "psychosocial_factors": responses.get('emotional_impact', '')
        },
        "acute_lymphangitis": {
            "red_streaks_present": responses.get('red_streaks', ''),
            "painful_cords": responses.get('painful_cords', ''),
            "lymphatic_vessel_inflammation": responses.get('lymphatic_inflammation', ''),
            "associated_cellulitis": responses.get('cellulitis_signs', ''),
            "systemic_signs": responses.get('systemic_infection_signs', ''),
            "entry_wound": responses.get('entry_wound', ''),
            "symptom_duration": responses.get('lymphangitis_timeline', ''),
            "progression": responses.get('lymphangitis_progression', ''),
            "lymphangitis_diagnosis": "To be determined by clinician based on clinical findings"
        },
        "functional_impact": {
            "activities_of_daily_living": responses.get('work_impact', ''),
            "work_impact": responses.get('work_impact', ''),
            "social_impact": responses.get('emotional_impact', ''),
            "mental_health_impact": responses.get('emotional_impact', ''),
            "mobility_impact": responses.get('exercise_tolerance', ''),
            "exercise_tolerance": responses.get('exercise_tolerance', ''),
            "sleep_quality": responses.get('sleep_impact', '')
        },
        "assessment_summary": {
            "lymphatic_function_status": "To be determined by clinician",
            "lymph_node_findings": "To be assessed by clinician",
            "edema_status": f"Patient reported: {responses.get('arm_swelling', '')}, {responses.get('leg_swelling', '')}",
            "lymphedema_presence": "To be determined",
            "identified_complications": f"Infections: {responses.get('infections', '')}, Previous treatment: {responses.get('previous_treatment', '')}",
            "contributing_factors": f"Cancer: {responses.get('cancer_history', '')}, Surgery: {responses.get('node_removal', '')}, Activity: {responses.get('activity_level', '')}",
            "major_findings": "To be identified by clinician",
            "risk_stratification": "To be determined",
            "recommendations": "Clinical examination and assessment by lymphatic specialist",
            "specialist_referral": "Lymphedema specialist referral recommended for evaluation and management",
            "follow_up_plan": "Follow-up based on clinical assessment and severity of findings"
        }
    }

    # Create assessment object
    assessment = LymphaticSystemAssessment(**assessment_data)

    # Save to file if path provided
    if output_path is None:
        output_path = Path("outputs") / f"{patient_name.lower().replace(' ', '_')}_lymphatic_system.json"

    # Create outputs directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save assessment as JSON
    save_model_response(assessment, output_path)

    print(f"\n✓ Assessment saved to: {output_path}")

    return assessment


def evaluate_lymphatic_system(
    patient_name: str,
    output_path: Optional[Path] = None,
    use_schema_prompt: bool = True,
    prompt_style: PromptStyle = PromptStyle.DETAILED,
) -> LymphaticSystemAssessment:
    """
    Evaluate patient lymphatic system health through interactive questionnaire.

    Args:
        patient_name: Name or identifier of the patient
        output_path: Optional path to save JSON output. Defaults to outputs/{patient_name}_lymphatic_system.json
        use_schema_prompt: Whether to use PydanticPromptGenerator for schema
        prompt_style: Style of schema prompt (DETAILED, CONCISE, TECHNICAL)

    Returns:
        LymphaticSystemAssessment: Validated lymphatic system assessment object
    """
    if not patient_name or not patient_name.strip():
        raise ValueError("Patient name cannot be empty")

    # Ask patient questions interactively
    print(f"\nStarting lymphatic system assessment for: {patient_name}")
    responses = ask_lymphatic_questions()

    # Create assessment from responses
    assessment = create_lymphatic_assessment_from_responses(patient_name, responses, output_path)

    return assessment


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate patient lymphatic system health through structured assessment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default - saves to outputs/patient_lymphatic_system.json
  python exam_lymphatic_system.py "John Doe"

  # Custom output path
  python exam_lymphatic_system.py "John Doe" -o custom_assessment.json

  # With concise prompting
  python exam_lymphatic_system.py "John Doe" --concise

Lymphatic System Assessment Protocol:
  1. LYMPH NODE ASSESSMENT: Palpate nodes in neck, armpits, groin, elbows
     - Document size, location, consistency, mobility, tenderness
     - Assess for generalized vs localized lymphadenopathy

  2. EDEMA ASSESSMENT: Check for swelling in arms, legs, face
     - Determine if pitting or non-pitting
     - Measure circumferences for asymmetry
     - Assess skin changes (fibrosis, color changes)

  3. DRAINAGE ASSESSMENT: Evaluate lymphatic flow and obstruction
     - Check for asymmetry suggesting obstruction
     - Assess venous insufficiency
     - Look for collateral circulation

  4. SYSTEMIC ASSESSMENT: Evaluate for associated symptoms
     - Fever, night sweats, fatigue, weight loss
     - Recurrent infections in affected areas
     - Pain and functional limitations

  5. HISTORY: Cancer treatment, surgery, trauma affecting lymphatic system
     - Node removal, radiation, chemotherapy
     - Previous surgeries in affected areas
     - Current medications affecting function
        """
    )
    parser.add_argument("patient", nargs='+', help="Name or identifier of the patient")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Path to save JSON output. Defaults to outputs/{patient_name}_lymphatic_system.json"
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

        result = evaluate_lymphatic_system(
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
