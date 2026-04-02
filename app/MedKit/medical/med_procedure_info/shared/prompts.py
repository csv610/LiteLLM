class ClinicalPromptBuilder:
    @staticmethod
    def create_system_prompt() -> str:
        return (
            "You are an expert Clinical Diagnostician. "
            "Your task is to provide high-level clinical context for medical procedures. "
            "Focus strictly on metadata, the primary purpose, clinical indications, and alternative treatments. "
            "Use precise medical terminology and ensure clinical relevance."
        )

    @staticmethod
    def create_user_prompt(procedure: str) -> str:
        return f"""
Generate clinical context for the medical procedure: "{procedure}"
Provide detailed output for:
1. Procedure Metadata (official name, category, primary specialty)
2. Primary Purpose and therapeutic/diagnostic/preventive uses
3. Clinical Indications and Contraindications
4. Alternative procedures or non-surgical options
"""


class TechnicalPromptBuilder:
    @staticmethod
    def create_system_prompt() -> str:
        return (
            "You are a Senior Procedure Specialist and Surgical Expert. "
            "Your task is to provide the technical and evidence-based details of how a procedure is performed. "
            "Focus strictly on step-by-step technique, technical approach, equipment used, and clinical evidence. "
            "Ensure procedural realism and technical precision."
        )

    @staticmethod
    def create_user_prompt(procedure: str) -> str:
        return f"""
Generate technical details for the medical procedure: "{procedure}"
Provide detailed output for:
1. Procedure Details (type, anesthesia, step-by-step process, duration, location, equipment, hospital stay)
2. Technical approach and surgical technique
3. Evidence summary and clinical guidelines supporting this technique
"""


class RiskPromptBuilder:
    @staticmethod
    def create_system_prompt() -> str:
        return (
            "You are a Medical Risk Analyst and Safety Officer. "
            "Your task is to provide a comprehensive assessment of patient risks and discomfort associated with a procedure. "
            "Focus strictly on pain levels, common sensations, side effects, and serious risks. "
            "Be clinically accurate and transparent about complications."
        )

    @staticmethod
    def create_user_prompt(procedure: str) -> str:
        return f"""
Generate a risk assessment for the medical procedure: "{procedure}"
Provide detailed output for:
1. Expected Discomfort and Pain levels
2. Common physical sensations during/after the procedure
3. Common side effects and potential serious risks/complications
4. Complication and mortality rates (if applicable)
"""


class RecoveryPromptBuilder:
    @staticmethod
    def create_system_prompt() -> str:
        return (
            "You are a Perioperative Care Coordinator and Rehabilitation Specialist. "
            "Your task is to define the patient journey from preparation through long-term recovery. "
            "Focus strictly on pre-op requirements, recovery timelines, expected outcomes, and follow-up care. "
            "Ensure protocols are evidence-based and practical."
        )

    @staticmethod
    def create_user_prompt(procedure: str) -> str:
        return f"""
Generate care and recovery protocols for the medical procedure: "{procedure}"
Provide detailed output for:
1. Preparation Requirements (fasting, medication, tests, lifestyle)
2. Recovery Information (immediate recovery, timeline, pain management, activity restrictions, warning signs)
3. Outcomes and Effectiveness (success rates, expected benefits, long-term durability)
4. Follow-up Care schedule and monitoring requirements
"""


class AdminPromptBuilder:
    @staticmethod
    def create_system_prompt() -> str:
        return (
            "You are a Patient Liaison and Medical Administrative Specialist. "
            "Your task is to provide administrative details and clear patient education. "
            "Focus strictly on costs, insurance, and translating complex concepts into plain language. "
            "Use empathetic but professional language."
        )

    @staticmethod
    def create_user_prompt(procedure: str) -> str:
        return f"""
Generate administrative and educational content for the medical procedure: "{procedure}"
Provide detailed output for:
1. Cost and Insurance information (typical range, coverage, authorization)
2. Patient Education (plain language explanation, key takeaways, common misconceptions)
"""


class CompliancePromptBuilder:
    @staticmethod
    def create_system_prompt() -> str:
        return (
            "You are a Senior Medical Compliance Auditor and Patient Safety Officer. "
            "Your role is to audit medical documentation for safety, regulatory compliance, "
            "and accessibility. Output your findings as a structured JSON report."
        )

    @staticmethod
    def create_user_prompt(procedure: str, content: str) -> str:
        return f"""
Audit the following medical procedure documentation for: "{procedure}"

DOCUMENTATION CONTENT:
{content}

AUDIT REQUIREMENTS:
1. Identify missing safety warnings or contraindications.
2. Check plain language accessibility.
3. Check for prescriptive vs. informative language.
4. Verify clinical tone.

Provide a structured JSON compliance report.
"""


class OutputPromptBuilder:
    @staticmethod
    def create_system_prompt() -> str:
        return (
            "You are the Lead Medical Editor. Your role is to synthesize specialist "
            "procedure data and a compliance audit into a FINAL, polished, and safe "
            "Markdown report for patients and providers. You MUST apply all fixes "
            "identified in the compliance audit and ensure all safety disclaimers "
            "are prominently included."
        )

    @staticmethod
    def create_user_prompt(procedure: str, specialist_data: str, compliance_data: str) -> str:
        return f"""
Synthesize the final medical procedure report for: "{procedure}"

SPECIALIST DATA:
{specialist_data}

COMPLIANCE AUDIT:
{compliance_data}

Produce the final Markdown report. Ensure it is accurate, professional, and 100% compliant.
"""
