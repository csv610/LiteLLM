import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch, MagicMock

import pytest
from lite.config import ModelConfig

from herbal_info import HerbalInfoGenerator
from herbal_info_models import (
    AdministrationGuidanceModel,
    AlternativesModel,
    CostAndAvailabilityModel,
    DosageModel,
    EfficacyModel,
    HerbalBackgroundModel,
    HerbalClassificationModel,
    HerbalEducationModel,
    HerbalEvidenceModel,
    HerbalInfoModel,
    HerbalInteractionsModel,
    HerbalMechanismModel,
    HerbalMetadataModel,
    HerbalResearchModel,
    ModelOutput,
    SafetyInformationModel,
    SpecialInstructionsModel,
    SpecialPopulationsModel,
    UsageAndAdministrationModel,
)


@pytest.fixture
def mock_lite_client():
    with patch("herbal_info.LiteClient") as mock:
        yield mock


def test_herbal_info_generator_init():
    config = ModelConfig(model="test-model")
    generator = HerbalInfoGenerator(config)
    assert generator.model_config == config
    assert len(generator.agents) == 5


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = HerbalInfoGenerator(config)
    
    # Each agent returns the same markdown in this simple test
    mock_output = ModelOutput(markdown="Agent info", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Ashwagandha")
    # 5 agents, so "Agent info" repeated 5 times with separators
    assert "Agent info" in result.markdown
    assert generator.herb == "Ashwagandha"
    assert mock_lite_client.return_value.generate_text.call_count == 5


def test_generate_text_empty_herb():
    config = ModelConfig(model="test-model")
    generator = HerbalInfoGenerator(config)
    with pytest.raises(ValueError, match="Herb name cannot be empty"):
        generator.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = HerbalInfoGenerator(config)

    # Mock different data for different agents would be better, 
    # but for simplicity let's mock one that has all fields needed.
    # We need to return specific output models for each agent.
    
    from herbal_info_agents import BotanicalOutput, PharmacologicalOutput, SafetyOutput, ClinicalOutput, EducatorOutput

    # Create dummy data for each agent's expected output format
    def side_effect(model_input):
        if model_input.response_format == BotanicalOutput:
            return ModelOutput(data=BotanicalOutput(
                metadata=HerbalMetadataModel(
                    common_name="Ashwagandha",
                    botanical_name="Withania somnifera",
                    other_names="Winter cherry",
                    plant_family="Solanaceae",
                    active_constituents="Withanolides",
                    forms_available="Powder, Capsule",
                ),
                classification=HerbalClassificationModel(
                    traditional_system="Ayurveda",
                    primary_uses="Adaptogen",
                    energetics="Warming",
                    taste_profile="Bitter",
                ),
                background=HerbalBackgroundModel(
                    origin_and_habitat="India",
                    history_and_traditional_use="Ancient",
                    botanical_description="Shrub",
                )
            ))
        elif model_input.response_format == PharmacologicalOutput:
            return ModelOutput(data=PharmacologicalOutput(
                mechanism=HerbalMechanismModel(
                    mechanism_of_action="HPA axis modulation",
                    active_constituents_effects="Anti-stress",
                    body_systems_affected="Endocrine",
                ),
                evidence=HerbalEvidenceModel(
                    evidence_level="Moderate",
                    clinical_studies="Multiple RCTs",
                    regulatory_status="Dietary supplement",
                ),
                research=HerbalResearchModel(
                    recent_research="Sleep studies",
                    ongoing_studies="Cognition",
                    future_applications="Neuroprotection",
                )
            ))
        elif model_input.response_format == SafetyOutput:
            return ModelOutput(data=SafetyOutput(
                safety=SafetyInformationModel(
                    common_side_effects="Drowsiness",
                    serious_adverse_effects="None",
                    interactions=HerbalInteractionsModel(
                        drug_interactions="Sedatives",
                        herb_interactions="None",
                        food_interactions="None",
                        caffeine_interactions="None",
                        alcohol_interactions="Increased sedation",
                    ),
                    contraindications="Pregnancy",
                    precautions="Thyroid conditions",
                ),
                special_instructions=SpecialInstructionsModel(
                    discontinuation_guidance="None",
                    overdose_information="Gastrointestinal upset",
                    quality_concerns="Heavy metals",
                ),
                special_populations=SpecialPopulationsModel(
                    pregnancy_use="Avoid",
                    breastfeeding_use="Consult doctor",
                    pediatric_use="Consult doctor",
                )
            ))
        elif model_input.response_format == ClinicalOutput:
            return ModelOutput(data=ClinicalOutput(
                usage_and_administration=UsageAndAdministrationModel(
                    suitable_conditions="Stress",
                    preparation_methods="Tea",
                    age_specific_dosage=DosageModel(
                        children_dosage="N/A", adult_dosage="500mg", elderly_dosage="500mg"
                    ),
                    administration_guidance=AdministrationGuidanceModel(
                        tea_infusion="Steep 5 mins"
                    ),
                    storage_instruction="Cool dry place",
                    quality_indicators="Standardized extract",
                ),
                efficacy=EfficacyModel(
                    traditional_efficacy_claims="Strong",
                    clinical_evidence="Promising",
                    onset_of_action="2-4 weeks",
                    duration_of_effect="Hours",
                    expected_outcomes="Reduced stress",
                ),
                alternatives=AlternativesModel(
                    similar_herbs="Ginseng",
                    complementary_herbs="Rhodiola",
                    non_herbal_alternatives="Meditation",
                    when_to_seek_conventional_care="Severe anxiety",
                )
            ))
        elif model_input.response_format == EducatorOutput:
            return ModelOutput(data=EducatorOutput(
                education=HerbalEducationModel(
                    plain_language_explanation="Helps with stress",
                    key_takeaways="Adaptogen",
                    common_misconceptions="Instant results",
                    sustainability_notes="Eco-friendly",
                ),
                cost_and_availability=CostAndAvailabilityModel(
                    typical_cost_range="$15-30",
                    availability="OTC",
                    quality_considerations="Look for withanolide content",
                    organic_availability="Widely available",
                    sourcing_information="Ethical sources",
                )
            ))
        return ModelOutput(data=None)

    mock_lite_client.return_value.generate_text.side_effect = side_effect

    result = generator.generate_text("Ashwagandha", structured=True)
    assert result.data.metadata.common_name == "Ashwagandha"
    assert result.data.mechanism.mechanism_of_action == "HPA axis modulation"
    assert result.data.safety.common_side_effects == "Drowsiness"
    assert result.data.usage_and_administration.suitable_conditions == "Stress"
    assert result.data.education.key_takeaways == "Adaptogen"


def test_save_error():
    config = ModelConfig(model="test-model")
    generator = HerbalInfoGenerator(config)
    with pytest.raises(ValueError, match="No herb information available"):
        generator.save(ModelOutput(), Path("/tmp"))


@patch("herbal_info.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = HerbalInfoGenerator(config)
    mock_output = ModelOutput(markdown="Ashwagandha info")
    mock_lite_client.return_value.generate_text.return_value = mock_output

    generator.generate_text("Ashwagandha")
    generator.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    # Check if it was called with something like Path('/tmp/ashwagandha')
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("ashwagandha")
