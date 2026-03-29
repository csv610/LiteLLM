import sys
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from unittest.mock import patch

import pytest
from lite.config import ModelConfig

from medical.surgical_tool_info.surgical_tool_info import SurgicalToolInfoGenerator
from medical.surgical_tool_info.surgical_tool_info_models import (
    AlternativesAndComparisonsModel,
    CostAndProcurementModel,
    DiscomfortRisksAndComplicationsModel,
    EducationalContentModel,
    HistoricalContextModel,
    IntraOperativeUseModel,
    MaintenanceAndCareModel,
    ModelOutput,
    OperationalCharacteristicsModel,
    PhysicalSpecificationsModel,
    PreOperativePreperationModel,
    RegulatoryAndStandardsModel,
    SafetyFeaturesModel,
    SpecialtySpecificConsiderationsModel,
    SterilizationAndDisinfectionModel,
    SurgicalToolInfoModel,
    ToolBasicsModel,
    ToolPurposeModel,
    TrainingAndCertificationModel,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.surgical_tool_info.surgical_tool_info.LiteClient") as mock:
        yield mock


def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = SurgicalToolInfoGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalToolInfoGenerator(config)
    mock_output = ModelOutput(markdown="Scalpel info", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Scalpel")
    assert result.markdown == "Scalpel info"
    assert generator.tool == "Scalpel"


def test_generate_text_empty():
    config = ModelConfig(model="test-model")
    generator = SurgicalToolInfoGenerator(config)
    with pytest.raises(ValueError, match="Tool name cannot be empty"):
        generator.generate_text("")


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalToolInfoGenerator(config)

    # Minimal mock data for structured output
    mock_data = SurgicalToolInfoModel(
        tool_basics=ToolBasicsModel(
            tool_name="Scalpel",
            alternative_names="Knife",
            tool_category="Cutting",
            surgical_specialties="All",
            instrument_family="Blades",
        ),
        tool_purpose=ToolPurposeModel(
            primary_purpose="Incision",
            surgical_applications="All",
            anatomical_targets="Skin",
            tissue_types="Soft tissue",
            unique_advantages="Sharpness",
        ),
        physical_specifications=PhysicalSpecificationsModel(
            dimensions="15cm",
            weight="20g",
            material_composition="Steel",
            finish_type="Polished",
            blade_or_tip_specifications="Sharp",
            handle_design="Flat",
            sterility_type="Single-use",
        ),
        operational_characteristics=OperationalCharacteristicsModel(
            cutting_or_grasping_force="Low",
            actuation_mechanism="Manual",
            degrees_of_freedom="Fixed",
            precision_level="High",
            engagement_depth="Variable",
            working_distance="Close",
        ),
        safety_features=SafetyFeaturesModel(
            safety_mechanisms="Blade guard",
            slip_resistance="Textured handle",
            wear_considerations="Dulling",
            maximum_safe_force="N/A",
            emergency_protocols="Discard if broken",
            tissue_damage_prevention="Sharpness control",
        ),
        preparation=PreOperativePreperationModel(
            inspection_requirements="Check sharpness",
            cleaning_protocols="None",
            sterilization_requirements="None",
            quality_assurance_tests="Visual",
            storage_requirements="Dry",
            preparation_time="1 min",
        ),
        intraoperative_use=IntraOperativeUseModel(
            positioning_in_field="Handheld",
            handling_technique="Pencil grip",
            hand_position_requirements="Stable",
            coordination_with_other_tools="Forceps",
            common_movements="Stroke",
            visibility_requirements="Clear",
            ergonomic_considerations="Grip",
        ),
        discomfort_risks_and_complications=DiscomfortRisksAndComplicationsModel(
            surgeon_fatigue_factors="None",
            common_handling_errors="Too deep",
            tissue_damage_risks="Accidental cut",
            instrument_complications="Breakage",
            cross_contamination_risks="Needlestick",
            material_reactions="None",
            electrical_safety="N/A",
        ),
        maintenance_and_care=MaintenanceAndCareModel(
            post_operative_cleaning="Discard",
            lubrication_schedule="None",
            inspection_frequency="Each use",
            wear_indicators="Dullness",
            sharpening_protocol="None",
            repair_guidelines="Replace",
            expected_lifespan="1 use",
        ),
        sterilization_and_disinfection=SterilizationAndDisinfectionModel(
            approved_sterilization_methods="Gamma",
            incompatible_sterilization="Autoclave",
            disinfection_alternatives="None",
            packaging_requirements="Peel pack",
            validation_standards="ISO",
            reprocessing_manufacturer_protocols="None",
        ),
        alternatives_and_comparisons=AlternativesAndComparisonsModel(
            similar_alternative_tools="Laser",
            advantages_over_alternatives="Cheap",
            disadvantages_vs_alternatives="Bleeding",
            cost_comparison="Low",
            when_to_use_this_tool="Initial incision",
            complementary_tools="Forceps",
        ),
        historical_context=HistoricalContextModel(
            invention_history="Ancient",
            evolution_timeline="Steel blades",
            clinical_evidence="Standard",
            widespread_adoption="Universal",
            current_status="Standard",
        ),
        specialty_specific_considerations=SpecialtySpecificConsiderationsModel(
            general_surgery_specific="Common",
            orthopedic_specific="Heavy duty",
            cardiac_specific="Fine",
            neurosurgery_specific="Micro",
            vascular_specific="Fine",
            laparoscopic_considerations="Trocar",
            robotic_integration="Robotic scalpel",
        ),
        training_and_certification=TrainingAndCertificationModel(
            training_requirements="Med school",
            proficiency_indicators="Clean cut",
            common_learning_mistakes="Shaky hand",
            skill_development_timeline="Months",
            formal_education_resources="Surgical texts",
            mentoring_best_practices="Supervision",
        ),
        regulatory_and_standards=RegulatoryAndStandardsModel(
            fda_classification="Class I",
            fda_status="Cleared",
            iso_standards="ISO 13485",
            country_approvals="Global",
            quality_certifications="CE",
            traceability_requirements="Lot number",
        ),
        cost_and_procurement=CostAndProcurementModel(
            single_use_cost="Low",
            reusable_initial_cost=None,
            lifecycle_cost="Low",
            vendor_options="Various",
            procurement_lead_time="1 week",
            inventory_recommendations="High",
            insurance_coverage="Yes",
        ),
        educational_content=EducationalContentModel(
            plain_language_explanation="Knife for surgery",
            key_takeaways="Sharp",
            common_misconceptions="Dull is safe",
            patient_communication="Standard consent",
            video_demonstration_topics="Handling",
        ),
    )

    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Scalpel", structured=True)
    assert result.data.tool_basics.tool_name == "Scalpel"


@patch("medical.surgical_tool_info.surgical_tool_info.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = SurgicalToolInfoGenerator(config)
    mock_output = ModelOutput(markdown="Info")
    mock_lite_client.return_value.generate_text.return_value = mock_output

    generator.generate_text("Scalpel")
    generator.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("scalpel")
