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
        """
        Create the user prompt for surgical tray generation.

        Args:
            surgery (str): The exact name of the surgical procedure.

        Returns:
            str: Prompt requesting a validated surgical instrument tray in JSON format.
        """
        return f"""Prepare a surgical instrument tray for the following procedure:

Procedure name: "{surgery}"

Instructions:
1. If the procedure name is vague, incomplete, or could refer to more than one surgery
   (for example: "eye surgery", "glaucoma surgery", "heart surgery", "tumor removal"),
   respond ONLY with:
   "ERROR: Please specify the exact surgical procedure (for example: laparoscopic cholecystectomy, trabeculectomy, total knee replacement, orthotopic heart transplant)."

2. Otherwise, generate a tray list using ONLY real instruments used for this specific procedure.

3. Group instruments by functional categories
   (for example: exposure, cutting and dissection, grasping and holding, vascular control, suturing, hemostasis).

4. For each instrument include:
   - "name": standard instrument name
   - "quantity": typical quantity
   - "purpose": brief surgical purpose

5. Exclude:
   - Brand names
   - Diagnostic equipment
   - Monitoring devices
   - Laser systems and laser accessories
   - Non-sterile room equipment

6. Do NOT include setup instructions or sterilization methods unless explicitly requested.

Output requirements:
- Output must be valid JSON only.
- Do not include explanations, commentary, or markdown outside JSON.
"""

