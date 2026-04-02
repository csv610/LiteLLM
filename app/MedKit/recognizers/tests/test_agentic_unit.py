"""
Unit tests for agentic recognizers.

These tests mock the LLM client to avoid requiring actual model inference.
Run with: pytest tests/test_agentic_unit.py -v
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from lite.config import ModelConfig

from app.MedKit.recognizers.base_agentic_recognizer import BaseAgenticRecognizer
from app.MedKit.recognizers.models import ModelOutput
from app.MedKit.recognizers.drug.agentic import DrugRecognizerAgent
from app.MedKit.recognizers.disease.agentic import DiseaseRecognizerAgent
from app.MedKit.recognizers.med_condition.agentic import MedicalConditionRecognizerAgent
from app.MedKit.recognizers.med_procedure.agentic import MedicalProcedureRecognizerAgent
from app.MedKit.recognizers.med_specialty.agentic import MedicalSpecialtyRecognizerAgent
from app.MedKit.recognizers.med_device.agentic import MedicalDeviceRecognizerAgent
from app.MedKit.recognizers.med_coding.agentic import MedicalCodingRecognizerAgent
from app.MedKit.recognizers.med_pathogen.agentic import MedicalPathogenRecognizerAgent
from app.MedKit.recognizers.genetic_variant.agentic import GeneticVariantRecognizerAgent
from app.MedKit.recognizers.med_anatomy.agentic import MedicalAnatomyRecognizerAgent
from app.MedKit.recognizers.med_test.agentic import MedicalTestRecognizerAgent
from app.MedKit.recognizers.imaging_finding.agentic import ImagingFindingRecognizerAgent
from app.MedKit.recognizers.med_symptom.agentic import MedicalSymptomRecognizerAgent
from app.MedKit.recognizers.med_vaccine.agentic import MedicalVaccineRecognizerAgent
from app.MedKit.recognizers.lab_unit.agentic import LabUnitRecognizerAgent
from app.MedKit.recognizers.med_abbreviation.agentic import (
    MedicalAbbreviationRecognizerAgent,
)
from app.MedKit.recognizers.med_supplement.agentic import (
    MedicalSupplementRecognizerAgent,
)
from app.MedKit.recognizers.medication_class.agentic import (
    MedicationClassRecognizerAgent,
)
from app.MedKit.recognizers.clinical_sign.agentic import ClinicalSignRecognizerAgent
from agno.tools.websearch import WebSearchTools


ALL_AGENTIC_RECOGNIZERS = [
    ("drug", DrugRecognizerAgent),
    ("disease", DiseaseRecognizerAgent),
    ("med_condition", MedicalConditionRecognizerAgent),
    ("med_procedure", MedicalProcedureRecognizerAgent),
    ("med_specialty", MedicalSpecialtyRecognizerAgent),
    ("med_device", MedicalDeviceRecognizerAgent),
    ("med_coding", MedicalCodingRecognizerAgent),
    ("med_pathogen", MedicalPathogenRecognizerAgent),
    ("genetic_variant", GeneticVariantRecognizerAgent),
    ("med_anatomy", MedicalAnatomyRecognizerAgent),
    ("med_test", MedicalTestRecognizerAgent),
    ("imaging_finding", ImagingFindingRecognizerAgent),
    ("med_symptom", MedicalSymptomRecognizerAgent),
    ("med_vaccine", MedicalVaccineRecognizerAgent),
    ("lab_unit", LabUnitRecognizerAgent),
    ("med_abbreviation", MedicalAbbreviationRecognizerAgent),
    ("med_supplement", MedicalSupplementRecognizerAgent),
    ("medication_class", MedicationClassRecognizerAgent),
    ("clinical_sign", ClinicalSignRecognizerAgent),
]


class TestBaseAgenticRecognizer:
    """Tests for BaseAgenticRecognizer abstract class."""

    def test_cannot_instantiate_directly(self):
        """Test that BaseAgenticRecognizer cannot be instantiated directly."""
        config = ModelConfig(model="test", temperature=0.2)

        with pytest.raises(TypeError):
            BaseAgenticRecognizer(config)

    def test_drug_recognizer_inherits_base(self):
        """Test that DrugRecognizerAgent inherits from BaseAgenticRecognizer."""
        config = ModelConfig(model="test", temperature=0.2)

        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(content="Test response")
            MockAgent.return_value = mock_agent

            agent = DrugRecognizerAgent(config)

            assert isinstance(agent, BaseAgenticRecognizer)
            assert hasattr(agent, "_agent")
            assert hasattr(agent, "max_retries")

    def test_default_retries(self):
        """Test default retry configuration."""
        config = ModelConfig(model="test", temperature=0.2)

        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(content="Test response")
            MockAgent.return_value = mock_agent

            agent = DrugRecognizerAgent(config)

            assert agent.max_retries == 3

    def test_custom_retries(self):
        """Test custom retry configuration."""
        config = ModelConfig(model="test", temperature=0.2)

        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(content="Test response")
            MockAgent.return_value = mock_agent

            agent = DrugRecognizerAgent(config, max_retries=5)

            assert agent.max_retries == 5


@pytest.mark.parametrize("name,agent_class", ALL_AGENTIC_RECOGNIZERS)
class TestAllRecognizers:
    """Parameterized tests for all agentic recognizers."""

    def test_instantiation(self, name, agent_class):
        """Test that each recognizer can be instantiated."""
        config = ModelConfig(model="test", temperature=0.2)

        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(content="Test")
            MockAgent.return_value = mock_agent

            agent = agent_class(config)
            assert agent is not None
            assert hasattr(agent, "max_retries")

    def test_identify_returns_model_output(self, name, agent_class):
        """Test that identify returns ModelOutput."""
        config = ModelConfig(model="test", temperature=0.2)

        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(content="Test result")
            MockAgent.return_value = mock_agent

            agent = agent_class(config)
            result = agent.identify("test entity")

            assert isinstance(result, ModelOutput)
            assert result.markdown == "Test result"


class TestWebSearchTools:
    """Tests for WebSearchTools integration."""

    def test_websearch_tools_added_to_agent(self):
        """Test that WebSearchTools is added to agent tools."""
        config = ModelConfig(model="test", temperature=0.2)

        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(content="Test")
            MockAgent.return_value = mock_agent

            agent = DrugRecognizerAgent(config)

            call_kwargs = MockAgent.call_args[1]
            tools = call_kwargs.get("tools", [])

            assert any(isinstance(t, WebSearchTools) for t in tools)


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_name_returns_error(self):
        """Test that empty name returns error."""
        config = ModelConfig(model="test", temperature=0.2)

        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(content="Test")
            MockAgent.return_value = mock_agent

            agent = DrugRecognizerAgent(config)
            result = agent.identify("")

            assert "Error" in result.markdown or "Error" in str(
                result.metadata.get("error", "")
            )

    def test_max_retries_exceeded(self):
        """Test that max retries returns error after all attempts fail."""
        config = ModelConfig(model="test", temperature=0.2)

        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.side_effect = Exception("API Error")
            MockAgent.return_value = mock_agent

            agent = DrugRecognizerAgent(config, max_retries=3)
            result = agent.identify("Aspirin")

            assert "error" in result.metadata
            assert mock_agent.run.call_count == 3

    def test_all_retries_fail_returns_error_with_attempts(self):
        """Test error metadata includes attempt count."""
        config = ModelConfig(model="test", temperature=0.2)

        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.side_effect = Exception("API Error")
            MockAgent.return_value = mock_agent

            agent = DrugRecognizerAgent(config, max_retries=2)
            result = agent.identify("Aspirin")

            assert result.metadata.get("attempts") == 2


class TestDrugRecognizerAgent:
    """Tests for DrugRecognizerAgent."""

    @pytest.fixture
    def mock_config(self):
        return ModelConfig(model="test/model", temperature=0.2)

    @pytest.fixture
    def agent(self, mock_config):
        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(
                content="Aspirin is a well-known drug"
            )
            MockAgent.return_value = mock_agent

            return DrugRecognizerAgent(mock_config)

    def test_identify_returns_markdown(self, agent):
        result = agent.identify("Aspirin", structured=False)

        assert isinstance(result, ModelOutput)
        assert result.markdown == "Aspirin is a well-known drug"
        assert result.data is None

    def test_identify_with_structured(self, agent):
        mock_response = MagicMock()
        mock_response.content = "Test content"
        mock_response.parse.return_value = MagicMock(
            drug_name="Aspirin", is_well_known=True
        )

        agent._agent.run.return_value = mock_response

        result = agent.identify("Aspirin", structured=True)

        assert isinstance(result, ModelOutput)
        assert result.data is not None

    def test_identify_with_tools(self, agent):
        result = agent.identify_with_tools("Aspirin")

        assert isinstance(result, ModelOutput)
        assert result.metadata["method"] == "tools"
        assert result.metadata["entity_name"] == "Aspirin"

    def test_reset_memory(self, agent):
        agent._agent.history = ["old message"]

        agent.reset_memory()

        assert agent._agent.history == []

    def test_error_handling_retries(self, mock_config):
        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.side_effect = [
                Exception("Error 1"),
                Exception("Error 2"),
                MagicMock(content="Success"),
            ]
            MockAgent.return_value = mock_agent

            agent = DrugRecognizerAgent(mock_config, max_retries=3)
            result = agent.identify("Aspirin")

            assert mock_agent.run.call_count == 3


class TestDiseaseRecognizerAgent:
    """Tests for DiseaseRecognizerAgent."""

    @pytest.fixture
    def mock_config(self):
        return ModelConfig(model="test/model", temperature=0.2)

    @pytest.fixture
    def agent(self, mock_config):
        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(
                content="Diabetes is a well-known disease"
            )
            MockAgent.return_value = mock_agent

            return DiseaseRecognizerAgent(mock_config)

    def test_identify_returns_markdown(self, agent):
        result = agent.identify("Diabetes", structured=False)

        assert isinstance(result, ModelOutput)
        assert "Diabetes" in result.markdown


class TestCompareMethod:
    """Tests for the generic compare method."""

    @pytest.fixture
    def mock_config(self):
        return ModelConfig(model="test/model", temperature=0.2)

    @pytest.fixture
    def agent(self, mock_config):
        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(content="Comparison result")
            MockAgent.return_value = mock_agent

            return DrugRecognizerAgent(mock_config)

    def test_compare_two_entities(self, agent):
        result = agent.compare("Aspirin", "Ibuprofen")

        assert isinstance(result, ModelOutput)
        assert result.metadata["entity1"] == "Aspirin"
        assert result.metadata["entity2"] == "Ibuprofen"

    def test_verify_method(self, agent):
        claims = ["Claim 1", "Claim 2"]

        result = agent.verify("Aspirin", claims)

        assert isinstance(result, ModelOutput)
        assert result.metadata["entity_name"] == "Aspirin"
        assert result.metadata["claims"] == claims


class TestMemoryManagement:
    """Tests for memory management."""

    @pytest.fixture
    def mock_config(self):
        return ModelConfig(model="test/model", temperature=0.2)

    @pytest.fixture
    def agent(self, mock_config):
        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(content="Test")
            mock_agent.history = []
            MockAgent.return_value = mock_agent

            return DrugRecognizerAgent(mock_config, enable_memory=True)

    def test_get_conversation_history(self, agent):
        agent._agent.history = [{"role": "user", "content": "Hello"}]

        history = agent.get_conversation_history()

        assert len(history) == 1
        assert history[0]["content"] == "Hello"

    def test_disable_memory(self, mock_config):
        with patch("app.MedKit.recognizers.base_agentic_recognizer.Agent") as MockAgent:
            mock_agent = MagicMock()
            mock_agent.run.return_value = MagicMock(content="Test")
            MockAgent.return_value = mock_agent

            agent = DrugRecognizerAgent(mock_config, enable_memory=False)

            call_kwargs = MockAgent.call_args[1]
            assert call_kwargs["add_history_to_context"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
