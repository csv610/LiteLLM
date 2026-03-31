"""
scholar_work_prompts.py - Multi-agent prompt logic

Provides specialized ModelInput objects for the 3-agent pipeline for scholar work.
"""

from lite.config import ModelInput
from .scholar_work_models import ResearchBrief, ScholarMajorWork

# --- RESEARCHER ---

def get_researcher_input(scholar_name: str, major_contribution: str) -> ModelInput:
    """Creates the ModelInput for the scientific research phase."""
    system_prompt = (
        "You are an elite science historian and technical researcher. "
        "You excel at uncovering the intellectual journey of great scientists— "
        "the specific problems they faced, the paradigms they overturned, "
        "and the human stories that define their breakthrough moments."
    )
    
    user_prompt = f"""Conduct deep research on {scholar_name}'s major work: {major_contribution}.
Focus on:
1. Historical context: What was the scientific consensus before this work?
2. Scientific core: Explain the logic of the discovery or theory.
3. Revolutionary impact: How exactly did this change the field of science?
4. Modern legacy: How is this work still relevant or influential today?
5. Human interest: Find compelling anecdotes or obstacles {scholar_name} had to overcome."""

    return ModelInput(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_format=ResearchBrief
    )

# --- JOURNALIST ---

def get_journalist_input(brief: ResearchBrief) -> ModelInput:
    """Creates the ModelInput for the narrative writing phase."""
    system_prompt = (
        "You are a world-class science journalist for 'The New Yorker' or 'Scientific American'. "
        "You specialize in long-form profiles that bring abstract scientific work to life. "
        "You weave raw research into a beautiful, flowing story without section headers."
    )
    
    user_prompt = f"""Using the following research brief, write a compelling narrative essay about {brief.scholar_name}'s {brief.major_contribution}.
        
RESEARCH BRIEF:
- Scholar: {brief.scholar_name}
- Work: {brief.major_contribution}
- History: {brief.historical_context}
- Scientific Core: {brief.scientific_core}
- Impact: {brief.revolutionary_impact}
- Legacy: {', '.join(brief.modern_legacy)}
- Anecdotes: {', '.join(brief.key_anecdotes)}

CONSTRAINTS:
1. Write as a SINGLE, COHERENT STORY with natural transitions.
2. NO section headers or bullet points.
3. Aim for 800-1500 words.
4. Capture the intellectual excitement and revolutionary nature of the discovery."""

    return ModelInput(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_format=None  # Raw text for maximum narrative freedom
    )

# --- EDITOR ---

def get_editor_input(scholar_name: str, major_contribution: str, story_text: str) -> ModelInput:
    """Creates the ModelInput for the final packaging phase."""
    system_prompt = (
        "You are a senior editor for a high-end science publication. You take "
        "a completed narrative profile and package it into a polished, structured "
        "format with educational materials and an impact summary."
    )
    
    user_prompt = f"""Finalize the following story about {scholar_name} and {major_contribution} into its published format.
        
THE STORY:
{story_text}

TASKS:
1. Create an engaging Title and Subtitle.
2. Extract 5-7 key technical terms and provide clear definitions.
3. Provide a concise impact summary (2-3 paragraphs).
4. Generate 3-5 thought-provoking discussion questions.
5. Ensure the story text is returned polished but structurally intact."""

    return ModelInput(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_format=ScholarMajorWork
    )
