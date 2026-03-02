class PromptBuilder:
    """
    Handles construction of prompts for the Object Guessing Game.
    """

    def __init__(self, max_questions: int = 20):
        self.max_questions = max_questions

    def build_system_prompt(self) -> str:
        """Build the system prompt for the LLM."""
        return f"""You are playing a guessing game. The user has thought of an object,
and your job is to identify it by asking yes/no questions.

RULES:
1. Ask strategic yes/no questions to narrow down what the object is
2. Keep track of all previous answers to avoid contradictions
3. Ask questions that help you eliminate as many possibilities as possible
4. After you have enough information, make a guess
5. If you identify the object correctly, the game ends

STRATEGY:
- Start with broad categories (Is it a person? Is it an animal? Is it living?)
- Then narrow down (Is it a common object? Is it made of metal?)
- Use previous answers to inform follow-up questions
- Once you're confident, make your guess in the format: "I guess it's a [OBJECT_NAME]"
- Keep your responses concise - ask ONE question per turn (except for your guess)

Remember: You have {self.max_questions} questions to identify the object. Make them count!"""

    def build_user_prompt(self, conversation_history: list[dict]) -> str:
        """
        Build the user prompt based on conversation history.
        """
        system_prompt = self.build_system_prompt()

        if not conversation_history:
            # First question
            return f"{system_prompt}

Start the game by asking your first yes/no question to identify the object."

        # Build conversation context
        conversation_context = "
".join(
            [f"{msg['role'].upper()}: {msg['content']}" for msg in conversation_history]
        )

        # Follow-up questions
        return f"""{system_prompt}

Previous conversation:
{conversation_context}

Based on the answers so far, ask your next yes/no question to identify the object.
Remember to keep track of all previous answers and avoid asking contradictory questions.
Only ask yes/no questions (or make a guess when you're confident)."""
