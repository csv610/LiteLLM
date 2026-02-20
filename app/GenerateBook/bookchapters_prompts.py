"""bookchapters_prompts.py - PromptBuilder class for book chapters generation

Contains the PromptBuilder class for creating structured prompts
for educational curriculum generation across different education levels.
"""

# Module-level constants
EDUCATION_LEVELS = [
    'Middle School',
    'High School', 
    'Undergraduate',
    'Post-Graduate',
    'Professional',
    'General Public'
]

LEVEL_CODES = {
    'Middle School': '0',
    'High School': '1',
    'Undergraduate': '2',
    'Post-Graduate': '3',
    'Professional': '4',
    'General Public': '5'
}


class PromptBuilder:
    """Builder class for creating educational curriculum prompts."""
    
    @staticmethod
    def build_curriculum_prompt(subject: str, level: str = None, num_chapters: int = 12) -> str:
        """
        Build a comprehensive prompt for curriculum generation.
        
        Args:
            subject: The subject or topic
            level: The education level (optional)
            num_chapters: Number of chapters to generate
            
        Returns:
            The complete prompt string
        """
        system_part = PromptBuilder.get_system_prompt(level)
        user_part = PromptBuilder.get_user_prompt(subject, level, num_chapters)
        
        return f"{system_part}\n\n{user_part}"

    @staticmethod
    def get_system_prompt(level: str = None) -> str:
        """
        Get the system prompt for educational curriculum generation.
        
        Args:
            level: The education level. If None, generates for all levels
            
        Returns:
            System prompt string for LLM
        """
        system_prompt = """You are an expert educational curriculum designer with deep knowledge of pedagogy, cognitive development, and educational psychology. Your task is to create comprehensive, engaging, and developmentally appropriate curricula that scaffold learning effectively.

Key Principles:
1. Developmental Appropriateness: Content must match cognitive abilities and developmental stage of target audience
2. Scaffolded Learning: Each chapter should build upon previous knowledge while introducing new concepts
3. Active Learning: Include hands-on activities, experiments, and projects
4. Assessment Alignment: Learning objectives must be measurable and action-oriented
5. Real-World Relevance: Connect academic concepts to practical applications
6. Inclusive Design: Consider diverse learning styles and accessibility needs

Quality Standards:
- Use clear, age-appropriate language
- Provide concrete examples and illustrations
- Ensure logical progression of concepts
- Include formative and summative assessment opportunities
- Address common misconceptions and difficulties
- Incorporate interdisciplinary connections where appropriate"""

        if level is None:
            return system_prompt
        
        # Define level-specific guidelines
        level_specific_guidelines = ""
        if level == 'Middle School':
            level_specific_guidelines = """
Middle School Guidelines (Ages 11-14):
- Focus on concrete thinking and foundational concepts
- Use simple, clear language with short sentences
- Include hands-on activities and simple experiments
- Connect to students' everyday experiences
- Use visual aids and concrete examples
- Limit abstract concepts without concrete examples
- Include group activities and collaborative learning
- Assessment through observation and simple projects
- Reading level: 4th-8th grade appropriate material"""
        elif level == 'High School':
            level_specific_guidelines = """
High School Guidelines (Ages 14-18):
- Build upon middle school foundations
- Introduce more abstract thinking and theoretical concepts
- Include problem-solving and critical thinking exercises
- Use more complex vocabulary with clear definitions
- Connect to real-world applications and career relevance
- Include data analysis and interpretation activities
- Individual and group projects with increasing complexity
- Research skills introduction and practice
- Assessment through presentations, reports, and exams
- Reading level: 9th-12th grade appropriate material"""
        elif level == 'Undergraduate':
            level_specific_guidelines = """
Undergraduate Guidelines (Ages 18-22):
- Advanced theoretical concepts and frameworks
- Emphasize critical analysis and evaluation of evidence
- Include research methodology and literature review
- Use technical terminology with precise definitions
- Connect to current research and industry applications
- Include case studies and problem-based learning
- Independent research projects and presentations
- Assessment through research papers, critiques, and presentations
- Reading level: College-level academic material"""
        elif level == 'Post-Graduate':
            level_specific_guidelines = """
Post-Graduate Guidelines (Ages 22+):
- Cutting-edge research and advanced theoretical frameworks
- Emphasize original research and contribution to knowledge
- Include critical analysis of current research limitations
- Use specialized technical language and methodology
- Connect to current research trends and future directions
- Include grant writing and research funding skills
- Advanced seminar and conference presentation skills
- Independent research with potential for publication
- Assessment through research proposals, literature reviews, and dissertations
- Reading level: Graduate-level academic material"""
        elif level == 'Professional':
            level_specific_guidelines = """
Professional Guidelines (Working Adults):
- Focus on practical applications and industry standards
- Emphasize skill development and competency-based learning
- Connect to professional standards and certifications
- Include real-world case studies and best practices
- Use industry-specific terminology and current trends
- Include project management and collaborative work skills
- Assessment through practical projects, presentations, and skill demonstrations
- Include continuing education and professional development components
- Reading level: Professional development material"""
        else:  # General Public
            level_specific_guidelines = """
General Public Guidelines (All Ages):
- Focus on engaging storytelling and fascinating content
- Use accessible language without technical jargon
- Include real-world examples and "wow factor" content
- Emphasize curiosity, wonder, and exploration
- Connect to everyday life and common experiences
- Use multimedia and interactive elements
- Include diverse perspectives and inclusive content
- Assessment through engagement, feedback, and participation
- Reading level: General audience accessible material"""

        return f"{system_prompt}\n{level_specific_guidelines}"

    @staticmethod
    def get_user_prompt(subject: str, level: str = None, num_chapters: int = 12) -> str:
        """
        Get the user prompt for educational curriculum generation.
        
        Args:
            subject: The subject or topic to create curriculum for
            level: The education level. If None, generates for all levels
            num_chapters: Number of chapters to generate per level
            
        Returns:
            User prompt string for LLM
        """
        if level is None:
            header = f"Create a comprehensive curriculum for teaching '{subject}' across all 6 education levels including General Public."
            instruction = """For each level (Middle School, High School, Undergraduate, Post-Graduate, Professional, General Public):
1. Suggest exactly {num_chapters} chapters that engage and educate the target audience
2. Ensure concepts are age, experience, and audience-appropriate
3. Include prerequisites where applicable
4. For each chapter, provide CLEAR and MEASURABLE LEARNING OBJECTIVES using action verbs (identify, explain, analyze, apply, evaluate, synthesize, etc.)
5. Learning objectives should state exactly what the audience will be able to do or understand after completing the chapter

The curriculum should show logical progression across levels:
- Middle School: introduces fundamental concepts with simple explanations
- High School: builds on fundamentals with more depth and real-world applications
- Undergraduate: covers theory, analysis, and practical applications
- Post-Graduate: includes advanced concepts, research, and specialized topics
- Professional: focuses on practical application, standards, and industry practices
- General Public: fascinating topics for general audience with no specialized background, emphasizing curiosity, wonder, and real-world relevance without technical jargon"""
        else:
            header = f"Create a comprehensive curriculum for teaching '{subject}' for the {level} level."
            instruction = f"Suggest exactly {num_chapters} chapters that engage and educate the target audience at the {level} level."

        return f"""{header}

{instruction}

Generate exactly {num_chapters} chapters for each level requested.

For each chapter, provide:
- Chapter number (sequential within the level)
- Title: Engaging and descriptive
- Summary: Brief overview of chapter content
- Key concepts: 5-7 core concepts with clear definitions
- Prerequisites: What students should know before this chapter
- Learning objectives: 3-5 measurable, action-oriented objectives using verbs like identify, explain, analyze, apply, evaluate, create, compare
- Estimated page count: Realistic length estimate
- Observations: AT LEAST 5 hands-on observations, experiments, or phenomena students should notice
- Experiments: AT LEAST 5 practical experiments or demonstrations students can conduct
- Projects: AT LEAST 5 real-world projects or creative assignments to apply concepts

Quality Requirements:
- Ensure age-appropriate complexity and vocabulary
- Include diverse examples and perspectives
- Provide clear connections to previous chapters
- Incorporate real-world applications and relevance
- Use inclusive and culturally responsive content
- Align with educational standards for the target level

Make sure that learning is truly incremental and builds naturally. For General Public, emphasize engaging storytelling, real-world examples, and the "wow factor" of the subject. Adapt all content to be age-appropriate and feasible for the education level."""
    
    @staticmethod
    def get_level_code(level: str) -> str:
        """
        Get the level code for filename generation.
        
        Args:
            level: The education level name
            
        Returns:
            Level code string
        """
        return LEVEL_CODES.get(level, 'all') if level else 'all'
