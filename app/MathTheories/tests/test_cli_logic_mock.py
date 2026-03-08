
import unittest
from unittest.mock import patch
from math_theory_cli import fetch_theory_info
from math_theory_models import MathTheory, AudienceLevel, TheoryExplanation, SolutionMethods
from lite.config import ModelConfig

class TestCLIFunctionality(unittest.TestCase):
    def setUp(self):
        self.model_config = ModelConfig(model="test-model")

    @patch('math_theory_cli.MathTheoryExplainer')
    def test_fetch_theory_info_call(self, MockExplainer):
        mock_explainer_instance = MockExplainer.return_value
        
        mock_explanation = TheoryExplanation(
            introduction="Intro",
            key_concepts=["Concept A"],
            why_it_was_created="Why",
            problems_solved_or_simplified="Problems",
            how_it_is_used_today="Usage",
            foundation_for_other_theories="Foundation",
            new_research="Research",
            solution_methods=SolutionMethods(analytical="A", numerical="N")
        )
        mock_theory = MathTheory(theory_name="Test", explanations={AudienceLevel.UNDERGRAD: mock_explanation})
        mock_explainer_instance.fetch_theory_explanation.return_value = mock_theory

        result = fetch_theory_info("Test", self.model_config, [AudienceLevel.UNDERGRAD])
        
        MockExplainer.assert_called_once_with(self.model_config)
        mock_explainer_instance.fetch_theory_explanation.assert_called_once_with("Test", audience_levels=[AudienceLevel.UNDERGRAD])
        self.assertEqual(result.theory_name, "Test")

if __name__ == "__main__":
    unittest.main()
