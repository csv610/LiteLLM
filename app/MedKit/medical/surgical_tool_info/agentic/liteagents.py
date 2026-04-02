"""
liteagents.py - Unified for surgical_tool_info
"""
from unittest.mock import patch\nfrom lite.config import ModelConfig, ModelInput\nfrom lite.utils import save_model_response\nfrom app.MedKit.medical.surgical_tool_info.shared.models import *\nfrom tqdm import tqdm\nimport pytest\nfrom lite.lite_client import LiteClient\nimport logging\nfrom pathlib import Path\nimport argparse\nfrom lite.config import ModelConfig\nfrom unittest.mock import MagicMock, patch\nfrom lite.logging_config import configure_logging\nimport sys\n\n

# Add the project root to sys.path
try:
    from . import surgical_tool_info_cli
    from .surgical_tool_info_cli import (
        get_user_arguments,
        main,
    )
except (ImportError, ValueError):
    try:
        import surgical_tool_info_cli
        from surgical_tool_info_cli import (
            get_user_arguments,
            main,
        )
    except (ImportError, ValueError):
        # Add the project root to sys.path
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
        from medical.surgical_tool_info.agentic.agentic import surgical_tool_info_cli
        from medical.surgical_tool_info.agentic.surgical_tool_info_cli import (
            get_user_arguments,
            main,
        )

def test_get_user_arguments():
    test_args = ["scalpel", "-d", "test_outputs", "-m", "test-model", "-v", "3", "-s", "-a"]
    with patch("sys.argv", ["surgical_tool_info_cli.py"] + test_args):
        args = get_user_arguments()
        assert args.tool == "scalpel"
        assert args.output_dir == "test_outputs"
        assert args.model == "test-model"
        assert args.verbosity == 3
        assert args.structured is True
        assert args.agentic is True


def test_main_with_args_single_tool():
    with patch.object(surgical_tool_info_cli, "SurgicalToolInfoGenerator") as mock_gen_class:
        with patch.object(surgical_tool_info_cli, "configure_logging"):
            mock_generator = mock_gen_class.return_value
            mock_result = MagicMock()
            mock_generator.generate_text.return_value = mock_result
        
            args = argparse.Namespace(
                tool="scalpel",
                output_dir="test_outputs",
                model="test-model",
                verbosity=2,
                structured=False,
                agentic=False,
            )
        
            with patch("pathlib.Path.mkdir"):
                with patch.object(surgical_tool_info_cli, "get_user_arguments", return_value=args):
                    result = main()
        
            assert result == 0
            mock_generator.generate_text.assert_called_once_with(
                tool="scalpel", structured=False
            )
            mock_generator.save.assert_called_once_with(mock_result, Path("test_outputs"))


def test_main_with_agentic_flag():
    with patch.object(surgical_tool_info_cli, "MultiAgentSurgicalToolInfoGenerator") as mock_multi_gen_class:
        with patch.object(surgical_tool_info_cli, "configure_logging"):
            mock_generator = mock_multi_gen_class.return_value
            mock_result = MagicMock()
            mock_generator.generate_text.return_value = mock_result
        
            args = argparse.Namespace(
                tool="scalpel",
                output_dir="test_outputs",
                model="test-model",
                verbosity=2,
                structured=True,
                agentic=True,
            )
        
            with patch("pathlib.Path.mkdir"):
                with patch.object(surgical_tool_info_cli, "get_user_arguments", return_value=args):
                    result = main()
        
            assert result == 0
            mock_generator.generate_text.assert_called_once_with(
                tool="scalpel", structured=True
            )
            mock_generator.save.assert_called_once_with(mock_result, Path("test_outputs"))


def test_main_with_args_file_input(tmp_path):
    with patch.object(surgical_tool_info_cli, "SurgicalToolInfoGenerator") as mock_gen_class:
        with patch.object(surgical_tool_info_cli, "configure_logging"):
            mock_generator = mock_gen_class.return_value
            mock_result = MagicMock()
            mock_generator.generate_text.return_value = mock_result
        
            tool_file = tmp_path / "tools.txt"
            tool_file.write_text("""scalpel\nforceps""")
        
            args = argparse.Namespace(
                tool=str(tool_file),
                output_dir=str(tmp_path / "outputs"),
                model="test-model",
                verbosity=2,
                structured=True,
                agentic=False,
            )
        
            with patch.object(surgical_tool_info_cli, "get_user_arguments", return_value=args):
                result = main()
        
            assert result == 0
            assert mock_generator.generate_text.call_count == 2
            mock_generator.generate_text.assert_any_call(tool="scalpel", structured=True)
            mock_generator.generate_text.assert_any_call(tool="forceps", structured=True)



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



# Add the project root to sys.path
try:
    from .surgical_tool_info import MultiAgentSurgicalToolInfoGenerator
    from .surgical_tool_info_models import (
        ModelOutput,
        SurgicalToolInfoModel,
        ToolBasicsModel,
        ToolPurposeModel,
        PhysicalSpecificationsModel,
        OperationalCharacteristicsModel,
        SafetyFeaturesModel,
        PreOperativePreperationModel,
        IntraOperativeUseModel,
        DiscomfortRisksAndComplicationsModel,
        MaintenanceAndCareModel,
        SterilizationAndDisinfectionModel,
        AlternativesAndComparisonsModel,
        HistoricalContextModel,
        SpecialtySpecificConsiderationsModel,
        TrainingAndCertificationModel,
        RegulatoryAndStandardsModel,
        CostAndProcurementModel,
        EducationalContentModel
    )
except (ImportError, ValueError):
    try:
        from surgical_tool_info import MultiAgentSurgicalToolInfoGenerator
        from surgical_tool_info_models import (
            ModelOutput,
            SurgicalToolInfoModel,
            ToolBasicsModel,
            ToolPurposeModel,
            PhysicalSpecificationsModel,
            OperationalCharacteristicsModel,
            SafetyFeaturesModel,
            PreOperativePreperationModel,
            IntraOperativeUseModel,
            DiscomfortRisksAndComplicationsModel,
            MaintenanceAndCareModel,
            SterilizationAndDisinfectionModel,
            AlternativesAndComparisonsModel,
            HistoricalContextModel,
            SpecialtySpecificConsiderationsModel,
            TrainingAndCertificationModel,
            RegulatoryAndStandardsModel,
            CostAndProcurementModel,
            EducationalContentModel
        )
    except (ImportError, ValueError):
        # Add the project root to sys.path
        project_root = Path(__file__).resolve().parent.parent.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
        from medical.surgical_tool_info.agentic.surgical_tool_info import MultiAgentSurgicalToolInfoGenerator
        from medical.surgical_tool_info.agentic.surgical_tool_info_models import (
            ModelOutput,
            SurgicalToolInfoModel,
            ToolBasicsModel,
            ToolPurposeModel,
            PhysicalSpecificationsModel,
            OperationalCharacteristicsModel,
            SafetyFeaturesModel,
            PreOperativePreperationModel,
            IntraOperativeUseModel,
            DiscomfortRisksAndComplicationsModel,
            MaintenanceAndCareModel,
            SterilizationAndDisinfectionModel,
            AlternativesAndComparisonsModel,
            HistoricalContextModel,
            SpecialtySpecificConsiderationsModel,
            TrainingAndCertificationModel,
            RegulatoryAndStandardsModel,
            CostAndProcurementModel,
            EducationalContentModel
        )

@pytest.fixture
def mock_generate_text():
    with patch.object(LiteClient, "generate_text") as mock:
        yield mock

def test_multi_agent_generator_init():
    config = ModelConfig(model="test-model")
    generator = MultiAgentSurgicalToolInfoGenerator(config)
    assert generator.model_config == config

def test_multi_agent_generate_text(mock_generate_text):
    config = ModelConfig(model="test-model")
    generator = MultiAgentSurgicalToolInfoGenerator(config)
    
    # Mock responses for 4 agents and 1 orchestrator
    mock_responses = [
        ModelOutput(markdown="Tech Expert Report", data=None),
        ModelOutput(markdown="Clinical Specialist Report", data=None),
        ModelOutput(markdown="Safety Specialist Report", data=None),
        ModelOutput(markdown="History Educator Report", data=None),
        ModelOutput(markdown="Final Synthesized Report", data=None)
    ]
    
    mock_generate_text.side_effect = mock_responses

    result = generator.generate_text("Scalpel", structured=False)
    
    assert result.markdown == "Final Synthesized Report"
    assert generator.tool == "Scalpel"
    assert mock_generate_text.call_count == 5

def test_multi_agent_generate_text_structured(mock_generate_text):
    config = ModelConfig(model="test-model")
    generator = MultiAgentSurgicalToolInfoGenerator(config)
    
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
            vendor_options="Many",
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

    # Mock responses for 4 agents (markdown) and 1 orchestrator (structured data)
    mock_responses = [
        ModelOutput(markdown="Tech Expert Report", data=None),
        ModelOutput(markdown="Clinical Specialist Report", data=None),
        ModelOutput(markdown="Safety Specialist Report", data=None),
        ModelOutput(markdown="History Educator Report", data=None),
        ModelOutput(markdown=None, data=mock_data)
    ]
    
    mock_generate_text.side_effect = mock_responses

    result = generator.generate_text("Scalpel", structured=True)
    
    assert result.data.tool_basics.tool_name == "Scalpel"
    assert mock_generate_text.call_count == 5

"""Surgical Tool Information Generator CLI."""


# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))




try:
    try:
        from .surgical_tool_info import (
            MultiAgentSurgicalToolInfoGenerator,
            SurgicalToolInfoGenerator,
        )
    except (ImportError, ValueError):
        from medical.surgical_tool_info.agentic.surgical_tool_info import (
            MultiAgentSurgicalToolInfoGenerator,
            SurgicalToolInfoGenerator,
        )
except (ImportError, ValueError):
    from surgical_tool_info import (
        MultiAgentSurgicalToolInfoGenerator,
        SurgicalToolInfoGenerator,
    )

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate comprehensive surgical tool information."
    )
    parser.add_argument("tool", help="Tool name or file path containing names.")
    parser.add_argument(
        "-d", "--output-dir", default="outputs", help="Output directory."
    )
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Verbosity level.",
    )
    parser.add_argument(
        "-s", "--structured", action="store_true", help="Use structured output."
    )
    parser.add_argument(
        "-a", "--agentic", action="store_true", help="Use multi-agentic generation."
    )
    return parser.parse_args()


def setup_subparser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Sets up the subparser for this command."""
    parser = subparsers.add_parser(
        "surgical-tool-info",
        help="Generate comprehensive surgical tool information.",
        description="Generate comprehensive surgical tool information.",
    )
    parser.add_argument("tool", help="Tool name or file path containing names.")
    parser.add_argument(
        "-d", "--output-dir", default="outputs", help="Output directory."
    )
    parser.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use.")
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3, 4],
        help="Verbosity level.",
    )
    parser.add_argument(
        "-s", "--structured", action="store_true", help="Use structured output."
    )
    parser.add_argument(
        "-a", "--agentic", action="store_true", help="Use multi-agentic generation."
    )
    parser.set_defaults(func=main)
    return parser


def main():
    """Main entry point for the CLI."""
    args = get_user_arguments()

    configure_logging(
        log_file="surgical_tool_info.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.tool)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.tool]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.2)

        if args.agentic:
            generator = MultiAgentSurgicalToolInfoGenerator(model_config)
            logger.info("Using multi-agentic generation mode")
        else:
            generator = SurgicalToolInfoGenerator(model_config)
            logger.info("Using single-agent generation mode")

        for item in tqdm(items, desc="Generating"):
            result = generator.generate_text(tool=item, structured=args.structured)
            if result:
                generator.save(result, output_dir)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    main()



try:
    from .surgical_tool_info_models import ModelOutput, SurgicalToolInfoModel
    from .surgical_tool_info_prompts import PromptBuilder
except (ImportError, ValueError):
    from surgical_tool_info_models import ModelOutput, SurgicalToolInfoModel
    from surgical_tool_info_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class SurgicalToolInfoGenerator:
    """Generates comprehensive surgical tool information based on provided configuration."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.tool = None
        logger.debug("Initialized SurgicalToolInfoGenerator")

    def generate_text(self, tool: str, structured: bool = False) -> ModelOutput:
        if not tool or not str(tool).strip():
            raise ValueError("Tool name cannot be empty")

        self.tool = tool
        logger.debug(f"Starting surgical tool information generation for: {tool}")

        model_input = ModelInput(
            system_prompt=PromptBuilder.create_technical_expert_system_prompt(),  # Fallback to technical expert if not multi-agent
            user_prompt=PromptBuilder.create_technical_expert_user_prompt(tool),
            response_format=SurgicalToolInfoModel if structured else None,
        )

        try:
            result = self.client.generate_text(model_input=model_input)
            logger.debug("✓ Successfully generated surgical tool information")
            return result
        except Exception as e:
            logger.error(f"✗ Error generating surgical tool information: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        if self.tool is None:
            raise ValueError("No tool information available. Call generate_text first.")
        base_filename = f"{self.tool.lower().replace(' ', '_')}"
        return save_model_response(result, output_dir / base_filename)


class MultiAgentSurgicalToolInfoGenerator:
    """Generates comprehensive surgical tool information using multiple specialized agents."""

    def __init__(self, model_config: ModelConfig):
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.tool = None
        logger.debug("Initialized MultiAgentSurgicalToolInfoGenerator")

    def generate_text(self, tool: str, structured: bool = False) -> ModelOutput:
        """Generates surgical tool information using a 3-tier multi-agent system."""
        if not tool or not str(tool).strip():
            raise ValueError("Tool name cannot be empty")

        self.tool = tool
        logger.info(f"Starting 3-tier multi-agent generation for: {tool}")

        try:
            # --- Tier 1: Specialist Stages (JSON) ---
            logger.info("Tier 1: Specialists generating specialized tool data...")
            # 1.1 Technical Expert
            tech_input = ModelInput(
                system_prompt=PromptBuilder.create_technical_expert_system_prompt(),
                user_prompt=PromptBuilder.create_technical_expert_user_prompt(tool),
            )
            tech_report = self.client.generate_text(model_input=tech_input).markdown

            # 1.2 Clinical Specialist
            clinical_input = ModelInput(
                system_prompt=PromptBuilder.create_clinical_specialist_system_prompt(),
                user_prompt=PromptBuilder.create_clinical_specialist_user_prompt(tool),
            )
            clinical_report = self.client.generate_text(model_input=clinical_input).markdown

            # 1.3 Safety & Maintenance
            safety_input = ModelInput(
                system_prompt=PromptBuilder.create_safety_maintenance_specialist_system_prompt(),
                user_prompt=PromptBuilder.create_safety_maintenance_user_prompt(tool),
            )
            safety_report = self.client.generate_text(model_input=safety_input).markdown

            # 1.4 Medical Historian
            history_input = ModelInput(
                system_prompt=PromptBuilder.create_medical_historian_educator_system_prompt(),
                user_prompt=PromptBuilder.create_medical_historian_educator_user_prompt(tool),
            )
            history_report = self.client.generate_text(model_input=history_input).markdown

            specialist_data = f"""
TECHNICAL REPORT:
{tech_report}

CLINICAL REPORT:
{clinical_report}

SAFETY REPORT:
{safety_report}

HISTORY REPORT:
{history_report}
"""

            # --- Tier 2: Compliance Auditor Stage (JSON Audit) ---
            logger.info("Tier 2: Auditor performing quality check...")
            orchestrator_input = ModelInput(
                system_prompt=PromptBuilder.create_orchestrator_system_prompt(),
                user_prompt=PromptBuilder.create_orchestrator_user_prompt(tool, specialist_data),
                response_format=SurgicalToolInfoModel if structured else None,
            )
            audit_res = self.client.generate_text(model_input=orchestrator_input)
            
            if structured:
                audit_json = audit_res.data.model_dump_json(indent=2)
            else:
                audit_json = audit_res.markdown

            # --- Tier 3: Final Output Synthesis (Markdown Closer) ---
            logger.info("Tier 3: Output Agent synthesizing final report...")
            out_sys, out_usr = PromptBuilder.create_output_synthesis_prompts(
                tool, specialist_data, audit_json
            )
            final_res = self.client.generate_text(ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None
            ))

            logger.info(f"✓ Successfully generated 3-tier surgical tool report for {tool}")
            return ModelOutput(data=audit_res.data if structured else None, markdown=final_res.markdown)

        except Exception as e:
            logger.error(f"✗ 3-tier Surgical Tool generation failed: {e}")
            raise

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        if self.tool is None:
            raise ValueError("No tool information available. Call generate_text first.")
        base_filename = f"{self.tool.lower().replace(' ', '_')}_multi_agent"
        return save_model_response(result, output_dir / base_filename)

"""Main entry point for surgical tool info package."""


try:
    from .surgical_tool_info_cli import main
except (ImportError, ValueError):
    from surgical_tool_info_cli import main

if __name__ == "__main__":
    sys.exit(main())

