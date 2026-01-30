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
        # Remove leading/trailing dots and spaces
        sanitized = sanitized.strip('. ')
        # Ensure we don't have empty string
        return sanitized if sanitized else "medical_quiz"

    def generate_quiz(
        self,
        topic: str,
        difficulty: str,
        num_questions: int,
        num_options: int = 4,
        structured: bool = False
    ) -> ModelOutput:
        """Generate medical quiz.

        Args:
            topic: Medical topic for quiz generation
            difficulty: Difficulty level
            num_questions: Number of questions
            num_options: Number of options per question
            structured: Whether to use structured output (Pydantic model)

        Returns:
            ModelOutput: Structured or plain text result
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
            raise ValueError("No topic information available. Call generate_text or generate_quiz first.")
        
        # Generate base filename - save_model_response will add appropriate extension
        base_filename = f"{self.topic.lower().replace(' ', '_')}_{self.content_type}"
        
        return save_model_response(result, output_dir / base_filename)
