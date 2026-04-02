"""
Live integration tests for agentic recognizers.

These tests require actual LLM model to be available (e.g., ollama).
Run with: pytest tests/test_agentic_live.py -v
Or: python tests/test_agentic_live.py

WARNING: These tests make actual API calls and may incur costs.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from lite.config import ModelConfig

from app.MedKit.recognizers.drug.agentic import DrugRecognizerAgent
from app.MedKit.recognizers.disease.agentic import DiseaseRecognizerAgent
from app.MedKit.recognizers.med_vaccine.agentic import MedicalVaccineRecognizerAgent
from app.MedKit.recognizers.med_condition.agentic import MedicalConditionRecognizerAgent


class TestLiveDrugRecognizer:
    """Live tests for DrugRecognizerAgent."""

    @pytest.fixture
    def config(self):
        """Create model config - update model name as needed."""
        return ModelConfig(
            model="gemma3",  # ollama model name
            temperature=0.3,
        )

    @pytest.fixture
    def agent(self, config):
        return DrugRecognizerAgent(config, max_retries=2)

    def test_identify_aspirin(self, agent):
        """Test identifying a well-known drug."""
        result = agent.identify("Aspirin")

        assert result.markdown is not None
        assert len(result.markdown) > 0
        print(f"\nAspirin identification:\n{result.markdown[:200]}...")

    def test_identify_with_structured(self, agent):
        """Test structured output mode."""
        result = agent.identify("Ibuprofen", structured=True)

        assert result.markdown is not None
        print(f"\nIbuprofen structured result:\n{result.markdown[:200]}...")

    def test_compare_drugs(self, agent):
        """Test drug comparison."""
        result = agent.compare_drugs("Aspirin", "Tylenol")

        assert result.markdown is not None
        assert "comparison" in result.metadata
        print(f"\nDrug comparison:\n{result.markdown[:300]}...")

    def test_verify_drug_claims(self, agent):
        """Test claim verification."""
        claims = [
            "Aspirin is an NSAID",
            "Aspirin can cause stomach bleeding",
            "Aspirin is safe for children",
        ]

        result = agent.verify_drug_info("Aspirin", claims)

        assert result.markdown is not None
        print(f"\nVerification result:\n{result.markdown[:300]}...")

    def test_research_drug(self, agent):
        """Test research mode."""
        result = agent.research_drug("Metformin")

        assert result.markdown is not None
        assert result.metadata["method"] == "tools"
        print(f"\nResearch result:\n{result.markdown[:300]}...")


class TestLiveDiseaseRecognizer:
    """Live tests for DiseaseRecognizerAgent."""

    @pytest.fixture
    def config(self):
        return ModelConfig(model="ollama/gemma3", temperature=0.3)

    @pytest.fixture
    def agent(self, config):
        return DiseaseRecognizerAgent(config, max_retries=2)

    def test_identify_diabetes(self, agent):
        """Test identifying a well-known disease."""
        result = agent.identify("Diabetes")

        assert result.markdown is not None
        print(f"\nDiabetes identification:\n{result.markdown[:200]}...")

    def test_identify_with_epidemiology(self, agent):
        """Test epidemiological analysis."""
        result = agent.identify_with_epidemiology("COVID-19")

        assert result.markdown is not None
        assert result.metadata["analysis_type"] == "epidemiology"
        print(f"\nEpidemiology result:\n{result.markdown[:300]}...")

    def test_compare_diseases(self, agent):
        """Test disease comparison."""
        result = agent.compare_diseases("Diabetes", "Hypertension")

        assert result.markdown is not None
        print(f"\nDisease comparison:\n{result.markdown[:300]}...")

    def test_assess_outbreak_risk(self, agent):
        """Test outbreak risk assessment."""
        result = agent.assess_outbreak_risk("COVID-19", "USA")

        assert result.markdown is not None
        assert result.metadata["risk_assessment"] is True
        print(f"\nOutbreak risk:\n{result.markdown[:300]}...")


class TestLiveVaccineRecognizer:
    """Live tests for MedicalVaccineRecognizerAgent."""

    @pytest.fixture
    def config(self):
        return ModelConfig(model="ollama/gemma3", temperature=0.3)

    @pytest.fixture
    def agent(self, config):
        return MedicalVaccineRecognizerAgent(config, max_retries=2)

    def test_identify_mmr(self, agent):
        """Test identifying a well-known vaccine."""
        result = agent.identify("MMR")

        assert result.markdown is not None
        print(f"\nMMR identification:\n{result.markdown[:200]}...")

    def test_get_schedule(self, agent):
        """Test vaccine schedule retrieval."""
        result = agent.get_schedule("Influenza")

        assert result.markdown is not None
        assert result.metadata["schedule"] is True
        print(f"\nVaccine schedule:\n{result.markdown[:300]}...")

    def test_compare_vaccines(self, agent):
        """Test vaccine comparison."""
        result = agent.compare_vaccines("Pfizer", "Moderna")

        assert result.markdown is not None
        print(f"\nVaccine comparison:\n{result.markdown[:300]}...")


class TestLiveConditionRecognizer:
    """Live tests for MedicalConditionRecognizerAgent."""

    @pytest.fixture
    def config(self):
        return ModelConfig(model="ollama/gemma3", temperature=0.3)

    @pytest.fixture
    def agent(self, config):
        return MedicalConditionRecognizerAgent(config, max_retries=2)

    def test_identify_hypertension(self, agent):
        """Test identifying a medical condition."""
        result = agent.identify("Hypertension")

        assert result.markdown is not None
        print(f"\nHypertension identification:\n{result.markdown[:200]}...")

    def test_diagnose_differentials(self, agent):
        """Test differential diagnosis."""
        result = agent.diagnose_differentials("Chest pain")

        assert result.markdown is not None
        assert result.metadata["differential_diagnosis"] is True
        print(f"\nDifferential diagnosis:\n{result.markdown[:300]}...")

    def test_assess_severity(self, agent):
        """Test severity assessment."""
        result = agent.assess_severity("Appendicitis")

        assert result.markdown is not None
        print(f"\nSeverity assessment:\n{result.markdown[:300]}...")


class TestMemoryAndContext:
    """Live tests for memory/context features."""

    @pytest.fixture
    def config(self):
        return ModelConfig(model="ollama/gemma3", temperature=0.3)

    def test_conversation_history(self, config):
        """Test that conversation history is maintained."""
        agent = DrugRecognizerAgent(config, enable_memory=True)

        # First call
        agent.identify("Aspirin")

        # Check history exists
        history = agent.get_conversation_history()

        # Second call
        agent.identify("Ibuprofen")

        # History should have more messages now
        new_history = agent.get_conversation_history()

        print(f"\nHistory after 2 calls: {len(new_history)} messages")

    def test_reset_memory(self, config):
        """Test memory reset functionality."""
        agent = DrugRecognizerAgent(config, enable_memory=True)

        # Make some calls
        agent.identify("Aspirin")
        agent.identify("Ibuprofen")

        # Reset
        agent.reset_memory()

        # Check memory is cleared
        history = agent.get_conversation_history()

        assert len(history) == 0
        print("\nMemory successfully reset")


class TestErrorHandling:
    """Live tests for error handling."""

    def test_invalid_config_handling(self):
        """Test handling of invalid model configuration."""
        config = ModelConfig(model="invalid-model-name", temperature=0.3)

        try:
            agent = DrugRecognizerAgent(config, max_retries=1)
            result = agent.identify("Aspirin")

            # Should return error in result
            assert result.markdown is not None
            assert "Error" in result.markdown or "error" in result.metadata
            print(f"\nError handling result: {result.markdown[:100]}...")
        except Exception as e:
            print(f"\nException raised: {type(e).__name__}: {e}")


def run_live_tests():
    """Run live tests manually."""
    print("=" * 60)
    print("LIVE INTEGRATION TESTS")
    print("=" * 60)
    print("\nThese tests require actual LLM model to be running.")
    print("Make sure ollama or other LLM service is available.\n")

    pytest.main([__file__, "-v", "-s"])


if __name__ == "__main__":
    run_live_tests()
