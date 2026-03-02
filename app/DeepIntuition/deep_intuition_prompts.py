"""
deep_intuition_prompts.py - Prompts for the Deep Intuition Engine

A comprehensive storytelling prompt designed to uncover the human human struggle, 
systematic exploration, and intuitive 'aha' moments.
"""

class PromptBuilder:
    """Builder class for the Deep Intuition storytelling prompt."""

    @staticmethod
    def get_storytelling_prompt(topic: str) -> str:
        """The single, authoritative prompt for deep intuition storytelling."""
        return f"""Topic: '{topic}'
        
        Your Mission: Uncover the human story behind this discovery.
        1. Demystify the Genius: Show that this discovery wasn't a sudden stroke of magic or superhuman intelligence. It was a human triumph born of persistence.
        2. The Systematic Exploration: Describe the methodical poking at boundaries that led to the discovery. 
        3. The Archive of Failures: What were the specific failed attempts, dead ends, or incorrect hypotheses that thinkers before (or during) this discovery faced? 
        4. The 'Aha!' Moment: Explain the perspective shift that finally made it 'click.' Use an intuitive analogy that a student could grasp.
        5. The Human Triumph: Why does this discovery matter? What was the persistence that made it a triumph? 
        6. The World That Never Was: If this human struggle had failed, how would our world, technology, or mathematics be fundamentally stalled or different today?
        7. Modern Resonance: Why does this discovery still matter to us now?

        CRITICAL: 
        - The combined length of your response MUST BE AT LEAST 1000 WORDS. You must provide deep, rich, and detailed narratives for each section to meet this requirement. Do not provide brief summaries.
        - Use a professional but engaging storyteller tone. Avoid overly technical jargon. Focus on the motivation, the struggle, and the 'Why.'

        STRUCTURED_OUTPUT:
        - topic: {topic}
        - the_human_struggle: string
        - the_aha_moment: string
        - human_triumph_rationale: string
        - counterfactual_world: string
        - modern_resonance: string
        - key_historical_anchors: [list of strings]"""
