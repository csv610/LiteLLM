import unittest
import os
import shutil
from pathlib import Path
from lite.config import ModelConfig
from bookchapters_models import BookInput
from bookchapters_generator import BookChaptersGenerator

class LiveTestGenerateBook(unittest.TestCase):
    def setUp(self):
        self.output_dir = Path(__file__).parent / "test_outputs"
        self.output_dir.mkdir(exist_ok=True)
        # Change to this dir so output is saved here or we can delete it
        self.original_cwd = os.getcwd()
        os.chdir(self.output_dir)
        
    def tearDown(self):
        os.chdir(self.original_cwd)
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)

    def test_live_generate_book(self):
        print("\nStarting live test for GenerateBook...")
        model = os.getenv("DEFAULT_LLM_MODEL", "gemini/gemini-2.5-flash")
        model_config = ModelConfig(model=model, temperature=0.2)
        generator = BookChaptersGenerator(model_config=model_config)
        
        book_input = BookInput(
            subject="Introduction to Python",
            level="High School",
            num_chapters=2
        )
        
        output_file = generator.generate_and_save(book_input)
        
        self.assertIsNotNone(output_file)
        self.assertTrue(os.path.exists(output_file))
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
