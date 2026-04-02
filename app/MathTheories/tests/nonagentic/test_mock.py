import unittest
from unittest.mock import patch
from MathTheories.nonagentic.math_theory_models import (
    MathTheory, AudienceLevel, TheoryExplanation, SolutionMethods, TheoryResponse
)
from MathTheories.nonagentic.math_theory_element import MathTheoryExplainer
from lite.config import ModelConfig

class TestMathTheoryExplainer(unittest.TestCase):
    def setUp(self):
        self.model_config = ModelConfig(model="ollama/test-model")

    @patch('MathTheories.nonagentic.math_theory_element.LiteClient')
    def test_fetch_theory_explanation_success(self, MockLiteClient):
        # Mocking the client and its response
        mock_client = MockLiteClient.return_value
        
        # Initialize explainer after patching
        explainer = MathTheoryExplainer(self.model_config)
        
        mock_explanation = TheoryExplanation(
            introduction="Test Intro",
            key_concepts=["Concept 1", "Concept 2"],
            why_it_was_created="Test Why",
            problems_solved_or_simplified="Test Problems",
            how_it_is_used_today="Test Usage",
            foundation_for_other_theories="Test Foundation",
            new_research="Test Research",
            solution_methods=SolutionMethods(analytical="Analytical Test", numerical="Numerical Test")
        )
        
        mock_theory = MathTheory(
            theory_name="Test Theory",
            explanations={AudienceLevel.HIGH_SCHOOL: mock_explanation}
        )
        
        mock_response = TheoryResponse(theory=mock_theory)
        mock_client.generate_text.return_value = mock_response

        # Call the method
        result = explainer.fetch_theory_explanation("Test Theory", [AudienceLevel.HIGH_SCHOOL])

        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result.theory_name, "Test Theory")
        self.assertIn(AudienceLevel.HIGH_SCHOOL, result.explanations)
        self.assertEqual(result.explanations[AudienceLevel.HIGH_SCHOOL].introduction, "Test Intro")

    @patch('MathTheories.nonagentic.math_theory_element.LiteClient')
    def test_fetch_theory_explanation_default_level(self, MockLiteClient):
        # Mocking the client and its response
        mock_client = MockLiteClient.return_value
        
        # Initialize explainer after patching
        explainer = MathTheoryExplainer(self.model_config)
        
        mock_explanation = TheoryExplanation(
            introduction="Undergrad Intro",
            key_concepts=["Undergrad Concept"],
            why_it_was_created="Test Why",
            problems_solved_or_simplified="Test Problems",
            how_it_is_used_today="Test Usage",
            foundation_for_other_theories="Test Foundation",
            new_research="Test Research",
            solution_methods=SolutionMethods(analytical="Analytical Test", numerical="Numerical Test")
        )
        
        mock_theory = MathTheory(
            theory_name="Test Theory",
            explanations={AudienceLevel.UNDERGRAD: mock_explanation}
        )
        
        mock_response = TheoryResponse(theory=mock_theory)
        mock_client.generate_text.return_value = mock_response

        # Call the method WITHOUT specifying levels
        result = explainer.fetch_theory_explanation("Test Theory")

        # Assertions
        self.assertIsNotNone(result)
        self.assertIn(AudienceLevel.UNDERGRAD, result.explanations)
        self.assertEqual(len(result.explanations), 1)

if __name__ == "__main__":
    unittest.main()
