"""
faq_generator_prompts.py - Prompt builder for FAQ generation

Contains the PromptBuilder class for creating comprehensive prompts
for generating frequently asked questions with configurable difficulty levels.
"""

from typing import Optional


class PromptBuilder:
    """Builds prompts for FAQ generation with configurable difficulty levels."""

    DIFFICULTY_DESC = {
        "simple": "beginner-friendly and basic concepts that anyone can understand",
        "medium": "intermediate level covering practical knowledge and common scenarios",
        "hard": "advanced topics requiring specialized knowledge and deeper understanding",
        "research": "cutting-edge research questions, open problems, and expert-level discussions"
    }

    QUALITY_CRITERIA = """
QUALITY CRITERIA - ACADEMIC STANDARDS:
- Each question must be complete, standalone, and self-contained (understandable without external context)
- Questions must be precise, unambiguous, and professionally worded
- ANSWERS MUST BE OBJECTIVE, NOT SUBJECTIVE - avoid questions requiring opinions, beliefs, or personal judgment
- ANSWERS MUST BE VERIFIABLE FROM PEER-REVIEWED LITERATURE, ACADEMIC TEXTBOOKS, AND AUTHORITATIVE SCIENTIFIC SOURCES
- ONLY ask questions with definitive, measurable, scientifically-supported answers
- Avoid vague, open-ended, interpretive, or opinion-based questions
- Avoid questions about "best," "better," or subjective preferences without objective metrics
- Each question must meet the highest academic and scientific standards
- Questions should be suitable for academic papers, textbooks, and peer-reviewed publications"""

    SEMANTIC_DIVERSITY = """
SEMANTIC DIVERSITY REQUIREMENTS:
- Each question must address a DIFFERENT semantic concept or aspect of domain
- Questions must NOT be paraphrases or variations of the same underlying question
- Avoid asking about the same concept from only slightly different angles
- Each question should explore a fundamentally distinct topic area, perspective, or problem domain
- Vary question types: cause-effect, comparison, application, theory, challenges, evolution, relationships"""

    QUESTION_FORMAT = """
STRICT REQUIREMENTS - GENERATE QUESTIONS NOT IMPERATIVES:

1. ALL questions MUST be formatted as actual questions using interrogative sentence structure
2. Questions MUST start with question words: "What," "How," "Why," "When," "Where," "Which," "Can," "Does," "Is," "Should," etc.
3. Do NOT generate imperatives (commands like "Explain," "Describe," "Elaborate," "Differentiate")"""

    def __init__(self, num_faqs: int, difficulty: str):
        """
        Initialize prompt builder.

        Args:
            num_faqs: Number of FAQs to generate
            difficulty: Difficulty level (simple, medium, hard, research)
        """
        self.num_faqs = num_faqs
        self.difficulty = difficulty
        self.level_desc = self.DIFFICULTY_DESC.get(difficulty, "intermediate level")

    def _get_research_guidance(self, context: str = "") -> str:
        """
        Get research-level guidance for prompt.

        Args:
            context: Optional context (topic or "content" for file-based)

        Returns:
            Research guidance string or empty string if not research level
        """
        if self.difficulty != "research":
            return ""

        context_str = f" in {context}" if context else ""
        return f"""
RESEARCH-LEVEL FOCUS:
- Generate questions about OPEN PROBLEMS and unsolved challenges{context_str}
- Focus on CUTTING-EDGE research directions and recent advances that challenge prior assumptions
- Ask about CURRENT RESEARCH GAPS and what remains unknown or contested
- Include questions about EXPERIMENTAL METHODOLOGIES used to investigate phenomena{context_str}
- Ask about LIMITATIONS of current theories, models, or approaches in this field
- Include questions about COMPETING THEORIES or different interpretations of research findings
- Focus on FUTURE RESEARCH DIRECTIONS and emerging methodologies
- Ask about INTERDISCIPLINARY CONNECTIONS and novel approaches from other fields
- Include questions that leading RESEARCHERS AND EXPERTS actively debate or investigate{context_str}
- Questions should address what scholars do NOT yet know or where consensus is evolving"""

    def _get_content_specific_requirements(self) -> str:
        """
        Get content-specific requirements for file-based FAQ generation.

        Returns:
            Content-specific requirements string
        """
        return """
4. Do NOT ask about facts explicitly stated in content
5. Do NOT ask about information directly inferrable from content
6. Instead, generate questions about:
   - Prerequisites and foundational concepts needed to understand this topic
   - Common misconceptions or frequently confused concepts in this domain
   - Practical tips, best practices, and common mistakes people make
   - Related fields, alternative approaches, or competing solutions
   - How this topic relates to other domains or real-world applications
   - Historical context or evolution of concepts in this field
   - Questions that require domain expertise but are independent from the provided text"""

    def _get_topic_question_types(self) -> str:
        """Get question type suggestions for topic-based generation."""
        if self.difficulty == "research":
            return "open problems, cutting-edge advances, research gaps, methodologies, limitations, competing theories, future directions, interdisciplinary connections, emerging consensus"
        return "fundamentals, comparison, application, challenges, best practices, evolution, relationships, controversies"

    def build_content_prompt(self, content: str) -> str:
        """
        Build prompt for content-based FAQ generation.

        Args:
            content: File content to analyze

        Returns:
            Formatted prompt string
        """
        return f"""Analyze the following content to understand its domain and topic. Then generate {self.num_faqs} frequently asked questions with {self.level_desc} answers.

Content:
{content}

{self.QUESTION_FORMAT}{self._get_content_specific_requirements()}{self._get_research_guidance()}

{self.SEMANTIC_DIVERSITY}

{self.QUALITY_CRITERIA}

For each FAQ, provide:
1. Question: A rigorous, academically-sound {self.level_desc} question formatted as an actual interrogative sentence, independent from content, semantically distinct from other questions, precisely formulated, with an OBJECTIVE answer verifiable from peer-reviewed sources
2. Answer: A comprehensive, academically rigorous answer grounded in peer-reviewed literature, established theories, and empirical evidence, NOT the provided content"""

    def build_topic_prompt(self, topic: str) -> str:
        """
        Build prompt for topic-based FAQ generation.

        Args:
            topic: Topic to generate FAQs about

        Returns:
            Formatted prompt string
        """
        question_types = self._get_topic_question_types()
        return f"""Generate {self.num_faqs} frequently asked questions about {topic} with {self.level_desc} answers.

{self.QUESTION_FORMAT}{self._get_research_guidance(topic)}

SEMANTIC DIVERSITY REQUIREMENTS:
- Each question must address a DIFFERENT semantic concept or aspect of {topic}
- Questions must NOT be paraphrases or variations of the same underlying question
- Avoid asking about the same concept from only slightly different angles
- Each question should explore a fundamentally distinct topic area, perspective, or problem domain
- Vary question types: {question_types}

{self.QUALITY_CRITERIA}
- Questions should cover established knowledge and empirically-supported practices in the domain
- Answers should be comprehensive, rigorous, and grounded in peer-reviewed scholarship

For each FAQ, provide:
1. Question: A rigorous, academically-sound {self.level_desc} question formatted as an actual interrogative sentence, precise, professionally worded, semantically distinct from other questions, and with an OBJECTIVE answer verifiable from peer-reviewed sources
2. Answer: A comprehensive, academically rigorous answer grounded in peer-reviewed literature, established theories, and empirical evidence in the field

Generate questions that leading researchers and experts in {topic} would ask. Ensure all questions are formatted as actual interrogative sentences, are unique, semantically diverse, rigorous, and have objective answers supported by peer-reviewed literature and established consensus. Each question should explore a different facet of the topic at an academic standard."""
