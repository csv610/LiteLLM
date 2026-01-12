import sys
import json
import argparse
from pathlib import Path
from typing import Optional, Union, List, Dict
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pydantic import BaseModel, Field
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from logging_util import setup_logging

log_file = Path(__file__).parent / "logs" / "multiple_choice_solver.log"
logger = setup_logging(str(log_file))


class CorrectOption(BaseModel):
    key: str = Field(..., description="The key or index of the correct option (e.g., 'A', 'B', '0', '1')")
    value: str = Field(..., description="The text of the correct option")


class MultipleChoiceAnswer(BaseModel):
    question: str = Field(..., description="The multiple-choice question")
    correct_options: List[CorrectOption] = Field(
        ...,
        description="List of correct option(s). Can be single or multiple."
    )
    reasoning: str = Field(
        ...,
        description="Detailed explanation of why these are the correct answers"
    )
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence level in the answer (0.0 to 1.0)"
    )


class MultipleChoiceSolverResponse(BaseModel):
    answer: MultipleChoiceAnswer


@dataclass
class MultipleChoiceQuestion:
    """Represents a multiple-choice question with options."""
    question: str
    options: Union[List[str], Dict[str, str]]  # List or Dict format
    context: Optional[str] = None  # Context/background information
    image_paths: Optional[List[str]] = None  # Multiple images supported

    def _format_options_for_prompt(self) -> str:
        """Format options as a string for the prompt."""
        if isinstance(self.options, dict):
            formatted = "\n".join([f"{key}: {value}" for key, value in self.options.items()])
        else:
            # Convert list to dict with A, B, C, etc. keys
            keys = [chr(65 + i) for i in range(len(self.options))]
            formatted = "\n".join([f"{key}: {value}" for key, value in zip(keys, self.options)])
        return formatted


class MultipleChoiceSolver:
    """Solves multiple-choice questions using LLM."""

    SYSTEM_PROMPT = """You are an expert at solving multiple-choice questions accurately.
Your task is to:
1. Carefully read the question and all options
2. Identify which option(s) are correct
3. Provide clear reasoning for your answer
4. Be confident in your answer when you have strong justification

Always respond in the requested JSON format."""

    def __init__(self, model: str = "gemini/gemini-2.5-flash", temperature: float = 0.2):
        """Initialize the MultipleChoiceSolver with a model and temperature."""
        try:
            model_config = ModelConfig(model=model, temperature=temperature)
            self.client = LiteClient(model_config=model_config)
            self.logger = logger
            self.logger.info(f"MultipleChoiceSolver initialized with model: {model}, temperature: {temperature}")
        except Exception as e:
            self.logger.error(f"Failed to initialize MultipleChoiceSolver: {e}")
            raise

    def solve(self, question: Union[MultipleChoiceQuestion, str, dict],
              options: Optional[Union[List[str], Dict[str, str]]] = None,
              context: Optional[str] = None,
              image_paths: Optional[List[str]] = None) -> Optional[MultipleChoiceAnswer]:
        """
        Solve a multiple-choice question.

        Args:
            question: Either a MultipleChoiceQuestion object, a string question, or a dict with question data
            options: Options as list or dict (required if question is a string)
            context: Context/background information (optional)
            image_paths: List of image paths (optional)

        Returns:
            MultipleChoiceAnswer with correct option(s) and reasoning
        """
        try:
            # Parse input formats
            if isinstance(question, MultipleChoiceQuestion):
                q_obj = question
            elif isinstance(question, dict):
                q_obj = MultipleChoiceQuestion(
                    question=question.get("question", ""),
                    options=question.get("options", []),
                    context=question.get("context", context),
                    image_paths=question.get("image_paths", image_paths)
                )
            else:
                if options is None:
                    raise ValueError("Options must be provided when question is a string")
                q_obj = MultipleChoiceQuestion(
                    question=str(question),
                    options=options,
                    context=context,
                    image_paths=image_paths
                )

            # Create prompt
            prompt = self._create_prompt(q_obj)

            # Build model input
            model_input = ModelInput(
                user_prompt=prompt,
                response_format=MultipleChoiceSolverResponse,
                system_prompt=self.SYSTEM_PROMPT
            )

            # Add images if provided
            if q_obj.image_paths:
                model_input.image_paths = q_obj.image_paths

            # Get response
            response_content = self.client.generate_text(model_input=model_input)

            if not isinstance(response_content, str):
                self.logger.error("Expected string response from model")
                return None

            # Parse response
            parsed = self._parse_response(response_content)
            if parsed and "answer" in parsed:
                answer = MultipleChoiceAnswer(**parsed["answer"])
                self.logger.info(f"Successfully solved question: {q_obj.question[:50]}...")
                return answer
            else:
                self.logger.error("Failed to parse response")
                return None

        except Exception as e:
            self.logger.error(f"Error solving question: {e}")
            raise

    def solve_batch(self, questions: List[Union[MultipleChoiceQuestion, dict, str]]) -> List[Optional[MultipleChoiceAnswer]]:
        """
        Solve multiple questions in batch.

        Args:
            questions: List of questions (can be mixed formats)

        Returns:
            List of answers corresponding to the questions
        """
        answers = []
        for i, q in enumerate(questions, 1):
            try:
                self.logger.info(f"Solving question {i}/{len(questions)}")
                answer = self.solve(q)
                answers.append(answer)
            except Exception as e:
                self.logger.error(f"Failed to solve question {i}: {e}")
                answers.append(None)
        return answers

    def _create_prompt(self, question: MultipleChoiceQuestion) -> str:
        """Create a prompt for the model."""
        formatted_options = question._format_options_for_prompt()

        prompt = f"""Question: {question.question}

Options:
{formatted_options}

Please analyze this question carefully and determine which option(s) is/are correct.
Provide your answer in the specified JSON format."""

        if question.context:
            prompt = f"""Context:
{question.context}

{prompt}"""

        if question.image_paths:
            num_images = len(question.image_paths)
            prompt += f"\n\nNote: {num_images} image(s) are provided. Please analyze them along with the question."

        return prompt

    def _parse_response(self, response_content: str) -> Optional[dict]:
        """Parse JSON response from model."""
        try:
            # Try to parse as JSON directly
            parsed = json.loads(response_content)
            return parsed
        except json.JSONDecodeError:
            # Try to extract JSON from the response
            try:
                start = response_content.find("{")
                end = response_content.rfind("}") + 1
                if start >= 0 and end > start:
                    json_str = response_content[start:end]
                    parsed = json.loads(json_str)
                    return parsed
            except json.JSONDecodeError:
                self.logger.error(f"Failed to parse JSON response: {response_content}")
                return None


def main_cli():
    """Command-line interface for the multiple choice solver."""
    parser = argparse.ArgumentParser(
        description="Solve multiple-choice questions using LLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Simple question with options
  python multiple_choice_solver.py -q "What is the capital of France?" \\
    -o "A: London" "B: Paris" "C: Berlin"

  # Question with context and multiple images
  python multiple_choice_solver.py -q "Which image contains a tiger?" \\
    -c "You have 4 animal images" \\
    -i image1.jpg image2.jpg image3.jpg image4.jpg \\
    -o "Image 1" "Image 2" "Image 3" "Image 4"

  # Load from JSON file
  python multiple_choice_solver.py -f questions.json
        """
    )

    parser.add_argument(
        "-q", "--question",
        type=str,
        help="The multiple-choice question"
    )
    parser.add_argument(
        "-o", "--options",
        nargs="+",
        help="Options as space-separated strings"
    )
    parser.add_argument(
        "-c", "--context",
        type=str,
        default=None,
        help="Context/background information (optional)"
    )
    parser.add_argument(
        "-i", "--images",
        nargs="+",
        default=None,
        help="Paths to image files (multiple images supported)"
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default="gemini/gemini-2.5-flash",
        help="Model name (default: gemini/gemini-2.5-flash)"
    )
    parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=0.2,
        help="Temperature for model (default: 0.2)"
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Path to JSON file with questions"
    )

    args = parser.parse_args()

    solver = MultipleChoiceSolver(model=args.model, temperature=args.temperature)

    if args.file:
        # Load questions from file
        with open(args.file, "r") as f:
            questions = json.load(f)
        if not isinstance(questions, list):
            questions = [questions]
        answers = solver.solve_batch(questions)
        for q, ans in zip(questions, answers):
            print_answer(ans)
    elif args.question and args.options:
        # Single question
        question = MultipleChoiceQuestion(
            question=args.question,
            options=args.options,
            context=args.context,
            image_paths=args.images
        )
        answer = solver.solve(question)
        print_answer(answer)
    else:
        parser.print_help()


def print_answer(answer: Optional[MultipleChoiceAnswer]) -> None:
    """Pretty print an answer."""
    if answer is None:
        print("Failed to solve question")
        return

    print("\n" + "="*60)
    print(f"Question: {answer.question}")
    print("-"*60)

    correct_str = ", ".join([f"{opt.key}: {opt.value}" for opt in answer.correct_options])
    print(f"Correct Answer(s): {correct_str}")
    print(f"Confidence: {answer.confidence:.1%}")
    print("-"*60)
    print(f"Reasoning:\n{answer.reasoning}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main_cli()
