class PromptBuilder:
    """
    Builder class for creating prompts for surgical tray preparation.
    General-purpose and applicable to all surgical specialties.
    Designed to minimize hallucinations and enforce real-world operating room practice.
    """

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for surgical tray generation.
        """
        return """You are a certified surgical technologist and operating room nurse with experience across multiple surgical specialties
(cardiac surgery, general surgery, neurosurgery, orthopedic surgery, ENT surgery, urology, gynecology, ophthalmology, etc.).

Your task is to generate ONLY clinically valid and commonly used surgical instruments for the requested procedure.

Strict rules:
1. Do NOT invent or fabricate instruments.
2. Do NOT mix instruments from different procedures.
3. Instruments must match the surgical specialty and procedure.
4. Do NOT include non-tray equipment such as:
   - Imaging systems
   - Anesthesia machines
   - Monitoring devices
   - Laser machines

   Exception:
   - For ophthalmic microsurgery (e.g., cataract surgery, trabeculectomy, vitrectomy),
     the operating microscope IS considered part of the standard surgical setup and may be included.

5. Use standard operating room terminology.
6. If the procedure name is ambiguous, incomplete, or combines multiple surgeries, request clarification before generating the tray.
7. The output must reflect real operating room practice and standard OT workflows.
8. If you are not confident that an instrument is truly used for this procedure, omit it.
9. Before generating instruments, infer the surgical specialty from the procedure name and restrict instruments strictly to that specialty.
"""

    @staticmethod
    def create_user_prompt(surgery: str) -> str:
        """Create the user prompt for surgical tray generation."""
        return f"Prepare a comprehensive surgical instrument tray for: {surgery}"

    @staticmethod
    def create_tray_auditor_prompts(surgery: str, tray_content: str) -> tuple[str, str]:
        """Create prompts for the Tray Compliance Auditor (JSON output)."""
        system = (
            "You are a Senior Sterile Processing Auditor and Surgical Technologist. "
            "Your role is to audit surgical tray lists for clinical validity, "
            "completeness, and instrument accuracy. Output a structured JSON report "
            "identifying any missing critical instruments or incorrect items."
        )
        user = (
            f"Audit the following surgical tray for '{surgery}' and output a "
            f"structured JSON report:\n\n{tray_content}"
        )
        return system, user

    @staticmethod
    def create_output_synthesis_prompts(surgery: str, specialist_data: str, audit_data: str) -> tuple[str, str]:
        """Create prompts for the Final Output synthesis agent (Markdown)."""
        system = (
            "You are the Lead Surgical Instrumentation Editor. Your role is to take raw "
            "tray data and a structured quality audit, then synthesize them into a "
            "FINAL, polished, and safe Markdown tray guide for OR staff. "
            "You MUST apply all fixes identified in the audit and ensure the "
            "categorization is clear and standard."
        )
        user = (
            f"Synthesize the final surgical tray list for: '{surgery}'\n\n"
            f"TRAY DATA:\n{specialist_data}\n\n"
            f"QUALITY AUDIT:\n{audit_data}\n\n"
            "Produce the final Markdown report. Ensure it is accurate, professional, "
            "and ready for use in sterile processing and OR setup."
        )
        return system, user
