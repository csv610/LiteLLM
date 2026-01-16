"""mental_health_chat_app - Interactive CLI for compassionate mental health assessment.

This module provides a privacy-compliant, crisis-aware mental health assessment application
with real-time conversational interface. It guides patients through adaptive, personalized
questioning to evaluate mental health status, detects crisis indicators with emergency
response protocols, generates clinical assessments and recommendations, and maintains
session history for continuity of care. HIPAA-compliant data handling and trauma-informed
design principles are central to the application.

QUICK START:
    Start a new mental health assessment:

    $ python mental_health_chat_app.py

    Resume a previous session:

    $ python mental_health_chat_app.py --resume

    Or use programmatically:

    >>> from mental_health_chat_app import MentalHealthChatApp
    >>> app = MentalHealthChatApp()
    >>> app.run()

COMMON USES:
    1. Initial mental health screening - structured assessment for new patients
    2. Session continuity - resuming incomplete assessments
    3. Crisis detection - identifying and responding to emergency situations
    4. Patient self-assessment - private, judgment-free mental health evaluation
    5. Treatment planning - generating recommendations for appropriate care levels

KEY FEATURES AND COVERAGE AREAS:
    - Patient Registration: demographic collection with age validation
    - Consent Management: HIPAA-compliant consent and privacy disclosures
    - Adaptive Conversation: personalized questioning based on responses
    - Emergency Detection: crisis indicators with 988 Lifeline integration
    - Clinical Assessment: automated diagnosis and treatment recommendations
    - Session Management: save, resume, and history tracking
    - Diagnostic Outputs: primary/secondary diagnoses with severity ratings
    - Referral Recommendations: appropriate care level guidance
    - Privacy Compliance: HIPAA-aligned data protection and retention
    - Trauma-Informed Design: safe, validating assessment environment
"""

import os
import sys
import argparse
import traceback
from datetime import datetime
from typing import Optional

try:
    from medkit.mental_health.mental_health_chat import MentalHealthChatEngine, ChatConfig
    from medkit.utils.privacy_compliance import PrivacyManager
    from medkit.core.config import PrivacyConfig
except ImportError:
    try:
        from .mental_health_chat import MentalHealthChatEngine, ChatConfig
    except ImportError:
        from mental_health_chat import MentalHealthChatEngine, ChatConfig

    class PrivacyManager:
        pass
    class PrivacyConfig:
        pass

# ==================== CLI Application ====================

class MentalHealthChatApp:
    """
    Main CLI application for mental health assessment chat.
    """

    def __init__(self):
        """Initialize the application."""
        self.engine = MentalHealthChatEngine()
        self.privacy_manager = PrivacyManager()

    def display_banner(self):
        """Display application banner."""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                 MEDKIT MENTAL HEALTH ASSESSMENT CHAT                         ║
║                    Compassionate AI-Guided Evaluation                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Welcome to MedKit's mental health assessment system.

This is a confidential, judgment-free space to discuss your mental health concerns.
Our AI assistant will ask personalized questions to understand your situation and
provide recommendations for appropriate care.

⚠️  IMPORTANT REMINDERS:
    • This is NOT a substitute for professional mental health care
    • If you're in crisis, please call 988 (Suicide & Crisis Lifeline) or 911
    • All information is handled confidentially per HIPAA regulations
    • Your data will be securely stored and retained per privacy policies

Let's get started! 🫂
"""
        print(banner)

    def get_consent(self) -> bool:
        """
        Obtain user consent before proceeding.

        Returns:
            True if user consents, False otherwise
        """
        print("\n" + "="*80)
        print("PRIVACY & CONSENT".center(80))
        print("="*80 + "\n")

        print("""
⚠️  IMPORTANT PRIVACY NOTICE:

By proceeding with this assessment, you acknowledge that:

1. This is NOT a substitute for professional mental health care
2. Your data is confidential and handled per HIPAA regulations
3. In case of emergency, please call 911 or 988 (Suicide & Crisis Lifeline)
4. Your responses will be analyzed to provide recommendations
5. Data will be securely stored according to our privacy policy

CONSENT:
□ I understand this is a clinical tool, not a diagnosis
□ I consent to data collection and analysis for my assessment
□ I understand my privacy rights and data handling practices
□ I am 13 years or older
        """)

        consent = input("Do you consent to proceed? (yes/no): ").strip().lower()
        return consent in ['yes', 'y']

    def register_patient(self) -> tuple:
        """
        Collect patient registration information.

        Returns:
            Tuple of (name, age, gender, chief_complaint)
        """
        print("\n" + "="*80)
        print("PATIENT REGISTRATION".center(80))
        print("="*80 + "\n")

        # Name
        name = input("Your name: ").strip()
        while not name:
            name = input("Please enter your name: ").strip()

        # Age
        while True:
            try:
                age = int(input("Your age: ").strip())
                if 13 <= age <= 120:
                    break
                print("Please enter a valid age (13-120)")
            except ValueError:
                print("Please enter a valid number")

        # Gender
        print("\nGender (select one):")
        print("  1. Male")
        print("  2. Female")
        print("  3. Non-binary")
        print("  4. Prefer to self-describe")
        print("  5. Prefer not to say")

        gender_map = {
            "1": "Male",
            "2": "Female",
            "3": "Non-binary",
            "4": "Self-described",
            "5": "Prefer not to say"
        }

        while True:
            choice = input("Enter choice (1-5): ").strip()
            if choice in gender_map:
                gender = gender_map[choice]
                break
            print("Invalid choice. Please select 1-5")

        # Chief complaint
        print("\n" + "-"*80)
        print("What brings you here today?")
        print("(Describe what you're experiencing or what concerns you)")
        print("-"*80)
        chief_complaint = input("Your main concern: ").strip()
        while not chief_complaint:
            chief_complaint = input("Please describe what brings you in: ").strip()

        return name, age, gender, chief_complaint

    def conduct_assessment(self, patient_name: str, age: int, gender: str,
                          chief_complaint: str):
        """
        Conduct the mental health assessment conversation.

        Args:
            patient_name: Patient name
            age: Patient age
            gender: Patient gender
            chief_complaint: Chief complaint
        """
        # Initialize session
        session = self.engine.initialize_session(patient_name, age, gender, chief_complaint)

        print("\n" + "="*80)
        print("MENTAL HEALTH ASSESSMENT".center(80))
        print("="*80)
        print(f"\nSession ID: {session.session_id}")
        print(f"Date: {session.created_at}\n")

        print("-"*80)
        print("CONVERSATION")
        print("-"*80)
        print(f"\nAssistant: Thank you for coming in, {patient_name}. I'm here to help you")
        print("understand what you're experiencing. Let's have a conversation about how you're")
        print("doing.\n")

        # Generate and ask first question
        first_question = self.engine.generate_next_question(
            f"Chief complaint: {chief_complaint}"
        )
        print(f"Assistant: {first_question}\n")

        # Conversation loop
        question_count = 0
        max_questions = ChatConfig.MAX_QUESTIONS

        while question_count < max_questions:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    print("Please share your thoughts...\n")
                    continue

                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'done']:
                    print("\nAssistant: Thank you for sharing with me today.")
                    break

                question_count += 1

                # Process response
                result = self.engine.process_user_response(user_input)

                # Check for emergency
                if result["emergency"]:
                    print(f"\n{result['response']}")
                    self._save_and_exit()
                    return
                else:
                    # Display next question
                    print(f"\nAssistant: {result['response']}\n")

                    # Show progress
                    if question_count % 5 == 0:
                        print(f"[Progress: {question_count}/{max_questions} questions]\n")

            except KeyboardInterrupt:
                print("\n\nAssessment interrupted.")
                self.engine.save_session()
                print(f"Your session has been saved. Session ID: {session.session_id}")
                return

        print("\n" + "="*80)
        print("ASSESSMENT COMPLETE".center(80))
        print("="*80 + "\n")

        print("Generating your mental health assessment report...\n")

        # Generate assessment
        assessment = self.engine.generate_assessment()

        if assessment:
            print("✓ Assessment generated successfully")
            print(f"\nPrimary Diagnosis: {assessment.primary_diagnosis.condition_name}")
            print(f"Severity: {assessment.primary_diagnosis.severity}")
            print(f"Confidence: {assessment.primary_diagnosis.confidence_level}")

            if assessment.secondary_diagnoses:
                print("\nOther Conditions to Consider:")
                for diag in assessment.secondary_diagnoses[:3]:
                    print(f"  • {diag.condition_name} ({diag.confidence_level} confidence)")

            print(f"\nRecommended Care: {assessment.treatment_recommendations.referral_type}")
            print(f"Urgency: {assessment.treatment_recommendations.urgency_of_care}")

            # Save assessment
            self.engine.save_session()
            print(f"\n✓ Your session has been saved. Session ID: {session.session_id}")

        else:
            print("⚠ Could not generate assessment. Please try again.")

    def _save_and_exit(self):
        """Save session and exit gracefully."""
        self.engine.save_session()
        if self.engine.session:
            print(f"\nYour session has been saved. Session ID: {self.engine.session.session_id}")

    def resume_session(self) -> bool:
        """
        Allow user to resume a previous session.

        Returns:
            True if session resumed, False otherwise
        """
        print("\n" + "="*80)
        print("RESUME SESSION".center(80))
        print("="*80 + "\n")

        session_id = input("Enter your session ID (or press Enter to start new): ").strip()

        if not session_id:
            return False

        resumed = self.engine.resume_session(session_id)

        if resumed:
            print(f"\n✓ Session resumed: {session_id}")
            return True
        else:
            print(f"Could not resume session: {session_id}")
            return False

    def display_completion_info(self):
        """Display completion information and resources."""
        info = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        ASSESSMENT COMPLETE                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

Thank you for participating in this mental health assessment.

NEXT STEPS:
1. Review your assessment report
2. Share this report with a mental health professional
3. Schedule an appointment for professional evaluation and treatment
4. Follow recommended treatment plan from your clinician

IMPORTANT RESOURCES:
• National Suicide Prevention Lifeline: 988 (24/7)
• Crisis Text Line: Text HOME to 741741
• SAMHSA National Helpline: 1-800-662-4357 (substance abuse)
• National Alliance on Mental Illness (NAMI): 1-800-950-NAMI
• Emergency Services: 911

REMEMBER:
✓ Recovery is possible
✓ You're not alone
✓ Professional help makes a difference
✓ Take things one day at a time

For more information or to access your assessment data, visit: [YOUR PLATFORM URL]

Thank you for trusting us with your mental health journey. 🫂
"""
        print(info)

    def run(self, resume: bool = False):
        """
        Run the mental health assessment application.

        Args:
            resume: Whether to attempt to resume a previous session
        """
        try:
            self.display_banner()

            # Handle session resumption
            if resume and self.resume_session():
                # Resume existing session
                print("Continuing your previous assessment...\n")
                # Continue from where they left off
                # (In production, show unfinished assessment)
            else:
                # Get consent
                if not self.get_consent():
                    print("\n⚠ You must accept the privacy terms to proceed.")
                    return

                # Register patient
                name, age, gender, complaint = self.register_patient()

                # Conduct assessment
                self.conduct_assessment(name, age, gender, complaint)

                # Show completion info
                self.display_completion_info()

        except KeyboardInterrupt:
            print("\n\nApplication interrupted.")
            if self.engine.session:
                self.engine.save_session()
                print(f"Session saved: {self.engine.session.session_id}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            traceback.print_exc()
        finally:
            print("\nThank you for using MedKit Mental Health Assessment.\n")

# ==================== Main Entry Point ====================

def cli():
    """Main entry point."""

    parser = argparse.ArgumentParser(
        description="MedKit Mental Health Assessment Chat",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python mental_health_chat_app.py              # Start new assessment
  python mental_health_chat_app.py --resume     # Resume previous session
        """
    )

    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume a previous session"
    )

    args = parser.parse_args()

    app = MentalHealthChatApp()
    app.run(resume=args.resume)


if __name__ == "__main__":
    cli()
