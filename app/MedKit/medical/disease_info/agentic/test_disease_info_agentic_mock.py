import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.disease_info.agentic.disease_info import DiseaseInfoGenerator
from medical.disease_info.agentic.disease_info_models import (
    DiagnosticCriteriaModel,
    DiseaseBackgroundModel,
    DiseaseClinicalPresentationModel,
    DiseaseDiagnosisModel,
    DiseaseEpidemiologyModel,
    DiseaseIdentityModel,
    DiseaseInfoModel,
    DiseaseLivingWithModel,
    DiseaseManagementModel,
    DiseaseResearchModel,
    DiseaseSpecialPopulationsModel,
    ModelOutput,
    RiskFactorsModel,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.disease_info.agentic.disease_info.LiteClient") as mock:
        yield mock


def test_disease_info_generator_init():
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    assert generator.model_config == config
    assert generator.client is not None


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)
    mock_output = ModelOutput(
        markdown="Disease information in markdown", data_available=True
    )
    mock_lite_client.return_value.generate_text.return_value = mock_output
    result = generator.generate_text("Diabetes")
    assert result.markdown == "Disease information in markdown"


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = DiseaseInfoGenerator(config)

    mock_data = DiseaseInfoModel(
        identity=DiseaseIdentityModel(
            name="Diabetes",
            disease_name="Diabetes",
            icd_10_code="E11",
            icd10_code="E11",
            icd11_code="5A11",
            synonyms=[],
        ),
        background=DiseaseBackgroundModel(
            definition="Chronic", pathophysiology="Insulin", etiology="Multiple factors"
        ),
        epidemiology=DiseaseEpidemiologyModel(
            prevalence="High",
            incidence="Rising",
            risk_factors=RiskFactorsModel(
                lifestyle=[],
                genetic=[],
                environmental=[],
                modifiable=[],
                non_modifiable=[],
            ),
        ),
        clinical_presentation=DiseaseClinicalPresentationModel(
            symptoms=[], complications=[], signs=[], natural_history="Progressive"
        ),
        diagnosis=DiseaseDiagnosisModel(
            criteria=[],
            tests=[],
            diagnostic_criteria=DiagnosticCriteriaModel(
                primary=[],
                secondary=[],
                exclusion=[],
                symptoms=[],
                physical_exam=[],
                laboratory_tests=[],
                imaging_studies=[],
            ),
            differential_diagnosis=[],
        ),
        management=DiseaseManagementModel(
            treatments=[],
            medications=[],
            lifestyle=[],
            treatment_options=[],
            prevention=[],
            prognosis="Variable",
        ),
        research=DiseaseResearchModel(
            current_research="None",
            recent_advancements="None",
            future_outlooks=[],
            current_trends=[],
        ),
        special_populations=DiseaseSpecialPopulationsModel(
            pediatric="None", geriatric="None", pregnancy="None"
        ),
        living_with=DiseaseLivingWithModel(
            quality_of_life="None", support_resources=[]
        ),
        summary="A chronic disease",
    )
    mock_output = ModelOutput(data=mock_data, data_available=True)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Diabetes", structured=True)
    assert result.data.identity.name == "Diabetes"
