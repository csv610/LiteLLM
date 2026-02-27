import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from unittest.mock import patch
from medical.organ_diseases.organ_disease_info import DiseaseInfoGenerator
from lite.config import ModelConfig
from medical.organ_diseases.organ_disease_info_models import (
    OrganDiseasesModel, ModelOutput, DiseaseIdentityModel, 
    DiseaseBackgroundModel, DiseaseEpidemiologyModel, 
    DiseaseClinicalPresentationModel, DiseaseDiagnosisModel, 
    DiseaseManagementModel, DiseaseResearchModel, 
    DiseaseSpecialPopulationsModel, DiseaseLivingWithModel, 
    RiskFactorsModel, DiagnosticCriteriaModel
)

@pytest.fixture
def mock_lite_client():
    with patch('medical.organ_diseases.organ_disease_info.LiteClient') as mock:
        yield mock

def test_disease_info_generator_init():
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    assert generator.model_config == config

def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    mock_output = ModelOutput(markdown="Organ disease info", data_available=True)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    result = generator.generate_text("Heart", "Heart attack")
    assert result.markdown == "Organ disease info"

def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    
    mock_inner = DiseaseIdentityModel(name="Heart attack", disease_name="Heart attack", icd_10_code="I21", icd10_code="I21", icd11_code="BA41", synonyms=[])
    
    mock_data = OrganDiseasesModel(
        organ="Heart",
        disease="Heart attack",
        identity=mock_inner,
        background=DiseaseBackgroundModel(definition="Ischemia", pathophysiology="Blocked artery", etiology="Plaque"),
        epidemiology=DiseaseEpidemiologyModel(prevalence="High", incidence="Rising", risk_factors=RiskFactorsModel(lifestyle=[], genetic=[], environmental=[], modifiable=[], non_modifiable=[])),
        clinical_presentation=DiseaseClinicalPresentationModel(symptoms=["Pain"], complications=[], signs=[], natural_history="Acute"),
        diagnosis=DiseaseDiagnosisModel(criteria=[], tests=[], diagnostic_criteria=DiagnosticCriteriaModel(primary=[], secondary=[], exclusion=[], symptoms=[], physical_exam=[], laboratory_tests=[], imaging_studies=[]), differential_diagnosis=[]),
        management=DiseaseManagementModel(treatments=[], medications=[], lifestyle=[], treatment_options=[], prevention=[], prognosis="Variable"),
        research=DiseaseResearchModel(current_research="None", recent_advancements="None", future_outlooks=[], current_trends=[]),
        special_populations=DiseaseSpecialPopulationsModel(pediatric="None", geriatric="None", pregnancy="None"),
        living_with=DiseaseLivingWithModel(dietary_guidelines=[], physical_activity=[], support_resources=[]),
        summary="Heart info"
    )
    mock_output = ModelOutput(data=mock_data, data_available=True)
    mock_lite_client.return_value.generate_text.return_value = mock_output
    result = generator.generate_text("Heart", "Heart attack", structured=True)
    assert result.data.identification.organ == "Heart"
