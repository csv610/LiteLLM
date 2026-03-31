"""nobel_prize_prompts.py - PromptBuilder class for Nobel Prize information

Contains the PromptBuilder class for creating structured prompts
for fetching Nobel Prize winner information from LLM.
"""

class PromptBuilder:
    """Builder class for creating prompts for Nobel Prize information."""
    
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
    def create_validation_prompt() -> str:
        """
        Create a prompt for validating Nobel Prize information.
        
        Returns:
            Validation prompt string for LLM
        """
        return """Please validate the following Nobel Prize information for accuracy and completeness:

Check for:
1. Factual accuracy of dates, names, and events
2. Proper scientific terminology and concepts
3. Logical consistency in career timelines
4. Appropriate level of detail for educational content
5. Absence of subjective language or superlatives
6. Complete coverage of all required sections

Ensure the information is:
- Factually correct and verifiable
- Educational and informative
- Free from bias or subjective claims
- Well-structured and organized
- Appropriate for the intended audience"""
