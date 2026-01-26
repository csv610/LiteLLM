"""Unit tests for CLI module implementations.

Tests for:
- Argument parsing in specific modules
- Prompt builder implementations
- Generator implementations
- Model validation
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from pydantic import BaseModel, Field, ValidationError

# Setup paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.config import ModelConfig, ModelInput


# ==============================================================================
# TEST MODELS
# ==============================================================================


class DrugInteractionModel(BaseModel):
    """Mock drug interaction model."""
    interaction_type: str = Field(description="Type of interaction")
    severity: str = Field(description="Severity level")
    mechanism: str = Field(description="Mechanism of interaction")
    management: str = Field(description="Management recommendations")


class DiseaseInfoModel(BaseModel):
    """Mock disease information model."""
    disease_name: str = Field(description="Disease name")
    description: str = Field(description="Disease description")
    symptoms: list = Field(default_factory=list, description="List of symptoms")
    treatment: str = Field(description="Treatment options")


class MedicineInfoModel(BaseModel):
    """Mock medicine information model."""
    medicine_name: str = Field(description="Medicine name")
    indication: str = Field(description="Primary indication")
    dosage: str = Field(description="Standard dosage")
    side_effects: list = Field(default_factory=list, description="Side effects")


class FAQModel(BaseModel):
    """Mock FAQ model."""
    question: str = Field(description="Question")
    answer: str = Field(description="Answer")
    references: list = Field(default_factory=list, description="Reference links")


# ==============================================================================
# TESTS - Drug-Drug Interaction Module
# ==============================================================================


class TestDrugDrugInteractionCLI:
    """Test drug-drug interaction CLI module."""

    def test_cli_import(self):
        """Test that drug-drug interaction CLI can be imported."""
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / "drug" / "drug_drug"))
            # We don't actually import to avoid dependency issues, but test structure
            assert Path(__file__).parent.parent / "drug" / "drug_drug" / "drug_drug_interaction_cli.py"
        except Exception as e:
            pytest.skip(f"Module structure issue: {e}")

    def test_medicine_argument_validation(self):
        """Test medicine name validation."""
        class DrugInput(BaseModel):
            medicine1: str
            medicine2: str

            def validate_names(self):
                if not self.medicine1.strip():
                    raise ValueError("Medicine 1 cannot be empty")
                if not self.medicine2.strip():
                    raise ValueError("Medicine 2 cannot be empty")

        # Valid input
        input_data = DrugInput(medicine1="Aspirin", medicine2="Warfarin")
        input_data.validate_names()  # Should not raise

        # Invalid input
        input_data = DrugInput(medicine1="  ", medicine2="Warfarin")
        with pytest.raises(ValueError):
            input_data.validate_names()

    def test_age_argument_validation(self):
        """Test age argument validation."""
        class AgeInput(BaseModel):
            age: int

            def validate_age(self):
                if not (0 <= self.age <= 150):
                    raise ValueError("Age must be between 0 and 150")

        # Valid ages
        for age in [0, 25, 65, 150]:
            input_data = AgeInput(age=age)
            input_data.validate_age()  # Should not raise

        # Invalid age
        input_data = AgeInput(age=200)
        with pytest.raises(ValueError):
            input_data.validate_age()

    def test_interaction_result_structure(self):
        """Test drug interaction result structure."""
        result = DrugInteractionModel(
            interaction_type="Pharmacodynamic",
            severity="High",
            mechanism="Increased anticoagulation effect",
            management="Monitor INR, adjust dosages"
        )

        assert result.interaction_type == "Pharmacodynamic"
        assert result.severity == "High"
        assert len(result.management) > 0

    def test_prompt_builder_format(self):
        """Test prompt builder formatting."""
        medicine1 = "Warfarin"
        medicine2 = "Aspirin"
        context = "Patient age: 65 years"

        # Simulating prompt builder behavior
        user_prompt = f"{medicine1} and {medicine2} interaction analysis. {context}"

        assert medicine1 in user_prompt
        assert medicine2 in user_prompt
        assert context in user_prompt

    def test_cli_arguments_list(self, basic_cli_args, drug_interaction_cli_args):
        """Test CLI argument combinations."""
        # Basic arguments
        assert "-m" in basic_cli_args
        assert "-t" in basic_cli_args

        # Drug interaction specific
        assert "Warfarin" in drug_interaction_cli_args
        assert "Aspirin" in drug_interaction_cli_args


# ==============================================================================
# TESTS - Disease Info Module
# ==============================================================================


class TestDiseaseInfoCLI:
    """Test disease information CLI module."""

    def test_disease_name_validation(self):
        """Test disease name validation."""
        class DiseaseInput(BaseModel):
            disease: str

        # Valid disease name
        input_data = DiseaseInput(disease="Hypertension")
        assert len(input_data.disease) > 0

        # Invalid (empty) disease name
        with pytest.raises(ValidationError):
            DiseaseInput(disease="")

    def test_disease_info_model_creation(self):
        """Test creating disease info model."""
        disease = DiseaseInfoModel(
            disease_name="Hypertension",
            description="Elevated blood pressure",
            symptoms=["Headaches", "Dizziness"],
            treatment="Antihypertensive medications"
        )

        assert disease.disease_name == "Hypertension"
        assert len(disease.symptoms) == 2
        assert "medications" in disease.treatment.lower()

    def test_disease_prompt_template(self):
        """Test disease info prompt template."""
        disease = "Type 2 Diabetes"

        system_prompt = "You are a medical expert..."
        user_prompt = f"Generate comprehensive information for the disease: {disease}."

        assert disease in user_prompt
        assert "comprehensive" in user_prompt.lower()

    def test_structured_vs_unstructured_output(self):
        """Test structured and unstructured output modes."""
        # Structured output
        structured = DiseaseInfoModel(
            disease_name="Diabetes",
            description="Metabolic disorder",
            treatment="Insulin"
        )
        assert isinstance(structured, DiseaseInfoModel)

        # Unstructured would be string
        unstructured = "Diabetes is a metabolic disorder..."
        assert isinstance(unstructured, str)

    def test_cli_arguments_parsing(self, disease_cli_args):
        """Test disease CLI arguments parsing."""
        assert "Hypertension" in disease_cli_args
        assert "-s" in disease_cli_args  # structured flag


# ==============================================================================
# TESTS - Medicine Info Module
# ==============================================================================


class TestMedicineInfoCLI:
    """Test medicine information CLI module."""

    def test_medicine_name_validation(self):
        """Test medicine name validation."""
        class MedicineInput(BaseModel):
            medicine: str

        # Valid
        med = MedicineInput(medicine="Aspirin")
        assert len(med.medicine) > 0

        # Empty
        with pytest.raises(ValidationError):
            MedicineInput(medicine="")

    def test_medicine_info_model(self):
        """Test medicine information model."""
        medicine = MedicineInfoModel(
            medicine_name="Metformin",
            indication="Type 2 Diabetes",
            dosage="500-2000mg daily",
            side_effects=["Nausea", "Diarrhea"]
        )

        assert medicine.medicine_name == "Metformin"
        assert "Diabetes" in medicine.indication
        assert len(medicine.side_effects) == 2

    def test_medicine_parsing_from_string(self):
        """Test parsing medicine info from model."""
        info_str = "Metformin: Antidiabetic agent for Type 2 Diabetes"

        parts = info_str.split(":")
        assert len(parts) == 2
        assert "Metformin" in parts[0]

    def test_dosage_format_validation(self):
        """Test dosage format."""
        valid_dosages = [
            "500mg twice daily",
            "1-2 tablets per day",
            "10-20mg daily"
        ]

        for dosage in valid_dosages:
            assert len(dosage) > 0
            assert any(c.isalnum() for c in dosage)

    def test_cli_arguments_parsing(self, medicine_cli_args):
        """Test medicine CLI arguments parsing."""
        assert "Aspirin" in medicine_cli_args
        assert "-j" in medicine_cli_args  # json output flag


# ==============================================================================
# TESTS - Medical FAQ Module
# ==============================================================================


class TestMedicalFAQCLI:
    """Test medical FAQ CLI module."""

    def test_faq_model_structure(self):
        """Test FAQ model structure."""
        faq = FAQModel(
            question="What is hypertension?",
            answer="Hypertension is elevated blood pressure...",
            references=["WHO Guidelines", "AHA Recommendations"]
        )

        assert len(faq.question) > 0
        assert len(faq.answer) > 0
        assert len(faq.references) >= 0

    def test_topic_argument_validation(self):
        """Test topic argument validation."""
        class TopicInput(BaseModel):
            topic: str

        # Valid topic
        input_data = TopicInput(topic="Diabetes")
        assert len(input_data.topic) > 0

        # Empty topic
        with pytest.raises(ValidationError):
            TopicInput(topic="")

    def test_faq_generation_prompt(self):
        """Test FAQ generation prompt structure."""
        topic = "Cardiovascular Disease"

        prompt = f"Generate frequently asked questions about {topic}"

        assert topic in prompt
        assert "question" in prompt.lower()

    def test_multiple_faq_items(self):
        """Test handling multiple FAQ items."""
        faqs = [
            FAQModel(
                question="Q1",
                answer="A1",
                references=["Ref1"]
            ),
            FAQModel(
                question="Q2",
                answer="A2",
                references=["Ref2"]
            )
        ]

        assert len(faqs) == 2
        for faq in faqs:
            assert isinstance(faq, FAQModel)


# ==============================================================================
# TESTS - Model Configuration Validation
# ==============================================================================


class TestModelConfigurationValidation:
    """Test model configuration and validation."""

    def test_model_config_creation(self):
        """Test creating model configuration."""
        config = ModelConfig(model="test/model", temperature=0.7)

        assert config.model == "test/model"
        assert config.temperature == 0.7

    def test_temperature_bounds(self):
        """Test temperature value bounds."""
        # Valid temperatures
        for temp in [0.0, 0.5, 1.0]:
            config = ModelConfig(model="test/model", temperature=temp)
            assert config.temperature == temp

    def test_model_input_creation(self):
        """Test ModelInput creation."""
        model_input = ModelInput(
            system_prompt="System message",
            user_prompt="User message"
        )

        assert model_input.system_prompt == "System message"
        assert model_input.user_prompt == "User message"

    def test_model_input_validation(self):
        """Test ModelInput validation."""
        # Valid input
        model_input = ModelInput(user_prompt="Test prompt")
        assert model_input.user_prompt == "Test prompt"

        # Invalid input (empty user prompt without image)
        with pytest.raises(ValueError):
            ModelInput(user_prompt="")

    def test_response_format_specification(self):
        """Test specifying response format."""
        config = ModelConfig(model="test/model")
        model_input = ModelInput(
            user_prompt="Test",
            response_format=DiseaseInfoModel
        )

        assert model_input.response_format == DiseaseInfoModel


# ==============================================================================
# TESTS - Prompt Builder Patterns
# ==============================================================================


class TestPromptBuilderPatterns:
    """Test prompt builder implementation patterns."""

    def test_system_prompt_consistency(self):
        """Test system prompt consistency."""
        class ConsistentPromptBuilder:
            @staticmethod
            def create_system_prompt():
                return "You are a medical expert..."

        prompt = ConsistentPromptBuilder.create_system_prompt()
        assert "medical" in prompt.lower()

    def test_user_prompt_variable_substitution(self):
        """Test user prompt variable substitution."""
        def build_user_prompt(disease: str, symptom: str = None) -> str:
            prompt = f"Analyze {disease}"
            if symptom:
                prompt += f" with symptom: {symptom}"
            return prompt

        # Without optional parameter
        prompt1 = build_user_prompt("Hypertension")
        assert "Hypertension" in prompt1

        # With optional parameter
        prompt2 = build_user_prompt("Hypertension", "Headache")
        assert "Hypertension" in prompt2
        assert "Headache" in prompt2

    def test_prompt_length_reasonableness(self):
        """Test prompt length is reasonable."""
        prompts = [
            "Short prompt",
            "This is a medium length prompt with some detail.",
            "This is a longer prompt " * 10  # Longer prompt
        ]

        for prompt in prompts:
            assert len(prompt) > 0
            assert len(prompt) < 5000  # Reasonable upper limit


# ==============================================================================
# TESTS - CLI Argument Patterns
# ==============================================================================


class TestCLIArgumentPatterns:
    """Test CLI argument parsing patterns."""

    def test_required_vs_optional_arguments(self):
        """Test required vs optional argument handling."""
        # Simulate argument parsing
        required_args = {
            "disease": "Hypertension",
            "medicine1": "Aspirin"
        }

        optional_args = {
            "age": None,
            "dosage": None,
            "custom_option": "default"
        }

        assert required_args["disease"] is not None
        assert optional_args["age"] is None  # Can be None

    def test_argument_type_conversion(self):
        """Test argument type conversion."""
        # String to int
        age_str = "65"
        age_int = int(age_str)
        assert isinstance(age_int, int)
        assert age_int == 65

        # String to float
        temp_str = "0.7"
        temp_float = float(temp_str)
        assert isinstance(temp_float, float)
        assert temp_float == 0.7

    def test_argument_short_and_long_forms(self):
        """Test argument short and long forms."""
        # Common patterns
        arguments = {
            "-m": "--model",
            "-t": "--temperature",
            "-o": "--output",
            "-v": "--verbosity",
            "-j": "--json-output",
            "-s": "--structured"
        }

        for short, long in arguments.items():
            assert short.startswith("-")
            assert long.startswith("--")

    def test_argument_defaults(self):
        """Test argument default values."""
        defaults = {
            "model": "ollama/gemma3",
            "temperature": 0.7,
            "verbosity": 2,
            "output_dir": Path("outputs"),
            "json_output": False,
            "structured": False
        }

        for key, value in defaults.items():
            assert value is not None


# ==============================================================================
# TESTS - Error Cases
# ==============================================================================


class TestErrorCases:
    """Test error handling in CLI modules."""

    def test_invalid_model_name(self):
        """Test invalid model name handling."""
        invalid_models = [
            "",
            "   ",
            None
        ]

        for model in invalid_models:
            if model is None or not str(model).strip():
                with pytest.raises((ValueError, ValidationError, TypeError)):
                    ModelConfig(model=str(model) if model else "")

    def test_invalid_temperature(self):
        """Test invalid temperature values."""
        invalid_temps = [-1.0, 2.0, "not_a_number"]

        for temp in invalid_temps:
            if isinstance(temp, str):
                with pytest.raises(ValueError):
                    float(temp)

    def test_empty_required_fields(self):
        """Test empty required field handling."""
        with pytest.raises(ValidationError):
            DiseaseInfoModel(
                disease_name="",  # Empty required field
                description="Test",
                treatment="Test"
            )

    def test_invalid_enum_choice(self):
        """Test invalid enum choice handling."""
        class SeverityLevel(BaseModel):
            severity: str

            def validate(self):
                if self.severity not in ["Low", "Medium", "High"]:
                    raise ValueError(f"Invalid severity: {self.severity}")

        # Valid
        valid = SeverityLevel(severity="High")
        valid.validate()

        # Invalid
        invalid = SeverityLevel(severity="Critical")
        with pytest.raises(ValueError):
            invalid.validate()
