import pytest
import os
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import argparse

# Import the FAQ generator components
from faq_generator import (
    FAQConfig,
    FAQ,
    FAQResponse,
    FAQGenerator,
    validate_num_faqs,
    validate_input_source,
    validate_difficulty,
    arguments_parser,
)


# ==============================================================================
# Tests for FAQConfig Validation
# ==============================================================================

class TestFAQConfig:
    """Test suite for FAQConfig dataclass."""

    def test_valid_config_with_topic(self):
        """Test creating valid config with a topic."""
        config = FAQConfig(
            input_source="Machine Learning",
            num_faqs=5,
            difficulty="simple",
        )
        assert config.input_source == "Machine Learning"
        assert config.num_faqs == 5
        assert config.difficulty == "simple"
        assert config.get_topic() == "Machine Learning"
        assert config.get_file_path() is None

    def test_valid_config_with_file(self, tmp_path):
        """Test creating valid config with a file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        config = FAQConfig(
            input_source=str(test_file),
            num_faqs=10,
            difficulty="medium",
        )
        assert config.is_file()
        assert config.get_file_path() == str(test_file)
        assert config.get_topic() is None

    def test_invalid_num_faqs_below_minimum(self):
        """Test that num_faqs below minimum raises ValueError."""
        with pytest.raises(ValueError, match="must be between"):
            FAQConfig(
                input_source="Topic",
                num_faqs=0,
                difficulty="simple",
            )

    def test_invalid_num_faqs_above_maximum(self):
        """Test that num_faqs above maximum raises ValueError."""
        with pytest.raises(ValueError, match="must be between"):
            FAQConfig(
                input_source="Topic",
                num_faqs=51,
                difficulty="simple",
            )

    def test_invalid_difficulty(self):
        """Test that invalid difficulty raises ValueError."""
        with pytest.raises(ValueError, match="Difficulty must be one of"):
            FAQConfig(
                input_source="Topic",
                num_faqs=5,
                difficulty="expert",
            )

    def test_invalid_input_source_empty(self):
        """Test that empty input source raises ValueError."""
        with pytest.raises(ValueError, match="must be provided"):
            FAQConfig(
                input_source="",
                num_faqs=5,
                difficulty="simple",
            )

    def test_invalid_output_directory(self):
        """Test that non-existent output directory raises ValueError."""
        with pytest.raises(ValueError, match="Output directory not found"):
            FAQConfig(
                input_source="Topic",
                num_faqs=5,
                difficulty="simple",
                output_dir="/nonexistent/directory/path",
            )

    def test_invalid_model_name_format(self):
        """Test that invalid model name raises ValueError."""
        with pytest.raises(ValueError, match="Invalid model name format"):
            FAQConfig(
                input_source="Topic",
                num_faqs=5,
                difficulty="simple",
                model="invalid@model#name!",
            )

    def test_valid_model_names(self):
        """Test that valid model names are accepted."""
        valid_models = [
            "gpt-4",
            "claude-3-opus",
            "gemini/gemini-2.5-flash",
            "model_name",
            "model.name",
            "model-name/variant",
        ]
        for model in valid_models:
            config = FAQConfig(
                input_source="Topic",
                num_faqs=5,
                difficulty="simple",
                model=model,
            )
            assert config.model == model

    def test_all_difficulty_levels(self):
        """Test that all valid difficulty levels work."""
        for difficulty in FAQConfig.VALID_DIFFICULTIES:
            config = FAQConfig(
                input_source="Topic",
                num_faqs=5,
                difficulty=difficulty,
            )
            assert config.difficulty == difficulty


# ==============================================================================
# Tests for Validation Functions
# ==============================================================================

class TestValidationFunctions:
    """Test suite for validation helper functions."""

    def test_validate_num_faqs_valid(self):
        """Test validate_num_faqs with valid inputs."""
        assert validate_num_faqs("5") == 5
        assert validate_num_faqs("1") == 1
        assert validate_num_faqs("50") == 50

    def test_validate_num_faqs_below_minimum(self):
        """Test validate_num_faqs with below minimum."""
        with pytest.raises(argparse.ArgumentTypeError, match="at least"):
            validate_num_faqs("0")

    def test_validate_num_faqs_above_maximum(self):
        """Test validate_num_faqs with above maximum."""
        with pytest.raises(argparse.ArgumentTypeError, match="cannot exceed"):
            validate_num_faqs("51")

    def test_validate_num_faqs_non_integer(self):
        """Test validate_num_faqs with non-integer input."""
        with pytest.raises(argparse.ArgumentTypeError, match="valid integer"):
            validate_num_faqs("abc")

    def test_validate_input_source_file(self, tmp_path):
        """Test validate_input_source with existing file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        result = validate_input_source(str(test_file))
        assert result == str(test_file)

    def test_validate_input_source_topic(self):
        """Test validate_input_source with valid topic."""
        result = validate_input_source("Machine Learning")
        assert result == "Machine Learning"

    def test_validate_input_source_topic_short(self):
        """Test validate_input_source with too short topic."""
        with pytest.raises(argparse.ArgumentTypeError, match="between 2 and 100"):
            validate_input_source("a")

    def test_validate_input_source_topic_long(self):
        """Test validate_input_source with too long topic."""
        long_topic = "a" * 101
        with pytest.raises(argparse.ArgumentTypeError, match="between 2 and 100"):
            validate_input_source(long_topic)

    def test_validate_input_source_empty(self):
        """Test validate_input_source with empty string."""
        with pytest.raises(argparse.ArgumentTypeError, match="cannot be empty"):
            validate_input_source("")

    def test_validate_difficulty_valid(self):
        """Test validate_difficulty with valid inputs."""
        for difficulty in FAQConfig.VALID_DIFFICULTIES:
            result = validate_difficulty(difficulty)
            assert result == difficulty

    def test_validate_difficulty_case_insensitive(self):
        """Test validate_difficulty is case insensitive."""
        assert validate_difficulty("SIMPLE") == "simple"
        assert validate_difficulty("Medium") == "medium"

    def test_validate_difficulty_invalid(self):
        """Test validate_difficulty with invalid input."""
        with pytest.raises(argparse.ArgumentTypeError, match="must be one of"):
            validate_difficulty("invalid")


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

    def test_generator_initialization(self, tmp_path):
        """Test FAQGenerator initialization."""
        config = FAQConfig(
            input_source="Topic",
            num_faqs=5,
            difficulty="simple",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)
        assert generator.config == config
        assert generator.model == "gemini/gemini-2.5-flash"

    def test_generator_custom_model(self, tmp_path):
        """Test FAQGenerator with custom model."""
        config = FAQConfig(
            input_source="Topic",
            num_faqs=5,
            difficulty="simple",
            model="gpt-4",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)
        assert generator.model == "gpt-4"

    def test_generator_model_from_env(self, tmp_path, monkeypatch):
        """Test FAQGenerator reads model from environment variable."""
        monkeypatch.setenv("FAQ_MODEL", "claude-3-opus")
        config = FAQConfig(
            input_source="Topic",
            num_faqs=5,
            difficulty="simple",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)
        assert generator.model == "claude-3-opus"

    def test_create_prompt_from_topic(self, tmp_path):
        """Test prompt creation from topic."""
        config = FAQConfig(
            input_source="Machine Learning",
            num_faqs=5,
            difficulty="simple",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)
        prompt = generator._create_prompt()

        assert "Machine Learning" in prompt
        assert "5" in prompt
        assert "simple" in prompt or "beginner-friendly" in prompt
        assert "SEMANTIC DIVERSITY REQUIREMENTS" in prompt
        assert "semantically distinct" in prompt
        assert "QUALITY CRITERIA - ACADEMIC STANDARDS" in prompt
        assert "complete, standalone" in prompt
        assert "precise, unambiguous" in prompt
        assert "OBJECTIVE, NOT SUBJECTIVE" in prompt
        assert "PEER-REVIEWED LITERATURE" in prompt
        assert "peer-reviewed sources" in prompt
        assert "academically rigorous" in prompt

    def test_create_prompt_from_content(self, tmp_path):
        """Test prompt creation from content."""
        config = FAQConfig(
            input_source="Topic",
            num_faqs=5,
            difficulty="medium",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)
        content = "This is test content about AI"
        prompt = generator._create_prompt(content)

        assert "This is test content about AI" in prompt
        assert "5" in prompt
        assert "STRICT REQUIREMENTS" in prompt
        assert "Do NOT ask about facts explicitly stated" in prompt
        assert "SEMANTIC DIVERSITY REQUIREMENTS" in prompt
        assert "semantically distinct" in prompt
        assert "QUALITY CRITERIA - ACADEMIC STANDARDS" in prompt
        assert "complete, standalone" in prompt
        assert "precise, unambiguous" in prompt
        assert "OBJECTIVE, NOT SUBJECTIVE" in prompt
        assert "PEER-REVIEWED LITERATURE" in prompt
        assert "peer-reviewed sources" in prompt
        assert "academically rigorous" in prompt
        assert "empirical evidence" in prompt

    def test_academic_standards_in_prompts(self, tmp_path):
        """Test that prompts enforce academic standards requirements."""
        config = FAQConfig(
            input_source="Physics",
            num_faqs=5,
            difficulty="hard",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)
        prompt = generator._create_prompt()

        # Verify academic standards are enforced
        assert "OBJECTIVE, NOT SUBJECTIVE" in prompt
        assert "PEER-REVIEWED LITERATURE" in prompt
        assert "definitive, measurable, scientifically-supported answers" in prompt
        assert "opinion-based questions" in prompt
        assert "academic papers, textbooks, and peer-reviewed publications" in prompt
        assert "leading researchers and experts" in prompt
        assert "peer-reviewed literature and established consensus" in prompt

    def test_read_content_file(self, tmp_path):
        """Test reading content from file."""
        test_file = tmp_path / "content.txt"
        test_content = "Test content for FAQ generation"
        test_file.write_text(test_content)

        config = FAQConfig(
            input_source=str(test_file),
            num_faqs=5,
            difficulty="simple",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)
        content = generator._read_content_file(str(test_file))
        assert content == test_content

    def test_read_content_file_not_found(self, tmp_path):
        """Test reading non-existent file raises error."""
        config = FAQConfig(
            input_source="Topic",
            num_faqs=5,
            difficulty="simple",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)

        with pytest.raises(ValueError, match="Failed to read"):
            generator._read_content_file("/nonexistent/file.txt")

    def test_save_to_file(self, tmp_path):
        """Test saving FAQs to JSON file."""
        config = FAQConfig(
            input_source="Machine Learning",
            num_faqs=2,
            difficulty="simple",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)

        faq1 = FAQ(question="Q1", answer="A1", difficulty="simple")
        faq2 = FAQ(question="Q2", answer="A2", difficulty="simple")
        faqs = [faq1, faq2]

        output_file = generator.save_to_file(faqs)

        assert os.path.exists(output_file)
        assert "faq_machine_learning" in output_file
        assert "simple" in output_file

        # Verify file contents
        with open(output_file, 'r') as f:
            data = json.load(f)

        assert data["source_type"] == "topic"
        assert data["source"] == "Machine Learning"
        assert data["difficulty"] == "simple"
        assert len(data["faqs"]) == 2
        assert data["num_faqs_generated"] == 2

    def test_save_to_file_from_file_source(self, tmp_path):
        """Test saving FAQs when source is a file."""
        content_file = tmp_path / "content.txt"
        content_file.write_text("ML content")

        config = FAQConfig(
            input_source=str(content_file),
            num_faqs=1,
            difficulty="hard",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)

        faq = FAQ(question="Q1", answer="A1", difficulty="hard")
        output_file = generator.save_to_file([faq])

        with open(output_file, 'r') as f:
            data = json.load(f)

        assert data["source_type"] == "file"

    def test_save_to_file_permissions(self, tmp_path):
        """Test that saved file has restricted permissions."""
        config = FAQConfig(
            input_source="Topic",
            num_faqs=1,
            difficulty="simple",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)
        faq = FAQ(question="Q1", answer="A1", difficulty="simple")
        output_file = generator.save_to_file([faq])

        # Check file permissions (0o600 = read/write owner only)
        file_stat = os.stat(output_file)
        file_mode = oct(file_stat.st_mode)[-3:]
        assert file_mode == "600"

    def test_handle_api_error_authentication(self, tmp_path):
        """Test handling of authentication errors."""
        config = FAQConfig(
            input_source="Topic",
            num_faqs=5,
            difficulty="simple",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)

        error = Exception("401 Unauthorized: Authentication failed")
        with pytest.raises(RuntimeError, match="authentication failed"):
            generator._handle_api_error(error)

    def test_handle_api_error_rate_limit(self, tmp_path):
        """Test handling of rate limit errors."""
        config = FAQConfig(
            input_source="Topic",
            num_faqs=5,
            difficulty="simple",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)

        error = Exception("429 Too Many Requests")
        with pytest.raises(RuntimeError, match="rate limit"):
            generator._handle_api_error(error)

    def test_handle_api_error_model_not_found(self, tmp_path):
        """Test handling of model not found errors."""
        config = FAQConfig(
            input_source="Topic",
            num_faqs=5,
            difficulty="simple",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)

        error = Exception("404 Model not found")
        with pytest.raises(RuntimeError, match="not found or not available"):
            generator._handle_api_error(error)

    def test_handle_api_error_generic(self, tmp_path):
        """Test handling of generic API errors."""
        config = FAQConfig(
            input_source="Topic",
            num_faqs=5,
            difficulty="simple",
            output_dir=str(tmp_path),
        )
        generator = FAQGenerator(config)

        error = Exception("Some other error")
        with pytest.raises(RuntimeError, match="Failed to generate FAQs"):
            generator._handle_api_error(error)


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

    def test_parser_long_form_arguments(self, tmp_path):
        """Test parsing with long-form argument names."""
        parser = arguments_parser()
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        args = parser.parse_args([
            "--input", str(test_file),
            "--num-faqs", "5",
            "--difficulty", "hard",
            "--model", "claude-3",
            "--output", str(tmp_path),
        ])

        assert args.input_source == str(test_file)
        assert args.num_faqs == 5
        assert args.difficulty == "hard"
        assert args.model == "claude-3"
        assert args.output_dir == str(tmp_path)

    def test_parser_defaults(self):
        """Test parser default values."""
        parser = arguments_parser()
        args = parser.parse_args([
            "-i", "topic",
            "-n", "5",
            "-d", "simple",
        ])

        assert args.model is None
        assert args.output_dir == "."


# ==============================================================================
# Integration Tests
# ==============================================================================

class TestIntegration:
    """Integration tests for the FAQ generator."""

    def test_end_to_end_with_topic(self, tmp_path, monkeypatch):
        """Test end-to-end workflow with topic."""
        monkeypatch.setenv("FAQ_MODEL", "test-model")

        config = FAQConfig(
            input_source="Python Programming",
            num_faqs=3,
            difficulty="simple",
            output_dir=str(tmp_path),
            log_file=str(tmp_path / "test.log"),
        )

        generator = FAQGenerator(config)
        assert not config.is_file()
        assert config.get_topic() == "Python Programming"

    def test_end_to_end_with_file(self, tmp_path):
        """Test end-to-end workflow with file."""
        content_file = tmp_path / "content.txt"
        content_file.write_text("This is test content")

        config = FAQConfig(
            input_source=str(content_file),
            num_faqs=2,
            difficulty="medium",
            output_dir=str(tmp_path),
            log_file=str(tmp_path / "test.log"),
        )

        generator = FAQGenerator(config)
        assert config.is_file()
        assert config.get_file_path() == str(content_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
