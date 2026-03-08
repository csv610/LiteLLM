import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path

from drugs_comparison import DrugsComparison, DrugsComparisonInput
from drugs_comparison_models import (
    MedicinesComparisonResult, 
    ClinicalMetrics, 
    RegulatoryMetrics, 
    PracticalMetrics, 
    ComparisonSummary, 
    RecommendationContext,
    EffectivenessRating,
    SafetyRating,
    AvailabilityStatus
)
from lite.config import ModelConfig, ModelInput

@pytest.fixture
def mock_model_config():
    return ModelConfig(model="test-model", temperature=0.1)

@pytest.fixture
def drugs_comparison_analyzer(mock_model_config):
    with patch("drugs_comparison.LiteClient"):
        return DrugsComparison(mock_model_config)

def test_drugs_comparison_input_validation():
    # Valid input
    valid_input = DrugsComparisonInput(medicine1="Aspirin", medicine2="Ibuprofen")
    # DrugsComparison._validate_input is called during generate_text
    
    analyzer = DrugsComparison(ModelConfig(model="test"))
    analyzer._validate_input(valid_input) # Should not raise

    # Invalid input (empty medicine 1)
    with pytest.raises(ValueError, match="Medicine 1 name cannot be empty"):
        analyzer._validate_input(DrugsComparisonInput(medicine1="", medicine2="Ibuprofen"))
    
    # Invalid input (empty medicine 2)
    with pytest.raises(ValueError, match="Medicine 2 name cannot be empty"):
        analyzer._validate_input(DrugsComparisonInput(medicine1="Aspirin", medicine2=" "))
        
    # Invalid input (invalid age)
    with pytest.raises(ValueError, match="Age must be between 0 and 150 years"):
        analyzer._validate_input(DrugsComparisonInput(medicine1="Aspirin", medicine2="Ibuprofen", patient_age=200))

@patch("drugs_comparison.LiteClient")
def test_generate_text_mock(mock_client_class, mock_model_config):
    mock_client_instance = mock_client_class.return_value
    raw_markdown = "# Comparison for Aspirin vs Ibuprofen"
    mock_client_instance.generate_text.return_value = raw_markdown
    
    analyzer = DrugsComparison(mock_model_config)
    config = DrugsComparisonInput(medicine1="Aspirin", medicine2="Ibuprofen")
    
    result = analyzer.generate_text(config)
    
    assert result == raw_markdown
    mock_client_instance.generate_text.assert_called_once()
    
    # Verify ModelInput passed to client
    args, kwargs = mock_client_instance.generate_text.call_args
    model_input = kwargs.get("model_input") or args[0]
    assert "Aspirin" in model_input.user_prompt
    assert "Ibuprofen" in model_input.user_prompt
    assert model_input.response_format is None

@patch("drugs_comparison.LiteClient")
def test_generate_text_structured_mock(mock_client_class, mock_model_config):
    mock_client_instance = mock_client_class.return_value
    
    # Create a dummy structured result
    m1_clinical = ClinicalMetrics(
        medicine_name="Aspirin",
        effectiveness_rating=EffectivenessRating.HIGH,
        efficacy_rate="80%",
        onset_of_action="30 min",
        duration_of_effect="4-6 hours",
        safety_rating=SafetyRating.LOW_RISK,
        common_side_effects="Stomach upset",
        serious_side_effects="Gastrointestinal bleeding",
        contraindications="Ulcers"
    )
    m2_clinical = m1_clinical.model_copy(update={"medicine_name": "Ibuprofen"})
    
    m1_reg = RegulatoryMetrics(
        medicine_name="Aspirin",
        fda_approval_status="Approved",
        approval_date="1899",
        approval_type="Standard",
        has_black_box_warning=False,
        fda_alerts="None",
        generic_available=True
    )
    m2_reg = m1_reg.model_copy(update={"medicine_name": "Ibuprofen"})
    
    m1_prac = PracticalMetrics(
        medicine_name="Aspirin",
        availability_status=AvailabilityStatus.OVER_THE_COUNTER,
        typical_cost_range="$5-10",
        insurance_coverage="Common",
        available_formulations="Tablet",
        dosage_strengths="325mg",
        patient_assistance_programs="None"
    )
    m2_prac = m1_prac.model_copy(update={"medicine_name": "Ibuprofen"})
    
    summary = ComparisonSummary(
        more_effective="Comparable",
        safer_option="Ibuprofen for some",
        more_affordable="Both affordable",
        easier_access="Both OTC",
        key_differences="Mechanism, Side effects"
    )
    
    recommendations = RecommendationContext(
        overall_recommendation="Use as directed"
    )
    
    structured_raw = MedicinesComparisonResult(
        medicine1_clinical=m1_clinical,
        medicine2_clinical=m2_clinical,
        medicine1_regulatory=m1_reg,
        medicine2_regulatory=m2_reg,
        medicine1_practical=m1_prac,
        medicine2_practical=m2_prac,
        comparison_summary=summary,
        recommendations=recommendations,
        narrative_analysis="Detailed analysis here",
        evidence_quality="High",
        limitations="None"
    )
    
    mock_client_instance.generate_text.return_value = structured_raw
    
    analyzer = DrugsComparison(mock_model_config)
    config = DrugsComparisonInput(medicine1="Aspirin", medicine2="Ibuprofen")
    
    result = analyzer.generate_text(config, structured=True)
    
    assert isinstance(result, MedicinesComparisonResult)
    assert result.medicine1_clinical.medicine_name == "Aspirin"
    assert result.medicine2_clinical.medicine_name == "Ibuprofen"
    
    # Verify response_format was set
    args, kwargs = mock_client_instance.generate_text.call_args
    model_input = kwargs.get("model_input") or args[0]
    assert model_input.response_format == MedicinesComparisonResult

@patch("drugs_comparison.save_model_response")
def test_save_mock(mock_save_response, drugs_comparison_analyzer):
    result = "# Analysis"
    output_dir = Path("test_outputs")
    
    config = DrugsComparisonInput(medicine1="Aspirin", medicine2="Ibuprofen")
    drugs_comparison_analyzer.config = config
    
    drugs_comparison_analyzer.save(result, output_dir)
    
    mock_save_response.assert_called_once()
    args, _ = mock_save_response.call_args
    assert args[0] == result
    assert "aspirin_vs_ibuprofen" in str(args[1])

def test_save_before_generate_raises(drugs_comparison_analyzer):
    result = "# Analysis"
    with pytest.raises(ValueError, match="No configuration information available"):
        drugs_comparison_analyzer.save(result, Path("outputs"))
