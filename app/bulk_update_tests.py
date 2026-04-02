import os

APPS = {
    "ArticleReviewer": {
        "nonagentic": {"file": "nonagentic/article_reviewer.py", "class": "ArticleReviewer", "method": "review", "is_async": False, "input": "'The quick brown fox jumps over the lazy dog. This is a redundant sentence.'", "model": "ArticleReviewModel"}
    },
    "DeepDeliberation": {
        "noagentic": {"file": "noagentic/deep_deliberation.py", "class": "DeepDeliberation", "method": "run", "is_async": False, "input": "('Quantum Computing', 1)", "model": "KnowledgeSynthesis"}
    },
    "DeepIntuition": {
        "nonagentic": {"file": "nonagentic/deep_intuition.py", "class": "DeepIntuition", "method": "generate_story", "is_async": False, "input": "'The First Moon Landing'", "model": "DeepIntuitionStory"}
    },
    "FAQGenerator": {
        "nonagentic": {"file": "nonagentic/faq_generator.py", "class": "FAQGenerator", "method": "generate_text", "is_async": False, "input": "FAQInput(input_source='Python', num_faqs=2, difficulty='simple')", "model": "FAQResponse", "extra_imports": ", FAQInput"}
    },
    "GenerateBook": {
        "nonagentic": {"file": "nonagentic/bookchapters_generator.py", "class": "BookChaptersGenerator", "method": "generate_text", "is_async": False, "input": "'The Future of Humanity'", "model": "BookChapters"}
    },
    "HilbertProblems": {
        "nonagentic": {"file": "nonagentic/hilbert_problems.py", "class": "HilbertProblemsGuide", "method": "generate_text", "is_async": False, "input": "'The Continuum Hypothesis'", "model": "HilbertProblemResponse"}
    },
    "MathEquationStory": {
        "nonagentic": {"file": "nonagentic/math_equation_story_generator.py", "class": "MathEquationStoryGenerator", "method": "generate_text", "is_async": False, "input": "'E=mc^2'", "model": "MathEquationStory"}
    },
    "MathTheories": {
        "nonagentic": {"file": "nonagentic/math_theory_element.py", "class": "MathTheoryExplainer", "method": "fetch_theory_explanation", "is_async": False, "input": "'Pythagorean Theorem'", "model": "MathTheory"}
    },
    "NobelPrizeWinners": {
        "nonagentic": {"file": "nonagentic/nobel_prize_explorer.py", "class": "NobelPrizeWinnerInfo", "method": "fetch_winners", "is_async": False, "input": "('Physics', 2023)", "model": "NobelWinnersResponse"}
    },
    "ObjectGuesser": {
        "nonagentic": {"file": "nonagentic/object_guesser_game.py", "class": "ObjectGuessingGame", "method": "play", "is_async": False, "input": "'Apple'", "model": "GameState"}
    },
    "Paradox": {
        "nonagentic": {"file": "nonagentic/paradox_element.py", "class": "ParadoxExplainer", "method": "fetch_paradox_explanation", "is_async": False, "input": "'The Grandfather Paradox'", "model": "Paradox"}
    },
    "PeriodicTable": {
        "nonagentic": {"file": "nonagentic/periodic_table_element.py", "class": "PeriodicTableElement", "method": "fetch_element_info", "is_async": False, "input": "'Gold'", "model": "ElementInfo"}
    },
    "Quadrails": {
        "nonagentic": {"file": "nonagentic/guardrail.py", "class": "GuardrailAnalyzer", "method": "analyze_text", "is_async": False, "input": "'I love coding and artificial intelligence.'", "model": "GuardrailResponse"}
    },
    "Riemann": {
        "nonagentic": {"file": "nonagentic/riemann_problems.py", "class": "RiemannTheoryGuide", "method": "generate_text", "is_async": False, "input": "'Riemann Hypothesis'", "model": "RiemannProblemResponse"}
    },
    "ScholarWork": {
        "nonagentic": {"file": "nonagentic/scholar_work_generator.py", "class": "ScholarWorkGenerator", "method": "generate_text", "is_async": False, "input": "'Albert Einstein'", "model": "ScholarMajorWork"}
    },
    "StudyGuide": {
        "nonagentic": {"file": "nonagentic/studyguide_generator.py", "class": "StudyGuideGenerator", "method": "generate_and_save", "is_async": False, "input": "'Calculus'", "model": "StudyGuide"}
    },
    "UnsolvedProblems": {
        "nonagentic": {"file": "nonagentic/unsolved_problems_explorer.py", "class": "UnsolvedProblemsExplorer", "method": "generate_text", "is_async": False, "input": "'Dark Matter'", "model": "UnsolvedProblemResponse"}
    }
}

TEMPLATE_SYNC = """import unittest
import os
import sys
import json
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from lite.config import ModelConfig
from {import_path} import {class_name}{extra_imports}
from {model_import_path} import {model_name}

class LiveTest{class_name}(unittest.TestCase):
    def test_live_{version}(self):
        print(f"\\nStarting live test for {app_name} ({version})...")
        model = os.getenv("DEFAULT_LLM_MODEL", "ollama/gemma3:12b-cloud")
        model_config = ModelConfig(model=model, temperature=0.3)
        instance = {class_name}(model_config)
        
        input_data = {input_data}
        
        if isinstance(input_data, tuple):
            result = instance.{method}(*input_data)
        else:
            result = instance.{method}(input_data)
        
        self.assertIsNotNone(result)
        print(f"\\nLive test for {app_name} ({version}) completed successfully.")

if __name__ == "__main__":
    unittest.main()
"""

def generate_tests():
    for app_name, versions in APPS.items():
        for version_name, info in versions.items():
            file_path = f"{app_name}/{info['file']}"
            dir_path = os.path.dirname(file_path)
            test_file_name = f"test_{app_name.lower()}_{version_name}_live.py"
            test_file_path = os.path.join(dir_path, test_file_name)
            
            import_path = f"{app_name}.{version_name}.{os.path.basename(info['file'])[:-3]}"
            
            model_file = os.path.basename(info['file']).replace("agents.py", "models.py").replace("_agents.py", "_models.py").replace("explorer.py", "models.py").replace("_explorer.py", "_models.py").replace("game.py", "models.py").replace("_game.py", "_models.py").replace("generator.py", "models.py").replace("_generator.py", "_models.py").replace("element.py", "models.py").replace("_element.py", "_models.py").replace("problems.py", "models.py").replace("_problems.py", "_models.py").replace("guardrail.py", "models.py")
            
            # Manual overrides for model file names if heuristic fails
            if app_name == "ArticleReviewer":
                model_file = "article_reviewer_models.py"
            elif app_name == "FAQGenerator":
                model_file = "faq_generator_models.py"
            elif app_name == "DeepDeliberation":
                model_file = "deep_deliberation_models.py"
            elif app_name == "MillenniumPrize":
                model_file = "millennium_prize_models.py"
            elif app_name == "Quadrails":
                model_file = "guardrail_models.py"
            
            model_import_path = f"{app_name}.{version_name}.{model_file[:-3]}"
            
            extra_imports = info.get("extra_imports", "")
            
            template_args = {
                "import_path": import_path,
                "class_name": info["class"],
                "extra_imports": extra_imports,
                "model_import_path": model_import_path,
                "model_name": info["model"],
                "version": version_name,
                "app_name": app_name,
                "method": info["method"],
                "input_data": info["input"]
            }
            
            content = TEMPLATE_SYNC.format(**template_args)
            
            with open(test_file_path, "w") as f:
                f.write(content)
            print(f"Created/Updated {test_file_path}")

if __name__ == "__main__":
    generate_tests()
