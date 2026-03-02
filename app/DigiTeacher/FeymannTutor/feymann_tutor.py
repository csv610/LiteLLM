# Acknowledgement: The following prompt has been copied verbatim from Dimitrios A. Karras’ Post on Linkedln.

from litellm import completion
from feymann_tutor_prompts import PromptBuilder

MODEL = "ollama/gemma3"

class FeynmanTutor:
    def __init__(self, topic, level):
        self.topic = topic
        self.level = level
        self.history = []  # List of (question, response) pairs
        self.summary = ""  # Summarized progress
        self.is_convinced = False
        self.messages = [
            {"role": "system", "content": PromptBuilder.get_system_prompt()},
            {"role": "system", "content": PromptBuilder.get_context()},
            {"role": "system", "content": PromptBuilder.get_instructions()},
            {
                "role": "user",
                "content": PromptBuilder.get_initial_user_prompt(topic, level)
            }
        ]

    def _ask_llm(self):
        try:
            response = completion(
                model=MODEL,
                messages=self.messages,
                temperature=0.4
            )
            content = response["choices"][0]["message"]["content"]
            
            if "[CONVINCED]" in content:
                self.is_convinced = True
                content = content.replace("[CONVINCED]", "").strip()
            
            self.messages.append({"role": "assistant", "content": content})
            return content
        except Exception as e:
            return f"🚨 Error communicating with the tutor: {str(e)}"

    def get_initial_explanation(self):
        question = self._ask_llm()
        self.history.append({"question": question, "response": None})
        return question

    def refine_explanation(self, feedback):
        # Update history with student response
        if self.history and self.history[-1]["response"] is None:
            self.history[-1]["response"] = feedback
        
        self.messages.append({"role": "user", "content": feedback})
        self.messages.append({"role": "user", "content": PromptBuilder.get_refinement_prompt()})
        
        question = self._ask_llm()
        
        # Track next question
        if not self.is_convinced:
            self.history.append({"question": question, "response": None})
        
        self._update_summary()
        return question

    def get_challenge(self):
        self.messages.append({"role": "user", "content": PromptBuilder.get_challenge_prompt()})
        question = self._ask_llm()
        
        # Track next question
        if not self.is_convinced:
            self.history.append({"question": question, "response": None})
        
        self._update_summary()
        return question

    def get_snapshot(self, user_answer):
        # Update history with student response
        if self.history and self.history[-1]["response"] is None:
            self.history[-1]["response"] = user_answer
        
        self.messages.append({"role": "user", "content": user_answer})
        self.messages.append({"role": "user", "content": PromptBuilder.get_snapshot_prompt()})
        
        question = self._ask_llm()
        
        # Track next question (though likely final)
        if not self.is_convinced:
            self.history.append({"question": question, "response": None})
            
        self._update_summary()
        return question

    def _update_summary(self):
        # Call LLM to summarize progress based on history
        history_text = "\n".join([f"Q: {h['question']}\nA: {h['response']}" for h in self.history if h['response']])
        summary_messages = [
            {"role": "system", "content": "You are an educational observer summarizing a tutor-student dialogue."},
            {"role": "user", "content": PromptBuilder.get_summarization_prompt(history_text)}
        ]
        try:
            response = completion(
                model=MODEL,
                messages=summary_messages,
                temperature=0.3
            )
            self.summary = response["choices"][0]["message"]["content"]
        except Exception:
            pass # Keep old summary if error
