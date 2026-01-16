import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pydantic import BaseModel, Field
import re

try:
    from medkit.core.gemini_client import GeminiClient, ModelConfig, ModelInput
except ImportError:
    # Fallback classes
    class ModelConfig:
        def __init__(self, model_name="gemini-2.5-flash", temperature=0.7, max_output_tokens=2048):
            self.model_name = model_name
            self.temperature = temperature
            self.max_output_tokens = max_output_tokens

    class ModelInput:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    class GeminiClient:
        def __init__(self, config=None):
            self.config = config or ModelConfig()

        def query(self, prompt, **kwargs):
            return "Mock medical response"

# ==================== Data Models ====================

class PatientDemographics(BaseModel):
    name: str
    age: int
    gender: str
    occupation: Optional[str] = None

class ChiefComplaint(BaseModel):
    primary_complaint: str
    duration: str
    severity: str  # mild, moderate, severe
    onset: str  # sudden, gradual

class SystemReview(BaseModel):
    constitutional: List[str] = Field(description="Fever, weight loss, fatigue, night sweats")
    cardiovascular: List[str] = Field(description="Chest pain, palpitations, edema")
    respiratory: List[str] = Field(description="Cough, shortness of breath, wheezing")
    gastrointestinal: List[str] = Field(description="Nausea, vomiting, diarrhea, constipation, abdominal pain")
    genitourinary: List[str] = Field(description="Dysuria, frequency, hematuria")
    musculoskeletal: List[str] = Field(description="Joint pain, muscle weakness, stiffness")
    neurological: List[str] = Field(description="Headache, dizziness, numbness, tingling, seizures")
    psychiatric: List[str] = Field(description="Anxiety, depression, sleep disturbances")
    skin: List[str] = Field(description="Rash, itching, lesions")

class MedicalHistory(BaseModel):
    past_medical_conditions: List[str]
    current_medications: List[str]
    allergies: List[str]
    surgical_history: List[str]
    family_history: List[str]
    social_history: Dict[str, str] = Field(description="Smoking, alcohol, drug use, occupation")

class PhysicalExamFindings(BaseModel):
    vital_signs: Dict[str, str] = Field(description="BP, HR, RR, Temp, SpO2")
    general_appearance: str
    specific_findings: List[str] = Field(description="Relevant positive and negative findings")

class ClinicalAssessment(BaseModel):
    differential_diagnosis: List[str] = Field(description="Ranked list of possible diagnoses with brief reasoning")
    most_likely_diagnosis: str
    diagnostic_confidence: str = Field(description="High, moderate, low")
    red_flags: List[str] = Field(description="Warning signs requiring immediate attention")

class ManagementPlan(BaseModel):
    investigations_ordered: List[str] = Field(description="Lab tests, imaging, other diagnostic tests")
    treatment_prescribed: List[str] = Field(description="Medications with dosage, non-pharmacological interventions")
    patient_education: List[str] = Field(description="Key points explained to patient")
    follow_up_plan: str
    referrals: Optional[List[str]] = None
    precautions: List[str] = Field(description="When to return immediately")

class EmergencyAlert(BaseModel):
    is_emergency: bool
    red_flags_detected: List[str]
    recommendation: str
    action_required: bool

class MedicalSummary(BaseModel):
    consultation_date: str
    patient_demographics: PatientDemographics
    chief_complaint: ChiefComplaint
    history_of_present_illness: str = Field(description="Detailed narrative of symptom progression")
    review_of_systems: SystemReview
    past_medical_history: MedicalHistory
    physical_examination: PhysicalExamFindings
    clinical_assessment: ClinicalAssessment
    management_plan: ManagementPlan
    clinical_notes: str = Field(description="Additional observations or concerns")
    emergency_alert: Optional[EmergencyAlert] = None

class EmergencyException(Exception):
    """Exception raised when emergency red flags are detected."""
    def __init__(self, red_flags: List[str], patient_name: str = ""):
        self.red_flags = red_flags
        self.patient_name = patient_name
        super().__init__(f"Emergency detected: {', '.join(red_flags)}")

# ==================== Main Consultation Class ====================

class MedicalConsultation:
    """Simple medical consultation system."""

    def __init__(self):
        config = ModelConfig(
            model_name='gemini-2.5-flash',
            temperature=0.7,
            max_output_tokens=2048
        )
        self.client = GeminiClient(config=config)
        self.conversation_history = []
        self.transcript = []  # Store all Q&A for transcript

        # Red flag keywords based on US medical standards
        self.red_flag_keywords = {
            "chest_pain": ["chest pain", "chest pressure", "chest tightness", "heart attack"],
            "respiratory_distress": ["shortness of breath", "short of breath", "trouble breathing", "difficulty breathing",
                                     "can't breathe", "gasping", "severe cough", "can't catch my breath", "breathing hard"],
            "neurological": ["stroke", "seizure", "loss of consciousness", "severe headache", "sudden weakness", "paralysis",
                            "slurred speech", "unconscious", "passed out", "loss of consciousness"],
            "severe_bleeding": ["severe bleeding", "can't stop bleeding", "can't stop the bleeding", "blood loss", "hemorrhage",
                               "bleeding won't stop", "profuse bleeding"],
            "severe_abdominal": ["severe abdominal pain", "acute abdomen", "belly bursting", "sharp pain", "severe stomach pain"],
            "signs_of_shock": ["fainting", "dizzy", "dizziness", "pale", "cold sweat", "rapid heart rate", "confusion",
                              "altered mental status", "confused", "feeling faint"],
            "allergic_reaction": ["anaphylaxis", "severe allergic", "throat closing", "can't swallow", "severe allergy"],
            "severe_trauma": ["severe injury", "major accident", "severe trauma", "severe fall", "severe injury"]
        }

    def _parse_json_from_response(self, response_text: str) -> dict:
        """Parse JSON from AI response, handling various formats."""
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass

        if "```json" in response_text:
            json_text = response_text.split("```json")[1].split("```")[0].strip()
            return json.loads(json_text)

        if "```" in response_text:
            json_text = response_text.split("```")[1].split("```")[0].strip()
            return json.loads(json_text)

        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

        raise ValueError("Could not parse JSON from response")

    def detect_red_flags(self, text: str) -> Tuple[bool, List[str]]:
        """Detect life-threatening red flags in text."""
        text_lower = text.lower()
        detected_flags = []

        for category, keywords in self.red_flag_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    detected_flags.append(keyword)

        return len(detected_flags) > 0, detected_flags

    def run(self):
        """Run the consultation from start to finish."""
        try:
            # Print disclaimers
            self._print_disclaimers()

            # Get consent
            if not self._get_consent():
                print("\nConsultation cannot proceed without acknowledgment.")
                return None, None, None

            # Collect basic info
            print("\n" + "="*80)
            print("PATIENT REGISTRATION")
            print("="*80)

            name = input("Patient Name: ").strip()
            age = int(input("Age: ").strip())
            gender = input("Gender (M/F/Other): ").strip()
            occupation = input("Occupation (optional): ").strip() or None

            print("\nCHIEF COMPLAINT")
            print("-" * 80)
            complaint = input("What brings you here today? ").strip()
            duration = input("How long have you had this? ").strip()
            severity = input("How severe? (mild/moderate/severe): ").strip()
            onset = input("How did it start? (sudden/gradual): ").strip()

            # Store basic data
            demographics = PatientDemographics(name=name, age=age, gender=gender, occupation=occupation)
            chief_complaint = ChiefComplaint(
                primary_complaint=complaint,
                duration=duration,
                severity=severity,
                onset=onset
            )

            # Build context and conduct Q&A
            context = self._build_context(demographics, chief_complaint)
            self.conversation_history.append({"role": "user", "content": context})

            print("\n" + "="*80)
            print("CONSULTATION")
            print("="*80)
            print(f"\nDoctor: Thank you for coming in, {name}. I'll ask you some questions to understand your condition.\n")

            conversation_log = self._conduct_qa(max_questions=15, patient_name=name)

            # Generate medical summary
            print("\n" + "="*80)
            print("Generating medical summary...")
            print("="*80 + "\n")

            summary_dict = self._generate_summary(demographics, chief_complaint, conversation_log)
            summary = MedicalSummary(**summary_dict)
            print("✓ Summary generated\n")

            # Save files
            summary_file = self._save_summary(summary)
            report_file = self._save_report(summary)
            transcript_file = self._save_transcript(name)

            print(f"\n✓ Medical Summary: {summary_file}")
            print(f"✓ Medical Report: {report_file}")
            print(f"✓ Transcript: {transcript_file}\n")

            return summary, summary_file, report_file

        except EmergencyException as e:
            self._handle_emergency(e.red_flags, e.patient_name)
            transcript_file = self._save_transcript(e.patient_name)
            return None, None, transcript_file

    def _print_disclaimers(self):
        """Print medical disclaimers."""
        print("\n" + "="*80)
        print("IMPORTANT MEDICAL DISCLAIMERS".center(80))
        print("="*80 + "\n")

        print("""
This is an AI-based consultation system and should NOT be used as a substitute
for professional medical advice, diagnosis, or treatment.

LIMITATIONS:
• Cannot perform physical examination
• Cannot order and interpret tests
• Cannot prescribe medications
• Based on patient self-reporting only

ALWAYS SEEK PROFESSIONAL MEDICAL CARE FOR:
• Any new or worsening symptoms
• Confirmation of diagnoses
• Prescription medications
• Professional medical examination

DATA PROTECTION (HIPAA):
• Your information is sensitive and protected
• Store securely and do not share without consent
• Consult privacy policy for data handling
""")
        print("="*80 + "\n")

    def _get_consent(self) -> bool:
        """Get patient consent."""
        response = input("Do you acknowledge and accept these disclaimers? (yes/no): ").strip().lower()
        return response in ['yes', 'y']

    def _build_context(self, demographics: PatientDemographics, complaint: ChiefComplaint) -> str:
        """Build context for AI doctor."""
        return f"""
PATIENT INFORMATION:
Name: {demographics.name}
Age: {demographics.age}
Gender: {demographics.gender}
Chief Complaint: {complaint.primary_complaint}
Duration: {complaint.duration}
Severity: {complaint.severity}
Onset: {complaint.onset}

You are a compassionate medical doctor conducting a consultation. Ask one question at a time
in simple, non-technical language. Be empathetic and adapt based on patient responses.
Focus on understanding the patient's symptoms and medical context.
"""

    def _conduct_qa(self, max_questions: int = 15, patient_name: str = "") -> list:
        """Conduct question-answer cycle."""
        conversation_log = []

        for q_num in range(max_questions):
            # Generate question
            prompt = f"""Ask the next relevant medical history question (Question {q_num + 1} of {max_questions}).
Use simple language. Be compassionate. Ask ONE clear question at a time.
Example: "You mentioned the headache started suddenly - what were you doing when it happened?"
Avoid jargon and overwhelming the patient."""

            conversation_content = [msg["content"] for msg in self.conversation_history]
            conversation_content.append(prompt)
            full_prompt = "\n".join(conversation_content)

            model_input = ModelInput(user_prompt=full_prompt)
            question = self.client.generate_content(model_input, stream=False).strip()

            print(f"Doctor: {question}")
            self.transcript.append(f"Doctor: {question}")

            # Get answer
            answer = input("Patient: ").strip()
            self.transcript.append(f"Patient: {answer}")

            if answer.lower() in ['done', 'finish', 'complete']:
                break

            # Check for red flags
            is_emergency, red_flags = self.detect_red_flags(answer)
            if is_emergency:
                raise EmergencyException(red_flags, patient_name=patient_name)

            conversation_log.append({"question": question, "answer": answer})
            self.conversation_history.extend([
                {"role": "model", "content": question},
                {"role": "user", "content": answer}
            ])

            print()

        return conversation_log

    def _generate_summary(self, demographics: PatientDemographics, complaint: ChiefComplaint,
                         conversation_log: list) -> dict:
        """Generate medical summary using AI."""
        prompt = f"""
Based on this consultation, generate a comprehensive medical summary:

Patient: {demographics.name}, {demographics.age}yo {demographics.gender}
Chief Complaint: {complaint.primary_complaint}

Consultation Q&A:
{json.dumps(conversation_log, indent=2)}

Generate ONLY valid JSON with these fields:
- consultation_date (today's date)
- patient_demographics (name, age, gender, occupation)
- chief_complaint (primary_complaint, duration, severity, onset)
- history_of_present_illness (narrative)
- review_of_systems (constitutional, cardiovascular, respiratory, gastrointestinal, genitourinary, musculoskeletal, neurological, psychiatric, skin - each an array)
- past_medical_history (past_medical_conditions, current_medications, allergies, surgical_history, family_history, social_history)
- physical_examination (vital_signs dict, general_appearance, specific_findings array)
- clinical_assessment (differential_diagnosis array, most_likely_diagnosis, diagnostic_confidence, red_flags array)
- management_plan (investigations_ordered array, treatment_prescribed array, patient_education array, follow_up_plan, referrals array, precautions array)
- clinical_notes (string)
- emergency_alert (null or object with is_emergency, red_flags_detected, recommendation, action_required)

Return ONLY the JSON object, no markdown or extra text."""

        model_input = ModelInput(user_prompt=prompt)
        response = self.client.generate_content(model_input, stream=False)

        return self._parse_json_from_response(response)

    def _save_summary(self, summary: MedicalSummary) -> str:
        """Save summary as JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = summary.patient_demographics.name.replace(" ", "_")
        filename = f"medical_summary_{name}_{timestamp}.json"

        with open(filename, 'w') as f:
            json.dump(summary.model_dump(), f, indent=2)

        return filename

    def _save_report(self, summary: MedicalSummary) -> str:
        """Save formatted report as text."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = summary.patient_demographics.name.replace(" ", "_")
        filename = f"medical_report_{name}_{timestamp}.txt"

        lines = []
        lines.append("\n" + "="*80)
        lines.append("MEDICAL CONSULTATION REPORT".center(80))
        lines.append("="*80 + "\n")

        # Patient info
        demo = summary.patient_demographics
        lines.append("PATIENT INFORMATION")
        lines.append("-" * 80)
        lines.append(f"Name: {demo.name}")
        lines.append(f"Age: {demo.age} | Gender: {demo.gender}")
        if demo.occupation:
            lines.append(f"Occupation: {demo.occupation}")
        lines.append(f"Date: {summary.consultation_date}\n")

        # Chief complaint
        lines.append("CHIEF COMPLAINT")
        lines.append("-" * 80)
        cc = summary.chief_complaint
        lines.append(f"Complaint: {cc.primary_complaint}")
        lines.append(f"Duration: {cc.duration} | Severity: {cc.severity} | Onset: {cc.onset}\n")

        # History
        lines.append("HISTORY OF PRESENT ILLNESS")
        lines.append("-" * 80)
        lines.append(f"{summary.history_of_present_illness}\n")

        # Review of systems
        lines.append("REVIEW OF SYSTEMS")
        lines.append("-" * 80)
        for system, findings in summary.review_of_systems.model_dump().items():
            if findings:
                lines.append(f"{system.upper()}: {', '.join(findings)}")
        lines.append()

        # Medical history
        lines.append("PAST MEDICAL HISTORY")
        lines.append("-" * 80)
        pmh = summary.past_medical_history
        if pmh.past_medical_conditions:
            lines.append(f"Conditions: {', '.join(pmh.past_medical_conditions)}")
        if pmh.current_medications:
            lines.append(f"Medications: {', '.join(pmh.current_medications)}")
        if pmh.allergies:
            lines.append(f"Allergies: {', '.join(pmh.allergies)}")
        if pmh.surgical_history:
            lines.append(f"Surgeries: {', '.join(pmh.surgical_history)}")
        if pmh.family_history:
            lines.append(f"Family History: {', '.join(pmh.family_history)}")
        lines.append()

        # Physical exam
        lines.append("PHYSICAL EXAMINATION")
        lines.append("-" * 80)
        pe = summary.physical_examination
        lines.append("Vital Signs:")
        for vital, value in pe.vital_signs.items():
            lines.append(f"  {vital}: {value}")
        lines.append(f"General: {pe.general_appearance}")
        if pe.specific_findings:
            lines.append("Findings:")
            for finding in pe.specific_findings:
                lines.append(f"  • {finding}")
        lines.append()

        # Assessment
        lines.append("CLINICAL ASSESSMENT")
        lines.append("-" * 80)
        ca = summary.clinical_assessment
        lines.append(f"Most Likely Diagnosis: {ca.most_likely_diagnosis}")
        lines.append(f"Confidence: {ca.diagnostic_confidence}")
        lines.append("Differential Diagnosis:")
        for i, dx in enumerate(ca.differential_diagnosis, 1):
            lines.append(f"  {i}. {dx}")
        if ca.red_flags:
            lines.append("\n⚠ RED FLAGS:")
            for flag in ca.red_flags:
                lines.append(f"  • {flag}")
        lines.append()

        # Management
        lines.append("MANAGEMENT PLAN")
        lines.append("-" * 80)
        mp = summary.management_plan
        lines.append("Investigations Ordered:")
        for inv in mp.investigations_ordered:
            lines.append(f"  • {inv}")
        lines.append("\nTreatment Prescribed:")
        for tx in mp.treatment_prescribed:
            lines.append(f"  • {tx}")
        lines.append("\nPatient Education:")
        for edu in mp.patient_education:
            lines.append(f"  • {edu}")
        lines.append(f"\nFollow-up: {mp.follow_up_plan}")
        if mp.referrals:
            lines.append(f"Referrals: {', '.join(mp.referrals)}")
        lines.append("\n⚠ Return Immediately If:")
        for precaution in mp.precautions:
            lines.append(f"  • {precaution}")
        lines.append()

        # Notes
        lines.append("CLINICAL NOTES")
        lines.append("-" * 80)
        lines.append(f"{summary.clinical_notes}\n")

        lines.append("="*80 + "\n")

        with open(filename, 'w') as f:
            f.write("\n".join(lines))

        return filename

    def _save_transcript(self, patient_name: str) -> str:
        """Save consultation transcript."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = patient_name.replace(" ", "_")
        filename = f"consultation_transcript_{name}_{timestamp}.txt"

        with open(filename, 'w') as f:
            f.write("\n".join(self.transcript))

        return filename

    def _handle_emergency(self, red_flags: List[str], patient_name: str):
        """Handle emergency escalation."""
        self.transcript.append("\n" + "="*80)
        self.transcript.append("⚠️  EMERGENCY ALERT - IMMEDIATE ACTION REQUIRED".center(80))
        self.transcript.append("="*80 + "\n")
        self.transcript.append(f"Dear {patient_name},\n")
        self.transcript.append("Based on what you've shared, I've identified serious warning signs")
        self.transcript.append("that require immediate medical attention.\n")
        self.transcript.append("RED FLAGS DETECTED:")
        for flag in red_flags:
            self.transcript.append(f"  • {flag}")
        self.transcript.append("\n⚠️  STOP THIS CONSULTATION")
        self.transcript.append("⚠️  CALL 911 IMMEDIATELY or go to the nearest Emergency Room")
        self.transcript.append("This is a medical emergency. Professional emergency care is required.")
        self.transcript.append("="*80 + "\n")

        print("\n" + "="*80)
        print("⚠️  EMERGENCY ALERT - IMMEDIATE ACTION REQUIRED".center(80))
        print("="*80)
        print(f"\nDear {patient_name},\n")
        print("Based on what you've shared, I've identified serious warning signs")
        print("that require immediate medical attention.\n")
        print("RED FLAGS DETECTED:")
        for flag in red_flags:
            print(f"  • {flag}")
        print("\n⚠️  STOP THIS CONSULTATION")
        print("⚠️  CALL 911 IMMEDIATELY or go to the nearest Emergency Room")
        print("="*80 + "\n")

def cli():
    """Run the medical consultation system."""
    app = MedicalConsultation()

    try:
        summary, summary_file, report_file = app.run()

        if summary:
            print("✓ Consultation completed successfully!")
        else:
            print("⚠️  Consultation ended due to emergency.")

    except KeyboardInterrupt:
        print("\n\nConsultation interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    cli()
