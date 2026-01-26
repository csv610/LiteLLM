"""Pydantic models for medical topic information structure.

Defines all the data models used for representing comprehensive medical topic
documentation including epidemiology, pathophysiology, clinical presentation,
diagnosis, treatment, and prognosis information.
"""

from pydantic import BaseModel, Field
from typing import Optional

#from medkit.medical.medical_faq import PatientFAQ


class TopicOverviewModel(BaseModel):
    """Basic information about the medical topic."""
    topic_name: str = Field(description="Official name of the medical topic")
    alternative_names: str = Field(description="Other names or abbreviations for this topic, comma-separated")
    topic_category: str = Field(description="Category (disease, condition, syndrome, disorder, etc)")
    medical_specialties: str = Field(description="Primary medical specialties that focus on this topic, comma-separated")
    prevalence: str = Field(description="How common this condition is in the population")


class DefinitionModel(BaseModel):
    """Definition and basic understanding of the topic."""
    plain_language_explanation: str = Field(description="Simple explanation for general audience")
    medical_definition: str = Field(description="Formal medical definition")
    key_characteristics: str = Field(description="Main defining characteristics, comma-separated")
    disease_classification: str = Field(description="How this condition is classified medically")


class EpidemiologyModel(BaseModel):
    """Statistical and demographic information."""
    incidence_rate: str = Field(description="How many new cases occur per year")
    prevalence_rate: str = Field(description="What percentage of population has this condition")
    age_of_onset: str = Field(description="Typical age when condition appears")
    gender_differences: str = Field(description="Whether males or females are more affected")
    geographic_variation: str = Field(description="Whether condition varies by geography or population")
    risk_groups: str = Field(description="Populations at highest risk, comma-separated")


class EtiologyModel(BaseModel):
    """Causes and risk factors."""
    primary_causes: str = Field(description="Main causes of this condition, comma-separated")
    genetic_factors: str = Field(description="Genetic predisposition or inheritance patterns")
    environmental_factors: str = Field(description="Environmental triggers or exposures, comma-separated")
    lifestyle_factors: str = Field(description="Lifestyle factors that increase risk, comma-separated")
    infectious_agents: str = Field(description="If applicable, organisms that cause this condition")
    contributing_factors: str = Field(description="Other factors that contribute to development, comma-separated")


class PathophysiologyModel(BaseModel):
    """How the condition develops and progresses."""
    mechanism_of_disease: str = Field(description="Biological mechanism of how disease develops")
    affected_systems: str = Field(description="Body systems or organs affected, comma-separated")
    cellular_changes: str = Field(description="Changes at cellular or molecular level")
    progression_stages: str = Field(description="How condition progresses over time, comma-separated")
    inflammatory_response: str = Field(description="Role of inflammation if applicable")
    immune_involvement: str = Field(description="Role of immune system if applicable")


class ClinicalPresentationModel(BaseModel):
    """Symptoms and clinical signs."""
    primary_symptoms: str = Field(description="Main symptoms patients experience, comma-separated")
    secondary_symptoms: str = Field(description="Associated or secondary symptoms, comma-separated")
    symptom_onset: str = Field(description="How symptoms typically begin and develop")
    severity_spectrum: str = Field(description="Range from mild to severe presentations")
    acute_vs_chronic: str = Field(description="Whether condition is acute, chronic, or can be both")
    symptom_triggers: str = Field(description="What triggers or worsens symptoms, comma-separated")
    asymptomatic_presentation: str = Field(description="Whether condition can exist without symptoms")


class DiagnosisModel(BaseModel):
    """Diagnostic methods and criteria."""
    diagnostic_tests: str = Field(description="Tests used to diagnose this condition, comma-separated")
    imaging_studies: str = Field(description="Imaging procedures if applicable, comma-separated")
    laboratory_findings: str = Field(description="Lab results indicative of condition")
    diagnostic_criteria: str = Field(description="Clinical criteria used to confirm diagnosis")
    differential_diagnosis: str = Field(description="Similar conditions to rule out, comma-separated")
    diagnostic_challenges: str = Field(description="Difficulties in diagnosis and why")
    time_to_diagnosis: str = Field(description="Average time from symptom onset to diagnosis")


class ComplicationsModel(BaseModel):
    """Potential complications and sequelae."""
    acute_complications: str = Field(description="Short-term complications, comma-separated")
    chronic_complications: str = Field(description="Long-term complications from untreated disease, comma-separated")
    complication_rates: str = Field(description="How often complications occur")
    organ_system_effects: str = Field(description="Which organ systems can be affected, comma-separated")
    mortality_rate: Optional[str] = Field(description="Risk of death if applicable")
    disability_outcomes: str = Field(description="Potential long-term disability or functional impairment")


class TreatmentModel(BaseModel):
    """Treatment options and management."""
    first_line_treatment: str = Field(description="Standard initial treatment")
    medications: str = Field(description="Common medications used, comma-separated")
    surgical_interventions: str = Field(description="Surgical options if applicable, comma-separated")
    physical_therapy: str = Field(description="Role of physical therapy or rehabilitation")
    lifestyle_modifications: str = Field(description="Lifestyle changes recommended, comma-separated")
    dietary_management: str = Field(description="Dietary modifications if applicable")
    complementary_approaches: str = Field(description="Alternative or complementary therapies, comma-separated")
    treatment_duration: str = Field(description="How long treatment typically lasts")


class PrognosisModel(BaseModel):
    """Expected outcomes and long-term outlook."""
    overall_prognosis: str = Field(description="General expected outcome")
    remission_possibility: str = Field(description="Whether condition can go into remission or resolve")
    cure_potential: str = Field(description="Whether condition is curable")
    recovery_rates: str = Field(description="Percentage of people who recover or improve")
    factors_affecting_prognosis: str = Field(description="What factors influence outcomes, comma-separated")
    long_term_outlook: str = Field(description="What to expect over years or decades")
    quality_of_life_impact: str = Field(description="Expected impact on daily functioning and quality of life")


class PreventionModel(BaseModel):
    """Prevention and risk reduction strategies."""
    primary_prevention: str = Field(description="Strategies to prevent disease onset, comma-separated")
    secondary_prevention: str = Field(description="Early detection and intervention strategies, comma-separated")
    screening_recommendations: str = Field(description="Who should be screened and how often")
    protective_factors: str = Field(description="Factors that reduce risk, comma-separated")
    lifestyle_prevention: str = Field(description="Lifestyle choices that prevent condition, comma-separated")
    vaccinations: str = Field(description="Vaccines if applicable")


class ResearchAndEvidenceModel(BaseModel):
    """Current evidence and research."""
    evidence_quality: str = Field(description="Quality of current evidence")
    current_research_areas: str = Field(description="Active areas of research, comma-separated")
    emerging_treatments: str = Field(description="Promising new treatments in development")
    clinical_trials: str = Field(description="Availability and types of clinical trials")
    guideline_sources: str = Field(description="Major clinical guidelines and organizations, comma-separated")


class PsychosocialImpactModel(BaseModel):
    """Mental health and quality of life aspects."""
    mental_health_effects: str = Field(description="Psychological effects like depression or anxiety")
    emotional_burden: str = Field(description="Emotional challenges patients face")
    social_impact: str = Field(description="Impact on relationships and social functioning")
    occupational_impact: str = Field(description="Effect on work and employment")
    coping_strategies: str = Field(description="Strategies to manage psychological impact, comma-separated")
    support_resources: str = Field(description="Mental health and support resources, comma-separated")


class TopicEducationModel(BaseModel):
    """Patient education and communication."""
    key_takeaways: str = Field(description="3-5 most important points, comma-separated")
    common_misconceptions: str = Field(description="Common myths about this condition, comma-separated")
    frequently_asked_questions: str = Field(description="Common patient questions and answers")
    when_to_see_doctor: str = Field(description="Symptoms or situations requiring medical attention")


class SpecialPopulationsModel(BaseModel):
    """Considerations for specific groups."""
    pediatric_considerations: str = Field(description="Special aspects in children if applicable")
    geriatric_considerations: str = Field(description="Special aspects in elderly if applicable")
    pregnancy_considerations: str = Field(description="Implications for pregnant women if applicable")
    gender_specific_aspects: str = Field(description="Differences between genders if applicable")
    ethnic_variations: str = Field(description="Variations across ethnic or genetic groups")


class CostAndImpactModel(BaseModel):
    """Economic and healthcare impact."""
    healthcare_costs: str = Field(description="Typical treatment and management costs")
    productivity_loss: str = Field(description="Economic impact from lost productivity")
    burden_on_healthcare_system: str = Field(description="Healthcare resource utilization")
    insurance_considerations: str = Field(description="Insurance coverage and costs")


class SeeAlsoModel(BaseModel):
    """Cross-references to related medical topics."""
    related_topics: str = Field(description="Related medical topics worth exploring, comma-separated")
    connection_types: str = Field(description="Types of connections (similar condition, related treatment, complication, risk factor, prevention, differential diagnosis, etc.), comma-separated")
    reason: str = Field(description="Brief explanation of how these topics relate to the main topic")


class TopicMetadataModel(BaseModel):
    """Metadata and information structure."""
    last_updated: str = Field(description="When this information was last reviewed")
    information_sources: str = Field(description="Primary sources of information, comma-separated")
    confidence_level: str = Field(description="Confidence in provided information (high, medium, low)")
    complexity_level: str = Field(description="Complexity of topic (basic, intermediate, advanced)")


class MedicalTopicModel(BaseModel):
    """
    Comprehensive medical topic information.
    """
    # Basic identification
    overview: TopicOverviewModel

    # Understanding the topic
    definition: DefinitionModel
    epidemiology: EpidemiologyModel

    # Causes and mechanisms
    etiology: EtiologyModel
    pathophysiology: PathophysiologyModel

    # Clinical aspects
    clinical_presentation: ClinicalPresentationModel
    diagnosis: DiagnosisModel
    complications: ComplicationsModel

    # Management and outcomes
    treatment: TreatmentModel
    prognosis: PrognosisModel
    prevention: PreventionModel

    # Evidence and research
    research_and_evidence: ResearchAndEvidenceModel

    # Human impact
    psychosocial_impact: PsychosocialImpactModel
    special_populations: SpecialPopulationsModel
    cost_and_impact: CostAndImpactModel

    # Patient communication
    education: TopicEducationModel
#    faq: Optional[PatientFAQ] = Field(default=None, description="Patient-friendly FAQ for this topic")

    # Cross-references
    see_also: SeeAlsoModel

    # Metadata
    metadata: TopicMetadataModel


class ModelOutput(BaseModel):
    data: Optional[MedicalTopicModel] = None
    markdown: Optional[str] = None
