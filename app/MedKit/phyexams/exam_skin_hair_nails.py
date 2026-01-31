"""
Skin, Hair, and Nails Examination Assessment

Comprehensive examination of skin, hair, and nails using structured
assessment of color, lesions, texture, and clinical findings using BaseModel
definitions and the MedKit AI client with schema-aware prompting.
"""

import sys
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional

from lite.utils import save_model_response

# Fix import path
from utils.pydantic_prompt_generator import PromptStyle


class GeneralSkinInspection(BaseModel):
    """Overall skin inspection and general characteristics."""
    skin_color_uniformity: str = Field(description="General uniformity of skin color - uniform/variations between sun-exposed and non-exposed areas/unexpected color changes. Describe distribution")
    sun_exposed_areas: str = Field(description="Observation of sun-exposed areas - darker/tan/sunburned/normal/photodamage evident. Comparison to non-exposed areas?")
    dark_skin_assessment: str = Field(description="If dark-skinned patient, assessment of color in sclerae/conjunctivae/buccal mucosa/tongue/lips/nail beds/palms - normal/pallor/jaundice/cyanosis/other")
    generalized_color_changes: str = Field(description="Any generalized color changes - none/jaundice/cyanosis/pallor/erythema/hyperpigmentation/hypopigmentation. Associated symptoms?")
    localized_discolorations: str = Field(description="Localized discolorations present - none/bruising/ecchymosis/petechiae/vitiligo patches/other. Location and pattern?")
    vascular_flush_areas: str = Field(description="Vascular flush areas or erythema noted - none/facial flush/chest flush/other locations. Pattern and cause?")
    body_area_inspection: str = Field(description="Inspection of all body areas including areas not usually exposed - scalp/axillae/inframammary/groin/feet/interdigital spaces. Any abnormal findings?")
    intertriginous_surfaces: str = Field(description="Assessment of intertriginous surfaces (skin folds) - clean/macerated/irritated/fungal changes/erythema/moisture. Areas affected?")
    overall_cleanliness: str = Field(description="Overall skin cleanliness and hygiene - clean/adequate/poor hygiene/visible dirt/debris. Appearance consistent with patient's stated hygiene?")
    visible_lesions_present: str = Field(description="Any visible lesions present - none/few/multiple. Types noted?")


class SkinColorAndPigmentation(BaseModel):
    """Assessment of skin color changes and pigmentation."""
    brown_discoloration: str = Field(description="Brown discoloration from melanin darkening - none/minimal/moderate/extensive. Areas: face/neck/hands/generalized? Freckles/age spots present?")
    white_discoloration: str = Field(description="White areas from absence of pigmentation (vitiligo) - none/small patches/large areas/generalized. Progressive? Family history?")
    red_coloration: str = Field(description="Red coloration from increased blood flow (erythema/flush) - none/limited/extensive. Blanching with pressure? Warm/hot to touch?")
    yellow_coloration: str = Field(description="Yellow coloration from bile or carotene - none/mild/moderate/severe. Associated with: jaundice/high carotene intake/other? Sclerae yellow?")
    blue_discoloration: str = Field(description="Blue discoloration from unsaturated hemoglobin (cyanosis) - none/central/peripheral/mixed. Lips/tongue/fingertips affected? Associated symptoms?")
    chloasma: str = Field(description="Chloasma (melasma) - symmetric facial hyperpigmentation - none/mild/moderate/extensive. Triggered by sun/pregnancy/medications?")
    pigmented_nevi: str = Field(description="Pigmented nevi (moles) present - none/few (<10)/multiple (10-15)/>15 (many). Location/appearance normal or concerning (see lesion assessment)?")
    freckles_present: str = Field(description="Freckles present - none/few/many. Distribution pattern? Related to sun exposure/genetics?")
    birthmarks_present: str = Field(description="Birthmarks or congenital lesions - none/present. Type (port-wine stain/hemangioma/other)? Size/location/color change over time?")


class SkinThicknessAndTexture(BaseModel):
    """Assessment of skin thickness and surface texture."""
    general_skin_thickness: str = Field(description="General skin thickness - normal/thin/thick/atrophic. Areas of variation noted?")
    eyelid_thickness: str = Field(description="Eyelid thickness (should be thinnest) - normal/thickened/thin/ptosis present. Edema evident?")
    calluses_on_hands_feet: str = Field(description="Calluses on hands/feet - none/minimal/moderate/extensive. Location suggests activity/occupation? Pain with pressure?")
    area_rubbing_thickening: str = Field(description="Areas of thickening from frequent rubbing/pressure - none noted/present. Location and cause?")
    corns_present: str = Field(description="Corns present (hard, thickened skin on toes) - none/one or few/multiple. Pain with pressure? Footwear-related?")
    atrophy_noted: str = Field(description="Skin atrophy (thin, paper-like appearance) - none/noted. Location? Associated with: aging/sun damage/steroid use/other?")
    hyperkeratosis: str = Field(description="Hyperkeratosis (thickened outer layer) - none/localized/generalized. Associated with: psoriasis/eczema/other conditions?")
    overall_texture: str = Field(description="Overall skin texture - smooth/soft/even/rough/sandpaper-like/scaly/velvety. Rough areas from cold/clothing/soap use?")
    symmetry: str = Field(description="Bilateral symmetry - symmetrical/asymmetrical. Describe asymmetry if present")


class SkinMoistureTemperatureTurgor(BaseModel):
    """Palpation assessment of skin moisture, temperature, turgor, and mobility."""
    moisture_level: str = Field(description="Skin moisture - dry/minimal perspiration (normal)/moist/damp/diaphoretic. Localized to certain areas (axillae/palms/forehead)? Excessive sweating?")
    moisture_distribution: str = Field(description="Distribution of moisture/sweat - uniform/localized to axillae/palms/scalp/forehead/intertriginous areas. Appropriate for activity level and temperature?")
    skin_temperature: str = Field(description="Skin temperature - cool/warm/hot/cold. Bilateral symmetry? Cold extremities? Warm to touch?")
    temperature_symmetry: str = Field(description="Temperature symmetry - symmetric/asymmetric. Any areas warmer or colder? Related to inflammation/circulation?")
    texture_palpation: str = Field(description="Texture on palpation - smooth/soft/rough/scaly/velvety. Extensive roughness or only from specific causes (clothing/cold)?")
    skin_turgor: str = Field(description="Skin turgor (elasticity) - good/normal/poor/tenting. Test: pinch skin gently on forearm, observe return speed. Returns immediately/returns slowly (dehydration)? Skin separation after pinch?")
    mobility: str = Field(description="Skin mobility and resilience - mobile/moveable/adhered/limited. Mobility reduced by: edema/inflammation/scarring/fibrosis/other?")
    edema_present: str = Field(description="Edema present - none/pitting/non-pitting. Location? Associated with: heart disease/kidney disease/liver disease/malnutrition/other?")


class SkinLesionAssessment(BaseModel):
    """Detailed assessment of any skin lesions if present."""
    lesion_presence: str = Field(description="Any skin lesions present - none/one/few/multiple. If present, continue detailed assessment")
    lesion_size: str = Field(description="Size of lesion(s) - measure in mm or cm using ruler. Single size or range if multiple")
    lesion_shape: str = Field(description="Shape of lesion(s) - round/oval/irregular/linear/geometric/other. Describe borders: sharp/ill-defined/raised/rolled")
    lesion_color: str = Field(description="Color of lesion(s) - tan/brown/black/red/pink/purple/yellow/white/flesh-colored/other. Uniform color or variegated? Use Wood's lamp if fluorescing suspected")
    lesion_blanching: str = Field(description="Blanching with pressure - blanches completely/partially blanches/does not blanch. Refill time when released?")
    lesion_texture: str = Field(description="Texture of lesion - smooth/rough/scaly/crusted/wet/dry/hairy. Uniform throughout or variable?")
    lesion_elevation_depression: str = Field(description="Elevation or depression - flat (macule/patch)/elevated (papule/plaque/nodule/tumor)/depressed/pedunculated")
    lesion_exudate: str = Field(description="Exudate present - none/present. If present: color (clear/yellow/green/purulent/bloody)/odor (none/foul)/amount (minimal/moderate/copious)/consistency (serous/purulent/serosanguineous)")
    lesion_configuration: str = Field(description="Configuration/arrangement - solitary/clustered/grouped/linear/arciform/annular (ring-shaped)/diffuse/confluent (merged). Pattern suggests: infection/contact dermatitis/other?")
    lesion_location: str = Field(description="Location(s) of lesion(s) - specific body region. Distribution: generalized/localized/unilateral/bilateral. Pattern: symmetric/asymmetric")
    lesion_secondary_changes: str = Field(description="Secondary changes - excoriation/erosion/fissuring/lichenification/scar/atrophy. Indicate self-trauma/chronicity?")


class PrimarySkinLesions(BaseModel):
    """Classification of primary skin lesion types if present."""
    macule: str = Field(description="Macule present (flat, circumscribed color change <1cm) - none/present. Examples: freckles, flat moles, petechiae, measles")
    papule: str = Field(description="Papule present (elevated, firm, <1cm) - none/present. Examples: warts, elevated moles, lichen planus")
    patch: str = Field(description="Patch present (flat, irregular macule >1cm) - none/present. Examples: vitiligo, port-wine stains")
    plaque: str = Field(description="Plaque present (elevated, firm, rough, >1cm with flat top) - none/present. Examples: psoriasis, seborrheic keratoses")
    wheal: str = Field(description="Wheal present (elevated, irregular, cutaneous edema, transient) - none/present. Examples: insect bites, urticaria")
    nodule: str = Field(description="Nodule present (elevated, firm, deeper in dermis, 1-2cm) - none/present. Examples: erythema nodosum, lipomas")
    tumor: str = Field(description="Tumor present (elevated, solid, >2cm, deeper in dermis) - none/present. Examples: neoplasms, hemangioma")
    vesicle: str = Field(description="Vesicle present (elevated, superficial, serous fluid, <1cm) - none/present. Examples: varicella, herpes zoster")
    bulla: str = Field(description="Bulla present (vesicle >1cm) - none/present. Examples: blister, pemphigus vulgaris")
    pustule: str = Field(description="Pustule present (elevated, superficial, purulent fluid) - none/present. Examples: impetigo, acne")
    cyst: str = Field(description="Cyst present (elevated, encapsulated, in dermis/subcutaneous, liquid/semisolid) - none/present. Examples: sebaceous cyst, cystic acne")
    telangiectasia: str = Field(description="Telangiectasia present (fine red lines from capillary dilation) - none/present. Examples: rosacea, spider angiomas")


class HairExamination(BaseModel):
    """Assessment of hair color, distribution, texture, and abnormalities."""
    scalp_hair_color: str = Field(description="Scalp hair color - light blond/blond/brown/black/red/gray/white/other. Uniform color or graying/salt-and-pepper pattern?")
    hair_color_abnormalities: str = Field(description="Unusual hair color alterations - none/premature graying/color change/discoloration. Associated with: genetics/nutritional deficiency/stress/medical condition?")
    hair_distribution_pattern: str = Field(description="Hair distribution pattern - normal for age/sex/ethnicity. Presence on: scalp/face/neck/ears/chest/axillae/back/shoulders/arms/legs/pubic area/areolae. Sparse/normal/dense?")
    scalp_hair_loss: str = Field(description="Scalp hair loss - none/minimal/moderate/significant. Pattern: androgenetic (vertex/crown)/female pattern (diffuse)/patchy/diffuse alopecia areata. Traumatic/telogen effluvium/other?")
    female_pattern_alopecia: str = Field(description="Female-pattern hair loss if applicable - none/present. Timing of onset? Progression? Stress/medications triggering?")
    male_pattern_baldness: str = Field(description="Male-pattern baldness if applicable - none/receding hairline/vertex loss/crown balding. Extent? Family history?")
    hirsutism_women: str = Field(description="Hirsutism in women (excessive hair in androgen-dependent areas) - none/present. Areas affected: face/chest/back/abdomen. Associated with: PCOS/endocrine disorder/medications/genetics?")
    hair_distribution_abnormality: str = Field(description="Localized or generalized abnormal hair distribution - none/present. Areas affected? Loss of hair from specific region(s)?")
    hair_inflammation_scarring: str = Field(description="Hair follicle inflammation or scarring alopecia - none/present. Areas? Associated with: folliculitis/lichen planus/lupus/burn scars?")
    broken_absent_hair_shafts: str = Field(description="Broken or absent hair shafts - none/present. Evidence of: trauma/alopecia areata/tinea capitis/hair pulling (trichotillomania)?")
    hair_texture: str = Field(description="Hair texture on palpation - coarse/fine/thin/thick/curly/straight. Expected variations for ethnicity?")
    hair_appearance: str = Field(description="Overall hair appearance - shiny/dull/smooth/rough/glossy/resilient. Texture: dry/brittle/oily. Shine suggests: good nutrition/good hair health?")
    hair_dryness_brittleness: str = Field(description="Dryness or brittleness - none/minimal/moderate/significant. Associated with: malnutrition/chemical damage/environmental/medications?")
    scalp_condition: str = Field(description="Scalp condition - clean/oily/dry/flaking/psoriasis/seborrheic dermatitis/folliculitis. Dandruff present?")


class NailExamination(BaseModel):
    """Comprehensive assessment of nail appearance and pathology."""
    nail_color_general: str = Field(description="General nail color - pink with varying opacity/normal/abnormal. Color variations expected in dark-skinned patients?")
    nail_color_abnormalities: str = Field(description="Abnormal nail colors - yellow (fungal/smoking/psoriasis)/green-black (bacterial/fungal)/white (kidney disease/liver disease)/blue (cyanosis). Which nails affected?")
    nail_pigment_deposits: str = Field(description="Pigment deposits in nails - none/present in dark-skinned individuals (normal)/present in light-skinned individuals (abnormal). Longitudinal streaks or bands? Splinter hemorrhages?")
    white_spots_nails: str = Field(description="White spots on nails - none/few/multiple. Transverse white bands or spots? Associated with: trauma/fungal infection/systemic disease?")
    diffuse_nail_darkening: str = Field(description="Diffuse darkening of nails - none/present. Associated with: pregnancy/endocrine disorder/medications/melanonychia?")
    longitudinal_streaks: str = Field(description="Longitudinal red, brown, or white streaks/bands - none/present. Distribution? Associated with: melanoma risk/normal variant?")
    nail_length_configuration: str = Field(description="Nail length and configuration - normal varying shape/jagged/broken/bitten. Shape: flat/slightly convex/clubbed? Length appropriate/neglected?")
    nail_edges: str = Field(description="Nail edges and cuticles - smooth/rounded/jagged/peeling/bitten. Cuticles: intact/ragged/missing. Appearance suggests: self-care/health status?")
    nail_cleanliness: str = Field(description="Nail cleanliness - clean/neat/dirty/unkempt. Debris under nails? Appearance consistent with reported hygiene?")
    nail_ridging: str = Field(description="Ridging patterns - none/longitudinal ridging (normal)/transverse grooving/rippling/depressions/pitting. Pattern suggests: lichen planus/psoriasis/Beau's lines/fungal?")
    nail_texture_palpation: str = Field(description="Nail texture on palpation - hard/soft/smooth/rough. Firmness: firm/boggy. Thickness: uniform/thickened/thinned")
    nail_plate_uniformity: str = Field(description="Nail plate uniformity - uniform thickness/variable/thickening/thinning. Consistent across all nails?")
    nail_bed_adherence: str = Field(description="Nail bed adherence - firmly attached/boggy/separation/onycholysis. Nail base angle: 160° (normal)/clubbing (>160°). Evidence of separation?")
    nail_base_angle: str = Field(description="Nail base angle measurement - place fingers dorsal surfaces together, observe angle. Normal: 160°/abnormal: >180° (clubbing indicates cardiopulmonary disease). Gradual vs acute change?")
    clubbing_present: str = Field(description="Clubbing present (increased base angle, loss of angle, spongy base) - none/mild/moderate/severe. Associated with: lung disease/heart disease/inflammatory bowel disease/malignancy?")
    nail_fold_assessment: str = Field(description="Proximal and lateral nail folds - normal/erythema/swelling/pus/redness/paronychia/warts/cysts/tumors/pain. Inflammation suggests: infection/trauma/psoriasis?")
    subungual_debris: str = Field(description="Material under nails - none/dirt/debris/blood/purulent material. Suggests: poor hygiene/fungal infection/trauma/infection?")


class MucousalMembranesAndOralAssessment(BaseModel):
    """Assessment of visible mucous membranes and oral cavity."""
    lips_color: str = Field(description="Lip color - pink/pale/cyanotic/erythematous/pigmented. Uniform or patchy color? Lips dry/moist/cracked?")
    lips_texture: str = Field(description="Lip texture - smooth/dry/chapped/cracked/ulcerated. Evidence of: herpes/angular cheilitis/nutritional deficiency?")
    buccal_mucosa_color: str = Field(description="Buccal mucosa (inside cheek) color - pink/pale/erythematous/pigmented. Even color or patchy? Normal pigment in dark-skinned patients?")
    tongue_color: str = Field(description="Tongue color - pink/pale/red/white/furry/pigmented. Uniform or patchy? Cobblestone appearance?")
    tongue_texture: str = Field(description="Tongue texture - smooth/rough/fissured/swollen/atrophic. Evidence of: glossitis/geographic tongue/thrush/scarring?")
    oral_hygiene: str = Field(description="Oral hygiene - good/adequate/poor. Plaque present/absent? Debris noted?")
    gum_appearance: str = Field(description="Gum appearance - pink/pale/erythematous/swollen/recessed. Bleeding with examination? Gingivitis/periodontitis evident?")
    teeth_condition: str = Field(description="Teeth condition - healthy/cavities/missing/stained/worn/loose. Dentures present? Fit properly?")
    oral_lesions: str = Field(description="Oral lesions - none/ulcers/thrush/patches/bleeding/herpetic lesions. Location? Size? Associated symptoms (pain/difficulty eating)?")
    palate_assessment: str = Field(description="Hard and soft palate - normal/petechiae/telangiectasia/lesions/high arched/cleft. Color normal or abnormal?")
    pharynx_assessment: str = Field(description="Pharynx appearance - pink/erythematous/exudate/swollen tonsils/petechiae. Evidence of: infection/strep/mononucleosis?")
    sclerae_icterus: str = Field(description="Sclerae (whites of eyes) assessment - white/yellow (icterus/jaundice)/reddened/injected. Uniform or patchy? Associated with: jaundice/hepatic disease?")


class DermatologicalDifferentialDiagnosis(BaseModel):
    """Assessment of specific dermatological conditions if identified."""
    eczematous_dermatitis: str = Field(description="Evidence of eczematous dermatitis - none/possible. Findings: itching/allergy history/acute (erythematous, weeping vesicles)/subacute (erythema, scaling)/chronic (thick, lichenified plaques). Areas: flexures/nape/dorsal limbs")
    folliculitis: str = Field(description="Evidence of folliculitis - none/possible. Findings: acute papules/pustules, 1-2cm over pilosebaceous orifices, pruritus/mild discomfort/pain (deep), crusting after rupture")
    tinea_dermatophytosis: str = Field(description="Evidence of tinea/dermatophytosis - none/possible. Findings: pruritus/papular/pustular/vesicular/erythematous/scaling lesions, possible secondary infection, KOH microscopy result?")
    basal_cell_carcinoma: str = Field(description="Evidence of basal cell carcinoma - none/possible/concern. Findings: persistent sore/lesion that doesn't heal, crusting, itching, shiny/pearly/translucent nodule (pink/red/white/tan/black/brown), rolled border, central indentation. Location? Duration?")
    squamous_cell_carcinoma: str = Field(description="Evidence of squamous cell carcinoma - none/possible/concern. Findings: persistent sore/lesion that doesn't heal or grows, crusting/bleeding, elevated growth with central depression, wart-like growth, scaly red patch with irregular borders, open sore. Location? Duration?")
    malignant_melanoma: str = Field(description="Evidence of malignant melanoma - none/possible/concern. Findings: new mole/changing mole, family history of melanoma, dysplastic nevi present. Features: asymmetry/irregular borders/color variation/diameter >6mm/evolution/itching/bleeding. Urgency for referral?")
    other_skin_conditions: str = Field(description="Other notable skin conditions identified - psoriasis/lichen planus/rosacea/urticaria/contact dermatitis/other. Description and concerns?")
    biopsies_recommended: str = Field(description="Skin biopsy recommended - none/yes for specific lesions. Which lesion(s)? Urgency? KOH/cultures recommended for fungal suspicion?")


class AssessmentSummary(BaseModel):
    """Overall assessment summary and clinical recommendations."""
    skin_health_status: str = Field(description="Overall skin health status - healthy/minor concerns/significant concerns/pathology present")
    skin_strengths: str = Field(description="Skin assessment strengths observed - good hygiene/normal color/good turgor/lesion-free/other")
    skin_concerns: str = Field(description="Identified skin concerns - color changes/lesions/poor turgor/poor hygiene/signs of disease/other")
    hair_health_status: str = Field(description="Overall hair health status - healthy/normal loss for age/concerning hair loss/abnormality present")
    hair_findings: str = Field(description="Hair assessment findings - normal color/distribution/texture/evidence of: alopecia/hirsutism/brittle hair/scalp condition/other")
    nail_health_status: str = Field(description="Overall nail health status - healthy/minor abnormalities/significant findings/disease indicators")
    nail_findings: str = Field(description="Nail assessment findings - normal color/shape/texture/evidence of: fungal infection/clubbing/beau's lines/psoriasis/systemic disease/other")
    suspected_diagnoses: str = Field(description="Suspected dermatological diagnoses if any - none/possible conditions identified (list)")
    concerning_lesions: str = Field(description="Any concerning lesions warranting further evaluation - none/yes. Description? Risk for: skin cancer/infection/other?")
    malignancy_risk: str = Field(description="Risk for skin malignancy - low/intermediate/high. Basis: history/appearance/location/change over time?")
    dermatology_referral_indicated: str = Field(description="Dermatology referral indicated - none/routine/urgent. Reason(s)?")
    biopsy_needed: str = Field(description="Skin biopsy indicated - none/recommended/urgent. Which lesion(s)? Suspicion for malignancy?")
    nutritional_indicators: str = Field(description="Nutritional indicators from skin/hair/nails assessment - well-nourished appearance/signs of protein deficiency/vitamin deficiency/mineral deficiency/poor nutritional status")
    systemic_disease_indicators: str = Field(description="Indicators of systemic disease from skin/hair/nails - none/possible signs of: jaundice/cyanosis/clubbing/specific deficiency state")
    recommendations: str = Field(description="Clinical recommendations - monitoring/local treatment/systemic treatment/lifestyle modifications/referrals/investigations needed")
    follow_up_plan: str = Field(description="Follow-up plan - routine monitoring/lesion tracking/biopsy/specialist referral/educational counseling/reassurance")


class SkinHairNailsAssessment(BaseModel):
    """
    Comprehensive Skin, Hair, and Nails Assessment.

    Organized as a collection of BaseModel sections representing distinct
    aspects of dermatological examination including inspection and palpation
    of skin, assessment of lesions, hair distribution and texture,
    nail characteristics, and mucousal membranes. Includes differential
    diagnosis for common skin conditions.
    """
    # General skin inspection
    general_skin_inspection: GeneralSkinInspection

    # Skin color and pigmentation
    skin_color_and_pigmentation: SkinColorAndPigmentation

    # Skin thickness and texture
    skin_thickness_and_texture: SkinThicknessAndTexture

    # Skin moisture, temperature, turgor
    skin_moisture_temperature_turgor: SkinMoistureTemperatureTurgor

    # Skin lesion assessment if present
    skin_lesion_assessment: SkinLesionAssessment

    # Primary skin lesion types
    primary_skin_lesions: PrimarySkinLesions

    # Hair examination
    hair_examination: HairExamination

    # Nail examination
    nail_examination: NailExamination

    # Mucous membranes and oral assessment
    mucousal_membranes_oral: MucousalMembranesAndOralAssessment

    # Differential diagnosis for skin conditions
    dermatological_differential_diagnosis: DermatologicalDifferentialDiagnosis

    # Final assessment summary
    assessment_summary: AssessmentSummary


def ask_dermatological_questions() -> dict:
    """
    Ask patient dermatological assessment questions interactively.
    """
    print("\n" + "="*60)
    print("SKIN, HAIR, AND NAILS ASSESSMENT")
    print("="*60)
    print()
    print("MEASURES: This assessment evaluates the health of skin, hair, and nails, and")
    print("  identifies potential dermatological conditions or systemic diseases.")
    print("  • Skin color, texture, moisture, and integrity")
    print("  • Presence of lesions, rashes, or abnormal markings")
    print("  • Hair distribution, texture, and quality")
    print("  • Nail color, shape, and abnormalities")
    print("  • Signs of infection, inflammation, or systemic disease")
    print()
    print("TOP 10 KEY ASSESSMENT QUESTIONS:")
    print("  1. How would you describe your skin color and texture?")
    print("  2. Do you have any skin lesions, rashes, or unusual markings?")
    print("  3. Have you noticed any recent changes in your skin?")
    print("  4. Do you have any areas of itching or discomfort?")
    print("  5. How would you describe your hair texture and distribution?")
    print("  6. Have you noticed any hair loss or thinning?")
    print("  7. How would you describe the condition of your nails?")
    print("  8. Have you noticed any nail discoloration or changes?")
    print("  9. Do you have any history of skin conditions or allergies?")
    print(" 10. What is your sun exposure history and protection habits?")
    print()
    print("="*60)
    print("DETAILED SKIN, HAIR, AND NAILS QUESTIONNAIRE")
    print("="*60)

    responses = {}

    # SKIN ASSESSMENT
    print("\n--- SKIN ASSESSMENT ---")
    responses['skin_color'] = input("How would you describe your skin color? (fair/medium/dark/olive/other): ").strip()
    responses['skin_texture'] = input("How is your skin texture? (smooth/dry/oily/mixed/rough): ").strip()
    responses['skin_lesions'] = input("Do you have any skin lesions, rashes, or unusual markings? (no/yes, describe): ").strip()
    responses['skin_itching'] = input("Do you experience itching, burning, or pain on your skin? (no/yes, where/severity): ").strip()
    responses['moles_spots'] = input("Do you have moles or age spots? (no/yes, how many): ").strip()

    # HAIR ASSESSMENT
    print("\n--- HAIR ASSESSMENT ---")
    responses['hair_color'] = input("What is your natural hair color? ").strip()
    responses['hair_texture'] = input("How is your hair texture? (straight/wavy/curly/coarse/fine): ").strip()
    responses['hair_thickness'] = input("How thick is your hair? (thin/normal/thick/very thick): ").strip()
    responses['hair_loss'] = input("Do you experience hair loss? (no/yes, how much/where): ").strip()
    responses['hair_growth'] = input("Has your hair growth changed recently? (no/yes, describe): ").strip()

    # NAILS ASSESSMENT
    print("\n--- NAILS ASSESSMENT ---")
    responses['nail_color'] = input("What color are your nails? (pink/white/pale/discolored/other): ").strip()
    responses['nail_texture'] = input("How are your nails? (smooth/ridged/brittle/thick/thin): ").strip()
    responses['nail_problems'] = input("Do you have nail problems? (no/yes, describe - splitting, peeling, discoloration): ").strip()
    responses['nail_shape'] = input("Are your nails normal shape or curved/clubbed?: ").strip()

    # INFECTIONS AND CONDITIONS
    print("\n--- INFECTIONS AND CONDITIONS ---")
    responses['fungal_infection'] = input("Do you have any fungal infections (athlete's foot, nail fungus)?: ").strip()
    responses['acne'] = input("Do you experience acne or breakouts?: ").strip()
    responses['skin_condition'] = input("Do you have any chronic skin conditions (eczema, psoriasis, etc.)?: ").strip()

    # SENSATIONS AND SYMPTOMS
    print("\n--- SENSATIONS AND SYMPTOMS ---")
    responses['pain_sensitivity'] = input("Is your skin sensitive to pain or touch?: ").strip()
    responses['temperature_sensitivity'] = input("Are you sensitive to temperature changes?: ").strip()

    return responses


def create_skin_hair_nails_assessment_from_responses(patient_name: str, responses: dict, output_path: Optional[Path] = None) -> SkinHairNailsAssessment:
    """
    Create a structured dermatological assessment object from collected patient responses.
    """
    assessment_data = {
        "general_skin_inspection": {
            "skin_color_uniformity": responses.get('skin_color', 'Not assessed'),
            "sun_exposed_areas": "To be assessed by clinician",
            "dark_skin_assessment": "Not applicable",
            "generalized_color_changes": "None reported",
            "localized_discolorations": "None reported",
            "vascular_flush_areas": "None reported",
            "body_area_inspection": "To be assessed",
            "intertriginous_surfaces": "To be assessed",
            "overall_cleanliness": "To be assessed",
            "visible_lesions_present": responses.get('skin_lesions', 'None reported')
        },
        "skin_color_and_pigmentation": {
            "brown_discoloration": "To be assessed",
            "white_discoloration": "None noted",
            "red_coloration": "None noted",
            "yellow_coloration": "None noted",
            "blue_discoloration": "None noted",
            "chloasma": "None noted",
            "pigmented_nevi": responses.get('moles_spots', 'None reported'),
            "freckles_present": "To be assessed",
            "birthmarks_present": "None reported"
        },
        "skin_thickness_and_texture": {
            "general_skin_thickness": responses.get('skin_texture', 'To be assessed'),
            "eyelid_thickness": "Normal",
            "calluses_on_hands_feet": "To be assessed",
            "area_rubbing_thickening": "None noted",
            "corns_present": "None noted",
            "atrophy_noted": "None noted",
            "hyperkeratosis": "None noted",
            "overall_texture": responses.get('skin_texture', 'To be assessed'),
            "symmetry": "To be assessed"
        },
        "skin_moisture_temperature_turgor": {
            "moisture_level": "To be assessed by clinician",
            "moisture_distribution": "To be assessed",
            "skin_temperature": "To be assessed",
            "temperature_symmetry": "To be assessed",
            "texture_palpation": responses.get('skin_texture', 'To be assessed'),
            "skin_turgor": "To be assessed",
            "mobility": "To be assessed",
            "edema_present": "None reported"
        },
        "skin_lesion_assessment": {
            "lesion_presence": responses.get('skin_lesions', 'None reported'),
            "lesion_size": "To be measured",
            "lesion_shape": "To be assessed",
            "lesion_color": "To be assessed",
            "lesion_blanching": "To be assessed",
            "lesion_texture": "To be assessed",
            "lesion_elevation_depression": "To be assessed",
            "lesion_exudate": "None noted",
            "lesion_configuration": "To be assessed",
            "lesion_location": "To be assessed",
            "lesion_secondary_changes": "None noted"
        },
        "primary_skin_lesions": {
            "macule": "None present",
            "papule": "None present",
            "patch": "None present",
            "plaque": "None present",
            "wheal": "None present",
            "nodule": "None present",
            "tumor": "None present",
            "vesicle": "None present",
            "bulla": "None present",
            "pustule": "None present",
            "cyst": "None present",
            "telangiectasia": "None present"
        },
        "hair_examination": {
            "scalp_hair_color": responses.get('hair_color', 'Not specified'),
            "hair_color_abnormalities": "None reported",
            "hair_distribution_pattern": "To be assessed",
            "scalp_hair_loss": responses.get('hair_loss', 'None reported'),
            "female_pattern_alopecia": "To be assessed",
            "male_pattern_baldness": "To be assessed",
            "hirsutism_women": "To be assessed",
            "hair_distribution_abnormality": "None noted",
            "hair_inflammation_scarring": "None noted",
            "broken_absent_hair_shafts": "None noted",
            "hair_texture": responses.get('hair_texture', 'To be assessed'),
            "hair_appearance": "To be assessed",
            "hair_dryness_brittleness": "To be assessed",
            "scalp_condition": "To be assessed"
        },
        "nail_examination": {
            "nail_color_general": responses.get('nail_color', 'Normal'),
            "nail_color_abnormalities": responses.get('nail_problems', 'None noted'),
            "nail_pigment_deposits": "None noted",
            "white_spots_nails": "None noted",
            "diffuse_nail_darkening": "None noted",
            "longitudinal_streaks": "None noted",
            "nail_length_configuration": responses.get('nail_shape', 'Normal'),
            "nail_edges": "To be assessed",
            "nail_cleanliness": "To be assessed",
            "nail_ridging": "None noted",
            "nail_texture_palpation": responses.get('nail_texture', 'To be assessed'),
            "nail_plate_uniformity": "To be assessed",
            "nail_bed_adherence": "Normal",
            "nail_base_angle": "Normal (160°)",
            "clubbing_present": "None noted",
            "nail_fold_assessment": "Normal",
            "subungual_debris": "None noted"
        },
        "mucousal_membranes_oral": {
            "lips_color": "To be assessed",
            "lips_texture": "To be assessed",
            "buccal_mucosa_color": "To be assessed",
            "tongue_color": "To be assessed",
            "tongue_texture": "To be assessed",
            "oral_hygiene": "To be assessed",
            "gum_appearance": "To be assessed",
            "teeth_condition": "To be assessed",
            "oral_lesions": "None noted",
            "palate_assessment": "Normal",
            "pharynx_assessment": "To be assessed",
            "sclerae_icterus": "Not icteric"
        },
        "dermatological_differential_diagnosis": {
            "eczematous_dermatitis": "Not indicated",
            "folliculitis": "Not indicated",
            "tinea_dermatophytosis": responses.get('fungal_infection', 'Not reported'),
            "basal_cell_carcinoma": "Not suspected",
            "squamous_cell_carcinoma": "Not suspected",
            "malignant_melanoma": "Not suspected",
            "other_skin_conditions": responses.get('skin_condition', 'None reported'),
            "biopsies_recommended": "None at this time"
        },
        "assessment_summary": {
            "skin_health_status": "To be determined by clinician",
            "skin_strengths": "Patient reports no acute concerns",
            "skin_concerns": responses.get('skin_itching', 'None reported'),
            "hair_health_status": "To be assessed",
            "hair_findings": responses.get('hair_growth', 'Stable'),
            "nail_health_status": "To be assessed",
            "nail_findings": responses.get('nail_problems', 'No problems reported'),
            "suspected_diagnoses": "None at present",
            "concerning_lesions": "None identified",
            "malignancy_risk": "Low",
            "dermatology_referral_indicated": "None at this time",
            "biopsy_needed": "None indicated",
            "nutritional_indicators": "To be assessed",
            "systemic_disease_indicators": "None apparent",
            "recommendations": "Routine follow-up skin checks; patient education on sun protection",
            "follow_up_plan": "Routine monitoring at next visit"
        }
    }

    assessment = SkinHairNailsAssessment(**assessment_data)

    if output_path is None:
        output_path = Path("outputs") / f"{patient_name.lower().replace(' ', '_')}_skin_hair_nails.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    save_model_response(assessment, output_path)

    print(f"\n✓ Assessment saved to: {output_path}")

    return assessment


def evaluate_skin_hair_nails(
    patient_name: str,
    output_path: Optional[Path] = None,
    use_schema_prompt: bool = True,
    prompt_style: PromptStyle = PromptStyle.DETAILED,
) -> SkinHairNailsAssessment:
    """
    Evaluate patient skin, hair, and nails through interactive questionnaire.
    """
    if not patient_name or not patient_name.strip():
        raise ValueError("Patient name cannot be empty")

    print(f"\nStarting skin, hair, and nails assessment for: {patient_name}")
    responses = ask_dermatological_questions()

    assessment = create_skin_hair_nails_assessment_from_responses(patient_name, responses, output_path)

    return assessment


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Comprehensive skin, hair, and nails examination assessment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("patient", nargs='+', help="Name or identifier of the patient")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Path to save JSON output. Defaults to outputs/{patient_name}_skin_hair_nails.json"
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

        result = evaluate_skin_hair_nails(
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
