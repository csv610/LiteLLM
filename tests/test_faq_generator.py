import pytest
import os
import sys
import json
from pathlib import Path
from unittest.mock import patch
import argparse

# Add project root to sys.path
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))
# Add app/FAQGenerator to sys.path so we can import modules directly
sys.path.insert(0, str(root_path / "app" / "FAQGenerator"))

# Import the FAQ generator components
from faq_generator import (
    FAQInput,
    FAQGenerator,
    DataExporter,
)
from faq_generator_models import (
    FAQ,
    FAQResponse,
    VALID_DIFFICULTIES,
)
from faq_generator_cli import arguments_parser
from lite import ModelConfig


# ==============================================================================
# Tests for FAQInput Validation
# ==============================================================================

class TestFAQInput:
    """Test suite for FAQInput dataclass."""

    def test_valid_input_with_topic(self):
        """Test creating valid input with a topic."""
        faq_input = FAQInput(
            input_source="Machine Learning",
            num_faqs=5,
            difficulty="simple",
        )
        assert faq_input.input_source == "Machine Learning"
        assert faq_input.num_faqs == 5
        assert faq_input.difficulty == "simple"
        assert faq_input.get_topic() == "Machine Learning"
        assert faq_input.get_file_path() is None

    def test_valid_input_with_file(self, tmp_path):
        """Test creating valid input with a file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        faq_input = FAQInput(
            input_source=str(test_file),
            num_faqs=10,
            difficulty="medium",
        )
        assert faq_input.is_file()
        assert faq_input.get_file_path() == str(test_file)
        assert faq_input.get_topic() is None

    def test_invalid_num_faqs_below_minimum(self):
        """Test that num_faqs below minimum raises ValueError."""
        with pytest.raises(ValueError, match="must be between"):
            FAQInput(
                input_source="Topic",
                num_faqs=0,
                difficulty="simple",
            )

    def test_invalid_num_faqs_above_maximum(self):
        """Test that num_faqs above maximum raises ValueError."""
        with pytest.raises(ValueError, match="must be between"):
            FAQInput(
                input_source="Topic",
                num_faqs=101,
                difficulty="simple",
            )

    def test_invalid_difficulty(self):
        """Test that invalid difficulty raises ValueError."""
        with pytest.raises(ValueError, match="Difficulty must be one of"):
            FAQInput(
                input_source="Topic",
                num_faqs=5,
                difficulty="expert",
            )

    def test_invalid_input_source_empty(self):
        """Test that empty input source raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            FAQInput(
                input_source="",
                num_faqs=5,
                difficulty="simple",
            )

    def test_invalid_output_directory(self):
        """Test that non-existent output directory raises ValueError."""
        with pytest.raises(ValueError, match="Output directory not found"):
            FAQInput(
                input_source="Topic",
                num_faqs=5,
                difficulty="simple",
                output_dir="/nonexistent/directory/path",
            )

    def test_all_difficulty_levels(self):
        """Test that all valid difficulty levels work."""
        for difficulty in VALID_DIFFICULTIES:
            faq_input = FAQInput(
                input_source="Topic",
                num_faqs=5,
                difficulty=difficulty,
            )
            assert faq_input.difficulty == difficulty


# ==============================================================================
# Tests for FAQ and FAQResponse Models
# ==============================================================================

class TestFAQModels:
    """Test suite for Pydantic models."""

    def test_faq_model_valid(self):
        """Test creating a valid FAQ model."""
        faq = FAQ(
            question="What is ML?",
            answer="Machine learning...",
            difficulty="simple",
        )
        assert faq.question == "What is ML?"
        assert faq.answer == "Machine learning..."
        assert faq.difficulty == "simple"

    def test_faq_model_dump(self):
        """Test FAQ model serialization."""
        faq = FAQ(
            question="What is ML?",
            answer="Machine learning...",
            difficulty="simple",
        )
        data = faq.model_dump()
        assert data["question"] == "What is ML?"
        assert data["answer"] == "Machine learning..."
        assert data["difficulty"] == "simple"

    def test_faq_response_model_valid(self):
        """Test creating a valid FAQResponse model."""
        faq1 = FAQ(question="Q1", answer="A1", difficulty="simple")
        faq2 = FAQ(question="Q2", answer="A2", difficulty="medium")

        response = FAQResponse(
            topic="ML",
            difficulty="simple",
            num_faqs=2,
            faqs=[faq1, faq2],
        )
        assert response.topic == "ML"
        assert len(response.faqs) == 2
        assert response.num_faqs == 2

    def test_faq_response_json_serialization(self):
        """Test FAQResponse JSON serialization."""
        faq = FAQ(question="Q1", answer="A1", difficulty="simple")
        response = FAQResponse(
            topic="ML",
            difficulty="simple",
            num_faqs=1,
            faqs=[faq],
        )
        json_str = response.model_dump_json()
        assert "Q1" in json_str
        assert "A1" in json_str


# ==============================================================================
# Tests for FAQGenerator Class
# ==============================================================================

class TestFAQGenerator:
    """Test suite for FAQGenerator class."""

    def test_generator_initialization(self):
        """Test FAQGenerator initialization."""
        config = ModelConfig(model="gpt-4")
        generator = FAQGenerator(config)
        assert generator.model_config == config
        assert generator.model == "gpt-4"

    def test_generator_default_model(self):
        """Test FAQGenerator with default model."""
        config = ModelConfig(model="ollama/gemma3")
        generator = FAQGenerator(config)
        assert generator.model == "ollama/gemma3"

    def test_read_content_file(self, tmp_path):
        """Test reading content from file."""
        test_file = tmp_path / "content.txt"
        test_content = "Test content for FAQ generation"
        test_file.write_text(test_content)

        config = ModelConfig(model="gpt-4")
        generator = FAQGenerator(config)
        content = generator._read_content_file(str(test_file))
        assert content == test_content

    def test_read_content_file_not_found(self):
        """Test reading non-existent file raises error."""
        config = ModelConfig(model="gpt-4")
        generator = FAQGenerator(config)

        with pytest.raises(ValueError, match="Not a valid file"):
            generator._read_content_file("/nonexistent/file.txt")

    @patch("faq_generator.LiteClient")
    def test_generate_text_success(self, MockLiteClient):
        """Test generate_text with successful response."""
        mock_client_instance = MockLiteClient.return_value
        mock_response = FAQResponse(
            topic="Test Topic",
            difficulty="medium",
            num_faqs=1,
            faqs=[FAQ(
                question="What are the fundamental principles of machine learning?",
                answer="Machine learning is based on algorithms that can learn from and make predictions on data by identifying patterns.",
                difficulty="medium"
            )]
        )
        mock_client_instance.generate_text.return_value = mock_response

        config = ModelConfig(model="gpt-4")
        generator = FAQGenerator(config)
        faq_input = FAQInput(input_source="Test Topic", num_faqs=1, difficulty="medium")
        
        faqs = generator.generate_text(faq_input)
        
        assert len(faqs) == 1
        assert "fundamental principles" in faqs[0].question
        mock_client_instance.generate_text.assert_called_once()


# ==============================================================================
# Tests for DataExporter Class
# ==============================================================================

class TestDataExporter:
    """Test suite for DataExporter class."""

    def test_export_to_json(self, tmp_path):
        """Test exporting FAQs to JSON file."""
        faq_input = FAQInput(
            input_source="Machine Learning",
            num_faqs=2,
            difficulty="simple",
            output_dir=str(tmp_path),
        )
        
        faq1 = FAQ(question="Q1", answer="A1", difficulty="simple")
        faq2 = FAQ(question="Q2", answer="A2", difficulty="simple")
        faqs = [faq1, faq2]

        output_file = DataExporter.export_to_json(faqs, faq_input)

        assert os.path.exists(output_file)
        assert "faq_machine_learning" in output_file
        assert "simple" in output_file

        # Verify file contents
        with open(output_file, 'r') as f:
            data = json.load(f)

        assert data["metadata"]["source"] == "Machine Learning"
        assert data["metadata"]["difficulty"] == "simple"
        assert len(data["faqs"]) == 2
        assert data["metadata"]["count"] == 2

    def test_export_to_json_permissions(self, tmp_path):
        """Test that exported file has correct permissions."""
        faq_input = FAQInput(
            input_source="Topic",
            num_faqs=1,
            difficulty="simple",
            output_dir=str(tmp_path),
        )
        faq = FAQ(question="Q1", answer="A1", difficulty="simple")
        output_file = DataExporter.export_to_json([faq], faq_input)

        # Check file permissions (0o644 = rw-r--r--)
        file_stat = os.stat(output_file)
        file_mode = oct(file_stat.st_mode)[-3:]
        assert file_mode == "644"


# ==============================================================================
# Tests for Arguments Parser
# ==============================================================================

class TestArgumentsParser:
    """Test suite for CLI argument parser."""

    def test_parser_creation(self):
        """Test that parser is created successfully."""
        parser = arguments_parser()
        assert isinstance(parser, argparse.ArgumentParser)

    def test_parser_required_arguments(self):
        """Test that required arguments are enforced."""
        parser = arguments_parser()

        # Should fail without required args
        with pytest.raises(SystemExit):
            parser.parse_args([])

    def test_parser_all_arguments(self, tmp_path):
        """Test parsing all arguments."""
        parser = arguments_parser()
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        args = parser.parse_args([
            "-i", str(test_file),
            "-n", "10",
            "-d", "medium",
            "-m", "gpt-4",
            "-o", str(tmp_path),
        ])

        assert args.input_source == str(test_file)
        assert args.num_faqs == 10
        assert args.difficulty == "medium"
        assert args.model == "gpt-4"
        assert args.output_dir == str(tmp_path)

    def test_parser_defaults(self):
        """Test parser default values."""
        parser = arguments_parser()
        args = parser.parse_args([
            "-i", "topic",
        ])

        assert args.num_faqs == 5
        assert args.difficulty == "medium"
        assert args.model is None
        assert args.output_dir == "."


# ==============================================================================
# Integration Tests
# ==============================================================================

class TestIntegration:
    """Integration tests for the FAQ generator."""

    def test_workflow_with_topic(self, tmp_path):
        """Test workflow with topic."""
        faq_input = FAQInput(
            input_source="Python Programming",
            num_faqs=3,
            difficulty="simple",
            output_dir=str(tmp_path),
        )

        assert not faq_input.is_file()
        assert faq_input.get_topic() == "Python Programming"

    def test_workflow_with_file(self, tmp_path):
        """Test workflow with file."""
        content_file = tmp_path / "content.txt"
        content_file.write_text("This is test content")

        faq_input = FAQInput(
            input_source=str(content_file),
            num_faqs=2,
            difficulty="medium",
            output_dir=str(tmp_path),
        )

        assert faq_input.is_file()
        assert faq_input.get_file_path() == str(content_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
