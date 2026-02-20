"""bookchapters_generator.py - BookChaptersGenerator class

Contains the BookChaptersGenerator class for generating educational
curriculum chapters using LiteClient and structured prompts.
"""

import json
from dataclasses import dataclass
from pathlib import Path

# Add parent directories to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from bookchapters_models import ChapterSuggestion, EducationLevel, BookChaptersModel, BookInput
from bookchapters_prompts import PromptBuilder


class BookChaptersGenerator:
    """Generator class for educational curriculum chapters using LiteClient."""
    
    def __init__(self, model_config: ModelConfig):
        """
        Initialize the generator with model configuration.
        
        Args:
            model_config: ModelConfig with model settings
        """
        self.model_config = model_config
        self.model = model_config.model or "ollama/gemma3"
        self.client = LiteClient(model_config=model_config)
    
    def generate_text(self, book_input: BookInput) -> BookChaptersModel:
        """
        Generate chapter suggestions for a subject at a specific education level.
        
        Args:
            book_input: BookInput containing subject, level, and num_chapters
            
        Returns:
            BookChaptersResponse with generated curriculum
            
        Raises:
            ValueError: If API response is invalid
            RuntimeError: If API call fails
        """
        # Create prompt using PromptBuilder
        prompt = PromptBuilder.build_curriculum_prompt(book_input.subject, book_input.level, book_input.num_chapters)
        
        # Create ModelInput with prompt and response format
        model_input = ModelInput(
            user_prompt=prompt,
            response_format=BookChaptersModel
        )
        
        try:
            # Generate text using LiteClient
            response = self.client.generate_text(model_input=model_input)
            
            if isinstance(response, BookChaptersModel):
                return response
            else:
                raise ValueError(f"Expected BookChaptersResponse, got {type(response).__name__}")
                
        except Exception as e:
            raise
    
    def save_to_file(self, response: BookChaptersModel, book_input: BookInput) -> str:
        """
        Save the generated curriculum to a JSON file.
        
        Args:
            response: BookChaptersResponse with generated curriculum
            book_input: BookInput containing subject and level for filename
            
        Returns:
            Path to the saved file
        """
        # Generate filename using PromptBuilder
        level_code = PromptBuilder.get_level_code(book_input.level)
        subject_normalized = book_input.subject.replace(' ', '_').lower()
        filename = f"{subject_normalized}_{level_code}.json"
        
        try:
            # Convert response to dictionary and save
            data = response.model_dump()
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            
            return filename
            
        except Exception as e:
            raise
    
    def generate_and_save(self, book_input: BookInput) -> str:
        """
        Generate chapters and save to file in one operation.
        
        Args:
            book_input: BookInput containing subject, level, and num_chapters
            
        Returns:
            Path to the saved file
        """
        # Generate curriculum
        response = self.generate_text(book_input)
        
        # Save to file
        return self.save_to_file(response, book_input)
