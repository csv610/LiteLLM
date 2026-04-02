"""
Mock tests for ScholarWorkGenerator
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from ScholarWork.nonagentic.scholar_work_generator import ScholarWorkGenerator
from ScholarWork.nonagentic.scholar_work_models import ScholarMajorWork
from lite.config import ModelConfig, ModelInput


class TestScholarWorkGeneratorMock(unittest.TestCase):
    """Mock tests for ScholarWorkGenerator"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.model_config = ModelConfig(model="test-model", temperature=0.7)
        self.generator = ScholarWorkGenerator(model_name="test-model", temperature=0.7)

    @patch("ScholarWork.nonagentic.scholar_work_generator.LiteClient")
    def test_generate_text_success(self, mock_lite_client):
        """Test successful text generation with mocked LiteClient"""
        # Arrange
        expected_result = ScholarMajorWork(
            scholar_name="Albert Einstein",
            title="Einstein's Revolutionary Contributions",
            subtitle="From Relativity to Quantum Theory",
            major_contributions=[
                "Albert Einstein developed the theory of relativity, which fundamentally changed our understanding of space, time, and gravity. His special theory of relativity (1905) introduced the concept that the laws of physics are the same for all non-accelerating observers, and that the speed of light in a vacuum is constant regardless of the motion of the light source.",
                "Einstein's explanation of the photoelectric effect (1905) proposed that light is made up of particles called photons, which was crucial for the development of quantum mechanics and earned him the Nobel Prize in Physics in 1921.",
                "His work on Brownian motion (1905) provided empirical evidence for the existence of atoms and molecules, helping to settle a long-standing debate in physics and chemistry.",
                "The general theory of relativity (1915) expanded upon special relativity to include gravity, describing it as the curvature of spacetime caused by mass and energy.",
                "Einstein also made significant contributions to statistical mechanics and quantum theory, including his work on quantum statistics and the Einstein-Podolsky-Rosen paradox.",
            ],
            key_terms="Relativity: The theory that describes the relationship between space, time, and gravity. Photoelectric effect: The emission of electrons when light shines on a material. Brownian motion: The random movement of particles suspended in a fluid.",
            impact_summary="Einstein's work laid the foundation for modern physics, influencing everything from nuclear energy and GPS technology to our understanding of the cosmos. His theories continue to be tested and confirmed by modern experiments.",
            discussion_questions=[
                "How did Einstein's theories change our understanding of the universe?",
                "What practical applications have emerged from Einstein's theoretical work?",
                "How might Einstein's approach to problem-solving inform scientific research today?",
                "What aspects of Einstein's work remain controversial or not fully understood?",
                "How did Einstein's personal beliefs and experiences influence his scientific work?",
            ],
        )

        # Configure the mock to return our expected result
        mock_client_instance = MagicMock()
        mock_client_instance.generate_text.return_value = expected_result
        mock_lite_client.return_value = mock_client_instance

        # Recreate generator with mocked client
        generator = ScholarWorkGenerator(model_name="test-model", temperature=0.7)
        generator.client = mock_client_instance

        # Act
        result = generator.generate_text("Albert Einstein")

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.scholar_name, "Albert Einstein")
        self.assertEqual(result.title, "Einstein's Revolutionary Contributions")
        self.assertEqual(len(result.major_contributions), 5)
        self.assertIn("theory of relativity", result.major_contributions[0].lower())
        self.assertEqual(len(result.discussion_questions), 5)

        # Verify the mock was called correctly
        mock_client_instance.generate_text.assert_called_once()
        call_args = mock_client_instance.generate_text.call_args
        self.assertIn("model_input", call_args.kwargs)
        model_input = call_args.kwargs["model_input"]
        self.assertIsInstance(model_input, ModelInput)
        # Check that the user prompt contains the scholar name
        self.assertIn("Albert Einstein", model_input.user_prompt)
        self.assertEqual(
            model_input.system_prompt,
            "You are a meticulous science historian and archivist. You specialize in documenting the complete work and contributions of great scientists.\n\nYour approach:\n- You provide comprehensive lists of scientific contributions, not narrative stories.\n- You focus on precision, completeness, and clarity.\n- You explain each major work in detail, highlighting its revolutionary nature.\n- You respect your readers' intelligence while ensuring the science is clearly explained.\n- You categorize and list work to provide a clear overview of a scholar's career.\n\nYour strength is providing a thorough and authoritative account of scientific achievements.\n\nWrite detailed, informative entries for each major work and contribution.",
        )

    @patch("ScholarWork.nonagentic.scholar_work_generator.LiteClient")
    def test_generate_text_with_focus_area(self, mock_lite_client):
        """Test text generation with specific focus area"""
        # Arrange
        expected_result = ScholarMajorWork(
            scholar_name="Marie Curie",
            title="Curie's Radioactivity Research",
            subtitle="Pioneering Work in Radiation Science",
            major_contributions=[
                "Marie Curie conducted pioneering research on radioactivity."
            ],
            key_terms="Radioactivity: The process by which unstable atomic nuclei lose energy.",
            impact_summary="Her work opened new fields in physics and chemistry.",
            discussion_questions=["What was Curie's biggest contribution?"],
        )

        # Configure the mock
        mock_client_instance = MagicMock()
        mock_client_instance.generate_text.return_value = expected_result
        mock_lite_client.return_value = mock_client_instance

        # Recreate generator with mocked client
        generator = ScholarWorkGenerator(model_name="test-model", temperature=0.7)
        generator.client = mock_client_instance

        # Act
        result = generator.generate_text("Marie Curie", "their work on radioactivity")

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.scholar_name, "Marie Curie")
        mock_client_instance.generate_text.assert_called_once()
        call_args = mock_client_instance.generate_text.call_args
        self.assertIn("model_input", call_args.kwargs)
        model_input = call_args.kwargs["model_input"]
        self.assertIsInstance(model_input, ModelInput)
        # Check that the user prompt contains the scholar name
        self.assertIn("Marie Curie", model_input.user_prompt)
        self.assertEqual(
            model_input.system_prompt,
            "You are a meticulous science historian and archivist. You specialize in documenting the complete work and contributions of great scientists.\n\nYour approach:\n- You provide comprehensive lists of scientific contributions, not narrative stories.\n- You focus on precision, completeness, and clarity.\n- You explain each major work in detail, highlighting its revolutionary nature.\n- You respect your readers' intelligence while ensuring the science is clearly explained.\n- You categorize and list work to provide a clear overview of a scholar's career.\n\nYour strength is providing a thorough and authoritative account of scientific achievements.\n\nWrite detailed, informative entries for each major work and contribution.",
        )

    @patch("ScholarWork.nonagentic.scholar_work_generator.LiteClient")
    def test_update_model(self, mock_lite_client):
        """Test updating the model configuration"""
        # Arrange
        mock_client_instance = MagicMock()
        mock_lite_client.return_value = mock_client_instance

        generator = ScholarWorkGenerator(model_name="old-model", temperature=0.5)

        # Act
        generator.update_model("new-model", 0.8)

        # Assert
        self.assertEqual(generator.model_name, "new-model")
        self.assertEqual(generator.model_config.temperature, 0.8)
        # Verify that LiteClient was re-instantiated with new config
        self.assertEqual(
            mock_lite_client.call_count, 2
        )  # Called once in init, once in update_model

    @patch("ScholarWork.nonagentic.scholar_work_generator.LiteClient")
    def test_get_model_info(self, mock_lite_client):
        """Test getting model information"""
        # Arrange
        mock_client_instance = MagicMock()
        mock_lite_client.return_value = mock_client_instance

        generator = ScholarWorkGenerator(model_name="test-model", temperature=0.6)

        # Act
        info = generator.get_model_info()

        # Assert
        self.assertEqual(info["model_name"], "test-model")
        self.assertEqual(info["temperature"], 0.6)


if __name__ == "__main__":
    unittest.main()
