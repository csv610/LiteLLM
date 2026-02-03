#!/usr/bin/env python3
"""
Script to create example_inputs.txt files for modules that are missing them.
"""

import sys
from pathlib import Path

# Module configurations with relevant examples
MODULE_EXAMPLES = {
    "genetic_variant": """# Genetic Variant Examples

## Common Genetic Variants
brca1_mutation
brca2_mutation
cystic_fibrosis_delta_f508
huntington_cag_repeat
sickle_cell_mutation
thrombophilia_factor_v
marfan_fbn1_mutation
achondroplasia_fgfr3
phenylketonuria_pah
tay_sachs_hexa

## Pharmacogenomic Variants
cyp2d6_poor_metabolizer
cyp2c19_loss_of_function
tpmt_deficiency
dpd_deficiency
ugt1a1_variant
nudt15_variant
hlab5801_allele
slco1b1_variant
vkorc1_variant
cyp2c9_variant

## Cancer-Related Variants
egfr_mutation
alk_rearrangement
braf_v600e
kras_mutation
ntrk_fusion
her2_amplification
p53_mutation
msi_high
tmb_high
pd_l1_expression

## Cardiovascular Variants
ldlr_mutation
apob_mutation
pcsk9_variant
mthfr_variant
factor_v_leiden
prothrombin_mutation
fibrillin_mutation
myosin_binding_protein_c
titin_mutation
lamin_ac_mutation

## Neurological Variants
app_mutation
presenilin_mutation
alpha_synuclein
lrrk2_mutation
parkin_mutation
huntingtin_cag_expansion
ataxin_mutation
sod1_mutation
fus_mutation
tar_dna_binding_protein
""",

    "imaging_finding": """# Imaging Finding Examples

## Common Radiological Findings
pulmonary_nodule
lung_mass
pleural_effusion
pneumothorax
atelectasis
consolidation
interstitial_lung_disease
pulmonary_infiltrate
cavitary_lesion
ground_glass_opacity

## Cardiac Imaging Findings
left_ventricular_hypertrophy
right_ventricular_hypertrophy
cardiomegaly
pericardial_effusion
aortic_aneurysm
aortic_dissection
valvular_stenosis
valvular_regurgitation
wall_motion_abnormality
myocardial_infarction

## Neurological Imaging Findings
brain_tumor
cerebral_edema
hydrocephalus
subdural_hematoma
epidural_hematoma
subarachnoid_hemorrhage
intracerebral_hemorrhage
ischemic_stroke
hemorrhagic_stroke
white_matter_lesions

## Abdominal Imaging Findings
hepatic_lesion
renal_mass
splenomegaly
hepatomegaly
gallstones
kidney_stones
pancreatic_mass
adrenal_mass
lymphadenopathy
ascites

## Musculoskeletal Findings
fracture
dislocation
bone_lesion
soft_tissue_mass
joint_effusion
osteomyelitis
septic_arthritis
degenerative_joint_disease
herniated_disc
spinal_stenosis

## Vascular Imaging Findings
atherosclerosis
stenosis
occlusion
aneurysm
thrombosis
embolism
vascular_malformation
venous_insufficiency
deep_vein_thrombosis
pulmonary_embolism
""",

    "lab_unit": """# Laboratory Unit Examples

## Common Laboratory Units
mg_dl
g_dl
mmol_l
umol_l
ng_ml
pg_ml
iu_l
miu_ml
ul_u_ml
kat_l

## Hematology Units
cells_mcl
cells_ul
fl
pg
g_dl
percent
ratio
absolute_count
relative_count
index

## Chemistry Units
mg_dl
g_dl
mmol_l
umol_l
meq_l
mm_hg
ph_units
mosm_kg
ng_ml
iu_l

## Hormone Units
ng_ml
pg_ml
miu_ml
iu_l
pmol_l
nmol_l
umol_l
mg_dl
mcg_dl
pmol_l

## Enzyme Units
u_l
iu_l
kat_l
ul_u_ml
nkatal_l
international_units
enzyme_units
activity_units
catalytic_activity
reaction_rate

## Drug Level Units
ng_ml
ug_ml
mg_l
umol_l
mcg_ml
pmol_l
nmol_l
free_concentration
total_concentration
therapeutic_range

## Specialized Units
arbitrary_units
relative_units
standard_deviation
coefficient_variation
titer
dilution
concentration
activity
index
score
""",

    "medical_abbreviation": """# Medical Abbreviation Examples

## Common Medical Abbreviations
cpr
cpr
cpr
cpr
cpr
cpr
cpr
cpr
cpr
cpr

## Vital Signs Abbreviations
hr
bp
rr
temp
spo2
map
cpp
svr
pvr
co

## Laboratory Abbreviations
cbc
cmp
bmp
lft
lipid_panel
hba1c
esr
crp
pt
inr

## Imaging Abbreviations
ct
mri
xray
us
pet
spect
cta
mra
doppler
fluoroscopy

## Procedure Abbreviations
ecg
eeg
emg
npg
ppg
ekg
eeg
mri
ct_scan
ultrasound

## Medication Abbreviations
po
iv
im
sc
sl
pr
bid
tid
qid
qid

## Clinical Terms
sob
cp
nvd
heme
melena
hematuria
dysuria
oliguria
anuria
polyuria
""",

    "medical_coding": """# Medical Coding Examples

## ICD-10 Codes
icd_10
icd_10_cm
icd_10_pcs
diagnosis_codes
procedure_codes
morbidity_codes
mortality_codes
clinical_modification
procedure_coding_system

## CPT Codes
cpt
current_procedural_terminology
procedure_codes
surgical_codes
medical_procedures
evaluation_management
radiology_procedures
pathology_procedures
medicine_services

## HCPCS Codes
hcpcs
healthcare_common_procedure_coding_system
dme_codes
supplies_codes
medicare_codes
medicaid_codes
j_codes
k_codes
l_codes

## DRG Codes
drg
diagnosis_related_groups
ms_drg
apr_drg
severity_levels
case_mix_groups
hospital_payment
inpatient_reimbursement
length_of_stay

## SNOMED CT
snomed_ct
clinical_terminology
concept_codes
descriptions
relationships
reference_sets
clinical_findings
procedures
organisms

## LOINC Codes
loinc
logical_observation_identifiers
laboratory_codes
clinical_measurements
vital_signs
laboratory_tests
clinical_observations
test_results
reference_ranges

## Other Coding Systems
ndc
national_drug_codes
rxnorm
drug_terminology
cpt_modifiers
icd_9_cm
icd_9_pcs
hcpcs_level_2
revenue_codes
""",

    "medical_condition": """# Medical Condition Examples

## Common Chronic Conditions
hypertension
diabetes_mellitus
hyperlipidemia
asthma
copd
coronary_artery_disease
heart_failure
arthritis
osteoporosis
depression

## Acute Conditions
pneumonia
urinary_tract_infection
cellulitis
gastroenteritis
appendicitis
cholecystitis
pancreatitis
myocardial_infarction
stroke
pulmonary_embolism

## Neurological Conditions
alzheimer_disease
parkinson_disease
multiple_sclerosis
epilepsy
migraine
neuropathy
myasthenia_gravis
als
huntington_disease
cerebral_palsy

## Endocrine Conditions
hypothyroidism
hyperthyroidism
addison_disease
cushing_syndrome
diabetes_insipidus
parathyroid_disorder
pituitary_disorder
adrenal_insufficiency
metabolic_syndrome
polycystic_ovary_syndrome

## Gastrointestinal Conditions
gastroesophageal_reflux
irritable_bowel_syndrome
inflammatory_bowel_disease
crohn_disease
ulcerative_colitis
celiac_disease
liver_cirrhosis
hepatitis
pancreatitis
gallbladder_disease

## Respiratory Conditions
asthma
copd
pulmonary_fibrosis
sleep_apnea
bronchitis
pneumothorax
pleural_effusion
pulmonary_hypertension
cystic_fibrosis
sarcoidosis

## Autoimmune Conditions
lupus
rheumatoid_arthritis
psoriatic_arthritis
ankylosing_spondylitis
scleroderma
sjogren_syndrome
vasculitis
multiple_sclerosis
type_1_diabetes
graves_disease
""",

    "medical_device": """# Medical Device Examples

## Cardiovascular Devices
pacemaker
defibrillator
icd
cardiac_monitor
ecg_machine
holter_monitor
event_monitor
blood_pressure_monitor
heart_valve
stent

## Diagnostic Devices
xray_machine
ct_scanner
mri_machine
ultrasound_machine
pet_scanner
spect_scanner
mammography_machine
bone_density_scanner
fluoroscopy_machine
angiography_machine

## Surgical Instruments
scalpel
forceps
scissors
retractors
clamps
needles
sutures
electrosurgical_unit
laser_system
endoscope

## Monitoring Devices
pulse_oximeter
blood_glucose_monitor
thermometer
blood_pressure_cuff
heart_rate_monitor
respiratory_monitor
temperature_monitor
pressure_monitor
flow_meter
oxygen_monitor

## Orthopedic Devices
artificial_joint
prosthesis
implant
plate
screw
rod
external_fixator
internal_fixator
spinal_fusion_device
joint_replacement

## Respiratory Devices
ventilator
oxygen_tank
nebulizer
inhaler
cpap_machine
bipap_machine
oxygen_mask
tracheostomy_tube
chest_tube
suction_device

## Laboratory Equipment
centrifuge
microscope
spectrophotometer
incubator
autoclave
pipette
blood_analyzer
urine_analyzer
cell_counter
dna_sequencer

## Drug Delivery Devices
infusion_pump
syringe_pump
iv_pump
insulin_pump
pain_pump
chemotherapy_pump
antibiotic_pump
nutrition_pump
blood_product_pump
medication_dispenser
""",

    "medication_class": """# Medication Class Examples

## Common Drug Classes
beta_blockers
ace_inhibitors
statins
nsaids
opioids
antibiotics
antidepressants
antihypertensives
antidiabetics
anticoagulants

## Cardiovascular Medications
beta_blockers
ace_inhibitors
arb
calcium_channel_blockers
diuretics
statins
antiplatelets
anticoagulants
antiarrhythmics
vasodilators

## Antibiotics
penicillins
cephalosporins
macrolides
fluoroquinolones
tetracyclines
sulfonamides
aminoglycosides
carbapenems
monobactams
glycopeptides

## Pain Medications
opioids
nsaids
acetaminophen
muscle_relaxants
anticonvulsants
antidepressants
corticosteroids
local_anesthetics
topical_analgesics
nerve_blocks

## Psychiatric Medications
ssri
snri
tricyclic_antidepressants
maoi
atypical_antipsychotics
typical_antipsychotics
benzodiazepines
mood_stabilizers
stimulants
anxiolytics

## Diabetes Medications
metformin
sulfonylureas
dpp_4_inhibitors
sglt2_inhibitors
glp_1_agonists
insulin
thiazolidinediones
alpha_glucosidase_inhibitors
amylin_analogues
bile_acid_sequestrants

## Respiratory Medications
bronchodilators
inhaled_corticosteroids
leukotriene_modifiers
mast_cell_stabilizers
antihistamines
decongestants
expectorants
mucolytics
cough_suppressants
anticholinergics
"""
}

def create_assets_file(module_key, examples_content):
    """Create example_inputs.txt file for a module."""
    recognizers_dir = Path(__file__).parent
    assets_dir = recognizers_dir / module_key / "assets"
    
    # Create assets directory if it doesn't exist
    assets_dir.mkdir(exist_ok=True)
    
    # Create example_inputs.txt file
    assets_file = assets_dir / "example_inputs.txt"
    
    with open(assets_file, 'w') as f:
        f.write(examples_content)
    
    return assets_file

def main():
    """Create assets files for modules that are missing them."""
    print("Creating example_inputs.txt files for modules that are missing them...")
    
    created_files = []
    
    for module_key, examples_content in MODULE_EXAMPLES.items():
        assets_file = Path(__file__).parent / module_key / "assets" / "example_inputs.txt"
        
        if not assets_file.exists():
            print(f"Creating {module_key}/assets/example_inputs.txt...")
            
            created_file = create_assets_file(module_key, examples_content)
            created_files.append(created_file)
            print(f"✓ Created {created_file}")
        else:
            print(f"- {module_key}/assets/example_inputs.txt already exists")
    
    print(f"\n✅ Created {len(created_files)} assets files")
    print("\nAll modules now have example_inputs.txt files with:")
    print("- Domain-specific medical terminology")
    print("- Relevant examples for each medical specialty")
    print("- Comprehensive coverage of common terms")
    print("- Proper categorization and organization")

if __name__ == "__main__":
    main()
