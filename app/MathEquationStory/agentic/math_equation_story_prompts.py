"""
math_equation_story_prompts.py - Multi-agent prompt logic

Provides specialized ModelInput objects for the 3-agent pipeline.
"""

from lite.config import ModelInput
from .math_equation_story_models import ResearchBrief, MathematicalEquationStory

# --- RESEARCHER ---

def get_researcher_input(equation_name: str) -> ModelInput:
    """Creates the ModelInput for the technical research phase."""
    system_prompt = (
        "You are an elite mathematical historian and researcher. "
        "You excel at finding the 'why' behind the math—the human problems that "
        "led to its discovery and the subtle misconceptions people have today."
    )
    
    user_prompt = f"""Conduct deep research on the equation: {equation_name}.
Focus on:
1. Historical context: Who formalized this and what problem were they solving?
2. Mathematical core: Explain the logic simply but precisely.
3. Modern applications: How does this affect our lives today?
4. Metaphors: What are powerful analogies for a non-expert?
5. Misconceptions: What do people usually get wrong?"""

    return ModelInput(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_format=ResearchBrief
    )

# --- JOURNALIST ---

def get_journalist_input(brief: ResearchBrief) -> ModelInput:
    """Creates the ModelInput for the narrative writing phase."""
    system_prompt = (
        "You are a world-class science journalist for 'Quanta Magazine'. "
        "You specialize in long-form narrative essays that make abstract concepts feel visceral. "
        "You weave raw research into a beautiful, flowing story without section headers."
    )
    
    user_prompt = f"""Using the following research brief, write a compelling narrative essay about {brief.equation_name}.
        
RESEARCH BRIEF:
- History: {brief.historical_context}
- Math Core: {brief.mathematical_core}
- Applications: {', '.join(brief.real_world_applications)}
- Metaphors: {', '.join(brief.key_metaphors)}
- Misconceptions: {', '.join(brief.common_misconceptions)}

CONSTRAINTS:
1. Write as a SINGLE, COHERENT STORY with natural transitions.
2. NO section headers or bullet points.
3. Aim for 800-1200 words.
4. Use provided metaphors and show the beauty of the equation."""

    return ModelInput(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_format=None  # Raw text for maximum narrative freedom
    )

# --- EDITOR ---

def get_editor_input(equation_name: str, story_text: str) -> ModelInput:
    """Creates the ModelInput for the final packaging phase."""
    system_prompt = (
        "You are a senior editor and educational designer. You take a completed "
        "science essay and package it into a polished, structured format with "
        "accurate LaTeX and educational materials."
    )
    
    user_prompt = f"""Finalize the following story about {equation_name} into its published format.
        
THE STORY:
{story_text}

TASKS:
1. Create an engaging Title and Subtitle.
2. Provide the accurate LaTeX formula.
3. Extract 5-7 key technical terms and provide clear definitions.
4. Generate 3-5 thought-provoking discussion questions.
5. Ensure the story text is returned polished but structurally intact."""

    return ModelInput(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_format=MathematicalEquationStory
    )
