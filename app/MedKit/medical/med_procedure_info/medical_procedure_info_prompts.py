
class PromptBuilder:
    """Builder class for creating prompts for medical procedure documentation."""

    @staticmethod
    def create_system_prompt() -> str:
        """Create the system prompt for medical procedure documentation."""
        return (
            "You are an expert medical documentation specialist with surgical domain knowledge. "
            "Generate clinically accurate, structured, and technically precise medical procedure or surgery descriptions. "
            "Use standard medical terminology. Avoid vague or generic phrasing. "
            "Ensure procedural realism and evidence-based perioperative practices. "
            "Do not include legal disclaimers or advice to consult physicians."
        )

    @staticmethod
    def create_user_prompt(procedure: str) -> str:
        """Create the user prompt for procedure information."""
        return f"""
Generate comprehensive, evidence-based information for the medical procedure or surgery: "{procedure}"

First, determine whether this is:
- a non-surgical medical procedure, or
- a surgical operation involving tissue incision.

Then produce output under the following sections:

1. Definition and Purpose
2. Indications
3. Contraindications
4. Patient Preparation (include key labs, imaging, and risk assessment)
5. Required Instruments and Equipment (procedure-specific, not generic)
6. Anesthesia or Analgesia Used
7. Step-by-Step Procedure Technique (include positioning and key technical steps unique to this procedure)
8. Typical Duration of Procedure
9. Intraoperative Monitoring
10. Possible Complications
11. Post-procedure Care (evidence-based; do not assume routine postoperative antibiotics)
12. Recovery and Follow-up
13. Outcomes and Success Rates (if known)
14. Alternatives

Requirements:
- Use medically and surgically accurate terminology
- Use standard operative positioning when applicable
- Distinguish clearly between surgical and non-surgical procedures
- Avoid generic or boilerplate instrument lists
- Avoid vague statements (e.g., “as needed”, “may be considered” without context)
- Do not assume this is surgery unless it truly is
- Do not include conversational language or commentary
"""

