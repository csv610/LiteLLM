"""
disease_info_models.py - Pydantic Models for Disease Information

This module contains all Pydantic data models for organizing and validating
disease information across multiple dimensions.
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class RiskFactors(BaseModel):
    """
    Risk factors associated with developing a disease.
    """
    modifiable: List[str] = Field(description="Risk factors that can be changed (e.g., smoking, diet, exercise).")
    non_modifiable: List[str] = Field(description="Risk factors that cannot be changed (e.g., age, genetics, family history).")
    environmental: List[str] = Field(description="Environmental or occupational risk factors.")


class DiagnosticCriteria(BaseModel):
    """
    Diagnostic criteria for a disease.
    """
    symptoms: List[str] = Field(description="Key symptoms and clinical signs.")
    physical_exam: List[str] = Field(description="Physical examination findings.")
    laboratory_tests: List[str] = Field(description="Recommended laboratory tests (e.g., blood tests, urine tests).")
    imaging_studies: List[str] = Field(description="Recommended imaging studies (e.g., X-ray, CT scan, MRI).")


class DiseaseIdentity(BaseModel):
    """
    Basic identifying information about a disease.
    """
    name: str = Field(description="The common name of the disease.")
    icd_10_code: Optional[str] = Field(description="ICD-10 code for the disease.")
    synonyms: List[str] = Field(description="Alternative names or synonyms for the disease.")


class DiseaseBackground(BaseModel):
    """
    Background information on the disease, including definition and pathophysiology.
    """
    definition: str = Field(description="A concise definition of the disease.")
    pathophysiology: str = Field(description="The underlying physiological process of the disease.")
    etiology: str = Field(description="The cause or origin of the disease.")


class DiseaseEpidemiology(BaseModel):
    """
    Epidemiological information about the disease.
    """
    prevalence: str = Field(description="The proportion of a population found to have the disease.")
    incidence: str = Field(description="The number of new cases of the disease during a certain period.")
    risk_factors: RiskFactors = Field(description="Factors that increase the risk of developing the disease.")


class DiseaseClinicalPresentation(BaseModel):
    """
    How the disease presents in a clinical setting.
    """
    symptoms: List[str] = Field(description="Common symptoms experienced by patients.")
    signs: List[str] = Field(description="Objective medical signs observed by a clinician.")
    natural_history: str = Field(description="The progression of the disease without treatment.")


class DiseaseDiagnosis(BaseModel):
    """
    How the disease is diagnosed.
    """
    diagnostic_criteria: DiagnosticCriteria = Field(description="Criteria used to establish a diagnosis.")
    differential_diagnosis: List[str] = Field(description="Other diseases with similar presentations.")


class DiseaseManagement(BaseModel):
    """
    How the disease is managed and treated.
    """
    treatment_options: List[str] = Field(description="Available treatment options (e.g., medications, therapies).")
    prevention: List[str] = Field(description="Strategies for preventing the disease.")
    prognosis: str = Field(description="The likely course and outcome of the disease.")


class DiseaseResearch(BaseModel):
    """
    Current research and advancements related to the disease.
    """
    current_research: str = Field(description="Overview of current research areas.")
    recent_advancements: str = Field(description="Recent breakthroughs in diagnosis or treatment.")


class DiseaseSpecialPopulations(BaseModel):
    """
    Considerations for special patient populations.
    """
    pediatric: str = Field(description="Considerations for children.")
    geriatric: str = Field(description="Considerations for older adults.")
    pregnancy: str = Field(description="Considerations during pregnancy and lactation.")


class DiseaseLivingWith(BaseModel):
    """
    Information for patients living with the disease.
    """
    quality_of_life: str = Field(description="Impact on quality of life and daily activities.")
    support_resources: List[str] = Field(description="Patient support groups and resources.")


class DiseaseInfo(BaseModel):
    """
    Comprehensive, evidence-based information about a specific disease.
    """
    identity: DiseaseIdentity = Field(description="Basic identifying information.")
    background: DiseaseBackground = Field(description="Background and pathophysiology.")
    epidemiology: DiseaseEpidemiology = Field(description="Epidemiological data.")
    clinical_presentation: DiseaseClinicalPresentation = Field(description="Clinical presentation.")
    diagnosis: DiseaseDiagnosis = Field(description="Diagnostic criteria and methods.")
    management: DiseaseManagement = Field(description="Treatment and management strategies.")
    research: DiseaseResearch = Field(description="Current research and advancements.")
    special_populations: DiseaseSpecialPopulations = Field(description="Considerations for special populations.")
    living_with: DiseaseLivingWith = Field(description="Information for patients.")
