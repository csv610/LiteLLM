import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from lite.config import ModelConfig
from lite.lite_client import LiteClient

# Add the project root to sys.path
try:
    from . import surgical_tool_info
    from .surgical_tool_info import SurgicalToolInfoGenerator
    from .surgical_tool_info_models import (
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
except (ImportError, ValueError):
    try:
        import surgical_tool_info
        from surgical_tool_info import SurgicalToolInfoGenerator
        from surgical_tool_info_models import (
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
    except (ImportError, ValueError):
        # Add the project root to sys.path
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
        from medical.surgical_tool_info.agentic.agentic import surgical_tool_info
        from medical.surgical_tool_info.agentic.surgical_tool_info import SurgicalToolInfoGenerator
        from medical.surgical_tool_info.agentic.surgical_tool_info_models import (
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
def mock_generate_text():
    with patch.object(LiteClient, "generate_text") as mock:
        yield mock


def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = SurgicalToolInfoGenerator(config)
    assert generator.model_config == config


def test_generate_text_unstructured(mock_generate_text):
    config = ModelConfig(model="test-model")
    generator = SurgicalToolInfoGenerator(config)
    mock_output = ModelOutput(markdown="Scalpel info", data=None)
    mock_generate_text.return_value = mock_output

    result = generator.generate_text("Scalpel", structured=False)

    assert result.markdown == "Scalpel info"
    assert generator.tool == "Scalpel"
    mock_generate_text.assert_called_once()


def test_generate_text_structured(mock_generate_text):
    config = ModelConfig(model="test-model")
    generator = SurgicalToolInfoGenerator(config)

    mock_data = SurgicalToolInfoModel(
        tool_basics=ToolBasicsModel(
            tool_name="Scalpel",
            alternative_names="Surgical knife",
            tool_category="Cutting and Dissecting",
            surgical_specialties="General Surgery",
            instrument_family="Blades",
        ),
        tool_purpose=ToolPurposeModel(
            primary_purpose="Incision",
            surgical_applications="Initial skin incision",
            anatomical_targets="Skin and tissue",
            tissue_types="Soft tissue",
            unique_advantages="Precision",
        ),
        physical_specifications=PhysicalSpecificationsModel(
            dimensions="Varies",
            weight="Varies",
            material_composition="Stainless steel",
            finish_type="Satin",
            blade_or_tip_specifications="Pointed",
            handle_design="Flat",
            sterility_type="Sterile",
        ),
        operational_characteristics=OperationalCharacteristicsModel(
            cutting_or_grasping_force="Manual",
            actuation_mechanism="Manual",
            degrees_of_freedom="N/A",
            precision_level="High",
            engagement_depth="Variable",
            working_distance="N/A",
        ),
        safety_features=SafetyFeaturesModel(
            safety_mechanisms="Blade guard",
            slip_resistance="Grip",
            wear_considerations="Single use",
            maximum_safe_force="N/A",
            emergency_protocols="N/A",
            tissue_damage_prevention="Sharpness",
        ),
        preparation=PreOperativePreperationModel(
            inspection_requirements="Check integrity",
            cleaning_protocols="Disposable",
            sterilization_requirements="Gamma",
            quality_assurance_tests="Visual",
            storage_requirements="Dry",
            preparation_time="Fast",
        ),
        intraoperative_use=IntraOperativeUseModel(
            positioning_in_field="OR",
            handling_technique="Grip",
            hand_position_requirements="Stable",
            coordination_with_other_tools="Forceps",
            common_movements="Slice",
            visibility_requirements="Clear",
            ergonomic_considerations="Comfort",
        ),
        discomfort_risks_and_complications=DiscomfortRisksAndComplicationsModel(
            surgeon_fatigue_factors="None",
            common_handling_errors="Slip",
            tissue_damage_risks="Accidental cut",
            instrument_complications="Broken blade",
            cross_contamination_risks="Minimal",
            material_reactions="Latex free",
            electrical_safety="N/A",
        ),
        maintenance_and_care=MaintenanceAndCareModel(
            post_operative_cleaning="Discard",
            lubrication_schedule="None",
            inspection_frequency="N/A",
            wear_indicators="N/A",
            sharpening_protocol="N/A",
            repair_guidelines="N/A",
            expected_lifespan="Single use",
        ),
        sterilization_and_disinfection=SterilizationAndDisinfectionModel(
            approved_sterilization_methods="Gamma",
            incompatible_sterilization="Heat",
            disinfection_alternatives="None",
            packaging_requirements="Pouch",
            validation_standards="ISO",
            reprocessing_manufacturer_protocols="None",
        ),
        alternatives_and_comparisons=AlternativesAndComparisonsModel(
            similar_alternative_tools="Laser",
            advantages_over_alternatives="Low cost",
            disadvantages_vs_alternatives="Bleeding",
            cost_comparison="Cheap",
            when_to_use_this_tool="Skin",
            complementary_tools="Forceps",
        ),
        historical_context=HistoricalContextModel(
            invention_history="Ancient",
            evolution_timeline="Modern steel",
            clinical_evidence="Long history",
            widespread_adoption="Global",
            current_status="Standard",
        ),
        specialty_specific_considerations=SpecialtySpecificConsiderationsModel(
            general_surgery_specific="Primary tool",
            orthopedic_specific="Heavy",
            cardiac_specific="Fine",
            neurosurgery_specific="Micro",
            vascular_specific="Fine",
            laparoscopic_considerations="N/A",
            robotic_integration="N/A",
        ),
        training_and_certification=TrainingAndCertificationModel(
            training_requirements="Surgical residency",
            proficiency_indicators="Skill",
            common_learning_mistakes="Depth control",
            skill_development_timeline="Ongoing",
            formal_education_resources="Surgical manuals",
            mentoring_best_practices="Supervised",
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
            vendor_options="Many",
            procurement_lead_time="Short",
            inventory_recommendations="High",
            insurance_coverage="Standard",
        ),
        educational_content=EducationalContentModel(
            plain_language_explanation="Surgical knife",
            key_takeaways="Sharp and precise",
            common_misconceptions="All same",
            patient_communication="Consent",
            video_demonstration_topics="Grip",
        ),
    )

    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_generate_text.return_value = mock_output

    result = generator.generate_text("Scalpel", structured=True)
    assert result.data.tool_basics.tool_name == "Scalpel"


def test_save_success(mock_generate_text):
    with patch.object(surgical_tool_info, "save_model_response") as mock_save:
        config = ModelConfig(model="test-model")
        generator = SurgicalToolInfoGenerator(config)
        mock_output = ModelOutput(markdown="Info")
        mock_generate_text.return_value = mock_output
    
        generator.generate_text("Scalpel")
        generator.save(mock_output, Path("/tmp"))
    
        mock_save.assert_called_once()
        args, _ = mock_save.call_args
        assert args[0] == mock_output
        assert str(args[1]).endswith("scalpel")
