import unittest
from unittest.mock import MagicMock, patch
from bookchapters_models import BookInput, ChapterSuggestion, EducationLevel, BookChaptersModel
from bookchapters_prompts import PromptBuilder
from bookchapters_generator import BookChaptersGenerator

class TestBookChaptersModels(unittest.TestCase):
    def test_book_input_validation(self):
        # Test valid input
        book_input = BookInput(subject="Physics", level="High School", num_chapters=10)
        self.assertEqual(book_input.subject, "Physics")
        self.assertEqual(book_input.level, "High School")
        self.assertEqual(book_input.num_chapters, 10)

        # Test default values
        book_input_default = BookInput(subject="Biology")
        self.assertEqual(book_input_default.num_chapters, 12)
        self.assertIsNone(book_input_default.level)

    def test_chapter_suggestion_validation(self):
        chapter = ChapterSuggestion(
            chapter_number=1,
            title="Introduction",
            summary="Intro to physics",
            key_concepts=["Motion", "Force"],
            learning_objectives=["Define speed"],
            observations=["Ball falling"],
            experiments=["Drop a ball"],
            projects=["Build a ramp"]
        )
        self.assertEqual(chapter.chapter_number, 1)
        self.assertEqual(len(chapter.key_concepts), 2)

class TestPromptBuilder(unittest.TestCase):
    def test_build_curriculum_prompt(self):
        prompt = PromptBuilder.build_curriculum_prompt("Chemistry", "Middle School", 5)
        self.assertIn("Chemistry", prompt)
        self.assertIn("Middle School", prompt)
        self.assertIn("5 chapters", prompt)

    def test_get_level_code(self):
        self.assertEqual(PromptBuilder.get_level_code("Middle School"), "0")
        self.assertEqual(PromptBuilder.get_level_code("High School"), "1")
        self.assertEqual(PromptBuilder.get_level_code(None), "all")
        self.assertEqual(PromptBuilder.get_level_code("Unknown"), "all")

class TestBookChaptersGenerator(unittest.TestCase):
    @patch('bookchapters_generator.LiteClient')
    def test_generate_text(self, MockLiteClient):
        # Mocking the LiteClient and its response
        mock_client_instance = MockLiteClient.return_value
        
        mock_response = BookChaptersModel(
            subject="History",
            description="World History",
            education_levels=[
                EducationLevel(
                    level="High School",
                    age_range="14-18",
                    chapters=[
                        ChapterSuggestion(
                            chapter_number=1,
                            title="Ancient Rome",
                            summary="Rise and fall",
                            key_concepts=["Empire", "Republic"],
                            learning_objectives=["Identify key figures"],
                            observations=["Arch structure"],
                            experiments=["Build an arch"],
                            projects=["Map of Rome"]
                        )
                    ],
                    rationale="Foundation for modern history"
                )
            ]
        )
        mock_client_instance.generate_text.return_value = mock_response

        # Initialize generator with a dummy config
        mock_config = MagicMock()
        mock_config.model = "test-model"
        generator = BookChaptersGenerator(mock_config)

        book_input = BookInput(subject="History", level="High School", num_chapters=1)
        result = generator.generate_text(book_input)

        self.assertIsInstance(result, BookChaptersModel)
        self.assertEqual(result.subject, "History")
        mock_client_instance.generate_text.assert_called_once()

    @patch('bookchapters_generator.LiteClient')
    def test_save_to_file(self, MockLiteClient):
        mock_config = MagicMock()
        mock_config.model = "test-model"
        generator = BookChaptersGenerator(mock_config)

        mock_response = BookChaptersModel(
            subject="Math",
            description="Basic Math",
            education_levels=[]
        )
        book_input = BookInput(subject="Math", level="Middle School")
        
        filename = generator.save_to_file(mock_response, book_input)
        self.assertEqual(filename, "math_0.json")

        import os
        self.assertTrue(os.path.exists(filename))
        os.remove(filename) # Clean up

if __name__ == '__main__':
    unittest.main()
