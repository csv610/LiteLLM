"""
liteagents.py - Unified LiteClient-based agents for ObjectGuesser.
"""

from lite import ModelOutput
from app.ObjectGuesser.shared.prompts import PromptBuilder
from app.ObjectGuesser.shared.utils import *
from lite.config import ModelConfig, ModelInput
from lite.lite_client import LiteClient
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
import json
import logging


class GameState(BaseModel):
    action: str = Field(
        ..., description="Next action for the game, such as ASK_QUESTION or MAKE_GUESS."
    )
    content: str = Field(
        ..., description="Question or guess content associated with the action."
    )


__all__ = ["GameState", "ModelOutput"]

"""
Multi-Agent Object Guessing Game using LiteClient

This version uses multiple specialized agents (State, Strategy, Extraction)
to provide a more robust and intelligent guessing game.
"""

logger = logging.getLogger(__name__)


class ObjectGuesserGame:
    """
    A multi-agent guessing game where the LLM tries to identify an object.
    """

    def __init__(
        self,
        model: str = "ollama/gemma3",
        temperature: float = 0.7,
        max_questions: int = 20,
    ):
        """
        Initialize the multi-agent guessing game.
        """
        self.model_config = ModelConfig(
            model=model, temperature=0.2
        )  # Low temperature for extraction/state
        self.client = LiteClient(model_config=self.model_config)
        self.prompt_builder = PromptBuilder(max_questions=max_questions)
        self.conversation_history = []
        self.blackboard = {"properties": {}, "category": None, "excluded_objects": []}
        self.question_count = 0
        self.max_questions = max_questions

    def add_to_history(self, role: str, content: str):
        """Add a message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def _call_agent(self, system_prompt: str, user_prompt: str) -> dict:
        """Utility method to call an agent and parse JSON response."""
        model_input = ModelInput(user_prompt=user_prompt, system_prompt=system_prompt)
        response_res = self.client.generate_text(model_input=model_input)
        response = response_res.markdown if response_res.markdown else str(response_res)

        # Clean up response if it contains markdown code blocks
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback for simple non-JSON responses if needed
            raise Exception(f"Failed to parse agent response as JSON: {response}")

    def update_state(self):
        """State Management Agent: Updates the blackboard based on history."""
        system_prompt = self.prompt_builder.build_state_system_prompt()
        user_prompt = self.prompt_builder.build_user_prompt(
            self.conversation_history, self.blackboard
        )

        updated_blackboard = self._call_agent(system_prompt, user_prompt)
        self.blackboard = updated_blackboard

    def decide_strategy(self) -> dict:
        """Strategy Agent: Decides whether to ask a question or make a guess."""
        system_prompt = self.prompt_builder.build_strategy_system_prompt()
        user_prompt = self.prompt_builder.build_user_prompt(
            [], self.blackboard
        )  # Just needs current state

        return self._call_agent(system_prompt, user_prompt)

    def extract_info(self, latest_exchange: list[dict]) -> dict:
        """Extraction Agent: Extracts structured data from user input."""
        system_prompt = self.prompt_builder.build_extraction_system_prompt()
        user_prompt = self.prompt_builder.build_user_prompt(latest_exchange)

        return self._call_agent(system_prompt, user_prompt)

    def play(self) -> ModelOutput:
        """Main game loop driven by multi-agent coordination."""
        print("\n" + "=" * 60)
        print("MULTI-AGENT OBJECT GUESSING GAME")
        print("=" * 60)
        print("\nThink of an object and keep it in mind.")
        print("The LLM will use multiple agents to identify it.")
        print("Answer with 'yes', 'no', or 'somewhat'.\n")

        won = False
        while self.question_count < self.max_questions:
            try:
                # 1. Update internal state (Blackboard)
                self.update_state()

                # 2. Decide next action (Strategy)
                decision = self.decide_strategy()

                if decision["action"] == "MAKE_GUESS":
                    guess = decision["content"]
                    print(
                        f"\n[Question {self.question_count + 1}] LLM Guess: Is it a {guess}?"
                    )
                    user_answer = input("User: ").strip()

                    # 3. Extraction Agent parses the result of the guess
                    latest_exchange = [
                        {"role": "assistant", "content": f"Is it a {guess}?"},
                        {"role": "user", "content": user_answer},
                    ]
                    extraction = self.extract_info(latest_exchange)

                    if extraction["user_sentiment"] == "yes":
                        print(f"\n🎉 Correct! The object was a {guess}!")
                        print(
                            f"The LLM identified it in {self.question_count + 1} turns."
                        )
                        won = True
                        break
                    else:
                        print("\nLLM: Oops, let me refine my information...")
                        self.blackboard["excluded_objects"].append(guess)
                        self.add_to_history("assistant", f"Is it a {guess}?")
                        self.add_to_history("user", user_answer)
                        self.question_count += 1
                        continue

                elif decision["action"] == "ASK_QUESTION":
                    question = decision["content"]
                    self.question_count += 1
                    print(f"\n[Question {self.question_count}] LLM: {question}")

                    user_answer = input("User: ").strip()

                    # 4. Record history for state update in next turn
                    self.add_to_history("assistant", question)
                    self.add_to_history("user", user_answer)

            except KeyboardInterrupt:
                print("\n\nGame interrupted by user.")
                break
            except Exception as e:
                print(f"\nAgent Error: {e}")
                print("Continuing...")
                continue

        if not won and self.question_count >= self.max_questions:
            print(
                f"\nGame Over! The LLM couldn't identify the object in {self.max_questions} questions."
            )

        return self.generate_summary(won)

    def generate_summary(self, won: bool) -> ModelOutput:
        """Synthesize the game session into a ModelOutput artifact."""
        status = "Correctly Guessed" if won else "Not Identified"

        # Tier 3: Output Synthesis (Markdown Closer)
        history_str = json.dumps(self.conversation_history, indent=2)
        synth_prompt = f"Synthesize a fun, engaging Markdown summary of this object guessing game.\nStatus: {status}\nTurns: {self.question_count}\n\nHistory:\n{history_str}"

        synth_input = ModelInput(
            system_prompt="You are a Game Master Narrator. Synthesize the game session into a beautiful Markdown report.",
            user_prompt=synth_prompt,
            response_format=None,
        )
        final_markdown_res = self.client.generate_text(synth_input)
        final_markdown = final_markdown_res.markdown

        return ModelOutput(
            data={
                "status": status,
                "turns": self.question_count,
                "blackboard": self.blackboard,
            },
            markdown=final_markdown,
            metadata={"conversation_history": self.conversation_history},
        )
