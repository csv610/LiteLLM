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
    def create_quiz_user_prompt(topic: str, difficulty: str, num_questions: int, num_options: int = 4) -> str:
        """Create the user prompt for quiz generation.

        Args:
            topic: The medical topic to generate a quiz for
            difficulty: The difficulty level of the quiz
            num_questions: The number of questions to generate
            num_options: The number of options per question

        Returns:
            str: Formatted user prompt
        """
        # Generate the list of option identifiers dynamically (e.g., A, B, C, D)
        option_identifiers = [chr(65 + i) for i in range(num_options)]
        options_str = ", ".join(option_identifiers)

        return (
            f"Topic: {topic}\n"
            f"Difficulty: {difficulty}\n"
            f"Quantity: {num_questions} questions\n"
            f"Format: Multiple choice with {num_options} options ({options_str}) per question.\n\n"
            "Task: Create a set of high-quality clinical board questions (USMLE/MCCQE/UKMLA style) for the above topic. "
            "Each question MUST begin with a unique clinical vignette (patient case). "
            "Ensure the correct answer is indisputable based on current international medical evidence. "
            "Explain the clinical reasoning for the correct answer and why other options are incorrect.\n\n"
            "**CRITICAL REQUIREMENTS FOR UNIQUENESS & DIVERSITY:**\n"
            f"1. Generate EXACTLY {num_questions} UNIQUE questions - no duplicates or similar scenarios\n"
            "2. Each question must explore DIFFERENT aspects of {topic}\n"
            "3. Vary patient demographics (age, gender, ethnicity, background)\n"
            "4. Include different clinical presentations and disease stages\n"
            "5. Cover various management approaches (diagnostic, therapeutic, preventive)\n"
            "6. Incorporate different clinical settings and scenarios\n"
            "7. Ensure questions test different cognitive skills and reasoning levels\n\n"
            "Output Format:\n"
            "- For each question, provide options as a simple dictionary: {'A': 'option text', 'B': 'option text', 'C': 'option text', 'D': 'option text'}\n"
            "- Specify the correct answer as the key (e.g., 'A', 'B', 'C', or 'D')\n"
            "- Provide detailed explanations for clinical reasoning\n\n"
            "**CRITICAL: SEMANTIC DIFFERENTIATION REQUIREMENTS:**\n"
            "Each option must represent a GENUINELY DIFFERENT clinical concept:\n"
            "- **Option A**: One distinct diagnostic/therapeutic possibility\n"
            "- **Option B**: A completely different clinical consideration\n"
            "- **Option C**: Another separate medical reasoning pathway\n"
            "- **Option D**: A fourth distinct clinical alternative\n\n"
            "**AVOID THESE PROBLEMS:**\n"
            "- Word twisting: 'Heart attack' vs 'Myocardial infarction' (same concept)\n"
            "- Paraphrasing: 'High blood pressure' vs 'Elevated blood pressure' (identical)\n"
            "- Similar concepts: 'Type 1 diabetes' vs 'Insulin-dependent diabetes' (same condition)\n"
            "- Overlapping: 'Chest pain' vs 'Thoracic pain' (same symptom)\n\n"
            "**GOOD EXAMPLES OF SEMANTIC DIFFERENTIATION:**\n"
            "For chest pain question:\n"
            "A) Acute myocardial infarction (cardiac emergency)\n"
            "B) Pulmonary embolism (respiratory emergency)\n"
            "C) Esophageal spasm (gastrointestinal condition)\n"
            "D) Musculoskeletal pain (orthopedic issue)\n\n"
            f"REVIEW YOUR OUTPUT: Ensure all {num_options} options are SEMANTICALLY DISTINCT and represent different clinical pathways within {topic}."
        )
