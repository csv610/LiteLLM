import unittest
import os
from lite.config import ModelConfig
from app.ArticleReviewer.nonagentic.article_reviewer import ArticleReviewer

class LiveTestArticleReviewer(unittest.TestCase):
    def test_live_review(self):
        print("\nStarting live test for ArticleReviewer...")
        model = os.getenv("DEFAULT_LLM_MODEL", "gemini/gemini-2.5-flash")
        model_config = ModelConfig(model=model, temperature=0.3)
        reviewer = ArticleReviewer(model_config=model_config)
        
        test_article = "The quick brown fox jumps over the lazy dog. This is a redundant sentence. In conclusion, testing is good."
        
        result = reviewer.review(test_article)
        
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, "score"))
        self.assertTrue(hasattr(result, "summary"))
        print("\nLive test completed successfully.")

if __name__ == "__main__":
    unittest.main()
