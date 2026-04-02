#!/usr/bin/env python3
"""
Unit tests for recognizer modules using mocking.

These tests mock the LLM client to avoid requiring actual model inference.
Run with: pytest tests/test_recognizers_unit.py -v
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from lite.config import ModelConfig

from app.MedKit.recognizers.base_recognizer import BaseRecognizer
from app.MedKit.recognizers.models import ModelOutput
from app.MedKit.recognizers.recognizer_factory import RecognizerFactory


class TestBaseRecognizer:
    """Tests for BaseRecognizer abstract class."""

    def test_base_recognizer_is_abstract(self):
        """Test that BaseRecognizer cannot be instantiated directly."""
        config = ModelConfig(model="test", temperature=0.2)
        with pytest.raises(TypeError):
            BaseRecognizer(config)

    @pytest.mark.parametrize(
        "recognizer_name",
        [
            "drug",
            "disease",
            "condition",
            "clinical_sign",
            "procedure",
            "med_class",
            "imaging",
            "vaccine",
            "genetic",
            "supplement",
            "test",
            "coding",
            "device",
            "pathogen",
            "anatomy",
            "abbreviation",
            "lab_unit",
            "symptom",
            "specialty",
        ],
    )
    def test_factory_creates_all_recognizers(self, recognizer_name):
        """Test that factory can create all registered recognizers."""
        config = ModelConfig(model="test", temperature=0.2)
        recognizer = RecognizerFactory.get(recognizer_name, config)
        assert recognizer is not None
        assert isinstance(recognizer, BaseRecognizer)
        assert hasattr(recognizer, "identify")

    def test_model_config_creation(self):
        """Test ModelConfig creation and attributes."""
        config = ModelConfig(model="ollama/gemma3", temperature=0.2)
        assert config.model == "ollama/gemma3"
        assert config.temperature == 0.2


class TestModelOutput:
    """Tests for ModelOutput class."""

    def test_model_output_with_data(self):
        """Test ModelOutput with data field."""
        mock_data = {"key": "value"}
        output = ModelOutput(data=mock_data)
        assert output.data == mock_data
        assert output.markdown is None
        assert output.metadata == {}

    def test_model_output_with_markdown(self):
        """Test ModelOutput with markdown field."""
        output = ModelOutput(markdown="# Test")
        assert output.data is None
        assert output.markdown == "# Test"

    def test_model_output_with_metadata(self):
        """Test ModelOutput with metadata."""
        metadata = {"source": "test", "version": 1}
        output = ModelOutput(data={}, metadata=metadata)
        assert output.metadata == metadata

    def test_model_output_empty(self):
        """Test empty ModelOutput."""
        output = ModelOutput()
        assert output.data is None
        assert output.markdown is None
        assert output.metadata == {}


class TestRecognizerBehavior:
    """Tests for recognizer behavior with mocked LLM client."""

    @pytest.fixture
    def mock_config(self):
        """Create a test model config."""
        return ModelConfig(model="test/model", temperature=0.2)

    @pytest.mark.parametrize(
        "recognizer_name,test_input",
        [
            ("drug", "Aspirin"),
            ("disease", "Diabetes"),
            ("condition", "Hypertension"),
            ("clinical_sign", "Babinski sign"),
            ("procedure", "Appendectomy"),
            ("vaccine", "MMR"),
            ("anatomy", "heart"),
            ("symptom", "chest pain"),
            ("specialty", "Cardiology"),
        ],
    )
    def test_identify_returns_markdown(self, mock_config, recognizer_name, test_input):
        """Test that identify returns proper ModelOutput with markdown."""
        with patch("app.MedKit.recognizers.base_recognizer.LiteClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_instance.generate_text.return_value = "Test response"

            recognizer = RecognizerFactory.get(recognizer_name, mock_config)
            result = recognizer.identify(test_input, structured=False)

            assert isinstance(result, ModelOutput)
            assert result.markdown == "Test response"
            assert result.data is None

    @pytest.mark.parametrize(
        "recognizer_name,test_input",
        [
            ("drug", "Aspirin"),
            ("disease", "Diabetes"),
            ("procedure", "Appendectomy"),
            ("vaccine", "MMR"),
        ],
    )
    def test_identify_returns_structured_data(
        self, mock_config, recognizer_name, test_input
    ):
        """Test that identify returns proper ModelOutput with structured data."""
        with patch("app.MedKit.recognizers.base_recognizer.LiteClient") as MockClient:
            mock_instance = MockClient.return_value
            mock_response = MagicMock()
            mock_response.drug_name = test_input
            mock_response.is_well_known = True
            mock_instance.generate_text.return_value = mock_response

            recognizer = RecognizerFactory.get(recognizer_name, mock_config)
            result = recognizer.identify(test_input, structured=True)

            assert isinstance(result, ModelOutput)
            assert result.data is not None
            assert result.markdown is None


class TestInputValidation:
    """Tests for input validation across recognizers."""

    @pytest.mark.parametrize(
        "InputClass,empty_value",
        [
            ("DrugIdentifierInput", ""),
            ("DiseaseIdentifierInput", ""),
            ("MedicalAnatomyIdentifierInput", ""),
            ("MedicalConditionIdentifierInput", ""),
            ("MedicalProcedureIdentifierInput", ""),
            ("MedicalSymptomIdentifierInput", ""),
            ("MedicalVaccineIdentifierInput", ""),
            ("MedicalSpecialtyIdentifierInput", ""),
        ],
    )
    def test_empty_input_raises_error(self, InputClass, empty_value):
        """Test that empty input raises ValueError."""
        from app.MedKit.recognizers.drug.shared.drug_recognizer_prompts import (
            DrugIdentifierInput,
        )
        from app.MedKit.recognizers.disease.shared.disease_identifier_prompts import (
            DiseaseIdentifierInput,
        )
        from app.MedKit.recognizers.med_anatomy.shared.med_anatomy_identifier_prompts import (
            MedicalAnatomyIdentifierInput,
        )
        from app.MedKit.recognizers.med_condition.shared.med_condition_prompts import (
            MedicalConditionIdentifierInput,
        )
        from app.MedKit.recognizers.med_procedure.shared.med_procedure_prompts import (
            MedicalProcedureIdentifierInput,
        )
        from app.MedKit.recognizers.med_symptom.shared.med_symptom_prompts import (
            MedicalSymptomIdentifierInput,
        )
        from app.MedKit.recognizers.med_vaccine.shared.med_vaccine_prompts import (
            VaccineIdentifierInput,
        )
        from app.MedKit.recognizers.med_specialty.shared.med_specialty_prompts import (
            MedicalSpecialtyIdentifierInput,
        )

        input_map = {
            "DrugIdentifierInput": DrugIdentifierInput,
            "DiseaseIdentifierInput": DiseaseIdentifierInput,
            "MedicalAnatomyIdentifierInput": MedicalAnatomyIdentifierInput,
            "MedicalConditionIdentifierInput": MedicalConditionIdentifierInput,
            "MedicalProcedureIdentifierInput": MedicalProcedureIdentifierInput,
            "MedicalSymptomIdentifierInput": MedicalSymptomIdentifierInput,
            "MedicalVaccineIdentifierInput": VaccineIdentifierInput,
            "MedicalSpecialtyIdentifierInput": MedicalSpecialtyIdentifierInput,
        }

        InputClassRef = input_map[InputClass]
        with pytest.raises(ValueError):
            InputClassRef(empty_value)

    @pytest.mark.parametrize(
        "InputClass",
        [
            "DrugIdentifierInput",
            "DiseaseIdentifierInput",
            "MedicalAnatomyIdentifierInput",
        ],
    )
    def test_whitespace_input_raises_error(self, InputClass):
        """Test that whitespace-only input raises ValueError."""
        from app.MedKit.recognizers.drug.shared.drug_recognizer_prompts import (
            DrugIdentifierInput,
        )
        from app.MedKit.recognizers.disease.shared.disease_identifier_prompts import (
            DiseaseIdentifierInput,
        )
        from app.MedKit.recognizers.med_anatomy.shared.med_anatomy_identifier_prompts import (
            MedicalAnatomyIdentifierInput,
        )

        input_map = {
            "DrugIdentifierInput": DrugIdentifierInput,
            "DiseaseIdentifierInput": DiseaseIdentifierInput,
            "MedicalAnatomyIdentifierInput": MedicalAnatomyIdentifierInput,
        }

        InputClassRef = input_map[InputClass]
        with pytest.raises(ValueError):
            InputClassRef("   ")


class TestPromptBuilders:
    """Tests for prompt builder functionality."""

    def test_drug_prompt_builder(self):
        """Test DrugIdentifierInput and PromptBuilder."""
        from app.MedKit.recognizers.drug.shared.drug_recognizer_prompts import (
            DrugIdentifierInput,
            PromptBuilder,
        )

        test_input = DrugIdentifierInput("Aspirin")
        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(test_input)

        assert len(system_prompt) > 0
        assert "Aspirin" in user_prompt

    def test_disease_prompt_builder(self):
        """Test DiseaseIdentifierInput and PromptBuilder."""
        from app.MedKit.recognizers.disease.shared.disease_identifier_prompts import (
            DiseaseIdentifierInput,
            PromptBuilder,
        )

        test_input = DiseaseIdentifierInput("Diabetes")
        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(test_input)

        assert len(system_prompt) > 0
        assert "Diabetes" in user_prompt

    def test_anatomy_prompt_builder(self):
        """Test MedicalAnatomyIdentifierInput and PromptBuilder."""
        from app.MedKit.recognizers.med_anatomy.shared.med_anatomy_identifier_prompts import (
            MedicalAnatomyIdentifierInput,
            PromptBuilder,
        )

        test_input = MedicalAnatomyIdentifierInput("heart")
        system_prompt = PromptBuilder.create_system_prompt()
        user_prompt = PromptBuilder.create_user_prompt(test_input)

        assert len(system_prompt) > 0
        assert "heart" in user_prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
