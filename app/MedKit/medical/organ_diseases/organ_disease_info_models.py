"""
organ_disease_info_models.py - Pydantic Models for Organ-specific Disease Information
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class RiskFactorsModel(BaseModel):
    modifiable: List[str] = Field(description="Risk factors that can be changed.")
    non_modifiable: List[str] = Field(
        description="Risk factors that cannot be changed."
    )
    environmental: List[str] = Field(
        description="Environmental or occupational risk factors."
    )


class DiagnosticCriteriaModel(BaseModel):
    symptoms: List[str] = Field(description="Key symptoms and clinical signs.")
    physical_exam: List[str] = Field(description="Physical examination findings.")
    laboratory_tests: List[str] = Field(description="Recommended laboratory tests.")
    imaging_studies: List[str] = Field(description="Recommended imaging studies.")


class DiseaseIdentityModel(BaseModel):
    name: str = Field(description="The common name of the disease.")
    icd_10_code: Optional[str] = Field(description="ICD-10 code for the disease.")
    synonyms: List[str] = Field(description="Alternative names or synonyms.")


class DiseaseBackgroundModel(BaseModel):
    definition: str = Field(description="A concise definition.")
    pathophysiology: str = Field(description="The underlying physiological process.")
    etiology: str = Field(description="The cause or origin.")


class DiseaseEpidemiologyModel(BaseModel):
    prevalence: str = Field(description="The proportion found to have the disease.")
    incidence: str = Field(description="The number of new cases.")
    risk_factors: RiskFactorsModel = Field(
        description="Factors that increase the risk."
    )


class DiseaseClinicalPresentationModel(BaseModel):
    symptoms: List[str] = Field(description="Common symptoms.")
    signs: List[str] = Field(description="Objective medical signs.")
    natural_history: str = Field(description="The progression without treatment.")


class DiseaseDiagnosisModel(BaseModel):
    diagnostic_criteria: DiagnosticCriteriaModel = Field(
        description="Criteria used for diagnosis."
    )
    differential_diagnosis: List[str] = Field(
        description="Other diseases with similar presentations."
    )


class DiseaseManagementModel(BaseModel):
    treatment_options: List[str] = Field(description="Available treatment options.")
    prevention: List[str] = Field(description="Strategies for prevention.")
    prognosis: str = Field(description="The likely course and outcome.")


class DiseaseResearchModel(BaseModel):
    current_research: str = Field(description="Overview of current research areas.")
    recent_advancements: str = Field(description="Recent breakthroughs.")


class DiseaseSpecialPopulationsModel(BaseModel):
    pediatric: str = Field(description="Considerations for children.")
    geriatric: str = Field(description="Considerations for older adults.")
    pregnancy: str = Field(description="Considerations during pregnancy.")


class DiseaseLivingWithModel(BaseModel):
    quality_of_life: str = Field(description="Impact on quality of life.")
    support_resources: List[str] = Field(description="Support groups and resources.")


class DiseaseInfoModel(BaseModel):
    identity: DiseaseIdentityModel
    background: DiseaseBackgroundModel
    epidemiology: DiseaseEpidemiologyModel
    clinical_presentation: DiseaseClinicalPresentationModel
    diagnosis: DiseaseDiagnosisModel
    management: DiseaseManagementModel
    research: DiseaseResearchModel
    special_populations: DiseaseSpecialPopulationsModel
    living_with: DiseaseLivingWithModel


class OrganDiseasesModel(BaseModel):
    organ: str = Field(description="The name of the organ.")
    common_diseases: List[str] = Field(description="Common diseases associated.")
    rare_diseases: List[str] = Field(description="Rare diseases associated.")
    educational_points: List[str] = Field(description="Key educational points.")


class ModelOutput(BaseModel):
    data: Optional[OrganDiseasesModel] = None
    markdown: Optional[str] = None
