"""
deep_intuition_prompts.py - Structured Agent Prompts for the Deep Intuition Engine
"""

from typing import Dict, Any

class AgentPrompts:
    """Templates and builders for the 5-agent storytelling architecture."""

    HISTORICAL_RESEARCHER = """
    Topic: '{topic}'
    
    Your Mission: Dig into the 'Archive of Failures' for this discovery.
    1. Find at least 3-5 specific historical figures, events, or earlier failed attempts/hypotheses.
    2. Identify the intellectual 'dead ends' that thinkers faced before the breakthrough.
    3. Provide concrete details that anchor the story in reality.

    STRUCTURED_OUTPUT:
    - key_historical_anchors: [list of strings]
    - archive_of_failures_details: string (detailed research notes)
    """

    INTUITION_SPECIALIST = """
    Topic: '{topic}'
    
    Your Mission: Craft the 'Aha!' moment.
    1. Identify the specific perspective shift that finally made the concept 'click.'
    2. Create an intuitive, brilliant analogy that a student could grasp.
    3. Explain the core insight without relying on heavy jargon.

    STRUCTURED_OUTPUT:
    - the_aha_moment: string (the moment of insight)
    - intuitive_analogy: string (the core analogy)
    - core_insight_summary: string
    """

    COUNTERFACTUAL_ANALYST = """
    Topic: '{topic}'
    
    Your Mission: Explore the 'World That Never Was.'
    1. Describe how mathematics, science, or technology would be fundamentally stalled if this discovery hadn't been made.
    2. Identify 2-3 modern applications or resonances of this discovery today.
    3. Articulate the 'cost of failure' for this specific human struggle.

    STRUCTURED_OUTPUT:
    - counterfactual_world: string (a deep look at a world without this discovery)
    - modern_resonance: string (current relevance and applications)
    """

    HUMAN_STRUGGLE_NARRATOR = """
    Topic: '{topic}'
    Research Notes: {historical_data}
    
    Your Mission: Narrate the human triumph.
    1. Frame the discovery as a human triumph born of persistence, not 'superhuman magic.'
    2. Describe the methodical, systematic poking at boundaries.
    3. Synthesize the struggle into a compelling narrative about the human spirit.

    STRUCTURED_OUTPUT:
    - the_human_struggle: string (the narrative of the struggle)
    - human_triumph_rationale: string (why this was a persistence-based triumph)
    """

    LEAD_EDITOR_WEAVER = """
    Topic: '{topic}'
    
    Agent Contributions:
    - Historical/Failures: {historical}
    - Aha! Moment/Analogy: {intuition}
    - Counterfactual/Modern: {counterfactual}
    - Human Struggle Narrative: {struggle}
    
    Your Mission: Weave these contributions into a final, authoritative 1000+ word story.
    1. Ensure the tone is professional, engaging, and storyteller-like.
    2. Connect the sections seamlessly. 
    3. CRITICAL: The total length MUST be at least 1000 words. Expand on the agent contributions to provide deep, rich detail.
    4. Maintain the structure defined in the DeepIntuitionStory model.

    STRUCTURED_OUTPUT (DeepIntuitionStory):
    - topic: {topic}
    - the_human_struggle: string
    - the_aha_moment: string
    - human_triumph_rationale: string
    - counterfactual_world: string
    - modern_resonance: string
    - key_historical_anchors: [list of strings]
    """

    @classmethod
    def build(cls, template: str, **kwargs) -> str:
        """Helper to format templates safely."""
        return template.strip().format(**kwargs)
