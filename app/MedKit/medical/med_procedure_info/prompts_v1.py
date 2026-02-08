#!/usr/bin/env python3
"""
Standalone module for creating medical procedure info prompts.

This module provides a builder class for generating system and user prompts
for structured, evidence-based medical procedure documentation using AI models.
"""


class PromptBuilder:
    """Builder class for creating prompts for medical procedure documentation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for medical procedure documentation."""
        return (
            "You are an expert medical documentation specialist. "
            "Generate structured, clinically accurate, evidence-based medical procedure information. "
            "Use precise medical terminology. Avoid vague language. "
            "Do not include legal disclaimers or advice to consult doctors."
        )

    @staticmethod
    def create_user_prompt(procedure: str) -> str:
        """Create the user prompt for procedure information."""
        return f"""
Generate comprehensive, evidence-based information for the medical procedure or surgery: "{procedure}"

Organize the output under the following sections:

1. Definition and Purpose
2. Indications
3. Contraindications
4. Patient Preparation
5. Required Instruments and Equipment
6. Anesthesia or Analgesia Used
7. Step-by-Step Procedure Technique
8. Duration of Procedure
9. Intraoperative Monitoring
10. Possible Complications
11. Post-procedure Care
12. Recovery and Follow-up
13. Outcomes and Success Rates (if known)
14. Alternatives

Requirements:
- Use medically accurate terminology
- Be clinically precise and complete
- Do not use conversational tone
- Do not add unnecessary commentary
- Do not assume the procedure is surgical unless it truly is
- Clearly state whether it is minimally invasive or surgical when relevant
"""

