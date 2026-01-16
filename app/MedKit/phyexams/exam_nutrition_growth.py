"""
Nutrition and Growth Measurements Assessment

Doctor-Nurse Consultation Model: The doctor directs the nurse to perform
examination and ask questions about patient's nutrition and growth.
The nurse collects observations and reports findings using BaseModel
definitions and the MedKit AI client with schema-aware prompting.
"""

import sys
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional

# Fix import paths
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.pydantic_prompt_generator import PromptStyle
from core.medkit_client import MedKitClient
from core.module_config import get_module_config


class TwentyFourHourDietRecall(BaseModel):
    """24-hour diet recall documentation."""
    breakfast: str = Field(description="Breakfast foods and approximate portions consumed")
    morning_snack: str = Field(description="Morning snacks if any")
    lunch: str = Field(description="Lunch foods and approximate portions")
    afternoon_snack: str = Field(description="Afternoon snacks if any")
    dinner: str = Field(description="Dinner foods and approximate portions")
    evening_snack: str = Field(description="Evening snacks if any")
    beverages: str = Field(description="Beverages consumed throughout the day")
    supplements: str = Field(description="Vitamins, minerals, or supplements taken")


class DietaryRecommendations(BaseModel):
    """Recommended dietary changes based on assessment."""
    caloric_goal: str = Field(description="Recommended daily caloric intake")
    protein_recommendation: str = Field(description="Protein intake recommendation")
    carbohydrate_recommendation: str = Field(description="Carbohydrate intake recommendation")
    fat_recommendation: str = Field(description="Fat intake recommendation")
    fiber_recommendation: str = Field(description="Fiber intake recommendation")
    supplementation: str = Field(description="Recommended supplements if any")
    dietary_modifications: str = Field(description="Specific dietary modifications")
    meal_planning_suggestions: str = Field(description="Suggestions for meal planning")


class AnthropometricMeasurements(BaseModel):
    """Physical measurements taken by the nurse."""
    height_cm: str = Field(description="Patient height in centimeters - measured value and method (standing/lying)")
    weight_kg: str = Field(description="Patient weight in kilograms - measured value and any clothing/shoes noted")
    head_circumference_cm: str = Field(description="Head circumference in centimeters if applicable (pediatric patient) - measured at widest point")
    chest_circumference_cm: str = Field(description="Chest circumference in centimeters if applicable - measured at nipple line")
    mid_upper_arm_circumference_cm: str = Field(description="Mid-upper arm circumference (MUAC) in centimeters - measured at midpoint between shoulder and elbow, non-dominant arm. Critical screening for malnutrition")
    triceps_skinfold_thickness_mm: str = Field(description="Triceps skinfold thickness in millimeters - measured at back of arm midway between shoulder and elbow using skinfold calipers. Pinch skin vertically at midline of triceps, measure thickness. Assess subcutaneous fat stores")
    biceps_skinfold_thickness_mm: str = Field(description="Biceps skinfold thickness in millimeters - measured at front of arm midway between shoulder and elbow. Optional but provides bilateral assessment")
    subscapular_skinfold_thickness_mm: str = Field(description="Subscapular skinfold thickness in millimeters - measured just below scapula at 45° angle to vertical. Assesses central fat distribution")
    waist_circumference_cm: str = Field(description="Waist circumference in centimeters - measured at narrowest point")
    hip_circumference_cm: str = Field(description="Hip circumference in centimeters - measured at widest gluteal point")
    measurement_reliability: str = Field(description="Reliability of measurements - accurate and cooperative/cooperative/some difficulty/uncooperative/unable to measure. Skinfold calipers available/used?")


class GrowthIndicators(BaseModel):
    """Growth status assessment by nurse observation."""
    bmi_calculation: str = Field(description="BMI calculation (weight kg / height m²) and category - underweight/normal/overweight/obese")
    height_for_age: str = Field(description="Height assessment for age - within normal range/above average/below average/short stature. Percentile if available")
    weight_for_height: str = Field(description="Weight for height assessment - appropriate/overweight/underweight. Percentile if available")
    weight_for_age: str = Field(description="Weight for age assessment - appropriate/above average/below average. Percentile if available")
    muac_interpretation: str = Field(description="Mid-upper arm circumference (MUAC) interpretation - normal/mild acute malnutrition (MAM 11.5-12.5cm)/moderate acute malnutrition (12.5-13.5cm)/severe acute malnutrition (<11.5cm)/well-nourished (>13.5cm for adults). Age and gender specific cutoffs if pediatric")
    muac_nutritional_status: str = Field(description="MUAC-based nutritional status - well-nourished/at-risk/malnourished/severely malnourished. Quick screening tool particularly useful in resource-limited settings")
    triceps_skinfold_interpretation: str = Field(description="Triceps skinfold thickness interpretation - normal/below average/above average/high. Compare to age/sex percentiles. Values: adult males typically 10-20mm, females 15-25mm. Low values suggest fat depletion, high values suggest excess fat")
    subscapular_skinfold_interpretation: str = Field(description="Subscapular skinfold interpretation - normal/below average/above average/high. Central fat distribution indicator. Elevated suggests increased cardiovascular risk and central obesity")
    body_composition_assessment: str = Field(description="Overall body composition from skinfold measurements - normal fat distribution/lean/obese/sarcopenic (low muscle)/central obesity pattern/wasted appearance")
    subcutaneous_fat_stores: str = Field(description="Assessment of subcutaneous fat stores - adequate/borderline/depleted/excessive. Based on triceps and subscapular skinfolds combined")
    waist_hip_ratio: str = Field(description="Waist-to-hip ratio calculation (waist cm / hip cm) - value and interpretation. Healthy <0.85 (women)/0.95 (men), increased cardiovascular risk if higher. Central obesity if elevated?")
    waist_circumference_category: str = Field(description="Waist circumference health category - normal/increased (CVD risk)/substantially increased (high CVD risk). Based on age and gender guidelines")
    growth_trend: str = Field(description="Growth trend if previous measurements available - steady growth/accelerating/plateauing/declining")
    growth_velocity: str = Field(description="Growth velocity if longitudinal data - normal/slow/rapid/not assessable")
    head_circumference_for_age: str = Field(description="Head circumference percentile for age if pediatric - normal/above normal/below normal/microcephaly/macrocephaly")
    proportionality: str = Field(description="Body proportionality assessment - proportional/disproportionate (describe specific disproportion). Central obesity pattern noted?")


class NutritionStatusAssessment(BaseModel):
    """Nurse's assessment of patient's nutritional status."""
    general_appearance: str = Field(description="General appearance indicating nutrition - well-nourished/adequately nourished/malnourished/overweight appearance")
    muscle_mass_assessment: str = Field(description="Muscle mass assessment - well-developed/normal/decreased/severely wasted/atrophic")
    subcutaneous_fat: str = Field(description="Subcutaneous fat assessment - adequate/normal/minimal/absent. Areas assessed (triceps, subscapular)")
    skin_turgor: str = Field(description="Skin turgor and elasticity - normal/decreased (dehydration)/loose (weight loss)/edematous")
    hair_quality: str = Field(description="Hair quality - lustrous and strong/normal/dull/sparse/brittle/hair loss")
    nail_quality: str = Field(description="Nail quality and appearance - normal/pale/brittle/spoon-shaped/clubbing/terry nails")
    eyes_brightness: str = Field(description="Eyes and vision signs - bright/clear/dry/xerosis/corneal involvement")
    oral_assessment: str = Field(description="Oral cavity assessment - healthy/pale mucosa/bleeding gums/angular cheilitis/glossitis/oral thrush")
    energy_level: str = Field(description="Patient energy level and activity - active/normal/fatigued/lethargic/appears weak")
    overall_nutrition_status: str = Field(description="Overall nutritional status rating - well-nourished/adequately nourished/at-risk/malnourished/severely malnourished")


class MacronutrientIntakeEstimation(BaseModel):
    """Nurse asks specific questions to estimate macronutrient and fiber intake."""
    protein_sources_questions: str = Field(description="Nurse asks: What protein sources do you eat? (meat/poultry/fish/eggs/beans/dairy/nuts/tofu/other). How often? How much per serving (palm-sized/fist-sized portion)?")
    protein_sources_identified: str = Field(description="Protein sources identified from patient responses - beef/chicken/fish/eggs/beans/legumes/dairy/nuts/seeds/plant-based/none/irregular")
    daily_protein_servings: str = Field(description="Estimated daily protein servings from 24-hour recall and questions - (3 oz/serving = 1 serving). Estimated ___servings/day")
    protein_quantity_estimation: str = Field(description="Patient's typical protein quantity per meal/day - small portions/adequate portions/large portions/variable/insufficient")

    carbohydrate_sources_questions: str = Field(description="Nurse asks: What grains/starches do you eat? (bread/rice/pasta/cereals/potatoes/tortillas). How often? Whole grain or refined? Portion size?")
    carbohydrate_sources_identified: str = Field(description="Carbohydrate sources identified - whole wheat/white bread/brown rice/white rice/whole grain pasta/refined pasta/potatoes/sweet potatoes/cereals/oats/beans/legumes/other")
    whole_grain_frequency: str = Field(description="Frequency of whole grain consumption - daily/most days/occasionally/rarely/never. Percentage of carbs from whole grains?")
    refined_carb_frequency: str = Field(description="Frequency of refined carbohydrate consumption - rarely/occasionally/frequently/daily. Types (white bread, regular pasta, sugary cereals)?")
    daily_carb_servings: str = Field(description="Estimated daily carbohydrate servings - (1 serving = 1 slice bread/1/2 cup rice/1 cup cereal). Estimated ___servings/day")
    carbohydrate_quantity_assessment: str = Field(description="Overall carbohydrate intake assessment - adequate/excessive/insufficient. Portion control observed?")

    fat_sources_questions: str = Field(description="Nurse asks: What fats/oils do you use? (butter/oil/margarine/cream/fatty meats). How often? How much (teaspoon/tablespoon)? What types of cooking?")
    fat_sources_identified: str = Field(description="Fat sources identified - butter/olive oil/vegetable oil/coconut oil/fried foods/fatty meats/full-fat dairy/nuts/seeds/processed foods/low-fat/none added")
    saturated_fat_intake: str = Field(description="Saturated fat sources and frequency - butter/red meat/full-fat dairy/fried foods/processed foods. How often? Estimated daily intake")
    unsaturated_fat_intake: str = Field(description="Unsaturated fat sources - olive oil/nuts/seeds/avocado/fish/other. Frequency and quantity")
    cooking_methods: str = Field(description="Cooking methods used - frying/sautéing/baking/grilling/steaming/boiling. Frequency of high-fat cooking methods?")
    daily_fat_servings: str = Field(description="Estimated daily fat servings - (1 serving = 1 tsp oil/1 tbsp nuts). Estimated ___servings/day")
    fat_quantity_assessment: str = Field(description="Overall fat intake assessment - appropriate/excessive/insufficient. Type of fats consumed (saturated/unsaturated/trans)?")

    fiber_sources_questions: str = Field(description="Nurse asks: Do you eat vegetables? How many servings daily? Whole grains? How often? Fruits? Beans/legumes? Estimated portions?")
    vegetable_intake: str = Field(description="Vegetable intake frequency and type - daily/most days/occasionally/rarely. Servings per day? Raw/cooked? Types (green/orange/legumes)?")
    fruit_intake: str = Field(description="Fruit intake frequency - daily/most days/occasionally/rarely. Servings per day? Fresh/canned/juice? Types?")
    whole_grain_intake_detail: str = Field(description="Whole grain intake - servings per day of whole wheat bread/brown rice/oats/whole grain cereals/other")
    legume_bean_intake: str = Field(description="Beans and legumes intake - frequency and amount. How often per week? Types (black beans/lentils/chickpeas/kidney beans)?")
    estimated_daily_fiber: str = Field(description="Estimated daily fiber intake from 24-hour recall and questions - (vegetables 2-3g/serving, fruits 3-4g, whole grains 3-4g, beans 6-8g). Total estimated ___g/day")
    fiber_quantity_assessment: str = Field(description="Overall fiber intake assessment - adequate (25-30g/day)/insufficient/excessive")

    sugary_food_questions: str = Field(description="Nurse asks: Do you eat sugary foods/sweets? How often? What types? Portion sizes? Sugary drinks? How many per day?")
    added_sugar_sources: str = Field(description="Added sugar sources identified - soda/juice/sweet tea/coffee drinks/desserts/candy/cookies/processed foods/added sugar to foods. Frequency?")
    estimated_added_sugar: str = Field(description="Estimated daily added sugar intake - sources and quantities identified. Approximate ___teaspoons/day of added sugar")

    fluid_intake_questions: str = Field(description="Nurse asks: How much water do you drink daily? Other beverages? (coffee/tea/soda/juice/sports drinks/milk/alcohol). How many cups/glasses per day?")
    water_intake_daily: str = Field(description="Daily water intake - cups/glasses per day. Patient perception of hydration adequate/poor?")
    other_beverages_detailed: str = Field(description="Other beverages consumed - coffee (cups, sugar added)/tea/soda (regular/diet)/juice/sports drinks/energy drinks/alcoholic beverages. Frequency and quantity")

    estimation_confidence: str = Field(description="Nurse assessment of estimation confidence - accurate/mostly accurate/approximate/patient unsure/difficult to quantify")


class DietaryIntakeAssessment(BaseModel):
    """Nurse's assessment of dietary intake and eating patterns."""
    # 24-hour detailed recall
    twenty_four_hour_recall: TwentyFourHourDietRecall

    # Specific questioning about macronutrient and fiber intake
    macronutrient_intake_estimation: MacronutrientIntakeEstimation

    typical_daily_meals: str = Field(description="Typical number of meals per day (usual pattern) - three meals/breakfast and dinner/two meals/one meal/irregular")
    meal_regularity: str = Field(description="Meal regularity and timing - regular schedule/somewhat regular/irregular/skips meals frequently")
    breakfast_consumption: str = Field(description="Breakfast pattern (usual) - eats daily/most days/occasionally/rarely/never")
    protein_intake: str = Field(description="Protein intake assessment (overall pattern) - adequate/reduced/minimal/dependent on type (animal/plant/mixed)")
    carbohydrate_intake: str = Field(description="Carbohydrate intake (overall) - adequate/excessive/refined vs whole grains/consistent/irregular")
    fat_intake: str = Field(description="Fat intake assessment (overall) - appropriate/excessive/minimal/type (saturated/unsaturated/trans)")
    fruit_vegetable_intake: str = Field(description="Fruit and vegetable consumption (usual) - daily consumption/adequate portions/minimal/rarely consumed")
    dairy_consumption: str = Field(description="Dairy product intake (usual) - adequate daily/occasional/minimal/none/lactose intolerance")
    sugary_drink_intake: str = Field(description="Sugary beverage consumption (usual) - none/occasional/frequent/excessive. Types consumed")
    fast_food_frequency: str = Field(description="Fast food or processed food consumption (usual) - rarely/occasionally/frequently/daily/dependent on availability")
    hydration: str = Field(description="Water/fluid intake (usual) - adequate (8+ glasses)/good (6-8 glasses)/fair (4-6 glasses)/poor (<4 glasses)/thirst issues")
    appetite: str = Field(description="Patient's appetite - good/normal/decreased/poor/absent/variable")
    feeding_difficulties: str = Field(description="Any feeding difficulties - no difficulty/chewing difficulty/swallowing difficulty/food aversions/picky eater")
    allergies_intolerances: str = Field(description="Food allergies or intolerances identified - none/peanuts/shellfish/dairy/gluten/other (comma-separated)")


class SocioeconomicNutritionFactors(BaseModel):
    """Socioeconomic factors affecting nutrition - nurse observation and report."""
    food_security: str = Field(description="Food security status - food secure/borderline/food insecure/very low food security")
    access_to_food: str = Field(description="Access to adequate food - easily accessible/somewhat accessible/limited access/significant barriers")
    ability_to_afford_nutritious_food: str = Field(description="Financial ability to purchase nutritious food - can afford adequate/struggles/cannot afford")
    food_preparation_facilities: str = Field(description="Access to facilities for food preparation - has full kitchen/limited kitchen/no cooking facilities")
    refrigeration_access: str = Field(description="Access to food storage/refrigeration - has refrigerator/unreliable/no refrigeration/food spoilage concern")
    community_resources: str = Field(description="Access to community nutrition resources - WIC/SNAP/food banks/school meals/none/multiple resources")
    living_situation_impact: str = Field(description="Living situation impact on nutrition - stable/unstable/homelessness/institutional/affects food access")
    cultural_dietary_practices: str = Field(description="Cultural or religious dietary practices affecting nutrition - yes (describe)/no. Provides adequate nutrition?")
    education_barriers: str = Field(description="Education or literacy barriers affecting nutrition - none/yes affects food choices/affects meal planning")


class GrowthMilestones(BaseModel):
    """For pediatric patients - developmental and growth milestone assessment."""
    age_months: str = Field(description="Patient age in months (if pediatric) or age in years")
    developmental_stage: str = Field(description="Developmental stage assessment - on track/advanced/delayed. Specifics?")
    motor_development: str = Field(description="Motor development milestones - sitting/standing/walking/coordinated movements/age-appropriate")
    feeding_milestone: str = Field(description="Feeding milestone - breast/bottle fed/solid foods started/self-feeding/eating adult foods/appropriate for age")
    tooth_eruption: str = Field(description="Tooth eruption status - no teeth/partial eruption/full primary dentition/mixed dentition/permanent teeth. Age-appropriate?")
    language_development: str = Field(description="Language development - babbling/words/phrases/sentences/age-appropriate")
    immunization_status: str = Field(description="Immunization status - up-to-date/partially up-to-date/delayed/not documented")


class BiochemicalMeasurements(BaseModel):
    """Biochemical and laboratory measurements for nutritional assessment."""
    hemoglobin_level: str = Field(description="Hemoglobin level (g/dL) - measured value and date. Normal: males 13.5-17.5 g/dL, females 12.0-15.5 g/dL. Low suggests anemia, iron deficiency")
    hematocrit_level: str = Field(description="Hematocrit (%) - measured value and date. Normal: males 41-50%, females 36-44%. Low indicates anemia")
    red_blood_cell_count: str = Field(description="Red blood cell count (millions/μL) - measured value. Normal: males 4.5-5.9, females 4.1-5.1. Assess for anemia")
    mean_corpuscular_volume_mcv: str = Field(description="Mean corpuscular volume (MCV) in fL - measured value. Normal: 80-100 fL. Microcytic (<80) suggests iron deficiency, macrocytic (>100) suggests B12/folate deficiency")

    serum_albumin: str = Field(description="Serum albumin (g/dL) - measured value and date. Normal: 3.5-5.0 g/dL. Low (<3.0) indicates protein malnutrition or liver disease. Sensitive marker of protein status")
    serum_prealbumin: str = Field(description="Serum prealbumin (transthyretin) (mg/dL) - measured value if available. Normal: 20-40 mg/dL. More sensitive than albumin for detecting protein malnutrition. Shorter half-life (2-3 days)")
    total_protein: str = Field(description="Total serum protein (g/dL) - measured value. Normal: 6.0-8.3 g/dL. Reflects nutritional protein status")

    blood_glucose: str = Field(description="Blood glucose (fasting if possible) (mg/dL or mmol/L) - measured value and date. Fasting normal: 70-100 mg/dL. Random normal: <140 mg/dL. Screen for diabetes")
    hemoglobin_a1c: str = Field(description="Hemoglobin A1C (%) - if available. Normal: <5.7%. 5.7-6.4% prediabetic range, >6.5% diabetes. 3-month glucose average")

    serum_iron: str = Field(description="Serum iron (μg/dL) - measured value. Normal: males 60-170, females 50-170. Low suggests iron deficiency")
    ferritin: str = Field(description="Ferritin (ng/mL or mcg/L) - measured value. Normal: males 30-400, females 15-200. Low suggests iron depletion, high suggests iron overload or inflammation")
    transferrin_saturation: str = Field(description="Transferrin saturation (%) - measured value. Normal: 20-50%. Low suggests iron deficiency")

    vitamin_b12: str = Field(description="Vitamin B12 (serum cobalamin) (pg/mL or pmol/L) - measured value. Normal: 200-900 pg/mL. Low suggests B12 deficiency, vegetarian/vegan risk")
    folate_level: str = Field(description="Serum folate (ng/mL or nmol/L) - measured value. Normal: >5.4 ng/mL. Low suggests folate deficiency, risk factors: poor diet, alcohol use")

    vitamin_d_25_oh: str = Field(description="Vitamin D (25-OH) level (ng/mL or nmol/L) - measured value. Normal: >30 ng/mL. 20-29 insufficient, <20 deficient. Risk: limited sun exposure, low dairy")

    total_cholesterol: str = Field(description="Total cholesterol (mg/dL or mmol/L) - measured value. Desirable: <200 mg/dL. Associated with nutritional status and cardiovascular risk")
    hdl_cholesterol: str = Field(description="HDL cholesterol (mg/dL) - measured value. Desirable: >40 mg/dL (males), >50 mg/dL (females). Protective cholesterol")
    ldl_cholesterol: str = Field(description="LDL cholesterol (mg/dL) - measured value. Desirable: <100 mg/dL. Higher risk with poor nutrition")
    triglycerides: str = Field(description="Triglycerides (mg/dL) - measured value. Normal: <150 mg/dL. Elevated with excess carbs/sugar, obesity")

    blood_urea_nitrogen_bun: str = Field(description="Blood urea nitrogen (BUN) (mg/dL) - measured value. Normal: 7-20 mg/dL. High with dehydration or high protein intake, low with malnutrition")
    serum_creatinine: str = Field(description="Serum creatinine (mg/dL) - measured value. Normal: 0.7-1.3 mg/dL. Assess kidney function and protein metabolism")
    bun_creatinine_ratio: str = Field(description="BUN to creatinine ratio - calculated. Normal: 10:1 to 20:1. Higher ratio suggests dehydration")

    electrolytes_sodium: str = Field(description="Serum sodium (Na+) (mEq/L) - measured value. Normal: 136-145 mEq/L. Low (hyponatremia) or high (hypernatremia) affects nutrition status")
    electrolytes_potassium: str = Field(description="Serum potassium (K+) (mEq/L) - measured value. Normal: 3.5-5.0 mEq/L. Critical for muscle/heart function. Affected by malnutrition")
    electrolytes_calcium: str = Field(description="Serum calcium (mg/dL) - measured value. Normal: 8.5-10.2 mg/dL. Low suggests calcium/vitamin D deficiency")
    electrolytes_magnesium: str = Field(description="Serum magnesium (mg/dL) - measured value. Normal: 1.7-2.2 mg/dL. Low with malnutrition, affects neuromuscular function")
    electrolytes_phosphorus: str = Field(description="Serum phosphorus (mg/dL) - measured value. Normal: 2.5-4.5 mg/dL. Reflects bone metabolism and nutrition")

    alkaline_phosphatase: str = Field(description="Alkaline phosphatase (U/L) - measured value. Normal: 30-120 U/L. High may indicate bone growth (children) or metabolic disease")
    alanine_aminotransferase_alt: str = Field(description="ALT (alanine aminotransferase) (U/L) - measured value. Normal: 7-56 U/L. Elevated suggests liver disease, reflects nutritional status")
    aspartate_aminotransferase_ast: str = Field(description="AST (aspartate aminotransferase) (U/L) - measured value. Normal: 10-40 U/L. Elevated suggests liver/muscle disease")

    lymphocyte_count: str = Field(description="Total lymphocyte count (cells/μL) - measured value from CBC. Normal: 1000-4800 cells/μL. Low (<1200) suggests malnutrition or immune compromise")

    biochemical_assessment_date: str = Field(description="Date of biochemical measurements - when were tests performed? Recent (within 3 months) or older?")
    lab_abnormalities_identified: str = Field(description="Abnormalities identified - anemia/iron deficiency/B12 deficiency/folate deficiency/protein malnutrition/vitamin D deficiency/diabetes/dyslipidemia/electrolyte abnormalities/other")
    biochemical_interpretation: str = Field(description="Overall interpretation of biochemical findings and nutritional implications - well-nourished/at-risk/malnourished/specific deficiencies identified/need for intervention")


class SpecificNutrientConcerns(BaseModel):
    """Assessment of specific nutrient deficiencies or concerns."""
    iron_status_signs: str = Field(description="Signs of iron deficiency - pale conjunctivae/pale palmar creases/fatigue/poor concentration/pica/none observed")
    vitamin_d_status: str = Field(description="Vitamin D status indicators - sun exposure adequate/limited/signs of deficiency/bone health concerns")
    calcium_intake_concerns: str = Field(description="Calcium intake adequacy - adequate/concerns due to low dairy/other sources/risk of deficiency")
    protein_adequacy: str = Field(description="Protein adequacy - adequate for age/activity/at-risk due to dietary choices/concerns")
    micronutrient_concerns: str = Field(description="Other micronutrient concerns - B12 (vegetarian)/folate/zinc/iodine/other identified deficiencies")
    vitamin_supplementation: str = Field(description="Current vitamin/mineral supplementation - none/multivitamin/specific vitamins/supplements used")
    hydration_status: str = Field(description="Hydration status assessment - well-hydrated/adequate/mildly dehydrated/moderately dehydrated/severely dehydrated")


class MedicalFactorsAffectingNutrition(BaseModel):
    """Medical conditions and treatments affecting nutrition - nurse reports observations."""
    chronic_illness_impact: str = Field(description="Impact of chronic illness on nutrition - no impact/mild impact/affects appetite/affects absorption/affects overall intake")
    gastrointestinal_issues: str = Field(description="GI symptoms - none/diarrhea/constipation/nausea/vomiting/reflux/IBS/impact on nutrition")
    malabsorption_concerns: str = Field(description="Malabsorption concerns - none/lactose intolerance/celiac disease/other. Impact on nutrition?")
    medication_impact: str = Field(description="Medications affecting appetite or nutrition - none/decreased appetite/nausea/altered taste/increased appetite")
    dental_issues: str = Field(description="Dental issues affecting nutrition - none/cavities/missing teeth/dental pain/orthodontia/affects food choices")
    metabolic_conditions: str = Field(description="Metabolic conditions (diabetes, thyroid, metabolism) - none/present (describe). Dietary requirements?")
    food_related_conditions: str = Field(description="Food-related medical conditions (allergies, intolerances, GERD) - none/present (describe impact)")


class NutritionalAdequacyReport(BaseModel):
    """Assessment of nutritional adequacy compared to recommended dietary allowances (RDA)."""
    caloric_intake_estimate: str = Field(description="Estimated daily caloric intake from 24-hour recall - approximate total calories. Compare to estimated needs based on age/sex/activity")
    caloric_adequacy: str = Field(description="Caloric adequacy assessment - adequate for needs/excessive for needs/insufficient for needs/significantly deficient. Calorie surplus/deficit?")
    protein_adequacy_rda: str = Field(description="Protein intake adequacy vs RDA - meets RDA/exceeds RDA/below RDA. RDA for age/sex = ___g. Actual intake approximately ___g")
    carbohydrate_adequacy: str = Field(description="Carbohydrate adequacy - adequate whole grains/refined carbs excessive/adequate simple carbs/deficient carbs. Meets 45-65% of calories?")
    fat_adequacy: str = Field(description="Fat intake adequacy - appropriate saturated/unsaturated balance/excessive saturated fat/insufficient fat. Meets 20-35% of calories?")
    fiber_adequacy: str = Field(description="Fiber adequacy vs recommendations - adequate fiber (25-30g/day)/insufficient/excess. Estimated intake ___g/day")
    calcium_adequacy_rda: str = Field(description="Calcium intake vs RDA - meets RDA/below RDA. RDA for age = ___mg. Estimated intake ___mg/day. Sources (dairy/fortified/other)")
    iron_adequacy_rda: str = Field(description="Iron intake vs RDA - meets RDA/below RDA. RDA for age/sex = ___mg. Estimated intake ___mg/day. Type (heme/non-heme)")
    vitamin_d_adequacy: str = Field(description="Vitamin D adequacy - adequate sun exposure/dietary sources adequate/insufficient/at risk. IU/day estimated")
    sodium_intake: str = Field(description="Sodium intake assessment - within guidelines (<2300mg)/excess/significantly excess. Estimated mg/day")
    water_hydration_adequacy: str = Field(description="Water intake vs guidelines - adequate (8+ glasses/64+ oz)/good/fair/poor/excessive")
    micronutrient_gaps: str = Field(description="Identified micronutrient gaps (B12, folate, zinc, iodine, etc.) - none/possible deficiencies/likely deficiencies. Supplements addressing gaps?")
    macronutrient_distribution: str = Field(description="Macronutrient distribution - protein ___%, carbs ___%, fat ___%. Balanced distribution or imbalanced? (Recommended: P 10-35%, C 45-65%, F 20-35%)")
    diet_quality_assessment: str = Field(description="Overall diet quality - excellent (balanced, varied, nutrient-dense)/good/fair/poor (processed, limited variety, nutrient-poor)")


class HealthyPatientNutritionalStatus(BaseModel):
    """Assessment specific to healthy, normal weight patients."""
    current_status: str = Field(description="Current status - maintains healthy weight/weight stable/minor fluctuation/health risks absent")
    intake_meets_needs: str = Field(description="Overall intake meets nutritional needs - yes, well-balanced/yes, adequate/borderline/some concerns")
    preventive_nutrition: str = Field(description="Nutritional practices that support health - regular meals/adequate variety/whole grains/fruits/vegetables/lean protein/adequate hydration")
    areas_for_improvement: str = Field(description="Areas where nutrition could be optimized - increased fruits/vegetables/reduce sugar/increase whole grains/other/none needed")
    risk_factors_present: str = Field(description="Any nutrition-related risk factors identified - none/minor concerns (e.g., low fruit intake)/potential future risks/good prevention practices")
    maintenance_recommendations: str = Field(description="Recommendations to maintain healthy nutrition - continue current pattern/minor adjustments/increase physical activity/maintain variety/other")


class ObesePatientNutritionalStatus(BaseModel):
    """Assessment specific to obese or overweight patients."""
    current_weight_status: str = Field(description="Current weight status - obese (BMI >30)/overweight (BMI 25-29.9)/at-risk. BMI = ___, weight-related health risks present?")
    caloric_excess: str = Field(description="Estimated daily caloric excess - surplus per day ___calories. Annual weight gain projection?")
    weight_gain_pattern: str = Field(description="Weight gain pattern - gradual/rapid/cyclical/fluctuating/progressive. Timeline of weight gain?")
    caloric_intake_vs_needs: str = Field(description="Caloric intake vs actual energy needs - significantly excessive/moderately excessive/borderline. Excess ___calories/day vs optimal")
    macronutrient_imbalance: str = Field(description="Macronutrient imbalance contributing to weight - excessive carbs/excessive fat/excessive protein/poor distribution")
    problematic_foods_identified: str = Field(description="Foods/beverages contributing to excess calories - sugary drinks/processed foods/fast food/large portions/snacking patterns/alcohol")
    eating_pattern_issues: str = Field(description="Eating pattern issues - skips breakfast then overeats/emotional eating/mindless eating/portion control poor/rapid eating/late night eating/other")
    physical_activity_level: str = Field(description="Physical activity level - sedentary/light/moderate/active. Impact on caloric balance?")
    weight_loss_readiness: str = Field(description="Readiness for weight management - motivated/somewhat motivated/ambivalent/resistant/willing but needs support. Barriers identified?")
    recommended_caloric_intake: str = Field(description="Recommended daily caloric intake for weight loss (if appropriate) - current ___cal, recommend ___cal for moderate deficit (~500cal = 1lb/week loss)")
    dietary_changes_priority: str = Field(description="Priority dietary changes needed (ranked) - reduce sugary drinks/portion control/increase vegetables/reduce processed foods/increase activity/other")
    behavioral_support_needed: str = Field(description="Behavioral support needed - nutrition counseling/dietitian referral/weight loss program/support group/app/other resources")
    comorbidity_nutrition_impact: str = Field(description="Nutrition-related comorbidities (diabetes, hypertension, dyslipidemia, PCOS, etc.) - present (describe)/none. Special dietary needs?")
    weight_loss_goals: str = Field(description="Realistic weight loss goals if appropriate - target weight/timeline/intermediate milestones/sustainability plan")


class AssessmentSummary(BaseModel):
    """Overall nutrition and growth assessment summary prepared by nurse for doctor."""
    overall_nutrition_status: str = Field(description="Overall nutrition status rating - well-nourished/adequately nourished/at-risk/malnourished/severely malnourished")
    overall_growth_status: str = Field(description="Overall growth status - normal for age/above average/below average/concerning/failure to thrive")
    growth_pattern_trend: str = Field(description="Growth pattern trend analysis - steady/accelerating/plateauing/declining/fluctuating")
    major_nutritional_strengths: str = Field(description="Major nutritional strengths observed, comma-separated")
    nutritional_concerns: str = Field(description="Identified nutritional concerns or deficiencies, comma-separated")
    growth_concerns: str = Field(description="Growth concerns if any - none/short stature/growth delay/rapid growth/other")
    urgent_interventions_needed: str = Field(description="Urgent interventions needed - none/nutrition support/referral to dietitian/medical investigation/growth monitoring")
    risk_factors_identified: str = Field(description="Risk factors for poor nutrition or growth (poverty, food insecurity, medical conditions, etc.), comma-separated")
    protective_factors: str = Field(description="Protective factors supporting good nutrition (food security, education, healthy practices, etc.), comma-separated")
    recommendations_for_doctor: str = Field(description="Key recommendations prepared for doctor review - dietary changes/supplementation/investigations/referrals/monitoring plan")
    follow_up_plan: str = Field(description="Recommended follow-up - routine monitoring/1 month follow-up/dietitian referral/other specialist/growth tracking")
    doctor_discussion_needed: str = Field(description="Topics that require doctor discussion with patient - explain/education needed/medication adjustment/investigation/specialist referral/reassurance")


class NutritionGrowthAssessment(BaseModel):
    """
    Comprehensive Nutrition and Growth Measurements Assessment.

    Doctor-Nurse Consultation Model: The doctor directs the nurse to perform
    physical measurements and assessments. The nurse collects objective
    measurements, makes observations, asks questions about dietary intake and
    nutrition, and prepares a comprehensive report for the doctor. The doctor
    reviews the nurse's findings and determines clinical management.

    Organized as a collection of BaseModel sections representing distinct
    aspects of nutrition and growth evaluation.
    """
    # Physical measurements taken by nurse
    anthropometric_measurements: AnthropometricMeasurements

    # Growth indicators calculated from measurements
    growth_indicators: GrowthIndicators

    # Nurse's nutritional status assessment
    nutrition_status_assessment: NutritionStatusAssessment

    # Dietary intake history including 24-hour recall
    dietary_intake_assessment: DietaryIntakeAssessment

    # Nutritional adequacy report (RDA comparison)
    nutritional_adequacy_report: NutritionalAdequacyReport

    # Socioeconomic factors
    socioeconomic_nutrition_factors: SocioeconomicNutritionFactors

    # Growth milestones (pediatric patients)
    growth_milestones: GrowthMilestones

    # Biochemical and laboratory measurements
    biochemical_measurements: BiochemicalMeasurements

    # Specific nutrient concerns
    specific_nutrient_concerns: SpecificNutrientConcerns

    # Medical factors affecting nutrition
    medical_factors_affecting_nutrition: MedicalFactorsAffectingNutrition

    # Assessment for healthy/normal weight patients
    healthy_patient_nutritional_status: Optional[HealthyPatientNutritionalStatus]

    # Assessment for obese/overweight patients
    obese_patient_nutritional_status: Optional[ObesePatientNutritionalStatus]

    # Current dietary recommendations
    dietary_recommendations: DietaryRecommendations

    # Nurse's summary and recommendations for doctor
    assessment_summary: AssessmentSummary


def ask_nutrition_questions() -> dict:
    """
    Ask patient nutrition and growth assessment questions interactively.
    Returns a dictionary of patient responses to be used in assessment.
    """
    print("\n" + "="*60)
    print("NUTRITION AND GROWTH ASSESSMENT")
    print("="*60)
    print()
    print("MEASURES: This assessment evaluates nutritional status, growth patterns, and")
    print("  identifies potential nutritional deficiencies or growth concerns.")
    print("  • Anthropometric measurements (height, weight, BMI, growth percentiles)")
    print("  • Dietary intake patterns and nutritional adequacy")
    print("  • Signs of malnutrition or nutritional deficiencies")
    print("  • Growth velocity and developmental milestones")
    print("  • Feeding behaviors and eating disorders risk")
    print()
    print("TOP 10 KEY ASSESSMENT QUESTIONS:")
    print("  1. What is your current height and weight?")
    print("  2. Have you noticed any recent weight changes?")
    print("  3. Describe a typical day's meals and snacks.")
    print("  4. Do you have any dietary restrictions or preferences?")
    print("  5. How many servings of fruits and vegetables do you eat daily?")
    print("  6. Do you take any vitamins or nutritional supplements?")
    print("  7. Have you experienced any changes in appetite?")
    print("  8. Do you have any difficulty swallowing or eating?")
    print("  9. Are you concerned about your weight or body image?")
    print(" 10. For children: Are they meeting growth and developmental milestones?")
    print()
    print("="*60)
    print("DETAILED NUTRITION AND GROWTH QUESTIONNAIRE")
    print("="*60)

    responses = {}

    # ANTHROPOMETRIC MEASUREMENTS
    print("\n--- ANTHROPOMETRIC MEASUREMENTS ---")
    responses['height_cm'] = input("Height in centimeters (standing): ").strip()
    responses['weight_kg'] = input("Weight in kilograms: ").strip()
    responses['waist_cm'] = input("Waist circumference in cm: ").strip()
    responses['hip_cm'] = input("Hip circumference in cm: ").strip()
    responses['muac_cm'] = input("Mid-upper arm circumference (MUAC) in cm: ").strip()

    # 24-HOUR DIET RECALL
    print("\n--- 24-HOUR DIET RECALL ---")
    responses['breakfast'] = input("What did you eat for breakfast yesterday? ").strip()
    responses['morning_snack'] = input("Any morning snacks?: ").strip()
    responses['lunch'] = input("What did you eat for lunch?: ").strip()
    responses['afternoon_snack'] = input("Any afternoon snacks?: ").strip()
    responses['dinner'] = input("What did you eat for dinner?: ").strip()
    responses['evening_snack'] = input("Any evening snacks?: ").strip()
    responses['beverages'] = input("What beverages did you drink? (water, coffee, soda, etc.): ").strip()

    # MACRONUTRIENT ASSESSMENT
    print("\n--- DIETARY INTAKE QUESTIONS ---")
    responses['protein_sources'] = input("What are your main protein sources? (meat/fish/eggs/beans/dairy): ").strip()
    responses['protein_frequency'] = input("How many servings of protein per day?: ").strip()

    responses['grain_sources'] = input("What grains do you eat? (bread/rice/pasta): ").strip()
    responses['whole_grain_frequency'] = input("How often do you eat whole grains?: ").strip()

    responses['vegetable_intake'] = input("How many servings of vegetables daily?: ").strip()
    responses['fruit_intake'] = input("How many servings of fruit daily?: ").strip()

    responses['fat_sources'] = input("What fats/oils do you use? (butter/oil/margarine): ").strip()
    responses['sugar_frequency'] = input("How often do you consume sugary foods/drinks?: ").strip()

    # PHYSICAL ASSESSMENT
    print("\n--- PHYSICAL ASSESSMENT ---")
    responses['general_appearance'] = input("Overall appearance (well-nourished/adequate/malnourished): ").strip()
    responses['muscle_assessment'] = input("Muscle mass appearance: ").strip()
    responses['hair_quality'] = input("Hair quality (lustrous/normal/dull): ").strip()
    responses['skin_condition'] = input("Skin condition (good/dry/other): ").strip()

    # GROWTH PATTERN
    print("\n--- GROWTH PATTERN ---")
    responses['patient_age'] = input("Age (years/months): ").strip()
    responses['growth_pattern'] = input("How has your growth been? (normal/slow/rapid/stable): ").strip()
    responses['weight_changes'] = input("Have you had recent weight changes? (no/gained/lost): ").strip()

    # MEDICAL AND CONTEXTUAL
    print("\n--- MEDICAL AND CONTEXTUAL FACTORS ---")
    responses['medical_conditions'] = input("Any medical conditions affecting nutrition?: ").strip()
    responses['medications'] = input("Current medications?: ").strip()
    responses['food_allergies'] = input("Any food allergies or intolerances?: ").strip()
    responses['food_security'] = input("Do you have reliable access to food? (yes/sometimes/no): ").strip()
    responses['physical_activity'] = input("Physical activity level (sedentary/light/moderate/active): ").strip()
    responses['sleep_hours'] = input("Average sleep per night (hours): ").strip()

    return responses


def generate_ai_nutrition_assessment(
    patient_name: str,
    responses: dict,
    output_path: Optional[Path] = None,
    prompt_style: PromptStyle = PromptStyle.DETAILED,
) -> NutritionGrowthAssessment:
    """
    Generate comprehensive nutrition assessment using MedKitClient AI.

    Uses schema-aware prompting to generate detailed medical assessment
    based on patient responses and clinical data.

    Args:
        patient_name: Name of the patient
        responses: Dictionary of patient responses from questions
        output_path: Optional path to save JSON output
        prompt_style: Style of schema prompt (DETAILED, CONCISE, TECHNICAL)

    Returns:
        NutritionGrowthAssessment: AI-generated validated assessment object
    """
    # Initialize MedKitClient with model from ModuleConfig
    try:
        module_config = get_module_config("exam_nutrition_growth")
        model_name = module_config.model_name
    except ValueError:
        # Fallback if module not registered yet
        model_name = "gemini-2.5-flash"

    client = MedKitClient(model_name=model_name)

    # Prepare patient context from responses
    patient_context = f"""
Patient Assessment Data:
- Name: {patient_name}
- Age: {responses.get('patient_age', 'Not provided')}
- Height: {responses.get('height_cm', 'Not measured')} cm
- Weight: {responses.get('weight_kg', 'Not measured')} kg
- MUAC: {responses.get('muac_cm', 'Not measured')} cm
- Waist: {responses.get('waist_cm', 'Not measured')} cm
- Hip: {responses.get('hip_cm', 'Not measured')} cm

24-Hour Diet Recall:
- Breakfast: {responses.get('breakfast', 'Not reported')}
- Morning snack: {responses.get('morning_snack', 'None')}
- Lunch: {responses.get('lunch', 'Not reported')}
- Afternoon snack: {responses.get('afternoon_snack', 'None')}
- Dinner: {responses.get('dinner', 'Not reported')}
- Evening snack: {responses.get('evening_snack', 'None')}
- Beverages: {responses.get('beverages', 'Not reported')}

Dietary Patterns:
- Protein sources: {responses.get('protein_sources', 'Not reported')}
- Protein frequency: {responses.get('protein_frequency', 'Not assessed')}
- Grain sources: {responses.get('grain_sources', 'Not reported')}
- Whole grain frequency: {responses.get('whole_grain_frequency', 'Not reported')}
- Vegetable intake: {responses.get('vegetable_intake', 'Not reported')} servings/day
- Fruit intake: {responses.get('fruit_intake', 'Not reported')} servings/day
- Fat sources: {responses.get('fat_sources', 'Not reported')}
- Sugar/Sweet consumption: {responses.get('sugar_frequency', 'Not assessed')}

Physical Assessment:
- General appearance: {responses.get('general_appearance', 'Not assessed')}
- Muscle mass: {responses.get('muscle_assessment', 'Not assessed')}
- Hair quality: {responses.get('hair_quality', 'Not assessed')}
- Skin condition: {responses.get('skin_condition', 'Not assessed')}

Growth and Medical Factors:
- Growth pattern: {responses.get('growth_pattern', 'Not assessed')}
- Weight changes: {responses.get('weight_changes', 'None reported')}
- Medical conditions: {responses.get('medical_conditions', 'None reported')}
- Medications: {responses.get('medications', 'None')}
- Food allergies/intolerances: {responses.get('food_allergies', 'None')}
- Food security: {responses.get('food_security', 'Not assessed')}
- Physical activity: {responses.get('physical_activity', 'Not assessed')}
- Sleep: {responses.get('sleep_hours', 'Not reported')} hours/night
"""

    # Generate assessment using MedKitClient
    sys_prompt = f"""You are an expert nutritionist and pediatrician specializing in nutrition and growth assessment.

Given the patient's detailed nutrition and growth data below, provide a comprehensive assessment:

{patient_context}

Generate a clinical assessment that includes:
- Nutritional status evaluation
- Growth assessment
- Key findings and concerns
- Recommendations for dietary improvement
- Educational guidance for the patient/family
- Return structured JSON matching the exact schema provided, with all required fields populated."""

    assessment = client.generate_text(
        prompt=f"Provide a comprehensive nutrition and growth assessment for {patient_name} based on the clinical data provided.",
        schema=NutritionGrowthAssessment,
        sys_prompt=sys_prompt,
    )

    # Save to file if path provided
    if output_path is None:
        output_path = Path("outputs") / f"{patient_name.lower().replace(' ', '_')}_nutrition_growth_ai.json"

    # Create outputs directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save assessment as JSON
    with open(output_path, 'w') as f:
        json.dump(assessment.model_dump(), f, indent=2)

    print(f"✓ AI Assessment saved to: {output_path}")

    return assessment


def create_nutrition_assessment_from_responses(patient_name: str, responses: dict, output_path: Optional[Path] = None) -> NutritionGrowthAssessment:
    """
    Create a structured nutrition assessment object from collected patient responses.

    Args:
        patient_name: Name of the patient
        responses: Dictionary of patient responses from questions
        output_path: Optional path to save JSON output

    Returns:
        NutritionGrowthAssessment: Validated assessment object
    """
    # Calculate BMI if measurements available
    try:
        height_m = float(responses.get('height_cm', '0')) / 100
        weight_kg = float(responses.get('weight_kg', '0'))
        bmi = weight_kg / (height_m ** 2) if height_m > 0 else 0
    except:
        bmi = 0

    # Create assessment object from responses
    assessment_data = {
        "anthropometric_measurements": {
            "height_cm": responses.get('height_cm', ''),
            "weight_kg": responses.get('weight_kg', ''),
            "head_circumference_cm": "Not measured",
            "chest_circumference_cm": "Not measured",
            "mid_upper_arm_circumference_cm": responses.get('muac_cm', ''),
            "triceps_skinfold_thickness_mm": "Not measured",
            "biceps_skinfold_thickness_mm": "Not measured",
            "subscapular_skinfold_thickness_mm": "Not measured",
            "waist_circumference_cm": responses.get('waist_cm', ''),
            "hip_circumference_cm": responses.get('hip_cm', ''),
            "measurement_reliability": "Patient-reported with some measurements"
        },
        "growth_indicators": {
            "bmi_calculation": f"BMI: {bmi:.1f}" if bmi > 0 else "BMI: Not calculated",
            "height_for_age": "To be assessed by clinician",
            "weight_for_height": "To be assessed by clinician",
            "weight_for_age": "To be assessed by clinician",
            "muac_interpretation": "To be assessed by clinician",
            "muac_nutritional_status": "To be assessed by clinician",
            "triceps_skinfold_interpretation": "Not measured",
            "subscapular_skinfold_interpretation": "Not measured",
            "body_composition_assessment": responses.get('general_appearance', ''),
            "subcutaneous_fat_stores": responses.get('muscle_assessment', ''),
            "waist_hip_ratio": "To be calculated",
            "waist_circumference_category": "To be assessed",
            "growth_trend": responses.get('growth_pattern', ''),
            "growth_velocity": "To be assessed",
            "head_circumference_for_age": "Not measured",
            "proportionality": "To be assessed"
        },
        "nutrition_status_assessment": {
            "general_appearance": responses.get('general_appearance', ''),
            "muscle_mass_assessment": responses.get('muscle_assessment', ''),
            "subcutaneous_fat": "To be assessed",
            "skin_turgor": responses.get('skin_condition', ''),
            "hair_quality": responses.get('hair_quality', ''),
            "nail_quality": "Not assessed",
            "eyes_brightness": "Normal",
            "oral_assessment": "Not assessed",
            "energy_level": "To be assessed",
            "overall_nutrition_status": "To be determined by clinician"
        },
        "dietary_intake_assessment": {
            "twenty_four_hour_recall": {
                "breakfast": responses.get('breakfast', ''),
                "morning_snack": responses.get('morning_snack', ''),
                "lunch": responses.get('lunch', ''),
                "afternoon_snack": responses.get('afternoon_snack', ''),
                "dinner": responses.get('dinner', ''),
                "evening_snack": responses.get('evening_snack', ''),
                "beverages": responses.get('beverages', ''),
                "supplements": "Not reported"
            },
            "macronutrient_intake_estimation": {
                "protein_sources_questions": "Protein sources identified",
                "protein_sources_identified": responses.get('protein_sources', ''),
                "daily_protein_servings": responses.get('protein_frequency', ''),
                "protein_quantity_estimation": "To be assessed",
                "carbohydrate_sources_questions": "Grains identified",
                "carbohydrate_sources_identified": responses.get('grain_sources', ''),
                "whole_grain_frequency": responses.get('whole_grain_frequency', ''),
                "refined_carb_frequency": "To be assessed",
                "daily_carb_servings": "To be estimated",
                "carbohydrate_quantity_assessment": "To be assessed",
                "fat_sources_questions": "Fat sources identified",
                "fat_sources_identified": responses.get('fat_sources', ''),
                "saturated_fat_intake": "To be assessed",
                "unsaturated_fat_intake": "To be assessed",
                "cooking_methods": "To be assessed",
                "daily_fat_servings": "To be estimated",
                "fat_quantity_assessment": "To be assessed",
                "fiber_sources_questions": "Fiber intake assessed",
                "vegetable_intake": responses.get('vegetable_intake', ''),
                "fruit_intake": responses.get('fruit_intake', ''),
                "whole_grain_intake_detail": responses.get('whole_grain_frequency', ''),
                "legume_bean_intake": "To be assessed",
                "estimated_daily_fiber": "To be calculated",
                "fiber_quantity_assessment": "To be assessed",
                "sugary_food_questions": "Sugar intake assessed",
                "added_sugar_sources": responses.get('sugar_frequency', ''),
                "estimated_added_sugar": "To be estimated",
                "fluid_intake_questions": "Beverages identified",
                "water_intake_daily": "To be assessed",
                "other_beverages_detailed": responses.get('beverages', ''),
                "estimation_confidence": "Approximate"
            },
            "typical_daily_meals": "To be assessed",
            "meal_regularity": "To be assessed",
            "breakfast_consumption": "To be assessed",
            "protein_intake": responses.get('protein_frequency', ''),
            "carbohydrate_intake": responses.get('grain_sources', ''),
            "fat_intake": responses.get('fat_sources', ''),
            "fruit_vegetable_intake": f"Vegetables: {responses.get('vegetable_intake', '')}, Fruits: {responses.get('fruit_intake', '')}",
            "dairy_consumption": "To be assessed",
            "sugary_drink_intake": responses.get('sugar_frequency', ''),
            "fast_food_frequency": "To be assessed",
            "hydration": "To be assessed",
            "appetite": "To be assessed",
            "feeding_difficulties": "None reported",
            "allergies_intolerances": responses.get('food_allergies', '')
        },
        "nutritional_adequacy_report": {
            "caloric_intake_estimate": "To be calculated",
            "caloric_adequacy": "To be assessed",
            "protein_adequacy_rda": responses.get('protein_frequency', ''),
            "carbohydrate_adequacy": "To be assessed",
            "fat_adequacy": "To be assessed",
            "fiber_adequacy_rda": "To be assessed",
            "calcium_adequacy_rda": "To be assessed",
            "iron_adequacy_rda": "To be assessed",
            "vitamin_d_adequacy": "To be assessed",
            "sodium_intake": "To be assessed",
            "water_hydration_adequacy": "To be assessed",
            "micronutrient_gaps": "To be assessed",
            "macronutrient_distribution": "To be assessed",
            "diet_quality_assessment": "To be determined by clinician"
        },
        "socioeconomic_nutrition_factors": {
            "food_security": responses.get('food_security', ''),
            "access_to_food": responses.get('food_security', ''),
            "ability_to_afford_nutritious_food": "To be assessed",
            "food_preparation_facilities": "To be assessed",
            "refrigeration_access": "To be assessed",
            "community_resources": "To be assessed",
            "living_situation_impact": "Stable",
            "cultural_dietary_practices": "To be assessed",
            "education_barriers": "None reported"
        },
        "growth_milestones": {
            "age_months": responses.get('patient_age', ''),
            "developmental_stage": "To be assessed",
            "motor_development": "To be assessed",
            "feeding_milestone": "Eating typical diet",
            "tooth_eruption": "Not assessed",
            "language_development": "Normal",
            "immunization_status": "To be assessed"
        },
        "biochemical_measurements": {
            "hemoglobin_level": "Not measured",
            "hematocrit_level": "Not measured",
            "red_blood_cell_count": "Not measured",
            "mean_corpuscular_volume_mcv": "Not measured",
            "serum_albumin": "Not measured",
            "serum_prealbumin": "Not measured",
            "total_protein": "Not measured",
            "blood_glucose": "Not measured",
            "hemoglobin_a1c": "Not measured",
            "serum_iron": "Not measured",
            "ferritin": "Not measured",
            "transferrin_saturation": "Not measured",
            "vitamin_b12": "Not measured",
            "folate_level": "Not measured",
            "vitamin_d_25_oh": "Not measured",
            "total_cholesterol": "Not measured",
            "hdl_cholesterol": "Not measured",
            "ldl_cholesterol": "Not measured",
            "triglycerides": "Not measured",
            "blood_urea_nitrogen_bun": "Not measured",
            "serum_creatinine": "Not measured",
            "bun_creatinine_ratio": "Not measured",
            "electrolytes_sodium": "Not measured",
            "electrolytes_potassium": "Not measured",
            "electrolytes_calcium": "Not measured",
            "electrolytes_magnesium": "Not measured",
            "electrolytes_phosphorus": "Not measured",
            "alkaline_phosphatase": "Not measured",
            "alanine_aminotransferase_alt": "Not measured",
            "aspartate_aminotransferase_ast": "Not measured",
            "lymphocyte_count": "Not measured",
            "biochemical_assessment_date": "None",
            "lab_abnormalities_identified": "Not tested",
            "biochemical_interpretation": "Lab work recommended"
        },
        "specific_nutrient_concerns": {
            "iron_status_signs": "To be assessed",
            "vitamin_d_status": "To be assessed",
            "calcium_intake_concerns": "To be assessed",
            "protein_adequacy": responses.get('protein_sources', ''),
            "micronutrient_concerns": "To be assessed",
            "vitamin_supplementation": "To be assessed",
            "hydration_status": "To be assessed"
        },
        "medical_factors_affecting_nutrition": {
            "chronic_illness_impact": responses.get('medical_conditions', ''),
            "gastrointestinal_issues": "None reported",
            "malabsorption_concerns": "None reported",
            "medication_impact": responses.get('medications', ''),
            "dental_issues": "Not assessed",
            "metabolic_conditions": "To be assessed",
            "food_related_conditions": responses.get('food_allergies', '')
        },
        "healthy_patient_nutritional_status": {
            "current_status": "To be determined",
            "intake_meets_needs": "To be assessed",
            "preventive_nutrition": "To be assessed",
            "areas_for_improvement": "To be identified",
            "risk_factors_present": "To be assessed",
            "maintenance_recommendations": "To be determined"
        },
        "obese_patient_nutritional_status": None,
        "dietary_recommendations": {
            "caloric_goal": "To be determined",
            "protein_recommendation": "To be determined",
            "carbohydrate_recommendation": "To be determined",
            "fat_recommendation": "To be determined",
            "fiber_recommendation": "To be determined",
            "supplementation": "To be determined",
            "dietary_modifications": "To be determined",
            "meal_planning_suggestions": "To be determined"
        },
        "assessment_summary": {
            "overall_nutrition_status": "To be determined by clinician",
            "overall_growth_status": "To be determined",
            "growth_pattern_trend": responses.get('growth_pattern', ''),
            "major_nutritional_strengths": "To be identified",
            "nutritional_concerns": "To be identified",
            "growth_concerns": responses.get('weight_changes', ''),
            "urgent_interventions_needed": "To be determined",
            "risk_factors_identified": responses.get('food_security', ''),
            "protective_factors": "To be identified",
            "recommendations_for_doctor": "Comprehensive dietary assessment and growth monitoring",
            "follow_up_plan": "Dietitian referral recommended",
            "doctor_discussion_needed": "Dietary habits, growth pattern, medical conditions"
        }
    }

    # Create assessment object
    assessment = NutritionGrowthAssessment(**assessment_data)

    # Save to file if path provided
    if output_path is None:
        output_path = Path("outputs") / f"{patient_name.lower().replace(' ', '_')}_nutrition_growth.json"

    # Create outputs directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save assessment as JSON
    with open(output_path, 'w') as f:
        json.dump(assessment_data, f, indent=2)

    print(f"\n✓ Assessment saved to: {output_path}")

    return assessment


def evaluate_nutrition_and_growth(
    patient_name: str,
    output_path: Optional[Path] = None,
    use_schema_prompt: bool = True,
    prompt_style: PromptStyle = PromptStyle.DETAILED,
    use_ai: bool = True,
) -> NutritionGrowthAssessment:
    """
    Evaluate patient nutrition and growth status through interactive questionnaire.

    Doctor directs the nurse to perform examination and measurements.
    Nurse collects findings and prepares AI-enhanced report for doctor.

    Args:
        patient_name: Name or identifier of the patient
        output_path: Optional path to save JSON output. Defaults to outputs/{patient_name}_nutrition_growth_ai.json
        use_schema_prompt: Whether to use PydanticPromptGenerator for schema
        prompt_style: Style of schema prompt (DETAILED, CONCISE, TECHNICAL)
        use_ai: Whether to use MedKitClient for AI-powered assessment generation (default: True)

    Returns:
        NutritionGrowthAssessment: Validated nutrition and growth assessment object
    """
    if not patient_name or not patient_name.strip():
        raise ValueError("Patient name cannot be empty")

    # Ask patient questions interactively
    print(f"\nStarting nutrition and growth assessment for: {patient_name}")
    responses = ask_nutrition_questions()

    # Generate assessment using AI if enabled, otherwise use template-based approach
    if use_ai:
        print("\n⏳ Generating AI-powered assessment using MedKitClient...")
        try:
            assessment = generate_ai_nutrition_assessment(
                patient_name,
                responses,
                output_path,
                prompt_style=prompt_style
            )
        except Exception as e:
            print(f"⚠️ AI assessment generation failed: {e}")
            print("Falling back to template-based assessment...")
            assessment = create_nutrition_assessment_from_responses(patient_name, responses, output_path)
    else:
        # Create assessment from responses using template-based approach
        assessment = create_nutrition_assessment_from_responses(patient_name, responses, output_path)

    return assessment


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Nutrition and Growth Measurements Assessment - Doctor-Nurse Consultation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Default - saves to outputs/patient_nutrition_growth.json
  python exam_nutrition_growth.py "John Doe"

  # Custom output path
  python exam_nutrition_growth.py "John Doe" -o custom_assessment.json

  # With concise prompting
  python exam_nutrition_growth.py "John Doe" --concise

Doctor-Nurse Consultation Process:

  DOCTOR DIRECTS NURSE TO:

  1. TAKE ANTHROPOMETRIC MEASUREMENTS:
     "Nurse, please measure the patient's height (standing or lying),
      weight, and if pediatric patient, head and chest circumference."

  2. ASSESS PHYSICAL SIGNS OF NUTRITION:
     "Observe and report on muscle mass, subcutaneous fat, skin turgor,
      hair quality, nails, eyes, and overall appearance."

  3. ASSESS GROWTH STATUS:
     "Compare measurements to age-appropriate standards and growth charts.
      Report height-for-age, weight-for-height, BMI, and growth trend."

  4. GATHER DIETARY HISTORY:
     "Ask about typical daily meals, food intake, eating patterns,
      food preferences, allergies, and dietary restrictions."

  5. ASSESS SOCIOECONOMIC FACTORS:
     "Inquire about food security, ability to afford nutritious food,
      access to food preparation facilities, and community resources."

  6. ASSESS MEDICAL FACTORS:
     "Note any chronic illnesses, GI issues, medications, dental problems,
      and how they affect nutrition."

  7. PREPARE COMPREHENSIVE REPORT:
     "Summarize all findings, identify nutritional concerns, growth issues,
      risk factors, and recommendations for doctor review."

  NURSE REPORTS TO DOCTOR:
  - Objective measurements and growth indicators
  - Physical signs of nutritional status
  - Dietary intake patterns
  - Socioeconomic context
  - Medical factors affecting nutrition
  - Overall assessment and recommendations

  DOCTOR REVIEWS AND DETERMINES:
  - Clinical significance of findings
  - Need for further investigations
  - Dietary or medical interventions
  - Referrals (dietitian, specialist)
  - Follow-up plan
        """
    )
    parser.add_argument("patient", nargs='+', help="Name or identifier of the patient")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Path to save JSON output. Defaults to outputs/{patient_name}_nutrition_growth.json"
    )
    parser.add_argument(
        "--concise",
        action="store_true",
        help="Use concise prompt style (faster generation)"
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Disable AI-powered assessment generation (use template-based approach)"
    )

    args = parser.parse_args()

    try:
        patient_name = " ".join(args.patient)
        prompt_style = PromptStyle.CONCISE if args.concise else PromptStyle.DETAILED
        use_ai = not args.no_ai

        result = evaluate_nutrition_and_growth(
            patient_name=patient_name,
            output_path=args.output,
            prompt_style=prompt_style,
            use_ai=use_ai,
        )
        print("✓ Success!")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
