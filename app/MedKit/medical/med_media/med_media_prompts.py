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
        return f"Generate a medical summary for a/an {media_type} or educational content about '{topic}'. Include key learning points and clinical significance."
