"""
liteagents.py - Unified for med_quiz
"""
import time
from unittest.mock import patch
from lite.utils import save_model_response
from tqdm import tqdm
import pytest
import logging
from lite.lite_client import LiteClient
from pathlib import Path
import re
import argparse
from lite.config import ModelConfig, ModelInput
from lite.logging_config import configure_logging
import sys
from app.MedKit.medical.med_quiz.shared.models import *


# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))



    MedicalQuizModel,
    ModelOutput,
    QuizQuestionModel,
)


@pytest.fixture
def mock_lite_client():
    with patch("medical.med_quiz.agentic.medical_quiz.LiteClient") as mock:
        yield mock


def test_generator_init():
    config = ModelConfig(model="test-model")
    generator = MedicalQuizGenerator(config)
    assert generator.model_config == config


def test_sanitize_topic():
    config = ModelConfig(model="test-model")
    generator = MedicalQuizGenerator(config)
    assert generator._sanitize_topic("Diabetes Mellitus") == "Diabetes_Mellitus"
    assert generator._sanitize_topic("Test/Topic?") == "TestTopic"


def test_generate_text_unstructured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalQuizGenerator(config)
    mock_output = ModelOutput(markdown="Quiz content", data=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Diabetes", "Easy", 1)
    assert result.markdown == "Quiz content"
    assert generator.topic == "Diabetes"


def test_generate_text_invalid_inputs():
    config = ModelConfig(model="test-model")
    generator = MedicalQuizGenerator(config)
    with pytest.raises(ValueError, match="Topic cannot be empty"):
        generator.generate_text("", "Easy", 1)
    with pytest.raises(ValueError, match="Number of questions must be >= 1"):
        generator.generate_text("Diabetes", "Easy", 0)
    with pytest.raises(ValueError, match="Number of options must be >= 2"):
        generator.generate_text("Diabetes", "Easy", 1, 1)


def test_generate_text_structured(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalQuizGenerator(config)

    mock_data = MedicalQuizModel(
        topic="Diabetes",
        difficulty="Easy",
        questions=[
            QuizQuestionModel(
                id=1,
                question="What is the main symptom of diabetes?",
                options={"A": "Polyuria", "B": "Headache", "C": "Cough", "D": "Rash"},
                answer="A",
                explanation="Polyuria is excessive urination.",
            )
        ],
    )

    mock_output = ModelOutput(data=mock_data, markdown=None)
    mock_lite_client.return_value.generate_text.return_value = mock_output

    result = generator.generate_text("Diabetes", "Easy", 1, structured=True)
    assert result.data.topic == "Diabetes"


@patch("medical.med_quiz.agentic.medical_quiz.save_model_response")
def test_save_success(mock_save, mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = MedicalQuizGenerator(config)
    mock_output = ModelOutput(markdown="Quiz content")
    mock_lite_client.return_value.generate_text.return_value = mock_output

    generator.generate_text("Diabetes", "Easy", 1)
    generator.save(mock_output, Path("/tmp"))

    mock_save.assert_called_once()
    args, _ = mock_save.call_args
    assert args[0] == mock_output
    assert str(args[1]).endswith("diabetes_quiz")

"""Medical Quiz Generator CLI."""



# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))


try:
    from .medical_quiz import MedicalQuizGenerator
except (ImportError, ValueError):
    from medical.med_quiz.agentic.medical_quiz import MedicalQuizGenerator

logger = logging.getLogger(__name__)


def get_user_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate comprehensive medical quizzes."
    )
    parser.add_argument("topic", help="Medical topic or file path containing topics.")
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
        help="Logging verbosity level.",
    )
    parser.add_argument("--difficulty", default="Intermediate", help="Quiz difficulty.")
    parser.add_argument(
        "--num-questions", type=int, default=5, help="Number of questions."
    )
    parser.add_argument(
        "--num-options", type=int, default=4, help="Number of options per question."
    )
    return parser.parse_args()


def main():
    args = get_user_arguments()
    configure_logging(
        log_file="medical_quiz.log", verbosity=args.verbosity, enable_console=True
    )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(args.topic)
    items = (
        [line.strip() for line in open(input_path)]
        if input_path.is_file()
        else [args.topic]
    )

    try:
        model_config = ModelConfig(model=args.model, temperature=0.7)
        generator = MedicalQuizGenerator(model_config)

        for item in tqdm(items, desc="Generating Quizzes"):
            result = generator.generate_text(
                topic=item,
                difficulty=args.difficulty,
                num_questions=args.num_questions,
                num_options=args.num_options,
                structured=True,
            )
            if result:
                generator.save(result, output_dir)

        logger.info("✓ Completed successfully")
    except Exception as e:
        logger.error(f"✗ Failed: {e}")
        return 1
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())

#!/usr/bin/env python3
"""
Medical Quiz Generation module.

This module provides the core MedicalContentGenerator class for generating
high-quality, board-style medical quizzes for various topics.
"""


sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    from .medical_quiz_models import MedicalQuizModel, ModelOutput
    from .medical_quiz_prompts import PromptBuilder
except (ImportError, ValueError):
    from medical_quiz_models import MedicalQuizModel, ModelOutput
    from medical_quiz_prompts import PromptBuilder

logger = logging.getLogger(__name__)


class SimpleProgressBar:
    """Simple progress bar for CLI feedback."""

    def __init__(self, total: int, description: str = "Processing"):
        self.total = total
        self.current = 0
        self.description = description
        self.start_time = time.time()

    def update(self, increment: int = 1):
        """Update progress bar."""
        self.current += increment
        self._display()

    def _display(self):
        """Display progress bar."""
        if self.total <= 1:
            return

        percentage = (self.current / self.total) * 100
        filled_length = int(50 * self.current // self.total)
        bar = "█" * filled_length + "-" * (50 - filled_length)

        elapsed_time = time.time() - self.start_time
        if self.current > 0:
            eta = (elapsed_time / self.current) * (self.total - self.current)
            eta_str = f"{eta:.1f}s"
        else:
            eta_str = "?.?s"

        print(
            f"\r{self.description}: |{bar}| {percentage:.1f}% ({self.current}/{self.total}) ETA: {eta_str}",
            end="",
            flush=True,
        )

        if self.current >= self.total:
            print()  # New line when complete


class MedicalQuizGenerator:
    """Generates comprehensive medical quizzes."""

    def __init__(self, model_config: ModelConfig):
        """Initialize the generator."""
        self.model_config = model_config
        self.client = LiteClient(model_config)
        self.topic = None  # Store the topic for later use in save
        self.content_type = "quiz"
        logger.debug("Initialized MedicalQuizGenerator")

    def _sanitize_topic(self, topic: str) -> str:
        """Sanitize topic for safe filename generation."""
        # Remove invalid characters for filenames
        sanitized = re.sub(r'[<>:"/\\|?*]', "", topic.strip())
        # Replace spaces with underscores
        sanitized = re.sub(r"\s+", "_", sanitized)
        sanitized = sanitized.strip(". ")  # Remove leading/trailing dots and spaces
        return sanitized if sanitized else "medical_quiz"

    def generate_text(
        self,
        topic: str,
        difficulty: str,
        num_questions: int,
        num_options: int = 4,
        structured: bool = False,
    ) -> ModelOutput:
        """Generate medical quiz using a 3-tier agent system."""
        # Input validation
        if not topic or not topic.strip():
            raise ValueError("Topic cannot be empty")
        
        self.topic = self._sanitize_topic(topic.strip())
        logger.info(f"Starting 3-tier Quiz generation for: {topic}")

        try:
            # 1. Specialist Stage (JSON)
            logger.debug("Tier 1: Specialist Agent generating quiz questions...")
            system_prompt = PromptBuilder.create_quiz_system_prompt()
            user_prompt = PromptBuilder.create_quiz_user_prompt(
                topic, difficulty, num_questions, num_options
            )
            
            spec_input = ModelInput(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                response_format=MedicalQuizModel if structured else None,
            )
            spec_res = self.ask_llm(spec_input)
            
            if structured:
                spec_json = spec_res.data.model_dump_json(indent=2)
            else:
                spec_json = spec_res.markdown

            # 2. Auditor Stage (JSON Audit)
            logger.debug("Tier 2: Auditor Agent reviewing quiz...")
            audit_sys, audit_usr = PromptBuilder.get_quiz_auditor_prompts(topic, spec_json)
            audit_input = ModelInput(
                system_prompt=audit_sys,
                user_prompt=audit_usr,
                response_format=None # Audit is markdown/json
            )
            audit_res = self.ask_llm(audit_input)
            audit_json = audit_res.markdown

            # 3. Final Synthesis Stage (Markdown)
            logger.debug("Tier 3: Output Agent synthesizing final quiz...")
            out_sys, out_usr = PromptBuilder.get_output_synthesis_prompts(topic, spec_json, audit_json)
            out_input = ModelInput(
                system_prompt=out_sys,
                user_prompt=out_usr,
                response_format=None,
            )
            final_res = self.ask_llm(out_input)

            logger.debug("✓ Successfully generated 3-tier Quiz")
            return ModelOutput(
                data=spec_res.data, 
                markdown=final_res.markdown,
                metadata={"audit": audit_json}
            )

        except Exception as e:
            logger.error(f"✗ 3-tier Quiz generation failed: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the generated information to a file."""
        if self.topic is None:
            raise ValueError(
                "No topic information available. Call generate_quiz first."
            )

        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.topic.lower().replace(' ', '_')}_quiz"

        # Always apply proper formatting regardless of input type
        if hasattr(result, "data") and result.data:
            # Structured output wrapped in ModelOutput
            if not result.markdown:
                result.markdown = self._format_quiz_markdown(result.data)
        elif hasattr(result, "topic"):
            # Direct MedicalQuizModel (structured output)
            # Wrap it in ModelOutput with proper formatting
            from .medical_quiz_models import ModelOutput

            wrapped_result = ModelOutput(
                data=result, markdown=self._format_quiz_markdown(result)
            )
            return save_model_response(wrapped_result, output_dir / base_filename)
        else:
            # For plain text, create a simple formatted version
            if hasattr(result, "markdown") and result.markdown:
                # Create a basic formatted version for better readability
                formatted_content = f"""# Medical Quiz: {self.topic}
**Difficulty:** Intermediate

## Question 1
**Medical quiz question generated successfully.**

**Options:**
A) Option A
B) Option B  
C) Option C
D) Option D

**Answer:** A

**Explanation:** 
Detailed explanation would be included here.

---

*Note: For the best formatting experience, use the -s flag for structured output.*

"""
                result.markdown = formatted_content

        return save_model_response(result, output_dir / base_filename)

    def _reformat_plain_text_quiz(self, plain_text: str) -> str:
        """Reformat plain text quiz output to proper markdown format."""
        import re

        # Try to extract the main question and options from the plain text
        lines = plain_text.split("
")

        # Look for the main question (usually a long sentence with clinical details)
        question_text = None
        options_dict = {}
        answer = None
        explanation_parts = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Find question - look for clinical presentation patterns
            if (
                not question_text
                and len(line) > 80
                and any(
                    keyword in line.lower()
                    for keyword in ["patient", "presents", "year-old", "male", "female"]
                )
                and not line.startswith(("A)", "B)", "C)", "D)", "#", "*"))
            ):
                question_text = line

            # Extract options from dictionary format
            if "'A':" in line or '"A":' in line:
                # Extract all options from this line
                matches = re.findall(r'["\']([A-D])["\']:\s*["\']([^"\']+)["\']', line)
                for key, value in matches:
                    options_dict[key] = value

            # Find answer
            if not answer and (
                "correct answer" in line.lower() or "answer:" in line.lower()
            ):
                answer_match = re.search(r"([A-D])", line)
                if answer_match:
                    answer = answer_match.group(1)

            # Collect explanation
            if any(
                keyword in line.lower()
                for keyword in ["explanation", "why", "correct", "distractor"]
            ):
                explanation_parts.append(line)

        # Build formatted output if we found the key components
        if question_text and options_dict:
            formatted_lines = [
                f"# Medical Quiz: {self.topic}",
                "**Difficulty:** Intermediate",
                "",
                "## Question 1",
                f"**{question_text}**",
                "",
                "**Options:**",
            ]

            # Add options in order
            for key in ["A", "B", "C", "D"]:
                if key in options_dict:
                    formatted_lines.append(f"{key}) {options_dict[key]}")

            formatted_lines.extend(
                ["", f"**Answer:** {answer or 'A'}", "", "**Explanation:**"]
            )

            # Add explanation
            if explanation_parts:
                for part in explanation_parts:
                    clean_part = part.replace("#", "").replace("*", "").strip()
                    if clean_part and len(clean_part) > 10:
                        formatted_lines.append(clean_part)

            formatted_lines.extend(["", "---", ""])

            return "
".join(formatted_lines)

        # If reformatting failed, return a basic formatted version
        if options_dict:
            options_text = "
".join(
                ["{}) {}".format(k, v) for k, v in options_dict.items()]
            )
        else:
            options_text = "A) Option A
B) Option B
C) Option C
D) Option D"

        template = """# Medical Quiz: {topic}
**Difficulty:** Intermediate

## Question 1
**{question}**

**Options:**
{options}

**Answer:** {answer}

**Explanation:** 
Detailed explanation would be included here.

---

"""
        return template.format(
            topic=self.topic,
            question=question_text or "Medical quiz question generated successfully.",
            options=options_text,
            answer=answer or "A",
        )

    def _format_quiz_markdown(self, quiz_data: MedicalQuizModel) -> str:
        """Format quiz data as properly formatted markdown."""
        lines = []

        # Header
        lines.append(f"# Medical Quiz: {quiz_data.topic}")
        lines.append(f"**Difficulty:** {quiz_data.difficulty}")
        lines.append("")

        # Questions
        for question in quiz_data.questions:
            lines.append(f"## Question {question.id}")
            lines.append(f"**{question.question}**")
            lines.append("")

            # Options on separate lines
            lines.append("**Options:**")
            for option_key, option_text in question.options.items():
                lines.append(f"{option_key}) {option_text}")
            lines.append("")

            # Answer and explanation
            lines.append(f"**Answer:** {question.answer}")
            lines.append("")
            lines.append(f"**Explanation:** {question.explanation}")
            lines.append("")
            lines.append("---")
            lines.append("")

        return "
".join(lines)