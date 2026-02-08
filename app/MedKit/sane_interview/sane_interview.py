"""
sane_interview.py - SANE interview chatbot implementation

Interactive chatbot for conducting SANE interviews with trauma-informed approach.
Provides structured interview flow with proper consent handling and support resources.
"""

from sane_interview_models import (
    YesNoUnsure, SexualContactType, PainLevel,
    ConsentSection, MedicalHistory, IncidentHistory, SexualContactDetails,
    InjuryAssessment, ForensicEvidence, TreatmentDiscussion,
    PsychologicalAssessment, LegalFollowUp, ClosureSupport,
    SANEInterviewRecord
)
from typing import Optional, List, Any, Generator, Union
from dataclasses import dataclass

@dataclass
class Question:
    text: str
    type: str = "text"  # "text", "yes_no", "info"
    allow_skip: bool = True
    options: Optional[List[str]] = None
    explanation: Optional[str] = None

class SANEInterview:
    """
    SANE Interview logic controller.
    """
    
    def __init__(self):
        self.interview = SANEInterviewRecord()
        self._generator = self._interview_flow()
        self._current_question: Optional[Question] = None
        self._interview_complete = False

    def get_next_question(self, last_answer: str = None) -> Optional[Question]:
        """
        Get the next question in the interview flow.
        Pass the answer to the *previous* question as `last_answer`.
        """
        if self._interview_complete:
            return None

        try:
            if self._current_question is None:
                # Start the generator
                self._current_question = next(self._generator)
            else:
                # Send the answer to the generator
                self._current_question = self._generator.send(last_answer)
            
            return self._current_question
        except StopIteration:
            self._interview_complete = True
            return None

    def _parse_yes_no(self, response: str) -> YesNoUnsure:
        if not response:
            return YesNoUnsure.DECLINE
        response_lower = response.lower().strip()
        if response_lower in ['y', 'yes']:
            return YesNoUnsure.YES
        elif response_lower in ['n', 'no']:
            return YesNoUnsure.NO
        elif response_lower in ['u', 'unsure', 'not sure']:
            return YesNoUnsure.UNSURE
        elif response_lower == 'skip':
            return YesNoUnsure.DECLINE
        elif response_lower == 'explain':
            return YesNoUnsure.EXPLAIN
        else:
            return YesNoUnsure.DECLINE

    def _interview_flow(self) -> Generator[Question, str, None]:
        # 0. Setup
        yield from self.intro_questions()

        # 1. Consent
        if not (yield from self.consent_questions()):
             return # Stop if no consent

        # 2. Medical History
        yield from self.medical_history_questions()

        # 3. Incident History
        yield from self.incident_questions()

        # 4. Sexual Contact Details
        yield from self.sexual_contact_questions()

        # 5. Injury and Pain
        yield from self.injury_questions()

        # 6. Forensic Evidence
        yield from self.forensic_questions()

        # 7. Treatment
        yield from self.treatment_questions()

        # 8. Emotional Support
        yield from self.psychological_questions()

        # 9. Legal and Follow-Up
        yield from self.legal_questions()

        # 10. Closure
        yield from self.closure_questions()

    def intro_questions(self):
        interviewer = yield Question("Enter interviewer name:", allow_skip=False)
        self.interview.interviewer_name = interviewer
        
        patient_id = yield Question("Enter patient identifier (anonymous):", allow_skip=False)
        self.interview.patient_id = patient_id

    def consent_questions(self):
        yield Question("🩺 1. INTRODUCTION AND CONSENT\n" + "-" * 60 + "\n\nI want to make sure you understand your rights and what will happen today.", type="info")
        
        ans = yield Question(
            "Do you understand the purpose of this examination and your rights during the process?", 
            type="yes_no",
            explanation="The SANE exam is a specialized medical-forensic examination designed to provide you with medical care and to collect evidence if you choose to report the assault."
        )
        self.interview.consent.understands_purpose = self._parse_yes_no(ans)
        
        if self.interview.consent.understands_purpose == YesNoUnsure.NO:
            explanation_text = (
                "\nThe SANE (Sexual Assault Nurse Examiner) examination is a comprehensive medical-forensic evaluation. It includes:\n\n"
                "1. Medical Care: We will assess and treat any physical injuries you may have.\n"
                "2. Health Services: We can provide medications to prevent STIs (including HIV) and emergency contraception if needed.\n"
                "3. Evidence Collection: With your consent, we will collect forensic evidence (DNA, clothing, etc.) that can be used if you decide to involve the legal system.\n"
                "4. Documentation: We will carefully document your account of the event and any physical findings.\n"
                "5. Your Rights: This is YOUR exam. You have the right to:\n"
                "   - Consent to all, part, or none of the exam.\n"
                "   - Stop the exam at any time.\n"
                "   - Skip any question or procedure.\n"
                "   - Have a support person or advocate present.\n\n"
                "Everything we discuss and find is confidential within the limits of the law.\n"
                "\nPress Enter when you are ready to continue..."
            )
            yield Question(explanation_text, type="info")
            self.interview.consent.wants_explanation = YesNoUnsure.YES
        elif self.interview.consent.understands_purpose == YesNoUnsure.YES:
            self.interview.consent.wants_explanation = YesNoUnsure.NO
        else:
            # For UNSURE or DECLINE, ask if they want an explanation
            ans = yield Question("Would you like me to explain what will happen during the exam?", type="yes_no")
            self.interview.consent.wants_explanation = self._parse_yes_no(ans)
            
            if self.interview.consent.wants_explanation == YesNoUnsure.YES:
                explanation_text = (
                    "\nThe SANE (Sexual Assault Nurse Examiner) examination is a comprehensive medical-forensic evaluation. It includes:\n\n"
                    "1. Medical Care: We will assess and treat any physical injuries you may have.\n"
                    "2. Health Services: We can provide medications to prevent STIs (including HIV) and emergency contraception if needed.\n"
                    "3. Evidence Collection: With your consent, we will collect forensic evidence (DNA, clothing, etc.) that can be used if you decide to involve the legal system.\n"
                    "4. Documentation: We will carefully document your account of the event and any physical findings.\n"
                    "5. Your Rights: This is YOUR exam. You have the right to:\n"
                    "   - Consent to all, part, or none of the exam.\n"
                    "   - Stop the exam at any time.\n"
                    "   - Skip any question or procedure.\n"
                    "   - Have a support person or advocate present.\n\n"
                    "Everything we discuss and find is confidential within the limits of the law.\n"
                    "\nPress Enter when you are ready to continue..."
                )
                yield Question(explanation_text, type="info")
        
        ans = yield Question(
            "Do I have your permission to proceed with the medical examination?", 
            type="yes_no",
            explanation="Your consent is required for the exam to proceed. You can stop or skip any part of the exam at any time."
        )
        self.interview.consent.gives_permission = self._parse_yes_no(ans)
        
        if self.interview.consent.gives_permission != YesNoUnsure.YES:
            yield Question("\nRespecting your decision. You can take time to decide.\n⚠️  Exam cannot proceed without consent.", type="info")
            return False
        
        # Collect basic demographic information tactfully
        yield Question("\nTo provide the best medical care, I need to collect some basic information.", type="info")
        
        ans = yield Question(
            "May I ask your age? This helps me provide age-appropriate care and medications.", 
            type="yes_no",
            explanation="Age is important for determining appropriate medical treatments and dosages."
        )
        if self._parse_yes_no(ans) == YesNoUnsure.YES:
            ans = yield Question("What is your age in years?", allow_skip=False)
            if ans and ans.isdigit():
                self.interview.consent.age = int(ans)
        
        ans = yield Question(
            "May I ask your sex assigned at birth? This information is important for specific medical assessments and treatments.", 
            type="yes_no",
            explanation="Biological sex helps us determine appropriate medical care, screenings, and potential risks."
        )
        if self._parse_yes_no(ans) == YesNoUnsure.YES:
            ans = yield Question("What sex were you assigned at birth? (male, female, or intersex)", allow_skip=False)
            if ans:
                self.interview.consent.sex = ans.lower()
        
        ans = yield Question(
            "Do you identify as transgender or have a different gender identity than your sex assigned at birth?", 
            type="yes_no",
            explanation="This helps us provide respectful, inclusive care and understand your specific health needs."
        )
        if self._parse_yes_no(ans) == YesNoUnsure.YES:
            ans = yield Question("What gender identity do you identify with?")
            if ans:
                self.interview.consent.gender_identity = ans
        
        ans = yield Question("Is there anything you would like me to know before we start?")
        self.interview.consent.additional_information = ans
        
        ans = yield Question(
            "Would you like someone (advocate, friend, or family member) to be with you during the exam?", 
            type="yes_no",
            explanation="Having a support person can help you feel safer and more comfortable during the examination process."
        )
        self.interview.consent.wants_advocate_present = self._parse_yes_no(ans)
        
        if self.interview.consent.wants_advocate_present == YesNoUnsure.YES:
            ans = yield Question("What is their name?", allow_skip=False)
            self.interview.consent.advocate_name = ans
        
        return True

    def medical_history_questions(self):
        yield Question("\n👩‍⚕️ 2. GENERAL MEDICAL HISTORY\n" + "-" * 60, type="info")
        
        ans = yield Question("Do you have any medical conditions I should know about?")
        self.interview.medical_history.medical_conditions = ans
        
        ans = yield Question("Are you currently taking any medications?")
        self.interview.medical_history.current_medications = ans
        
        ans = yield Question("Do you have any allergies, particularly to medications or latex?")
        self.interview.medical_history.allergies = ans
        
        # Only ask menstrual and pregnancy questions if age is 12 or older, or if age is unknown
        patient_age = self.interview.consent.age
        if patient_age is None or patient_age >= 12:
            ans = yield Question("When was your last menstrual period?")
            self.interview.medical_history.last_menstrual_period = ans
            
            ans = yield Question("Have you ever been pregnant? If yes, how many times?")
            self.interview.medical_history.pregnancy_history = ans
            
            ans = yield Question("Are you currently pregnant or do you think you could be?", type="yes_no")
            self.interview.medical_history.currently_pregnant = self._parse_yes_no(ans)

    def incident_questions(self):
        yield Question("\n⚕️ 3. INCIDENT HISTORY\n" + "-" * 60 + "\nRemember: You may decline to answer any question.\n\nI need to ask you some questions about what happened.\nTake your time, and use your own words.", type="info")
        
        ans = yield Question(
            "Can you tell me, in your own words, what happened?",
            explanation="Your narrative helps us understand the context of the assault, which guides both your medical care and the collection of forensic evidence."
        )
        self.interview.incident_history.narrative = ans
        
        ans = yield Question("When did the assault occur? (date)")
        self.interview.incident_history.incident_date = ans
        
        ans = yield Question("What time did it occur? (approximate is fine)")
        self.interview.incident_history.incident_time = ans
        
        ans = yield Question("Where did it happen? (location, indoors/outdoors, bed, car, etc.)")
        self.interview.incident_history.location = ans
        
        ans = yield Question("Do you know the person(s) who hurt you?", type="yes_no")
        self.interview.incident_history.knows_assailant = self._parse_yes_no(ans)
        
        ans = yield Question("How many individuals were involved? (number)")
        if ans and ans.isdigit():
            self.interview.incident_history.number_of_individuals = int(ans)
        
        ans = yield Question(
            "Were any weapons used or threats made?", 
            type="yes_no",
            explanation="Information about weapons or threats is important for assessing your safety and for legal documentation of the assault."
        )
        self.interview.incident_history.weapons_used = self._parse_yes_no(ans)
        
        if self.interview.incident_history.weapons_used == YesNoUnsure.YES:
            ans = yield Question("Can you describe the weapon(s) or threats?")
            self.interview.incident_history.weapon_details = ans
        
        ans = yield Question("Were you physically restrained (hands, ropes, clothing, etc.)?", type="yes_no")
        self.interview.incident_history.physically_restrained = self._parse_yes_no(ans)
        
        if self.interview.incident_history.physically_restrained == YesNoUnsure.YES:
            ans = yield Question("How were you restrained?")
            self.interview.incident_history.restraint_details = ans
        
        ans = yield Question(
            "Did you lose consciousness at any point?", 
            type="yes_no",
            explanation="Loss of consciousness can indicate head trauma or the use of substances, which requires specific medical evaluation."
        )
        self.interview.incident_history.lost_consciousness = self._parse_yes_no(ans)
        
        ans = yield Question(
            "Were you forced to drink alcohol, take drugs, or any substances?", 
            type="yes_no",
            explanation="This helps us determine if toxicology testing is needed and if any substances might interact with medications we provide today."
        )
        self.interview.incident_history.forced_substances = self._parse_yes_no(ans)
        
        if self.interview.incident_history.forced_substances == YesNoUnsure.YES:
            ans = yield Question("What substances were involved?")
            self.interview.incident_history.substance_details = ans
        
        ans = yield Question("Were there any witnesses or anyone who helped afterward?", type="yes_no")
        self.interview.incident_history.witnesses = self._parse_yes_no(ans)
        
        if self.interview.incident_history.witnesses == YesNoUnsure.YES:
            ans = yield Question("Can you provide details about witnesses or helpers?")
            self.interview.incident_history.witness_details = ans

    def sexual_contact_questions(self):
        yield Question("\n🧬 4. SEXUAL CONTACT DETAILS\n" + "-" * 60 + "\nThese questions help us collect appropriate forensic evidence.\n", type="info")
        
        contact_response = yield Question(
            "What parts of your body were touched or penetrated? (vagina, mouth, anus/bottom, fingers, or other)",
            explanation="Knowing the specific types of contact helps us identify where to collect DNA evidence and where to check for potential injuries."
        )
        if contact_response and contact_response.lower() != "skip":
            types = []
            # Map simple terms to clinical enum
            if any(x in contact_response.lower() for x in ["vagina", "vaginal"]):
                types.append(SexualContactType.VAGINAL)
            if any(x in contact_response.lower() for x in ["mouth", "oral"]):
                types.append(SexualContactType.ORAL)
            if any(x in contact_response.lower() for x in ["anal", "anus", "bottom"]):
                types.append(SexualContactType.ANAL)
            if any(x in contact_response.lower() for x in ["digital", "finger", "hand"]):
                types.append(SexualContactType.DIGITAL)
            if "other" in contact_response.lower():
                types.append(SexualContactType.OTHER)
            self.interview.sexual_contact.contact_types = types if types else None
        
        ans = yield Question("Was a condom or any protection used?", type="yes_no")
        self.interview.sexual_contact.condom_used = self._parse_yes_no(ans)
        
        ans = yield Question(
            "Did the person finish (ejaculate)?", 
            type="yes_no",
            explanation="This information is critical for locating and collecting potential DNA evidence."
        )
        self.interview.sexual_contact.ejaculation_noted = self._parse_yes_no(ans)
        
        if self.interview.sexual_contact.ejaculation_noted == YesNoUnsure.YES:
            ans = yield Question("Where did this happen (on your body, clothes, etc.)?")
            self.interview.sexual_contact.ejaculation_location = ans
        
        ans = yield Question("Did the person use any object(s)?", type="yes_no")
        self.interview.sexual_contact.objects_used = self._parse_yes_no(ans)
        
        if self.interview.sexual_contact.objects_used == YesNoUnsure.YES:
            ans = yield Question("Can you describe the object(s)?")
            self.interview.sexual_contact.object_details = ans
        
        ans = yield Question("Were you able to resist?", type="yes_no")
        self.interview.sexual_contact.able_to_resist = self._parse_yes_no(ans)
        
        if self.interview.sexual_contact.able_to_resist == YesNoUnsure.YES:
            ans = yield Question("How did you resist?")
            self.interview.sexual_contact.resistance_details = ans
        
        ans = yield Question("Did the assailant remove or tear any of your clothing?", type="yes_no")
        self.interview.sexual_contact.clothing_removed_torn = self._parse_yes_no(ans)
        
        activities_response = yield Question("Since the incident, have you: bathed, changed clothes, urinated, eaten, or brushed teeth? (list all that apply)")
        if activities_response and activities_response.lower() != "skip":
            self.interview.sexual_contact.post_incident_activities = [
                act.strip() for act in activities_response.split(',')
            ]
        
        ans = yield Question("Have you cleaned or disposed of any items related to the incident?", type="yes_no")
        self.interview.sexual_contact.items_cleaned_disposed = self._parse_yes_no(ans)

    def injury_questions(self):
        yield Question("\n👁️ 5. INJURY AND PAIN ASSESSMENT\n" + "-" * 60, type="info")
        
        ans = yield Question("Do you have any pain right now?", type="yes_no")
        self.interview.injury_assessment.has_pain = self._parse_yes_no(ans)
        
        if self.interview.injury_assessment.has_pain == YesNoUnsure.YES:
            ans = yield Question("Where is the pain located?")
            self.interview.injury_assessment.pain_locations = ans
            
            pain_response = yield Question("How severe is the pain on a scale of 1-10? (1=minimal, 10=worst possible)")
            if pain_response and pain_response.isdigit():
                level = int(pain_response)
                if 0 <= level <= 10:
                    self.interview.injury_assessment.pain_level = level
        
        assault_response = yield Question("Did the person hit, slap, kick, bite, or strangle (choke) you? (list all that apply)")
        if assault_response and assault_response.lower() != "skip":
            self.interview.injury_assessment.physical_assault_types = [
                act.strip() for act in assault_response.split(',')
            ]
        
        ans = yield Question("Do you have any bruises, scratches, or bleeding? Please describe locations.")
        self.interview.injury_assessment.visible_injuries = ans
        
        symptoms_response = yield Question("Are you experiencing: dizziness, nausea, or headaches? (list all that apply)")
        if symptoms_response and symptoms_response.lower() != "skip":
            self.interview.injury_assessment.symptoms = [
                sym.strip() for sym in symptoms_response.split(',')
            ]
        
        ans = yield Question("Are you having pain, discharge, or bleeding in your private parts (genital or anal areas)?")
        self.interview.injury_assessment.genital_anal_symptoms = ans

    def forensic_questions(self):
        yield Question("\n🧫 6. FORENSIC EVIDENCE COLLECTION\n" + "-" * 60, type="info")
        
        ans = yield Question("Have you peed (urinated) since the incident?", type="yes_no")
        self.interview.forensic_evidence.urinated_since = self._parse_yes_no(ans)
        
        ans = yield Question("Have you had a bowel movement (pooped) since the incident?", type="yes_no")
        self.interview.forensic_evidence.defecated_since = self._parse_yes_no(ans)
        
        ans = yield Question("Have you changed pads or tampons since the incident?", type="yes_no")
        self.interview.forensic_evidence.changed_sanitary_products = self._parse_yes_no(ans)
        
        ans = yield Question("Have you eaten, drunk, or smoked since the incident?", type="yes_no")
        self.interview.forensic_evidence.eaten_drunk_smoked = self._parse_yes_no(ans)
        
        ans = yield Question("Did the person involved leave any items behind (hair, condom, tissues, etc.)?", type="yes_no")
        self.interview.forensic_evidence.items_left_behind = self._parse_yes_no(ans)
        
        if self.interview.forensic_evidence.items_left_behind == YesNoUnsure.YES:
            ans = yield Question("Can you describe the items?")
            self.interview.forensic_evidence.items_description = ans
        
        ans = yield Question("Are you wearing the same clothes from the assault?", type="yes_no")
        self.interview.forensic_evidence.wearing_same_clothes = self._parse_yes_no(ans)
        
        ans = yield Question("Would you like these items collected for evidence?", type="yes_no")
        self.interview.forensic_evidence.wants_items_collected = self._parse_yes_no(ans)

    def treatment_questions(self):
        yield Question("\n💊 7. PROPHYLAXIS AND TREATMENT DISCUSSION\n" + "-" * 60 + "\n\nWe can provide preventive treatment for infections and pregnancy.", type="info")
        
        ans = yield Question("Are you willing to take medication to prevent sexually transmitted infections (STIs)?", type="yes_no")
        self.interview.treatment.accepts_sti_prophylaxis = self._parse_yes_no(ans)
        
        ans = yield Question("Would you like emergency contraception (if applicable)?", type="yes_no")
        self.interview.treatment.wants_emergency_contraception = self._parse_yes_no(ans)
        
        ans = yield Question("Have you had a recent HIV test?", type="yes_no")
        self.interview.treatment.recent_hiv_test = self._parse_yes_no(ans)
        
        ans = yield Question("Would you like to have an HIV test now?", type="yes_no")
        self.interview.treatment.wants_hiv_test = self._parse_yes_no(ans)
        
        ans = yield Question("Do you have any concerns about medications or treatment options?")
        self.interview.treatment.medication_concerns = ans

    def psychological_questions(self):
        yield Question("\n🧠 8. EMOTIONAL AND PSYCHOLOGICAL ASSESSMENT\n" + "-" * 60, type="info")
        
        ans = yield Question("How are you feeling emotionally right now?")
        self.interview.psychological.current_emotional_state = ans
        
        ans = yield Question("Do you have someone you trust to talk to about this?", type="yes_no")
        self.interview.psychological.has_trusted_support = self._parse_yes_no(ans)
        
        if self.interview.psychological.has_trusted_support == YesNoUnsure.YES:
            ans = yield Question("Who is your support person?")
            self.interview.psychological.support_person_details = ans
        
        ans = yield Question("Have you ever experienced anything like this before?", type="yes_no")
        self.interview.psychological.previous_trauma = self._parse_yes_no(ans)
        
        ans = yield Question("Do you feel safe going home today?", type="yes_no")
        self.interview.psychological.feels_safe_going_home = self._parse_yes_no(ans)
        
        ans = yield Question("Would you like to speak with a counselor or advocate?", type="yes_no")
        self.interview.psychological.wants_counselor = self._parse_yes_no(ans)

    def legal_questions(self):
        yield Question("\n📄 9. LEGAL AND FOLLOW-UP QUESTIONS\n" + "-" * 60, type="info")
        
        ans = yield Question("Have you already reported this assault to the police?", type="yes_no")
        self.interview.legal_followup.reported_to_police = self._parse_yes_no(ans)
        
        ans = yield Question("Would you like me to explain how reporting works?", type="yes_no")
        self.interview.legal_followup.wants_reporting_explanation = self._parse_yes_no(ans)
        
        if self.interview.legal_followup.wants_reporting_explanation == YesNoUnsure.YES:
            reporting_text = (
                "\nThere are different ways to report what happened, and you have choices:\n\n"
                "1. Forensic Medical Report (Non-Reporting): In many areas, you can have a forensic exam and have the evidence stored (for a certain period) without immediately reporting to the police. This gives you time to decide.\n"
                "2. Police Report: You can choose to report to law enforcement. They will begin an investigation, and the evidence collected during this exam will be used in that process.\n"
                "3. Anonymous/Jane Doe Report: Some jurisdictions allow for reporting without providing your name initially.\n\n"
                "Regardless of your choice, you are entitled to medical care. Choosing not to report today does not mean you cannot report later, though evidence is best collected as soon as possible.\n"
                "\nPress Enter when you are ready to continue..."
            )
            yield Question(reporting_text, type="info")
        
        ans = yield Question("Do you want forensic evidence collected even if you're undecided about reporting?", type="yes_no")
        self.interview.legal_followup.wants_evidence_collected = self._parse_yes_no(ans)
        
        ans = yield Question("Can we contact you for follow-up medical results?", type="yes_no")
        self.interview.legal_followup.contact_for_followup = self._parse_yes_no(ans)
        
        if self.interview.legal_followup.contact_for_followup == YesNoUnsure.YES:
            ans = yield Question("What is the best way to contact you? (phone/email)", allow_skip=False)
            self.interview.legal_followup.contact_information = ans
        
        ans = yield Question("Do you need help with transportation tonight?", type="yes_no")
        self.interview.legal_followup.needs_transportation = self._parse_yes_no(ans)
        
        ans = yield Question("Do you need help with safe housing tonight?", type="yes_no")
        self.interview.legal_followup.needs_safe_housing = self._parse_yes_no(ans)

    def closure_questions(self):
        yield Question("\n🩹 10. CLOSURE AND SUPPORT\n" + "-" * 60, type="info")
        
        ans = yield Question("Do you have any questions or concerns before we finish?")
        self.interview.closure.additional_questions = ans
        
        ans = yield Question("Would you like me to review your next steps (medical, legal, counseling)?", type="yes_no")
        self.interview.closure.wants_next_steps_review = self._parse_yes_no(ans)
        
        if self.interview.closure.wants_next_steps_review == YesNoUnsure.YES:
            review_text = (
                "\nLet's review the next steps for your care:\n\n"
                "1. Medical Follow-up: We recommend seeing your primary care provider or a clinic in 1-2 weeks to follow up on any injuries or medications.\n"
                "2. STI Testing: Some tests may need to be repeated in a few weeks or months.\n"
                "3. Support Services: We have provided contact information for local advocacy groups and counseling services. They can help with the emotional impact and guide you through the next steps.\n"
                "4. Evidence: If evidence was collected, it will be handled according to legal protocols.\n"
                "5. Safety: Please ensure you have a safe place to go today. If you don't feel safe, we can help you find emergency housing.\n\n"
                "Do you have any questions about these steps?\n"
                "\nPress Enter when review is complete..."
            )
            yield Question(review_text, type="info")
        
        ans = yield Question("I have resources and hotlines you can contact for help. Would you like me to explain them?", type="yes_no")
        self.interview.closure.wants_resources_explained = self._parse_yes_no(ans)
        
        if self.interview.closure.wants_resources_explained == YesNoUnsure.YES:
            yield Question("\n📞 IMPORTANT RESOURCES:\n• National Sexual Assault Hotline: 1-800-656-HOPE (4673)\n• Crisis Text Line: Text HOME to 741741\n• RAINN Online Chat: www.rainn.org\n• National Domestic Violence Hotline: 1-800-799-7233\nPress Enter to continue...", type="info")
