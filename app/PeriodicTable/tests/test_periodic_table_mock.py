import pytest
from unittest.mock import patch
from periodic_table_element import PeriodicTableElement
from periodic_table_models import ElementInfo, PhysicalCharacteristics, AtomicDimensions, ChemicalCharacteristics, ElementResponse
from lite import ModelConfig

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.2)

@pytest.fixture
def element_info_sample():
    return ElementInfo(
        atomic_number=1,
        symbol="H",
        name="Hydrogen",
        atomic_mass=1.008,
        period=1,
        group="1",
        block="s",
        category="nonmetal",
        electron_configuration="1s¹",
        physical_characteristics=PhysicalCharacteristics(standard_state="gas"),
        atomic_dimensions=AtomicDimensions(atomic_radius=37.0),
        chemical_characteristics=ChemicalCharacteristics(oxidation_states="+1, -1"),
        uses=["Fuel cells", "Rocket fuel"],
        properties=["Lightest element", "Highly flammable"]
    )

def test_element_info_validation(element_info_sample):
    """Test that ElementInfo model validates correctly."""
    assert element_info_sample.name == "Hydrogen"
    assert element_info_sample.atomic_number == 1

def test_periodic_table_element_init(mock_model_config):
    """Test initialization of PeriodicTableElement."""
    with patch('periodic_table_element.LiteClient') as MockClient:
        pte = PeriodicTableElement(mock_model_config)
        assert pte.model_config == mock_model_config
        MockClient.assert_called_once_with(model_config=mock_model_config)

def test_fetch_element_info_success(mock_model_config, element_info_sample):
    """Test successful fetching of element info."""
    with patch('periodic_table_element.LiteClient') as MockClient:
        mock_client_instance = MockClient.return_value
        mock_client_instance.generate_text.return_value = ElementResponse(element=element_info_sample)
        
        pte = PeriodicTableElement(mock_model_config)
        result = pte.fetch_element_info("Hydrogen")
        
        assert result.name == "Hydrogen"
        assert result.atomic_number == 1

def test_fetch_element_info_failure(mock_model_config):
    """Test failure in fetching element info."""
    with patch('periodic_table_element.LiteClient') as MockClient:
        mock_client_instance = MockClient.return_value
        mock_client_instance.generate_text.side_effect = Exception("API Error")
        
        pte = PeriodicTableElement(mock_model_config)
        result = pte.fetch_element_info("Hydrogen")
        
        assert result is None

def test_get_element_summary(mock_model_config, element_info_sample):
    """Test get_element_summary method."""
    with patch('periodic_table_element.LiteClient'):
        pte = PeriodicTableElement(mock_model_config)
        summary = pte.get_element_summary(element_info_sample)
        
        assert summary["name"] == "Hydrogen"
        assert summary["symbol"] == "H"
        assert summary["atomic_number"] == 1

def test_validate_element_name(mock_model_config):
    """Test validate_element_name method."""
    with patch('periodic_table_element.LiteClient'):
        pte = PeriodicTableElement(mock_model_config)
        valid_elements = ["Hydrogen", "Helium"]
        assert pte.validate_element_name("Hydrogen", valid_elements) is True
        assert pte.validate_element_name("Oxygen", valid_elements) is False
