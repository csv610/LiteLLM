#!/usr/bin/env python3
"""
Standalone module for creating medical quiz prompts.

This module provides a builder class for generating system and user prompts
for medical quiz generation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical quiz generation."""

    @staticmethod
    def create_quiz_system_prompt() -> str:
        """Create the system prompt for quiz generation.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return (
            "You are a board-certified medical education specialist creating high-quality multiple-choice questions "
            "that adhere to the standards of major international medical licensing exams: "
            "**USMLE (USA), MCCQE (Canada), and PLAB/UKMLA (UK)**.\n\n"
            "Adhere strictly to standard item-writing guidelines shared by these boards:\n"
            "1. **Clinical Vignettes:** Every question must start with a clinical vignette (patient presentation, "
            "history, vitals, exam findings). Do not ask recall questions without a case context.\n"
            "2. **Best Answer:** Questions should ask for the 'most likely diagnosis', 'best next step', "
            "or 'most appropriate management'.\n"
            "3. **Higher-Order Thinking:** Test application of knowledge, clinical reasoning, and decision making. "
            "Avoid simple recall of facts or definitions.\n"
            "4. **Distractors:** Incorrect options must be plausible and semantically distinct from each other and the correct answer. Each distractor should represent a genuinely different clinical possibility or reasoning pathway. Avoid:\n"
            "   - Word twisting or paraphrasing of the same concept\n"
            "   - Options that are essentially the same answer with different wording\n"
            "   - 'All of the above', 'None of the above', or negative phrasing (e.g., 'which is NOT')\n"
            "   - Options that are clearly implausible or ridiculous\n"
            "   - Options that are too similar to each other or the correct answer\n"
            "   Each distractor must represent a different diagnostic consideration, management approach, or clinical reasoning pathway.\n"
            "5. **Global Best Practices:** Ensure answers align with widely accepted international evidence-based guidelines.\n"
            "6. **Explanations:** Provide detailed explanations for WHY the correct answer is right and WHY "
            "each distractor is wrong.\n"
            "7. **UNIQUENESS & DIVERSITY:** Each question must be UNIQUE and cover DIFFERENT clinical scenarios, "
            "patient demographics, disease presentations, or management aspects. Avoid repetitive themes or similar case patterns.\n"
            "8. **FIELD COMPREHENSIVENESS:** Cover diverse aspects of the medical field including:\n"
            "   - Different age groups (pediatric, adult, geriatric)\n"
            "   - Various clinical settings (emergency, primary care, specialty)\n"
            "   - Multiple organ systems and disease categories\n"
            "   - Different question types (diagnosis, management, prognosis, prevention)\n"
            "   - Various levels of complexity and clinical reasoning"
        )

    @staticmethod
    def create_quiz_user_prompt(
        topic: str, difficulty: str, num_questions: int, num_options: int = 4
    ) -> str:
        """Create the user prompt for quiz generation."""
        # Generate the list of option identifiers dynamically (e.g., A, B, C, D)
        option_identifiers = [chr(65 + i) for i in range(num_options)]
        options_str = ", ".join(option_identifiers)

        return (
            f"Topic: {topic}\n"
            f"Difficulty: {difficulty}\n"
            f"Quantity: {num_questions} questions\n"
            f"Format: Multiple choice with {num_options} options ({options_str}) per question.\n\n"
            "Task: Create a set of high-quality clinical board questions (USMLE/MCCQE/UKMLA style). "
            "Output Format: Pydantic model."
        )

    @staticmethod
    def get_quiz_auditor_prompts(topic: str, quiz_content: str) -> tuple[str, str]:
        """Create prompts for the Quiz Compliance Auditor (JSON output)."""
        system = (
            "You are a Medical Education Quality Assurance Specialist. Your role is to "
            "audit medical quiz questions for accuracy, board-style formatting, "
            "and clinical relevance. Output a structured JSON report identifying "
            "any errors, low-quality distractors, or incorrect explanations."
        )
        user = (
            f"Audit the following medical quiz for the topic '{topic}' and output a "
            f"structured JSON report:\n\n{quiz_content}"
        )
        return system, user

    @staticmethod
    def get_output_synthesis_prompts(topic: str, quiz_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Medical Quiz Editor. Your role is to take raw quiz data "
            "and a structured quality audit, then synthesize them into a FINAL, "
            "polished, and board-ready Markdown quiz for students. You MUST apply all "
            "fixes identified in the audit and ensure a professional, consistent format."
        )
        user = (
            f"Synthesize the final medical quiz for '{topic}'.\n\n"
            f"QUIZ DATA:\n{quiz_data}\n\n"
            f"QUALITY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown quiz. Ensure it is accurate, board-style, "
            "and provides clear, educational explanations for all questions."
        )
        return system, user
