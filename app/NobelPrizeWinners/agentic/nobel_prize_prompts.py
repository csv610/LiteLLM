"""nobel_prize_prompts.py - PromptBuilder class for Nobel Prize information

Contains the PromptBuilder class for creating structured prompts
for fetching Nobel Prize winner information from LLM.
"""

from .nobel_prize_models import PrizeResponse

class PromptBuilder:
    """Builder class for creating prompts for Nobel Prize information."""

    @staticmethod
    def create_agent_system_prompt(agent_name: str) -> str:
        """Create a system prompt for a specific agent role."""
        if agent_name == "generation_agent":
            return (
                "You are the generation agent for Nobel Prize winner data. "
                "Produce complete, factual, structured educational content that matches the requested schema. "
                "Avoid subjective language and unsupported claims."
            )

        if agent_name == "validation_agent":
            return (
                "You are the validation agent for Nobel Prize winner data. "
                "Review generated content for factual consistency, schema correctness, and objective wording. "
                "Correct errors conservatively and return only the final structured response."
            )

        raise ValueError(f"Unknown agent name: {agent_name}")
    
    @staticmethod
    def create_nobel_prize_prompt(category: str, year: str) -> str:
        """
        Create a comprehensive prompt for fetching Nobel Prize information.
        
        Args:
            category: Nobel Prize category (Physics, Chemistry, Medicine, etc.)
            year: Year of the prize
            
        Returns:
            Formatted prompt string for LLM
        """
        return f"""Provide detailed, objective information about Nobel Prize winners in {category} for {year}.

IMPORTANT: Focus on factual, educational content. Avoid subjective language and superlatives.

For each winner, provide:

BIOGRAPHICAL INFORMATION:
1. Personal Background:
   - Birth date and place
   - Nationality
   - Family background and parents' professions
   - Educational timeline with institutions, degrees, and years
   - Early influences and mentors who shaped their scientific direction

2. Career Timeline:
   - Chronological list of major positions (title, institution, location, start/end years)
   - Key roles including postdoctoral positions, faculty appointments, research leadership
   - Institutional affiliations and their significance

3. Broader Recognition:
   - Major awards and honors (excluding Nobel Prize)
   - Academy and society memberships
   - Editorial roles in scientific journals
   - Notable students, postdocs, and collaborators mentored
   - Leadership positions in scientific organizations
   - Public engagement, outreach, and scientific advocacy efforts

SCIENTIFIC WORK:
4. Contribution: What they discovered or invented (facts only)
5. History: Chronological facts with dates, names, methods used
6. Impact: Measurable changes in scientific understanding - what became possible?
7. Foundation: Specific cross-disciplinary influence with concrete examples
8. Applications: Real-world uses, not speculative
9. Relevancy: How the idea is still valid and relevant today - explain current research, active fields using this work, and practical uses in modern science/industry
10. Advancements: Specific improvements and extensions with dates
11. Refinements: Methodological and theoretical improvements
12. Gaps: Unknown questions, limitations, and unsolved problems

EDUCATIONAL CONTENT:
13. Keywords: Important keywords and technical terms related to the discovery (core concepts, methods, substances, phenomena, and fields)
14. Learning Objectives: What a student can learn from this discovery (conceptual understanding, methodological approaches, problem-solving techniques, insights into the scientific process)
15. FAQ: Frequently asked questions with answers (include common misconceptions, practical questions, and educational queries)
16. Glossary: Dictionary of key terms and concepts with clear, concise definitions (specialized vocabulary, technical terminology, important concepts needed to understand the work)

Use objective language. Avoid words like "revolutionary," "profound," "amazing," "transformed."
Instead, describe what specifically changed and how we know it changed."""
    
    @staticmethod
    def create_validation_prompt(category: str, year: str, generated_response: PrizeResponse) -> str:
        """
        Create a prompt for validating Nobel Prize information.
        
        Returns:
            Validation prompt string for LLM
        """
        generated_json = generated_response.model_dump_json(indent=2)

        return f"""You are the validation agent in a two-agent workflow for Nobel Prize winner data.

The generation agent has already produced structured output for the {category} Nobel Prize in {year}.
Your job is to validate, correct, and return the final structured response.

Review the candidate JSON below and fix any factual issues, omissions, schema inconsistencies, timeline problems, or subjective language.

Check for:
1. Factual accuracy of dates, names, and events
2. Proper scientific terminology and concepts
3. Logical consistency in career timelines
4. Appropriate level of detail for educational content
5. Absence of subjective language or superlatives
6. Complete coverage of all required sections
7. Consistency between the requested category/year and each winner entry

Requirements:
- Return corrected data using the same schema as the input
- Preserve accurate content where possible instead of rewriting everything
- If a claim seems doubtful, prefer a conservative, objective phrasing
- Ensure every winner has category={category} and year={year}
- Output only the final corrected structured response

Candidate JSON:
{generated_json}"""
