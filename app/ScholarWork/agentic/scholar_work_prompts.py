"""
scholar_work_prompts.py - Multi-agent prompt logic

Provides specialized ModelInput objects for the 3-agent pipeline for scholar work.
"""

from lite.config import ModelInput
from .scholar_work_models import ResearchBrief, ScholarMajorWork, SynthesizedReport

# --- RESEARCHER ---


def get_researcher_input(scholar_name: str) -> ModelInput:
    """Creates the ModelInput for the scientific research phase."""
    return ModelInput(
        system_prompt="OUTPUT ONLY VALID JSON. ZERO PREAMBLE. ZERO EXPLANATIONS. NO MARKDOWN. NO CODE BLOCKS. YOUR ENTIRE RESPONSE MUST BE A SINGLE JSON OBJECT THAT VALIDATES AGAINST RESEARCHBRIEF SCHEMA.",
        user_prompt=f'Conduct deep research on {scholar_name}\'s complete body of work and identify their major scientific contributions. Return ONLY a JSON object that matches this exact schema: {{"scholar_name": "string", "major_contributions": ["string"], "historical_context": "string", "scientific_core": "string", "revolutionary_impact": "string", "modern_legacy": ["string"], "key_anecdotes": ["string"]}}',
        response_format=ResearchBrief,
    )


# --- SYNTHESIZER ---


def get_journalist_input(brief: ResearchBrief) -> ModelInput:
    """Creates the ModelInput for the synthesis phase."""
    user_prompt = f"""Create a comprehensive, technical list of {brief.scholar_name}'s major work and contributions.
         
RESEARCH DATA:
- Major Contributions: {", ".join(brief.major_contributions)}
- Historical Context: {brief.historical_context}
- Scientific Core: {brief.scientific_core}
- Impact: {brief.revolutionary_impact}
- Legacy: {", ".join(brief.modern_legacy)}
- Anecdotes: {", ".join(brief.key_anecdotes)}

CONSTRAINTS:
1. Provide a COMPREHENSIVE LIST of distinct major works, discoveries, and contributions.
2. DEPTH: Each item in the list should be a substantial paragraph explaining the work, its context, and its significance.
3. STRUCTURE: For each contribution, explain: What was it? Why was it revolutionary? What problem did it solve?
4. Connect each work to its lasting technical impact in the field.
5. Use clear, precise scientific language suitable for an intelligent reader.
6. OUTPUT ONLY VALID JSON. ZERO PREAMBLE. YOUR ENTIRE RESPONSE MUST BE A SINGLE JSON OBJECT THAT VALIDATES AGAINST SYNTHESIZEDREPORT SCHEMA."""

    return ModelInput(
        system_prompt="You are a meticulous science historian and technical synthesizer. You provide comprehensive, authoritative lists of scientific contributions. You MUST respond with ONLY a valid JSON object matching the SynthesizedReport schema.",
        user_prompt=user_prompt,
        response_format=SynthesizedReport,
    )


# --- EDITOR ---


def get_editor_input(scholar_name: str, synthesized_report: SynthesizedReport) -> ModelInput:
    """Creates the ModelInput for the final packaging phase."""
    report_text = "\n\n".join(synthesized_report.contributions)
    user_prompt = f"""Finalize this contribution report for {scholar_name} into its published format.
    
REPORT CONTENT:
{report_text}

TASKS:
1. Create a clear Title and Subtitle.
2. Extract key terms and definitions.
3. Provide an impact summary.
4. Generate 3-5 discussion questions.
5. Package the contribution list as provided.

OUTPUT FORMAT:
Return the final report as a BEAUTIFULLY FORMATTED MARKDOWN STRING.
Use:
- # for the Title
- ## for the Subtitle and main sections (Major Works, Key Terms, Impact, etc.)
- Bullet points for lists
- Bold text for emphasis
- Horizontal rules (---) to separate sections

DO NOT use JSON. DO NOT use code blocks for the entire response. Just return the Markdown text."""

    return ModelInput(
        system_prompt="You are a senior editor. Package the research report into a polished, publication-ready Markdown document.",
        user_prompt=user_prompt,
        response_format=None,
    )
