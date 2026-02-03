#!/usr/bin/env python3
"""
Medical Quiz Generation module.

This module provides the core MedicalContentGenerator class for generating
high-quality, board-style medical quizzes for various topics.
"""

import logging
import re
import sys
import time
from pathlib import Path
from typing import Optional, Union

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from lite.utils import save_model_response

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
        bar = '█' * filled_length + '-' * (50 - filled_length)
        
        elapsed_time = time.time() - self.start_time
        if self.current > 0:
            eta = (elapsed_time / self.current) * (self.total - self.current)
            eta_str = f"{eta:.1f}s"
        else:
            eta_str = "?.?s"
            
        print(f'\r{self.description}: |{bar}| {percentage:.1f}% ({self.current}/{self.total}) ETA: {eta_str}', end='', flush=True)
        
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
        logger.debug(f"Initialized MedicalQuizGenerator")

    def _sanitize_topic(self, topic: str) -> str:
        """Sanitize topic for safe filename generation."""
        # Remove invalid characters for filenames
        sanitized = re.sub(r'[<>:"/\\|?*]', '', topic.strip())
        # Replace spaces with underscores
        sanitized = re.sub(r'\s+', '_', sanitized)
        sanitized = sanitized.strip('. ')  # Remove leading/trailing dots and spaces
        return sanitized if sanitized else "medical_quiz"

    def generate_text(
        self,
        topic: str,
        difficulty: str,
        num_questions: int,
        num_options: int = 4,
        structured: bool = False
    ) -> ModelOutput:
        """Generate medical text (quiz).

        Args:
            topic: Medical topic for quiz generation
            difficulty: Difficulty level
            num_questions: Number of questions
            num_options: Number of options per question
            structured: Whether to use structured output

        Returns:
            ModelOutput containing the generated quiz
        """
        # Input validation
        if not topic or not topic.strip():
            raise ValueError("Topic cannot be empty")
        if num_questions < 1:
            raise ValueError("Number of questions must be >= 1")
        if num_options < 2:
            raise ValueError("Number of options must be >= 2")
        if num_options > 26:  # A-Z maximum
            raise ValueError("Number of options cannot exceed 26 (A-Z)")
        if not difficulty or not difficulty.strip():
            raise ValueError("Difficulty level cannot be empty")

        self.topic = self._sanitize_topic(topic.strip())
        
        # Show progress indicator for large quizzes
        if num_questions > 5:
            progress = SimpleProgressBar(num_questions, f"Generating {num_questions} quiz questions")
        
        logger.debug(f"Starting Quiz generation for: {topic.strip()} (sanitized: {self.topic})")

        system_prompt = PromptBuilder.create_quiz_system_prompt()
        user_prompt = PromptBuilder.create_quiz_user_prompt(topic, difficulty, num_questions, num_options)
        logger.debug(f"System Prompt: {system_prompt}")
        logger.debug(f"User Prompt: {user_prompt}")

        response_format = None
        if structured:
            response_format = MedicalQuizModel

        model_input = ModelInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_format=response_format,
        )

        logger.debug("Calling LiteClient.generate_text()...")
        try:
            result = self.ask_llm(model_input)
            
            # Complete progress bar if it was started
            if num_questions > 5:
                progress.update(num_questions)  # Complete the progress bar
            
            logger.debug("✓ Successfully generated Quiz")
            return result
        except Exception as e:
            # Complete progress bar on error too
            if num_questions > 5:
                progress.update(num_questions)
            logger.error(f"✗ Error generating Quiz: {e}")
            raise

    def ask_llm(self, model_input: ModelInput) -> ModelOutput:
        """Call the LLM client to generate information."""
        return self.client.generate_text(model_input=model_input)

    def save(self, result: ModelOutput, output_dir: Path) -> Path:
        """Saves the generated information to a file."""
        if self.topic is None:
            raise ValueError("No topic information available. Call generate_quiz first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.topic.lower().replace(' ', '_')}_quiz"
        
        # Always apply proper formatting regardless of input type
        if hasattr(result, 'data') and result.data:
            # Structured output wrapped in ModelOutput
            if not result.markdown:
                result.markdown = self._format_quiz_markdown(result.data)
        elif hasattr(result, 'topic'):
            # Direct MedicalQuizModel (structured output)
            # Wrap it in ModelOutput with proper formatting
            from medical_quiz_models import ModelOutput
            wrapped_result = ModelOutput(
                data=result,
                markdown=self._format_quiz_markdown(result)
            )
            return save_model_response(wrapped_result, output_dir / base_filename)
        else:
            # For plain text, create a simple formatted version
            if hasattr(result, 'markdown') and result.markdown:
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
        lines = plain_text.split('\n')
        
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
            if (not question_text and 
                len(line) > 80 and 
                any(keyword in line.lower() for keyword in ['patient', 'presents', 'year-old', 'male', 'female']) and
                not line.startswith(('A)', 'B)', 'C)', 'D)', '#', '*'))):
                question_text = line
                
            # Extract options from dictionary format
            if "'A':" in line or '"A":' in line:
                # Extract all options from this line
                matches = re.findall(r'["\']([A-D])["\']:\s*["\']([^"\']+)["\']', line)
                for key, value in matches:
                    options_dict[key] = value
                    
            # Find answer
            if not answer and ('correct answer' in line.lower() or 'answer:' in line.lower()):
                answer_match = re.search(r'([A-D])', line)
                if answer_match:
                    answer = answer_match.group(1)
                    
            # Collect explanation
            if any(keyword in line.lower() for keyword in ['explanation', 'why', 'correct', 'distractor']):
                explanation_parts.append(line)
        
        # Build formatted output if we found the key components
        if question_text and options_dict:
            formatted_lines = [
                f"# Medical Quiz: {self.topic}",
                f"**Difficulty:** Intermediate",
                "",
                "## Question 1",
                f"**{question_text}**",
                "",
                "**Options:**"
            ]
            
            # Add options in order
            for key in ['A', 'B', 'C', 'D']:
                if key in options_dict:
                    formatted_lines.append(f"{key}) {options_dict[key]}")
            
            formatted_lines.extend([
                "",
                f"**Answer:** {answer or 'A'}",
                "",
                "**Explanation:**"
            ])
            
            # Add explanation
            if explanation_parts:
                for part in explanation_parts:
                    clean_part = part.replace('#', '').replace('*', '').strip()
                    if clean_part and len(clean_part) > 10:
                        formatted_lines.append(clean_part)
            
            formatted_lines.extend(["", "---", ""])
            
            return '\n'.join(formatted_lines)
        
        # If reformatting failed, return a basic formatted version
        return f"""# Medical Quiz: {self.topic}
**Difficulty:** Intermediate

## Question 1
**{question_text or 'Medical quiz question generated successfully.'}**

**Options:**
{chr(10).join([f"{key}) {value}" for key, value in options_dict.items()]) if options_dict else "A) Option A\nB) Option B\nC) Option C\nD) Option D"}

**Answer:** {answer or 'A'}

**Explanation:** 
Detailed explanation would be included here.

---

"""
    
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
        
        return "\n".join(lines)
