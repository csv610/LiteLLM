"""
deep_deliberation_prompts.py - Prompts for the Knowledge Discovery Engine

Strategic adversarial prompts for probing beyond surface-level facts.
"""

from typing import List


class PromptBuilder:
    """Builder class for strategic knowledge discovery prompts."""

    @staticmethod
    def get_initial_prompt(topic: str, num_faqs: int = 5) -> str:
        """Prompt to map core pillars and probe the unknown."""
        return f"""Topic: '{topic}'
        Identify the 3 core pillars of established knowledge in this field. 
        Then, generate {num_faqs} strategic 'Discovery Questions' (FAQs) specifically designed to probe the most significant 'unknowns', 'contradictions', or 'emerging hypotheses' in this topic. 
        For each, provide a rationale on how this probes beyond conventional wisdom.
        
        STRUCTURED_OUTPUT:
        - topic: {topic}
        - core_pillars: [list of strings]
        - discovery_faqs: [list of {{question: string, rationale: string}}]"""

    @staticmethod
    def get_iteration_prompt(topic: str, current_faq: str, rationale: str, context_history: str) -> str:
        """Adversarial analytical prompt for deep discovery."""
        return f"""Main Field of Inquiry: {topic}
        
        Strategic Context (Accumulated Discoveries):
        {context_history}
        
        Target Question: {current_faq}
        Rationale for Inquiry: {rationale}
        
        Your Mission: Perform a deep adversarial analysis of this question. 
        1. Synthesis: Provide an analysis that build upon the strategic context.
        2. Evidence: Identify key evidence or theoretical frameworks.
        3. Counter-arguments: Specifically hunt for contradictions, flaws, or 'hidden' trade-offs. 
        
        CRITICAL: Do not repeat established facts unless they are necessary for a new connection.
        After your analysis, generate exactly ONE new Discovery FAQ that naturally follows this inquiry into deeper, more specialized territory. Provide its rationale.

        STRUCTURED_OUTPUT:
        - analysis: string
        - evidence: [list of strings]
        - counter_arguments: string or null
        - new_discovery_faq: {{question: string, rationale: string}}"""

    @staticmethod
    def get_summary_prompt(topic: str, response_analysis: str) -> str:
        """Prompt to distill a discovery for the next query's history."""
        return f"""Field: '{topic}'
        
        Analysis to distill:
        {response_analysis}
        
        Summarize the key discovery, the most critical piece of evidence, and any identified knowledge gaps in 2-3 dense sentences.

        STRUCTURED_OUTPUT:
        - summary: string"""

    @staticmethod
    def get_discovery_check_prompt(topic: str, response: str) -> str:
        """Target Objective: Knowledge Discovery in '{topic}'
        
        Proposed Insight:
        {response}
        
        Critique this insight. Does it actually discover a non-obvious connection, identify a genuine contradiction, or map a research frontier? 
        If it is purely descriptive, repetitive, or generic, mark it as 'Not Novel'. Give a discovery score from 1-10 based on the 'Density of New Insight'.

        STRUCTURED_OUTPUT:
        - is_novel: boolean
        - discovery_score: integer (1-10)
        - reasoning: string"""

    @staticmethod
    def get_verification_prompt(topic: str, analysis: str, evidence: List[str]) -> str:
        """Adversarial verification prompt to hunt for 'Lying Machine' hallucinations."""
        evidence_str = "\n".join([f"- {e}" for e in evidence])
        return f"""Topic: {topic}
        
        Proposed Analysis:
        {analysis}
        
        Provided Evidence:
        {evidence_str}
        
        Your Mission: Act as a 'Skeptic Verifier'. Interrogate the analysis and evidence above.
        1. Hunt for Hallucinations: Do the cited facts or frameworks sound fabricated or generic?
        2. Logical Leaps: Does the analysis claim more than the evidence supports?
        3. Circular Reasoning: Is the analysis just repeating the question in different words?
        
        If you find significant flaws, mark 'is_verified' as false. Be harsh.

        STRUCTURED_OUTPUT:
        - is_verified: boolean
        - flaws_identified: [list of strings] or null
        - credibility_score: integer (1-10)
        - critique: string"""

    @staticmethod
    def get_synthesis_prompt(topic: str, all_responses: List[str]) -> str:
        """Prompt for the final synthesis of the knowledge map."""
        combined_responses = "\n\n---\n\n".join(all_responses)
        return f"""Topic: {topic}
        
        Below are multiple rounds of deep analytical discovery on this topic.
        Your task is to synthesize these into a 'Strategic Knowledge Map'.
        1. Executive Summary: Synthesis of the discovery mission.
        2. Hidden Connections: Identify non-obvious links across different rounds.
        3. Research Frontiers: Map out exactly where our current understanding ends and the 'Great Unknown' begins.
        
        Responses:
        {combined_responses}

        STRUCTURED_OUTPUT:
        - topic: {topic}
        - executive_summary: string
        - hidden_connections: [list of strings]
        - research_frontiers: [list of strings]"""
