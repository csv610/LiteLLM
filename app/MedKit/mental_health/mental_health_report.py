"""mental_health_report - Professional report generation from mental health assessments.

This module generates comprehensive clinical and patient-friendly reports from
mental health assessment data. It converts structured assessment data into
professionally formatted documents suitable for healthcare providers, electronic
health records (EHR) systems, and patient use.

Reports include clinical summaries with diagnostic details, standardized screening
scores (PHQ-9, GAD-7), risk assessments, treatment recommendations, and crisis
resources. Multiple output formats support clinical documentation, care coordination,
and patient education.

QUICK START:
    from mental_health_report import MentalHealthReportGenerator
    from mental_health_assessment import MentalHealthAssessment
    import json

    # Load assessment data
    with open("assessment.json") as f:
        assessment_data = json.load(f)
    assessment = MentalHealthAssessment(**assessment_data)

    # Generate reports
    generator = MentalHealthReportGenerator()
    clinical_report = generator.generate_clinical_report(assessment)
    patient_summary = generator.generate_patient_summary(assessment)

    # Save all report formats
    reports = generator.generate_and_save_all_reports(assessment)
    print(f"Clinical Report: {reports['clinical']}")
    print(f"Patient Summary: {reports['patient_summary']}")
    print(f"JSON Assessment: {reports['assessment_json']}")

COMMON USES:
    1. Generate clinical reports for psychiatric consultation and referral
    2. Create patient-friendly summaries for informed consent and education
    3. Export assessment data as JSON for EHR/EMR integration
    4. Provide formatted documentation for insurance and administrative purposes
    5. Generate audit-ready records for compliance and quality assurance

KEY FEATURES:
    - Clinical Reports: Comprehensive clinician-focused reports with detailed
      diagnostic criteria, symptom listings, and evidence-based recommendations
    - Patient Summaries: Accessible patient-friendly version using simplified
      language with actionable next steps and resource information
    - JSON Export: Structured data export compatible with EHR systems and
      programmatic processing
    - Risk Highlighting: Clear risk assessment presentation with emergency
      indicators and safety planning resources
    - Treatment Recommendations: Evidence-based psychotherapy and medication
      suggestions with referral urgency levels
    - HIPAA Compliance: Secure file handling with restricted permissions and
      proper confidentiality disclaimers
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

try:
    from medkit.core.gemini_client import GeminiClient, ModelConfig, ModelInput
    from medkit.core.config import PrivacyConfig
except ImportError:
    # Fallback classes
    class ModelConfig:
        pass
    class ModelInput:
        pass
    class GeminiClient:
        pass
    class PrivacyConfig:
        pass

try:
    from .mental_health_assessment import (
        MentalHealthAssessment, ChatSession, MentalHealthCondition,
        RiskAssessment, TreatmentRecommendation
    )
    from .models import ChatMessage
except ImportError:
    try:
        from medkit.mental_health.mental_health_assessment import (
            MentalHealthAssessment, ChatSession, MentalHealthCondition,
            RiskAssessment, TreatmentRecommendation
        )
        from medkit.mental_health.models import ChatMessage
    except ImportError:
        from mental_health_assessment import (
            MentalHealthAssessment, ChatSession, MentalHealthCondition,
            RiskAssessment, TreatmentRecommendation
        )
        from models import ChatMessage

# ==================== Report Configuration ====================

class ReportConfig:
    """Report generation configuration."""

    # Output directories
    OUTPUT_DIR = Path(__file__).parent / "outputs" / "mental_health_reports"
    JSON_DIR = OUTPUT_DIR / "assessments"
    TEXT_DIR = OUTPUT_DIR / "clinical_reports"
    PATIENT_DIR = OUTPUT_DIR / "patient_summaries"

    @classmethod
    def setup_directories(cls):
        """Create output directories."""
        for dir_path in [cls.JSON_DIR, cls.TEXT_DIR, cls.PATIENT_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)

# ==================== Report Generator ====================

class MentalHealthReportGenerator:
    """
    Generates professional mental health assessment reports.
    """

    def __init__(self):
        """Initialize report generator."""
        ReportConfig.setup_directories()

    def generate_clinical_report(self, assessment: MentalHealthAssessment,
                                session: Optional[ChatSession] = None) -> str:
        """
        Generate comprehensive clinical mental health report.

        Args:
            assessment: MentalHealthAssessment object
            session: ChatSession object (optional)

        Returns:
            Formatted clinical report text
        """
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MENTAL HEALTH CLINICAL ASSESSMENT REPORT                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

PATIENT INFORMATION
{'='*80}
Name:              {assessment.patient_name}
Age:               {assessment.age} years
Gender:            {assessment.gender}
Assessment Date:   {assessment.assessment_date}
Session ID:        {assessment.session_id}

PRESENTING COMPLAINT
{'='*80}
Chief Complaint:   {assessment.chief_complaint}
Duration:          {assessment.complaint_duration}
Onset:             {assessment.complaint_onset}

STANDARDIZED SCREENING SCORES
{'='*80}
PHQ-9 (Depression) Assessment:
  Total Score: {assessment.phq9_assessment.total_score}/27
  Severity Level: {assessment.phq9_assessment.severity.title()}

  Individual Items:
    • Depressed mood: {assessment.phq9_assessment.depressed_mood}/3
    • Sleep disturbance: {assessment.phq9_assessment.sleep_disturbance}/3
    • Fatigue/low energy: {assessment.phq9_assessment.fatigue}/3
    • Appetite/weight change: {assessment.phq9_assessment.appetite_change}/3
    • Guilt/worthlessness: {assessment.phq9_assessment.guilt_shame}/3
    • Concentration difficulty: {assessment.phq9_assessment.concentration}/3
    • Psychomotor changes: {assessment.phq9_assessment.psychomotor}/3
    • Suicidal ideation: {assessment.phq9_assessment.suicidal_ideation}/3
    • Functional impairment: {assessment.phq9_assessment.functional_impairment}/3

GAD-7 (Anxiety) Assessment:
  Total Score: {assessment.gad7_assessment.total_score}/21
  Severity Level: {assessment.gad7_assessment.severity.title()}

  Individual Items:
    • Worry frequency: {assessment.gad7_assessment.worry_frequency}/3
    • Worry control: {assessment.gad7_assessment.worry_control}/3
    • Worry about different things: {assessment.gad7_assessment.worry_concentration}/3
    • Irritability: {assessment.gad7_assessment.irritability}/3
    • Restlessness: {assessment.gad7_assessment.restlessness}/3
    • Fatigue (anxiety): {assessment.gad7_assessment.fatigue_anxiety}/3
    • Fear/catastrophizing: {assessment.gad7_assessment.fear_catastrophe}/3

SYMPTOMS ASSESSMENT
{'='*80}

Mood Symptoms:
{self._format_symptom_list(assessment.mood_symptoms.model_dump())}

Anxiety Symptoms:
{self._format_symptom_list(assessment.anxiety_symptoms.model_dump())}

Cognitive Symptoms:
{self._format_symptom_list(assessment.cognitive_symptoms.model_dump())}

Physical Symptoms:
{self._format_symptom_list(assessment.physical_symptoms.model_dump())}

Trauma-Related Symptoms:
{self._format_symptom_list(assessment.trauma_symptoms.model_dump())}

Substance Use:
  Frequency: {assessment.substance_use.substance_use_frequency}
  Substances: {', '.join(assessment.substance_use.substances_used) if assessment.substance_use.substances_used else 'None reported'}

PSYCHIATRIC HISTORY
{'='*80}
Previous Diagnoses:     {', '.join(assessment.mental_health_history.previous_diagnoses) if assessment.mental_health_history.previous_diagnoses else 'None reported'}
Age of Onset:           {assessment.mental_health_history.age_of_onset or 'Unknown'}
Previous Treatment:     {', '.join(assessment.mental_health_history.previous_treatment) if assessment.mental_health_history.previous_treatment else 'None'}
Hospitalizations:       {assessment.mental_health_history.hospitalization_history}
Family History:         {', '.join(assessment.mental_health_history.family_mental_health_history) if assessment.mental_health_history.family_mental_health_history else 'None reported'}
Trauma History:         {', '.join(assessment.mental_health_history.trauma_history) if assessment.mental_health_history.trauma_history else 'None reported'}
Current Medications:    {', '.join(assessment.mental_health_history.current_medications) if assessment.mental_health_history.current_medications else 'None'}

SOCIAL FUNCTIONING
{'='*80}
Relationship Quality:        {assessment.social_functioning.relationship_quality}
Social Support:              {assessment.social_functioning.social_support_system}
Employment Status:           {assessment.social_functioning.employment_status}
Occupational Functioning:    {assessment.social_functioning.occupational_functioning}
Family Relationships:        {assessment.social_functioning.family_relationships}
Living Situation:            {assessment.social_functioning.living_situation}

RISK ASSESSMENT (CRITICAL)
{'='*80}
Suicidal Ideation:           {'YES' if assessment.risk_assessment.suicidal_ideation else 'No'}
{f'  Frequency: {assessment.risk_assessment.suicidal_ideation_frequency}' if assessment.risk_assessment.suicidal_ideation else ''}
{f'  Proposed Method: {assessment.risk_assessment.suicide_plan_method}' if assessment.risk_assessment.suicide_plan_method else ''}
{f'  Access to Means: {assessment.risk_assessment.access_to_means}' if assessment.risk_assessment.access_to_means is not None else ''}

Self-Harm Behavior:          {'YES' if assessment.risk_assessment.self_harm_behavior else 'No'}
Previous Suicide Attempts:   {assessment.risk_assessment.previous_suicide_attempts}
Thoughts of Harming Others:  {'YES' if assessment.risk_assessment.harm_to_others else 'No'}
Violence History:            {'YES' if assessment.risk_assessment.violence_history else 'No'}
Substance Abuse Severity:    {assessment.risk_assessment.substance_abuse_severity}
Homelessness Risk:           {'YES' if assessment.risk_assessment.homelessness_risk else 'No'}

⚠️  OVERALL RISK LEVEL: {assessment.risk_assessment.overall_risk_level.upper()}
Crisis Resources Aware:      {'YES' if assessment.risk_assessment.crisis_resources_aware else 'NO - NEEDS EDUCATION'}

CLINICAL ASSESSMENT & DIAGNOSIS
{'='*80}

PRIMARY DIAGNOSIS:
  Condition: {assessment.primary_diagnosis.condition_name}
  DSM-5 Code: {assessment.primary_diagnosis.diagnostic_code_dsm5}
  ICD-11 Code: {assessment.primary_diagnosis.diagnostic_code_icd11}
  Severity: {assessment.primary_diagnosis.severity}
  Duration: {assessment.primary_diagnosis.duration}
  Confidence Level: {assessment.primary_diagnosis.confidence_level}

  Diagnostic Criteria Met:
{self._format_criteria_list(assessment.primary_diagnosis.diagnostic_criteria_met)}

SECONDARY DIAGNOSES:
{self._format_secondary_diagnoses(assessment.secondary_diagnoses)}

CLINICAL SUMMARY
{'='*80}
{assessment.clinical_summary}

CLINICAL NOTES
{'='*80}
{assessment.clinical_notes}

TREATMENT RECOMMENDATIONS
{'='*80}
Recommended Psychotherapy:
{self._format_list(assessment.treatment_recommendations.psychotherapy_types)}

Medication Considerations:
{self._format_list(assessment.treatment_recommendations.medication_class_considerations)}

Lifestyle Interventions:
{self._format_list(assessment.treatment_recommendations.lifestyle_interventions)}

Specialty Referral:
  Type: {assessment.treatment_recommendations.referral_type}
  Urgency: {assessment.treatment_recommendations.urgency_of_care}
  Emergency Intervention Needed: {'YES' if assessment.treatment_recommendations.emergency_contact_needed else 'No'}

CRISIS RESOURCES (IF NEEDED)
{'='*80}
National Suicide Prevention Lifeline: 988 (24/7)
Crisis Text Line: Text HOME to 741741
SAMHSA National Helpline: 1-800-662-4357
Emergency Services: 911

International Crisis Resources: https://www.iasp.info/resources/Crisis_Centres/

IMPORTANT DISCLAIMERS & LIMITATIONS
{'='*80}
• This assessment is generated by an AI system and is NOT a substitute for
  professional mental health evaluation and diagnosis by a qualified clinician.

• This report should be reviewed and validated by a licensed mental health
  professional (psychiatrist, psychologist, licensed counselor, etc.)

• Clinical decisions should be based on comprehensive in-person evaluation,
  not solely on this AI assessment.

• Suicidal risk assessment is preliminary and must be thoroughly evaluated
  by a professional clinician.

• This system should be used as a screening and education tool, not for
  definitive diagnosis or treatment planning.

RECOMMENDATIONS FOR NEXT STEPS
{'='*80}
1. Schedule appointment with mental health professional (psychiatrist, psychologist,
   or licensed counselor) for comprehensive evaluation

2. Share this assessment report with your healthcare provider

3. If in crisis or having suicidal thoughts, contact emergency services or
   call 988 immediately

4. Follow the recommended treatment plan developed with your clinician

5. Maintain regular follow-up appointments

6. Consider therapy modalities recommended (CBT, DBT, psychodynamic, etc.)

7. Discuss medication options with a psychiatrist if appropriate

8. Implement lifestyle changes (sleep, exercise, stress management, etc.)

PRIVACY & CONFIDENTIALITY
{'='*80}
This report contains Protected Health Information (PHI) and must be handled
according to HIPAA regulations. It should be:
• Stored securely
• Shared only with authorized healthcare providers
• Not shared without patient consent
• Retained for appropriate retention periods

Report Generated: {datetime.now().isoformat()}
System: MedKit Mental Health Assessment AI
Version: 1.0

{'='*80}
END OF REPORT
{'='*80}
"""
        return report

    def _format_symptom_list(self, symptoms_dict: Dict[str, bool]) -> str:
        """Format symptom list for report."""
        present = [k.replace('_', ' ').title() for k, v in symptoms_dict.items() if v]
        if not present:
            return "  • No symptoms reported\n"
        return "\n".join([f"  • {symptom}" for symptom in present]) + "\n"

    def _format_list(self, items: List[str]) -> str:
        """Format list items for report."""
        if not items:
            return "  • None specified\n"
        return "\n".join([f"  • {item}" for item in items]) + "\n"

    def _format_criteria_list(self, criteria: List[str]) -> str:
        """Format diagnostic criteria for report."""
        if not criteria:
            return "    • Standard criteria met\n"
        return "\n".join([f"    • {criterion}" for criterion in criteria[:5]]) + "\n"

    def _format_secondary_diagnoses(self, diagnoses: List[MentalHealthCondition]) -> str:
        """Format secondary diagnoses for report."""
        if not diagnoses:
            return "  • No secondary diagnoses identified\n"

        text = ""
        for i, diag in enumerate(diagnoses[:3], 1):
            text += f"\n  Diagnosis {i}:\n"
            text += f"    • Condition: {diag.condition_name}\n"
            text += f"    • Severity: {diag.severity}\n"
            text += f"    • Confidence: {diag.confidence_level}\n"

        return text

    def generate_patient_summary(self, assessment: MentalHealthAssessment) -> str:
        """
        Generate patient-friendly summary (simpler language).

        Args:
            assessment: MentalHealthAssessment object

        Returns:
            Patient-friendly summary text
        """
        summary = f"""
MENTAL HEALTH ASSESSMENT SUMMARY
(For Your Records)

Date: {assessment.assessment_date}
Your Name: {assessment.patient_name}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHAT WE DISCUSSED:
You told us you're experiencing: {assessment.chief_complaint}
This has been going on for: {assessment.complaint_duration}

WHAT WE FOUND:
Based on our conversation, here's what we learned about your mental health:

Primary Concern: {assessment.primary_diagnosis.condition_name}
  - How severe it is: {assessment.primary_diagnosis.severity}
  - How confident we are in this: {assessment.primary_diagnosis.confidence_level}

Depression Screening Score: {assessment.phq9_assessment.total_score}/27
  ({assessment.phq9_assessment.severity.title()} level)

Anxiety Screening Score: {assessment.gad7_assessment.total_score}/21
  ({assessment.gad7_assessment.severity.title()} level)

SYMPTOMS YOU'RE EXPERIENCING:
Mood Changes: {'Yes' if any(assessment.mood_symptoms.model_dump().values()) else 'No'}
Anxiety or Worry: {'Yes' if any(assessment.anxiety_symptoms.model_dump().values()) else 'No'}
Sleep or Energy Problems: {'Yes' if assessment.physical_symptoms.sleep_disturbance or assessment.physical_symptoms.fatigue else 'No'}
Difficulty Concentrating: {'Yes' if assessment.cognitive_symptoms.poor_concentration else 'No'}

SAFETY ASSESSMENT:
Are you having thoughts of hurting yourself? {'YES - See Resources Below' if assessment.risk_assessment.suicidal_ideation else 'No'}
Are you hurting yourself? {'YES - Seek Help' if assessment.risk_assessment.self_harm_behavior else 'No'}

⚠️ IMPORTANT: If you're thinking about harming yourself or are in crisis:
   • Call 988 (Suicide & Crisis Lifeline)
   • Text HOME to 741741
   • Call 911 or go to nearest emergency room

WHAT WE RECOMMEND:
Treatment Type: {assessment.treatment_recommendations.referral_type}
How soon: {assessment.treatment_recommendations.urgency_of_care.title()}

Things that might help:
{self._format_list(assessment.treatment_recommendations.psychotherapy_types)}

Things to try on your own:
{self._format_list(assessment.treatment_recommendations.lifestyle_interventions)}

NEXT STEPS:
1. ☐ Schedule an appointment with a mental health professional
   (psychiatrist, therapist, or counselor)

2. ☐ Bring this report to your appointment

3. ☐ Discuss treatment options with your provider

4. ☐ Start recommended activities or treatments

5. ☐ Follow up regularly with your provider

IMPORTANT TO KNOW:
✓ This assessment is a screening tool, not a final diagnosis
✓ A professional needs to confirm any diagnosis
✓ Treatment really does help - recovery is possible
✓ Many people get better with the right support

HELPFUL RESOURCES:
National Suicide Prevention Lifeline: 988
Crisis Text Line: Text HOME to 741741
SAMHSA Helpline: 1-800-662-4357 (free, confidential, 24/7)
NAMI Helpline: 1-800-950-NAMI

Your Mental Health Matters. 🫂
You're taking a brave step by getting help.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Report created by: MedKit Mental Health Assessment System
Session ID: {assessment.session_id}
"""
        return summary

    def save_assessment_json(self, assessment: MentalHealthAssessment) -> Path:
        """
        Save assessment as JSON for integration with EHR systems.

        Args:
            assessment: MentalHealthAssessment object

        Returns:
            Path to saved JSON file
        """
        filename = f"assessment_{assessment.patient_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = ReportConfig.JSON_DIR / filename

        with open(filepath, 'w') as f:
            json.dump(assessment.model_dump(), f, indent=2)

        os.chmod(filepath, 0o600)  # Restrict access
        print(f"✓ Assessment saved: {filepath}")
        return filepath

    def save_clinical_report(self, report_text: str, patient_name: str) -> Path:
        """
        Save clinical report as text file.

        Args:
            report_text: Formatted clinical report
            patient_name: Patient name for filename

        Returns:
            Path to saved file
        """
        filename = f"clinical_report_{patient_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = ReportConfig.TEXT_DIR / filename

        with open(filepath, 'w') as f:
            f.write(report_text)

        os.chmod(filepath, 0o600)  # Restrict access
        print(f"✓ Clinical report saved: {filepath}")
        return filepath

    def save_patient_summary(self, summary_text: str, patient_name: str) -> Path:
        """
        Save patient-friendly summary.

        Args:
            summary_text: Formatted patient summary
            patient_name: Patient name for filename

        Returns:
            Path to saved file
        """
        filename = f"patient_summary_{patient_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filepath = ReportConfig.PATIENT_DIR / filename

        with open(filepath, 'w') as f:
            f.write(summary_text)

        os.chmod(filepath, 0o600)  # Restrict access
        print(f"✓ Patient summary saved: {filepath}")
        return filepath

    def generate_and_save_all_reports(self, assessment: MentalHealthAssessment,
                                     session: Optional[ChatSession] = None) -> Dict[str, Path]:
        """
        Generate and save all report formats.

        Args:
            assessment: MentalHealthAssessment object
            session: ChatSession object (optional)

        Returns:
            Dictionary with paths to all generated reports
        """
        reports = {}

        # Generate clinical report
        clinical_report = self.generate_clinical_report(assessment, session)
        reports['clinical'] = self.save_clinical_report(clinical_report, assessment.patient_name)

        # Generate patient summary
        patient_summary = self.generate_patient_summary(assessment)
        reports['patient_summary'] = self.save_patient_summary(patient_summary, assessment.patient_name)

        # Save assessment JSON
        reports['assessment_json'] = self.save_assessment_json(assessment)

        return reports
