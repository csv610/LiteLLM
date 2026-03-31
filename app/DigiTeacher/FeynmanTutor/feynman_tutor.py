# Acknowledgement: The following prompt has been copied verbatim from Dimitrios A. Karras’ Post on Linkedln.

from lite.lite_client import LiteClient
from .feynman_tutor_prompts import PromptBuilder

class ModelConfig:
    def __init__(self, topic, level, model="ollama/gemma3", temperature=0.4):
        self.topic = topic
        self.level = level
        self.model = model
        self.temperature = temperature

class FeynmanTutorQuestionGenerator:
    def __init__(self, config: ModelConfig):
        self.config = config
        self.history = []  # List of (question, response) pairs
        self.summary = ""  # Summarized progress
        self.is_convinced = False
        self.client = LiteClient()
        self.messages = [
            {"role": "system", "content": PromptBuilder.get_system_prompt()},
            {"role": "system", "content": PromptBuilder.get_context()},
            {"role": "system", "content": PromptBuilder.get_instructions()},
            {
                "role": "user",
                "content": PromptBuilder.get_initial_user_prompt(self.config.topic, self.config.level)
            }
        ]

    def _ask_llm(self):
        try:
            response = self.client.completion(
                model=self.config.model,
                messages=self.messages,
                temperature=self.config.temperature
            )
            content = response["choices"][0]["message"]["content"]
            
            if "[CONVINCED]" in content:
                self.is_convinced = True
                content = content.replace("[CONVINCED]", "").strip()
            
            self.messages.append({"role": "assistant", "content": content})
            return content
        except Exception as e:
            return f"🚨 Error communicating with the tutor: {str(e)}"

    def start_tutoring(self):
        question = self._ask_llm()
        self.history.append({"question": question, "response": None})
        return question

    def process_student_response(self, feedback):
        if self.is_convinced:
            return "The tutoring session is already complete. You have mastered the topic!"

        # Update history with student response
        if self.history and self.history[-1]["response"] is None:
            self.history[-1]["response"] = feedback
        
        self.messages.append({"role": "user", "content": feedback})
        self.messages.append({"role": "user", "content": PromptBuilder.get_refinement_prompt()})
        
        response_content = self._ask_llm()
        
        # Track next question if not convinced
        if not self.is_convinced:
            self.history.append({"question": response_content, "response": None})
        
        self._update_summary()
        return response_content

    def get_challenge(self):
        if self.is_convinced:
            return "The tutoring session is already complete. You have mastered the topic!"

        self.messages.append({"role": "user", "content": PromptBuilder.get_challenge_prompt()})
        response_content = self._ask_llm()
        
        # Track next question if not convinced
        if not self.is_convinced:
            self.history.append({"question": response_content, "response": None})
        
        self._update_summary()
        return response_content

    def get_snapshot(self, user_answer):
        if self.is_convinced:
            return "The tutoring session is already complete. You have mastered the topic!"

        # Update history with student response
        if self.history and self.history[-1]["response"] is None:
            self.history[-1]["response"] = user_answer
        
        self.messages.append({"role": "user", "content": user_answer})
        self.messages.append({"role": "user", "content": PromptBuilder.get_snapshot_prompt()})
        
        response_content = self._ask_llm()
        
        # Track next question (though likely final)
        if not self.is_convinced:
            self.history.append({"question": response_content, "response": None})
            
        self._update_summary()
        return response_content

    def _update_summary(self):
        # Call LLM to summarize progress based on history
        history_text = "\n".join([f"Q: {h['question']}\nA: {h['response']}" for h in self.history if h['response']])
        summary_messages = [
            {"role": "system", "content": "You are an educational observer summarizing a tutor-student dialogue."},
            {"role": "user", "content": PromptBuilder.get_summarization_prompt(history_text)}
        ]
        try:
            response = self.client.completion(
                model=self.config.model,
                messages=summary_messages,
                temperature=self.config.temperature
            )
            self.summary = response["choices"][0]["message"]["content"]
        except Exception:
            pass # Keep old summary if error
