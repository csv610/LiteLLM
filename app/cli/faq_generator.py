import argparse
import logging
import json
import sys
import os
import re
from pathlib import Path
from typing import Optional, NoReturn
from dataclasses import dataclass
from pydantic import BaseModel, Field

# Add parent directory to path to import lite module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lite import LiteClient, ModelConfig
from lite.config import ModelInput
from logging_util import setup_logging

# ==============================================================================
# Configuration Dataclass
# ==============================================================================

@dataclass
class FAQConfig:
	"""Configuration for FAQ generation."""
	input_source: str  # Can be a topic or a filename
	num_faqs: int
	difficulty: str
	model: Optional[str] = None
	temperature: float = 0.3
	output_dir: str = "."
	log_file: str = str(Path(__file__).parent / "logs" / "faq_generator.log")

	VALID_DIFFICULTIES = ["simple", "medium", "hard", "research"]
	MIN_FAQS = 1
	MAX_FAQS = 100
	MIN_TEMPERATURE = 0.0
	MAX_TEMPERATURE = 2.0

	def __post_init__(self) -> None:
		"""Validate configuration after initialization."""
		self._validate()

	def _validate(self) -> None:
		"""
		Validate configuration parameters.

		Raises:
			ValueError: If any parameter is invalid
		"""
		# Validate input_source
		if not self.input_source or len(self.input_source) < 1:
			raise ValueError("Input source (topic or filename) must be provided")

		# Validate num_faqs
		if self.num_faqs < self.MIN_FAQS or self.num_faqs > self.MAX_FAQS:
			raise ValueError(
				f"Number of FAQs must be between {self.MIN_FAQS} and {self.MAX_FAQS}"
			)

		# Validate difficulty
		if self.difficulty not in self.VALID_DIFFICULTIES:
			raise ValueError(
				f"Difficulty must be one of: {', '.join(self.VALID_DIFFICULTIES)}"
			)

		# Validate temperature
		if not (self.MIN_TEMPERATURE <= self.temperature <= self.MAX_TEMPERATURE):
			raise ValueError(
				f"Temperature must be between {self.MIN_TEMPERATURE} and {self.MAX_TEMPERATURE}"
			)

		# Validate model if provided
		if self.model and not re.match(r'^[a-zA-Z0-9\-\./_]+$', self.model):
			raise ValueError("Invalid model name format")

		# Validate output directory
		if not os.path.isdir(self.output_dir):
			raise ValueError(f"Output directory not found: {self.output_dir}")

	def is_file(self) -> bool:
		"""
		Check if input_source is a file or a topic.

		Returns:
			True if input_source is a file path, False if it's a topic
		"""
		return os.path.exists(self.input_source)

	def get_topic(self) -> Optional[str]:
		"""
		Get topic if input_source is a topic string.

		Returns:
			Topic string or None if input_source is a file
		"""
		if not self.is_file():
			return self.input_source
		return None

	def get_file_path(self) -> Optional[str]:
		"""
		Get file path if input_source is a file.

		Returns:
			File path or None if input_source is a topic
		"""
		if self.is_file():
			return self.input_source
		return None


# ==============================================================================
# Pydantic Models
# ==============================================================================

class FAQ(BaseModel):
	"""Represents a single FAQ entry."""
	question: str = Field(..., description="The frequently asked question")
	answer: str = Field(..., description="The answer to the question")
	difficulty: str = Field(..., description="Difficulty level (simple, medium, hard, research)")


class FAQResponse(BaseModel):
	"""Response containing a list of FAQs."""
	topic: str = Field(..., description="The topic for which FAQs are provided")
	difficulty: str = Field(..., description="Difficulty level (simple, medium, hard, research)")
	num_faqs: int = Field(..., description="Number of FAQs generated")
	faqs: list[FAQ]


# ==============================================================================
# Prompt Builder Class
# ==============================================================================

class PromptBuilder:
	"""Builds prompts for FAQ generation with configurable difficulty levels."""

	DIFFICULTY_DESC = {
		"simple": "beginner-friendly and basic concepts that anyone can understand",
		"medium": "intermediate level covering practical knowledge and common scenarios",
		"hard": "advanced topics requiring specialized knowledge and deeper understanding",
		"research": "cutting-edge research questions, open problems, and expert-level discussions"
	}

	QUALITY_CRITERIA = """
QUALITY CRITERIA - ACADEMIC STANDARDS:
- Each question must be complete, standalone, and self-contained (understandable without external context)
- Questions must be precise, unambiguous, and professionally worded
- ANSWERS MUST BE OBJECTIVE, NOT SUBJECTIVE - avoid questions requiring opinions, beliefs, or personal judgment
- ANSWERS MUST BE VERIFIABLE FROM PEER-REVIEWED LITERATURE, ACADEMIC TEXTBOOKS, AND AUTHORITATIVE SCIENTIFIC SOURCES
- ONLY ask questions with definitive, measurable, scientifically-supported answers
- Avoid vague, open-ended, interpretive, or opinion-based questions
- Avoid questions about "best," "better," or subjective preferences without objective metrics
- Each question must meet the highest academic and scientific standards
- Questions should be suitable for academic papers, textbooks, and peer-reviewed publications"""

	SEMANTIC_DIVERSITY = """
SEMANTIC DIVERSITY REQUIREMENTS:
- Each question must address a DIFFERENT semantic concept or aspect of the domain
- Questions must NOT be paraphrases or variations of the same underlying question
- Avoid asking about the same concept from only slightly different angles
- Each question should explore a fundamentally distinct topic area, perspective, or problem domain
- Vary the question types: cause-effect, comparison, application, theory, challenges, evolution, relationships"""

	QUESTION_FORMAT = """
STRICT REQUIREMENTS - GENERATE QUESTIONS NOT IMPERATIVES:

1. ALL questions MUST be formatted as actual questions using interrogative sentence structure
2. Questions MUST start with question words: "What," "How," "Why," "When," "Where," "Which," "Can," "Does," "Is," "Should," etc.
3. Do NOT generate imperatives (commands like "Explain," "Describe," "Elaborate," "Differentiate")"""

	def __init__(self, num_faqs: int, difficulty: str):
		"""
		Initialize the prompt builder.

		Args:
			num_faqs: Number of FAQs to generate
			difficulty: Difficulty level (simple, medium, hard, research)
		"""
		self.num_faqs = num_faqs
		self.difficulty = difficulty
		self.level_desc = self.DIFFICULTY_DESC.get(difficulty, "intermediate level")

	def _get_research_guidance(self, context: str = "") -> str:
		"""
		Get research-level guidance for prompt.

		Args:
			context: Optional context (topic or "content" for file-based)

		Returns:
			Research guidance string or empty string if not research level
		"""
		if self.difficulty != "research":
			return ""

		context_str = f" in {context}" if context else ""
		return f"""
RESEARCH-LEVEL FOCUS:
- Generate questions about OPEN PROBLEMS and unsolved challenges{context_str}
- Focus on CUTTING-EDGE research directions and recent advances that challenge prior assumptions
- Ask about CURRENT RESEARCH GAPS and what remains unknown or contested
- Include questions about EXPERIMENTAL METHODOLOGIES used to investigate phenomena{context_str}
- Ask about LIMITATIONS of current theories, models, or approaches in this field
- Include questions about COMPETING THEORIES or different interpretations of research findings
- Focus on FUTURE RESEARCH DIRECTIONS and emerging methodologies
- Ask about INTERDISCIPLINARY CONNECTIONS and novel approaches from other fields
- Include questions that leading RESEARCHERS AND EXPERTS actively debate or investigate{context_str}
- Questions should address what scholars do NOT yet know or where consensus is evolving"""

	def _get_content_specific_requirements(self) -> str:
		"""
		Get content-specific requirements for file-based FAQ generation.

		Returns:
			Content-specific requirements string
		"""
		return """
4. Do NOT ask about facts explicitly stated in the content
5. Do NOT ask about information directly inferrable from the content
6. Instead, generate questions about:
   - Prerequisites and foundational concepts needed to understand this topic
   - Common misconceptions or frequently confused concepts in this domain
   - Practical tips, best practices, and common mistakes people make
   - Related fields, alternative approaches, or competing solutions
   - How this topic relates to other domains or real-world applications
   - Historical context or evolution of concepts in this field
   - Questions that require domain expertise but are independent from the provided text"""

	def _get_topic_question_types(self) -> str:
		"""Get question type suggestions for topic-based generation."""
		if self.difficulty == "research":
			return "open problems, cutting-edge advances, research gaps, methodologies, limitations, competing theories, future directions, interdisciplinary connections, emerging consensus"
		return "fundamentals, comparison, application, challenges, best practices, evolution, relationships, controversies"

	def build_content_prompt(self, content: str) -> str:
		"""
		Build prompt for content-based FAQ generation.

		Args:
			content: File content to analyze

		Returns:
			Formatted prompt string
		"""
		return f"""Analyze the following content to understand its domain and topic. Then generate {self.num_faqs} frequently asked questions with {self.level_desc} answers.

Content:
{content}

{self.QUESTION_FORMAT}{self._get_content_specific_requirements()}{self._get_research_guidance()}

{self.SEMANTIC_DIVERSITY}

{self.QUALITY_CRITERIA}

For each FAQ, provide:
1. Question: A rigorous, academically-sound {self.level_desc} question formatted as an actual interrogative sentence, independent from the content, semantically distinct from other questions, precisely formulated, with an OBJECTIVE answer verifiable from peer-reviewed sources
2. Answer: A comprehensive, academically rigorous answer grounded in peer-reviewed literature, established theories, and empirical evidence, NOT the provided content"""

	def build_topic_prompt(self, topic: str) -> str:
		"""
		Build prompt for topic-based FAQ generation.

		Args:
			topic: Topic to generate FAQs about

		Returns:
			Formatted prompt string
		"""
		question_types = self._get_topic_question_types()
		return f"""Generate {self.num_faqs} frequently asked questions about {topic} with {self.level_desc} answers.

{self.QUESTION_FORMAT}{self._get_research_guidance(topic)}

SEMANTIC DIVERSITY REQUIREMENTS:
- Each question must address a DIFFERENT semantic concept or aspect of {topic}
- Questions must NOT be paraphrases or variations of the same underlying question
- Avoid asking about the same concept from only slightly different angles
- Each question should explore a fundamentally distinct topic area, perspective, or problem domain
- Vary the question types: {question_types}

{self.QUALITY_CRITERIA}
- Questions should cover established knowledge and empirically-supported practices in the domain
- Answers should be comprehensive, rigorous, and grounded in peer-reviewed scholarship

For each FAQ, provide:
1. Question: A rigorous, academically-sound {self.level_desc} question formatted as an actual interrogative sentence, precise, professionally worded, semantically distinct from other questions, and with an OBJECTIVE answer verifiable from peer-reviewed sources
2. Answer: A comprehensive, academically rigorous answer grounded in peer-reviewed literature, established theories, and empirical evidence in the field

Generate questions that leading researchers and experts in {topic} would ask. Ensure all questions are formatted as actual interrogative sentences, are unique, semantically diverse, rigorous, and have objective answers supported by peer-reviewed literature and established consensus. Each question should explore a different facet of the topic at an academic standard."""


# ==============================================================================
# FAQ Generator Class
# ==============================================================================

class FAQGenerator:
	"""Generate frequently asked questions on a given topic with selectable difficulty levels."""

	def __init__(self, config: FAQConfig):
		"""
		Initialize the FAQ generator.

		Args:
			config: FAQConfig dataclass with generator settings
		"""
		self.config = config
		self.logger = setup_logging(config.log_file)
		self.model = config.model or "ollama/gemma3"
		self.prompt_builder = PromptBuilder(config.num_faqs, config.difficulty)

	def _read_content_file(self, file_path: str) -> str:
		"""
		Read content from file.

		Args:
			file_path: Path to content file

		Returns:
			File content as string

		Raises:
			ValueError: If file cannot be read
		"""
		try:
			with open(file_path, 'r', encoding='utf-8') as f:
				content = f.read()
			self.logger.info(f"Loaded content from {file_path}")
			return content
		except IOError as e:
			raise ValueError(f"Failed to read content file: {e}")

	def _create_prompt(self, content: Optional[str] = None) -> str:
		"""
		Create the prompt for generating FAQs.

		Args:
			content: Optional content to extract FAQs from

		Returns:
			Formatted prompt string for the LLM
		"""
		if content:
			return self.prompt_builder.build_content_prompt(content)

		topic = self.config.get_topic() or "this topic"
		return self.prompt_builder.build_topic_prompt(topic)

	def _handle_api_error(self, error: Exception) -> NoReturn:
		"""
		Handle and translate API errors to meaningful exceptions.

		Args:
			error: Exception raised during API call

		Raises:
			RuntimeError: Always raises with appropriate error message
		"""
		error_str = str(error).lower()

		if "401" in str(error) or "authentication" in error_str:
			self.logger.error("Authentication failed: Check your API credentials")
			raise RuntimeError(
				"API authentication failed. Check LITELLM_API_KEY or model-specific credentials."
			)
		elif "429" in str(error):
			self.logger.error("Rate limit exceeded")
			raise RuntimeError("API rate limit exceeded. Please try again later.")
		elif "404" in str(error):
			self.logger.error("Model not found")
			raise RuntimeError("Model not found or not available.")
		else:
			self.logger.error(f"Unexpected error: {error}")
			raise RuntimeError(f"Failed to generate FAQs: {error}")

	def generate(self) -> list[FAQ]:
		"""
		Generate FAQs based on configuration.

		Returns:
			List of FAQ instances

		Raises:
			ValueError: If parameters are invalid
			RuntimeError: If API call fails or required credentials are missing
		"""
		# Read content file if input_source is a file
		content = None
		if self.config.is_file():
			content = self._read_content_file(self.config.get_file_path())

		source_type = "file" if self.config.is_file() else "topic"
		self.logger.info(
			f"Generating {self.config.num_faqs} {self.config.difficulty} FAQs from "
			f"{source_type} '{self.config.input_source}' using model: {self.model}"
		)

		try:
			# Create ModelConfig and LiteClient
			model_config = ModelConfig(model=self.model, temperature=self.config.temperature)
			client = LiteClient(model_config=model_config)

			# Create ModelInput with prompt and response format
			model_input = ModelInput(
				user_prompt=self._create_prompt(content),
				response_format=FAQResponse
			)

			# Generate text using LiteClient (returns parsed FAQResponse)
			response = client.generate_text(model_input=model_input)

			if not isinstance(response, FAQResponse):
				raise ValueError("Expected FAQResponse object from model")

			if not response.faqs:
				raise ValueError("No FAQs returned in response")

			self.logger.info(f"Successfully generated {len(response.faqs)} FAQ(s)")
			return response.faqs

		except Exception as e:
			self._handle_api_error(e)

	def save_to_file(self, faqs: list[FAQ]) -> str:
		"""
		Save FAQs to a JSON file.

		Args:
			faqs: List of FAQ objects to save

		Returns:
			Path to the saved file

		Raises:
			IOError: If file cannot be written
		"""
		# Generate automatic filename
		safe_source = re.sub(r'[^a-zA-Z0-9_-]', '_', self.config.input_source.lower())
		# Remove file extension if present
		safe_source = re.sub(r'\.[^.]+$', '', safe_source)
		output_filename = f"faq_{safe_source}_{self.config.difficulty}_{len(faqs)}.json"
		output_path = os.path.join(self.config.output_dir, output_filename)

		source_label = "file" if self.config.is_file() else "topic"
		data_to_save = {
			"source_type": source_label,
			"source": self.config.input_source,
			"difficulty": self.config.difficulty,
			"faqs": [faq.model_dump() for faq in faqs]
		}

		try:
			with open(output_path, 'w', encoding='utf-8') as f:
				json.dump(data_to_save, f, indent=4)

			os.chmod(output_path, 0o644)
			self.logger.info(f"Successfully saved {len(faqs)} FAQ(s) to {output_path}")
			return output_path

		except IOError as e:
			self.logger.error(f"Failed to write output file: {e}")
			raise


# ==============================================================================
# Validation Functions
# ==============================================================================

def validate_num_faqs(num_str: str) -> int:
	"""
	Validate number of FAQs is in valid range.

	Args:
		num_str: Number as string

	Returns:
		Validated integer

	Raises:
		argparse.ArgumentTypeError: If invalid
	"""
	try:
		num = int(num_str)
	except ValueError:
		raise argparse.ArgumentTypeError(f"Must be an integer, got '{num_str}'")

	if num < FAQConfig.MIN_FAQS or num > FAQConfig.MAX_FAQS:
		raise argparse.ArgumentTypeError(
			f"Must be between {FAQConfig.MIN_FAQS}-{FAQConfig.MAX_FAQS}, got {num}"
		)
	return num


def validate_input_source(source_str: str) -> str:
	"""
	Validate input source (file path or topic string).

	Args:
		source_str: Input source to validate

	Returns:
		Validated input source

	Raises:
		argparse.ArgumentTypeError: If invalid
	"""
	if not source_str or not source_str.strip():
		raise argparse.ArgumentTypeError("Input source cannot be empty")

	source_str = source_str.strip()

	# If file exists, accept it
	if os.path.exists(source_str):
		return source_str

	# Otherwise validate as topic string
	if len(source_str) < 2 or len(source_str) > 100:
		raise argparse.ArgumentTypeError(
			"Topic must be 2-100 characters (or provide valid file path)"
		)
	return source_str


def validate_difficulty(difficulty_str: str) -> str:
	"""
	Validate difficulty level.

	Args:
		difficulty_str: Difficulty level

	Returns:
		Normalized difficulty level

	Raises:
		argparse.ArgumentTypeError: If invalid
	"""
	difficulty = difficulty_str.lower().strip()
	if difficulty not in FAQConfig.VALID_DIFFICULTIES:
		raise argparse.ArgumentTypeError(
			f"Must be: {', '.join(FAQConfig.VALID_DIFFICULTIES)}, got '{difficulty_str}'"
		)
	return difficulty


# ==============================================================================
# CLI Functions
# ==============================================================================

def arguments_parser() -> argparse.ArgumentParser:
	"""Create and configure argument parser."""
	parser = argparse.ArgumentParser(
		description="Generate frequently asked questions on a given topic or from content",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""
Examples:
  # Generate FAQs from topic
  python faq_generator.py -i "Python Programming" -n 10 -d simple
  python faq_generator.py --input "Machine Learning" --num-faqs 5 --difficulty hard
  python faq_generator.py -i "Web Development" -n 8 -d medium -m claude-3-opus

  # Generate FAQs from content file
  python faq_generator.py -i content.txt -n 5 -d research
  python faq_generator.py --input article.md --num-faqs 10 --difficulty medium
		"""
	)

	parser.add_argument(
		"-i",
		"--input",
		required=True,
		type=validate_input_source,
		dest="input_source",
		help="Input source: topic string (2-100 chars) or path to content file (txt, md, etc). "
		     "If a file path exists, file is processed; otherwise treated as topic string"
	)

	parser.add_argument(
		"-n",
		"--num-faqs",
		default=5,
		type=validate_num_faqs,
		dest="num_faqs",
		help="Number of FAQs to generate (1-100). Determines how many question-answer pairs to create"
	)

	parser.add_argument(
		"-d",
		"--difficulty",
		required=False,
		default="medium",
		type=validate_difficulty,
		dest="difficulty",
		choices=FAQConfig.VALID_DIFFICULTIES,
		help="Difficulty level: simple (beginner-friendly), medium (intermediate, practical), "
		     "hard (advanced, specialized knowledge), research (cutting-edge, open problems). "
		     "Default: medium"
	)

	parser.add_argument(
		"-m",
		"--model",
		default=None,
		dest="model",
		help="LLM model identifier in format 'provider/model' (e.g., 'ollama/gemma3', 'gpt-4', 'claude-3-opus'). "
		     "Default: ollama/gemma3"
	)

	parser.add_argument(
		"-t",
		"--temperature",
		type=float,
		default=0.3,
		dest="temperature",
		help="Sampling temperature controlling output randomness (0.0-2.0). Lower values = more deterministic. "
		     "Default: 0.3"
	)

	parser.add_argument(
		"-o",
		"--output",
		default=".",
		dest="output_dir",
		help="Output directory path for saving FAQ JSON file. Directory must exist. Default: current directory"
	)

	return parser


def main() -> int:
	"""
	Main entry point for the FAQ generator CLI.

	Returns:
		Exit code (0 for success, 1 for error)
	"""
	parser = arguments_parser()
	args = parser.parse_args()

	try:
		# Create configuration
		config = FAQConfig(
			input_source=args.input_source,
			num_faqs=args.num_faqs,
			difficulty=args.difficulty,
			model=args.model,
			temperature=args.temperature,
			output_dir=args.output_dir
		)

		# Initialize generator
		generator = FAQGenerator(config)

		# Determine source type
		source_type = "file" if config.is_file() else "topic"
		print(f"Generating {config.num_faqs} {config.difficulty} FAQs from {source_type} '{config.input_source}'...")

		# Generate FAQs
		faqs = generator.generate()

		if not faqs:
			generator.logger.error("No FAQs returned from API")
			return 1

		# Save to file
		output_file = generator.save_to_file(faqs)

		print(f"FAQ generation complete. Saved to {output_file}")
		return 0

	except ValueError as e:
		print(f"Error: {e}", file=sys.stderr)
		return 1
	except RuntimeError as e:
		print(f"Error: {e}", file=sys.stderr)
		return 1
	except IOError as e:
		print(f"Error: {e}", file=sys.stderr)
		return 1
	except Exception as e:
		print(f"Unexpected error: {e}", file=sys.stderr)
		return 1


if __name__ == "__main__":
	sys.exit(main())
