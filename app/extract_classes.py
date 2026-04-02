import os
import re

def extract_info(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    
    classes = re.findall(r"class (\w+):", content)
    if not classes:
        classes = re.findall(r"class (\w+)\(\w+\):", content)
    
    methods = re.findall(r"def (\w+)\(self", content)
    
    return classes, methods

files = [
    "./ArticleReviewer/agentic/article_reviewer_agents.py",
    "./ArticleReviewer/nonagentic/article_reviewer.py",
    "./DeepDeliberation/agentic/deep_deliberation.py",
    "./DeepDeliberation/noagentic/deep_deliberation.py",
    "./DeepIntuition/agentic/deep_intuition.py",
    "./DeepIntuition/nonagentic/deep_intuition.py",
    "./FAQGenerator/agentic/faq_generator.py",
    "./FAQGenerator/nonagentic/faq_generator.py",
    "./GenerateBook/agentic/bookchapters_generator.py",
    "./GenerateBook/nonagentic/bookchapters_generator.py",
    "./HilbertProblems/agentic/hilbert_problems.py",
    "./HilbertProblems/nonagentic/hilbert_problems.py",
    "./MathEquationStory/agentic/math_equation_story_generator.py",
    "./MathEquationStory/nonagentic/math_equation_story_generator.py",
    "./MathTheories/agentic/math_theory_element.py",
    "./MathTheories/nonagentic/math_theory_element.py",
    "./MillenniumPrize/agentic/millennium_prize_agents.py",
    "./MillenniumPrize/nonagentic/millennium_prize_explorer.py", # Guessing
    "./NobelPrizeWinners/agentic/nobel_prize_explorer.py",
    "./NobelPrizeWinners/nonagentic/nobel_prize_explorer.py",
    "./ObjectGuesser/agentic/object_guesser_game.py",
    "./ObjectGuesser/nonagentic/object_guesser_game.py",
    "./Paradox/agentic/paradox_element.py",
    "./Paradox/nonagentic/paradox_element.py",
    "./PeriodicTable/agentic/periodic_table_element.py",
    "./PeriodicTable/nonagentic/periodic_table_element.py",
    "./Quadrails/agentic/guardrail.py",
    "./Quadrails/nonagentic/guardrail.py",
    "./Riemann/agentic/riemann_problems.py",
    "./Riemann/nonagentic/riemann_problems.py",
    "./ScholarWork/agentic/scholar_work_generator.py",
    "./ScholarWork/nonagentic/scholar_work_generator.py",
    "./StudyGuide/agentic/studyguide_generator.py",
    "./StudyGuide/nonagentic/studyguide_generator.py",
    "./UnsolvedProblems/agentic/unsolved_problems_explorer.py",
    "./UnsolvedProblems/nonagentic/unsolved_problems_explorer.py",
]

# Note: I need to check some guessed files.
for f in files:
    if os.path.exists(f):
        c, m = extract_info(f)
        print(f"{f}: Classes={c}, Methods={m}")
    else:
        print(f"{f}: FILE NOT FOUND")
