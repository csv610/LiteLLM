"""
mathematical_equation_story_prompts.py - Prompt builder for mathematical equation stories

Provides comprehensive prompt building functionality for generating narrative-driven
explanations of mathematical equations in the style of science journalism.
"""

from mathematical_equation_story_models import MathematicalEquationStory


class PromptBuilder:
    """Builder class for creating prompts for mathematical equation story generation."""
    
    @staticmethod
    def create_user_prompt(equation_name: str) -> str:
        """Create the user prompt for generating a mathematical equation story.
        
        Args:
            equation_name: The name of the equation to be explained
            
        Returns:
            str: The formatted user prompt
        """
        return f"""
Write a compelling narrative essay about {equation_name}, written like an article you'd find in Scientific American, Cosmos magazine, or a popular science publication.

CORE PRINCIPLES:
============================================================================

1. NARRATIVE FLOW: Write as a single, coherent story with natural transitions—NOT as sections or labeled parts. The story should flow like a professional essay.

2. ACCESSIBILITY: Make this accessible to intelligent high school students with no specialized math background. Use clear, elegant language.

3. ENGAGEMENT: Draw readers in with genuine intellectual interest. Show why this equation matters and why it's beautiful.

4. ACCURACY: Be mathematically accurate about core concepts, though you can simplify details for clarity.

5. STRUCTURE (But integrated seamlessly):
   - Hook readers with intrigue or a compelling question in the opening
   - Introduce the human or historical context: Who needed this? Why?
   - Build understanding through concrete examples and observations
   - Show how the equation emerges naturally from these observations
   - Explain what the equation really means and why it has this form
   - Connect to real-world applications and implications
   - Leave readers with a sense of wonder about the power of mathematics

THE STORY SHOULD:
============================================================================
- Feel like you're reading journalism or an essay, not a textbook
- Use vivid details and relatable contexts to ground abstract concepts
- Build intellectual momentum—each idea builds on the last
- Include moments that make readers think "Oh! That's why!"
- Show the elegance and beauty of the mathematics
- Make readers feel smart for understanding something profound
- Be substantial enough to fully explore the equation (700-1200 words)

SPECIFIC GUIDANCE FOR {equation_name}:
============================================================================
Research and explore:
1. Where did this equation come from? Who discovered it and why?
2. What real problem does it solve?
3. What makes this equation elegant or surprising?
4. How is it actually used in the modern world?
5. What misconceptions do people have about it?

Then weave these elements into a flowing narrative that brings the equation to life.

TONE & STYLE:
============================================================================
- Professional but warm and engaging
- Conversational without being casual
- Use specific examples and concrete details
- Build a sense of discovery as readers progress
- Celebrate the ingenuity of mathematical thinking
- Make the subject matter feel important and relevant

Write this as a complete essay that could be published in a science magazine.
The reader should finish feeling they understand something profound about mathematics
and the world."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for the mathematical equation story generator.
        
        Returns:
            str: The formatted system prompt
        """
        return """You are a science writer and storyteller for major publications like Scientific American, Cosmos, and The Atlantic. You have the rare ability to make complex mathematical ideas feel accessible, beautiful, and profoundly relevant without dumbing them down.

Your approach:
- You write flowing essays, not explanations with section headers
- You use narrative momentum to carry readers through complex ideas
- You find the human story behind each equation—the curiosity, the problem, the "aha" moment
- You use vivid examples and clear language to make abstractions concrete
- You respect your readers' intelligence while never assuming specialized knowledge
- You show why mathematics matters to real people and real problems
- You celebrate intellectual discovery

Your strength is making readers think: "I didn't know that. That's beautiful. That matters."

Write engaging, flowing prose that reads like published science journalism."""

    @staticmethod
    def create_model_input(equation_name: str) -> dict:
        """Create the complete model input with user prompt, system prompt, and response format.
        
        Args:
            equation_name: The name of the equation to be explained
            
        Returns:
            dict: Dictionary containing user_prompt, system_prompt, and response_format
        """
        return {
            "user_prompt": PromptBuilder.create_user_prompt(equation_name),
            "system_prompt": PromptBuilder.create_system_prompt(),
            "response_format": MathematicalEquationStory
        }
