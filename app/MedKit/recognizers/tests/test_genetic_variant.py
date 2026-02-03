import pytest
from unittest.mock import MagicMock, patch
from genetic_variant.recognizer import GeneticVariantIdentifier
from genetic_variant.models import ModelOutput, GeneticVariantIdentifierModel, GeneticVariantIdentificationModel
from lite.config import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def identifier(mock_model_config):
    with patch('genetic_variant.recognizer.LiteClient'):
        return GeneticVariantIdentifier(mock_model_config)

def test_identify(identifier):
    mock_data = GeneticVariantIdentifierModel(
        identification=GeneticVariantIdentificationModel(
            variant_name="BRCA1",
            is_well_known=True,
            inheritance_pattern='Autosomal dominant', clinical_implications='Increased cancer risk'
        ),
        summary="Summary",
        data_available=True
    )
    mock_output = ModelOutput(data=mock_data)
    identifier.client.generate_text.return_value = mock_output
    result = identifier.identify("BRCA1")
    assert getattr(result.data.identification, 'variant_name') == "BRCA1"
