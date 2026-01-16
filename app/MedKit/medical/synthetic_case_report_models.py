"""Pydantic models for synthetic medical case reports following CARE Guidelines.

This module defines the structured data models used for generating comprehensive
synthetic medical case reports with schema-aware prompting.
"""

from pydantic import BaseModel, Field


class PatientInformation(BaseModel):
    age: int = Field(description="Patient age in years")
    gender: str = Field(description="Patient gender (Male/Female/Other)")
    ethnicity: str = Field(description="Patient ethnicity or ancestry")
    occupation: str = Field(description="Patient's occupation or profession")
    relevant_family_history: str = Field(description="Family history relevant to the condition")
    past_medical_history: str = Field(description="Previous medical conditions, comma-separated")
    surgical_history: str = Field(description="Previous surgical procedures, comma-separated")
    medication_history: str = Field(description="Current and recent medications, comma-separated")
    allergy_history: str = Field(description="Known allergies or adverse reactions, comma-separated")
    social_history: str = Field(description="Smoking, alcohol, substance use, living situation")


class ClinicalFindings(BaseModel):
    chief_complaint: str = Field(description="Primary reason for presentation")
    history_of_present_illness: str = Field(description="Detailed chronological description of current illness")
    symptom_onset: str = Field(description="When symptoms started and initial presentation")
    symptom_progression: str = Field(description="How symptoms have changed over time")
    associated_symptoms: str = Field(description="Related symptoms experienced, comma-separated")
    alleviating_factors: str = Field(description="What makes symptoms better, comma-separated")
    aggravating_factors: str = Field(description="What makes symptoms worse, comma-separated")
    impact_on_activities: str = Field(description="Effect on daily activities and quality of life")
    physical_exam_findings: str = Field(description="Physical examination results with vital signs")
    abnormal_findings: str = Field(description="Specific abnormal clinical findings, comma-separated")


class Timeline(BaseModel):
    initial_presentation_date: str = Field(description="Date of first symptom or presentation (format: Month/Year or descriptive)")
    key_clinical_events: str = Field(description="Major events in chronological order with dates")
    diagnostic_workup_timeline: str = Field(description="Sequence of diagnostic tests and dates performed")
    treatment_initiation_date: str = Field(description="When treatment began")
    significant_changes: str = Field(description="Important changes in clinical status over time")
    duration_of_illness: str = Field(description="Total time from onset to current status")


class DiagnosticAssessment(BaseModel):
    laboratory_tests_performed: str = Field(description="Blood tests, CSF analysis, biopsies, etc. with results")
    laboratory_values: str = Field(description="Specific abnormal lab values with reference ranges")
    imaging_studies: str = Field(description="CT, MRI, X-ray, ultrasound, or other imaging with findings")
    imaging_findings: str = Field(description="Specific abnormal imaging findings with measurements")
    pathology_results: str = Field(description="Tissue diagnosis or pathological findings if applicable")
    specialized_testing: str = Field(description="EKG, EEG, genetic testing, immunology panels, etc.")
    diagnostic_criteria_assessment: str = Field(description="Clinical criteria findings without naming the diagnosis")
    diagnostic_challenges: str = Field(description="Difficulties encountered in reaching diagnosis")
    noteworthy_findings_pattern: str = Field(description="Overall pattern of findings without disclosing diagnosis")


class TherapeuticInterventions(BaseModel):
    initial_management: str = Field(description="First-line treatment approach and rationale")
    medications_prescribed: str = Field(description="Medications given with dosage, frequency, and dates")
    dosage_adjustments: str = Field(description="Changes in medication doses over time")
    surgical_interventions: str = Field(description="Any surgical procedures performed with dates and outcomes")
    procedural_interventions: str = Field(description="Non-surgical procedures (catheterization, biopsy, etc)")
    supportive_care: str = Field(description="Supportive measures, monitoring, and nursing care")
    lifestyle_modifications: str = Field(description="Recommended dietary, activity, or behavioral changes")
    rehabilitation_therapy: str = Field(description="Physical, occupational, or speech therapy if applicable")
    adverse_events: str = Field(description="Medication side effects or treatment complications, comma-separated")
    treatment_response: str = Field(description="How patient responded to treatment over time")


class FollowUpAndOutcomes(BaseModel):
    clinical_response_to_treatment: str = Field(description="How symptoms improved or changed with treatment")
    symptom_resolution: str = Field(description="Whether symptoms resolved, improved, or persisted")
    functional_status: str = Field(description="Ability to perform daily activities and return to work/life")
    final_clinical_status: str = Field(description="Current health status and disease state")
    complications_during_course: str = Field(description="Any complications that developed, comma-separated")
    length_of_hospital_stay: str = Field(description="If hospitalized, duration and reason for discharge")
    duration_of_followup: str = Field(description="How long patient was followed up after initial treatment")
    discharge_medications: str = Field(description="Medications at discharge or end of acute treatment")
    followup_schedule: str = Field(description="Planned follow-up appointments and monitoring")
    current_status: str = Field(description="Most recent assessment and current clinical condition")


class Discussion(BaseModel):
    case_significance: str = Field(description="Why this case is clinically important or unusual without naming diagnosis")
    findings_interpretation: str = Field(description="Analysis of clinical findings and their significance")
    diagnostic_approach_discussion: str = Field(description="Analysis of diagnostic strategy and reasoning process")
    treatment_rationale: str = Field(description="Why specific treatments were chosen and their evidence base")
    treatment_effectiveness: str = Field(description="Assessment of treatment response without assuming diagnosis")
    learning_points: str = Field(description="Key clinical lessons and takeaways from this case")
    pathophysiological_insights: str = Field(description="Biological mechanisms highlighted by findings")
    clinical_pearls: str = Field(description="Important clinical observations and patterns to recognize")
    implications_for_practice: str = Field(description="How this case may inform clinical practice and differential diagnosis")
    recommendations: str = Field(description="Recommendations for managing similar presentations")


class PatientPerspective(BaseModel):
    patient_experience: str = Field(description="How patient experienced the symptoms and treatment")
    understanding_of_diagnosis: str = Field(description="Patient's comprehension of their diagnosis")
    treatment_satisfaction: str = Field(description="Patient's satisfaction with care received")
    quality_of_life_impact: str = Field(description="Impact on patient's quality of life and well-being")
    adherence_to_treatment: str = Field(description="How well patient followed treatment recommendations")
    psychosocial_factors: str = Field(description="Emotional, social, or psychological aspects affecting recovery")


class InformedConsent(BaseModel):
    consent_statement: str = Field(description="Statement indicating informed consent was obtained from patient")
    patient_anonymity: str = Field(description="Confirmation that patient identifiers have been removed or anonymized")
    institutional_approval: str = Field(description="IRB approval or institutional review status if applicable")
    ethical_considerations: str = Field(description="Any ethical issues or considerations in the case")


class CaseReportMetadata(BaseModel):
    case_report_title: str = Field(description="Descriptive title describing patient presentation or clinical presentation, without naming the diagnosis")
    keywords: str = Field(description="5-10 clinical keywords describing findings/presentations without diagnosis, comma-separated")
    medical_specialty: str = Field(description="Primary medical specialty relevant to this case")
    date_case_compiled: str = Field(description="Date when case report was compiled")
    case_authors: str = Field(description="Treating physician/medical team names (can be fictional)")
    institution: str = Field(description="Medical institution or hospital where case was managed")
    information_sources: str = Field(description="Sources of medical information used, comma-separated")
    confidence_level: str = Field(description="Confidence in the realism of case data (high, medium)")
    clinical_accuracy: str = Field(description="Note on clinical accuracy and evidence-based information")
    bias_mitigation_note: str = Field(description="Note confirming diagnosis/condition name has been withheld to prevent diagnostic bias")


class SyntheticCaseReport(BaseModel):
    metadata: CaseReportMetadata
    patient_information: PatientInformation
    clinical_findings: ClinicalFindings
    timeline: Timeline
    diagnostic_assessment: DiagnosticAssessment
    therapeutic_interventions: TherapeuticInterventions
    follow_up_and_outcomes: FollowUpAndOutcomes
    discussion: Discussion
    patient_perspective: PatientPerspective
    informed_consent: InformedConsent
