class PromptBuilder:
    """Prompt builder for medical media analysis."""

    @staticmethod
    def create_system_prompt() -> str:
        return """You are a medical media specialist expert in medical imaging (radiology, pathology, dermatology), clinical photography, and educational videos.
Your task is to provide accurate, professional captions and summaries for medical visual or educational content.
Focus on:
- Anatomical identification
- Pathological findings
- Clinical relevance
- Technical terminology
Always maintain high professional standards and clarity."""

    @staticmethod
    def create_caption_prompt(topic: str, media_type: str = "image") -> str:
        return f"Generate a professional medical caption for a/an {media_type} of '{topic}'. Describe what is typically seen, the important landmarks, and what it represents clinically."

    @staticmethod
    def create_summary_prompt(topic: str, media_type: str = "video") -> str:
        """Create prompts for medical summary generation."""
        return f"Generate a medical summary for a/an {media_type} or educational content about '{topic}'. Include key learning points and clinical significance."

    @staticmethod
    def create_accuracy_auditor_prompts(topic: str, content: str) -> tuple[str, str]:
        """Create prompts for the Media Accuracy Auditor (JSON output)."""
        system = (
            "You are a Senior Radiologist and Medical Media Auditor. Your role is to "
            "audit medical captions and summaries for anatomical accuracy and "
            "clinical correctness. Output a structured JSON report identifying "
            "any mislabeled structures or incorrect clinical interpretations."
        )
        user = (
            f"Audit the following medical analysis for '{topic}' and output a "
            f"structured JSON report:\n\n{content}"
        )
        return system, user

    @staticmethod
    def create_output_synthesis_prompts(topic: str, specialist_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Medical Media Editor. Your role is to take raw specialist "
            "media analysis and a structured quality audit, then synthesize them into "
            "a FINAL, polished, and safe Markdown report. You MUST apply all fixes "
            "identified in the audit and ensure the description is clinically authoritative."
        )
        user = (
            f"Synthesize the final medical media report for: '{topic}'\n\n"
            f"MEDIA DATA:\n{specialist_data}\n\n"
            f"QUALITY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown report. Ensure it is accurate, professional, "
            "and ready for clinical or educational use."
        )
        return system, user
