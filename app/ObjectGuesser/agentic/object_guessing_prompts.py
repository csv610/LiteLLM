import json

class PromptBuilder:
    """
    Handles construction of prompts for the Object Guessing Game Agents.
    """

    def __init__(self, max_questions: int = 20):
        self.max_questions = max_questions

    def build_extraction_system_prompt(self) -> str:
        """System prompt for the Extraction Agent."""
        return """You are an Extraction Agent for an object guessing game.
Your job is to parse the latest exchange and extract structured data.

TASKS:
1. Classify the user's response: "yes", "no", or "somewhat".
2. Determine if the assistant made a guess (e.g., "Is it a cat?", "I guess it's a dog").
3. If a guess was made, extract the object name.

OUTPUT FORMAT (JSON):
{
    "user_sentiment": "yes" | "no" | "somewhat" | "unknown",
    "is_guess": boolean,
    "guessed_object": string | null
}

Only output valid JSON."""

    def build_state_system_prompt(self) -> str:
        """System prompt for the State Management Agent."""
        return """You are a State Management Agent.
Maintain a "Blackboard" of facts about the object being guessed.

INPUT: Conversation history and current blackboard.
OUTPUT: Updated blackboard reflecting all known properties.

BLACKBOARD STRUCTURE (JSON):
{
    "properties": {
        "property_name": "yes" | "no" | "somewhat",
        ...
    },
    "category": string | null,
    "excluded_objects": [string, ...]
}

Only output the updated JSON blackboard."""

    def build_strategy_system_prompt(self) -> str:
        """System prompt for the Strategy Agent."""
        return f"""You are a Strategy Agent for an object guessing game.
The goal is to identify the object in under {self.max_questions} questions.

INPUT: Current Blackboard of facts.
DECISION:
1. ASK_QUESTION: If more info is needed.
2. MAKE_GUESS: If confident about the object.

OUTPUT FORMAT (JSON):
{{
    "action": "ASK_QUESTION" | "MAKE_GUESS",
    "content": "The question text" | "The guessed object name"
}}

Only output valid JSON."""

    def build_user_prompt(self, conversation_history: list[dict], blackboard: dict = None) -> str:
        """Build user prompt with context."""
        context = "Conversation History:\n"
        for msg in conversation_history:
            context += f"{msg['role'].upper()}: {msg['content']}\n"
        
        if blackboard:
            context += f"\nCurrent Blackboard: {json.dumps(blackboard)}"
            
        return context
