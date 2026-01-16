from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class YesNoUnsure(str, Enum):
    YES = "yes"
    NO = "no"
    UNSURE = "unsure"
    DECLINE = "decline_to_answer"


class SexualContactType(str, Enum):
    VAGINAL = "vaginal"
    ORAL = "oral"
    ANAL = "anal"
    DIGITAL = "digital"
    OTHER = "other"


class PainLevel(int, Enum):
    NONE = 0
    MINIMAL = 1
    MILD = 3
    MODERATE = 5
    SEVERE = 7
    WORST = 10


# 1. Introduction and Consent
class ConsentSection(BaseModel):
    understands_purpose: Optional[YesNoUnsure] = None
    wants_explanation: Optional[YesNoUnsure] = None
    gives_permission: Optional[YesNoUnsure] = None
    additional_information: Optional[str] = None
    wants_advocate_present: Optional[YesNoUnsure] = None
    advocate_name: Optional[str] = None


# 2. General Medical History
class MedicalHistory(BaseModel):
    medical_conditions: Optional[str] = None
    current_medications: Optional[str] = None
    allergies: Optional[str] = None
    last_menstrual_period: Optional[str] = None
    pregnancy_history: Optional[str] = None
    currently_pregnant: Optional[YesNoUnsure] = None


# 3. Incident History
class IncidentHistory(BaseModel):
    narrative: Optional[str] = Field(None, description="Survivor's own words")
    incident_date: Optional[str] = None
    incident_time: Optional[str] = None
    location: Optional[str] = None
    knows_assailant: Optional[YesNoUnsure] = None
    number_of_individuals: Optional[int] = None
    weapons_used: Optional[YesNoUnsure] = None
    weapon_details: Optional[str] = None
    physically_restrained: Optional[YesNoUnsure] = None
    restraint_details: Optional[str] = None
    lost_consciousness: Optional[YesNoUnsure] = None
    forced_substances: Optional[YesNoUnsure] = None
    substance_details: Optional[str] = None
    witnesses: Optional[YesNoUnsure] = None
    witness_details: Optional[str] = None


# 4. Sexual Contact Details
class SexualContactDetails(BaseModel):
    contact_types: Optional[List[SexualContactType]] = None
    condom_used: Optional[YesNoUnsure] = None
    ejaculation_noted: Optional[YesNoUnsure] = None
    ejaculation_location: Optional[str] = None
    objects_used: Optional[YesNoUnsure] = None
    object_details: Optional[str] = None
    able_to_resist: Optional[YesNoUnsure] = None
    resistance_details: Optional[str] = None
    clothing_removed_torn: Optional[YesNoUnsure] = None
    post_incident_activities: Optional[List[str]] = Field(
        None, 
        description="bathed, changed clothes, urinated, eaten, brushed teeth, etc."
    )
    items_cleaned_disposed: Optional[YesNoUnsure] = None


# 5. Injury and Pain Assessment
class InjuryAssessment(BaseModel):
    has_pain: Optional[YesNoUnsure] = None
    pain_locations: Optional[str] = None
    pain_level: Optional[int] = Field(None, ge=0, le=10)
    physical_assault_types: Optional[List[str]] = Field(
        None,
        description="hit, slap, kick, bite, strangle, etc."
    )
    visible_injuries: Optional[str] = None
    symptoms: Optional[List[str]] = Field(
        None,
        description="dizzy, nauseous, headache, etc."
    )
    genital_anal_symptoms: Optional[str] = None


# 6. Forensic Evidence Collection
class ForensicEvidence(BaseModel):
    urinated_since: Optional[YesNoUnsure] = None
    defecated_since: Optional[YesNoUnsure] = None
    changed_sanitary_products: Optional[YesNoUnsure] = None
    eaten_drunk_smoked: Optional[YesNoUnsure] = None
    items_left_behind: Optional[YesNoUnsure] = None
    items_description: Optional[str] = None
    wearing_same_clothes: Optional[YesNoUnsure] = None
    wants_items_collected: Optional[YesNoUnsure] = None


# 7. Prophylaxis and Treatment
class TreatmentDiscussion(BaseModel):
    accepts_sti_prophylaxis: Optional[YesNoUnsure] = None
    wants_emergency_contraception: Optional[YesNoUnsure] = None
    recent_hiv_test: Optional[YesNoUnsure] = None
    wants_hiv_test: Optional[YesNoUnsure] = None
    medication_concerns: Optional[str] = None


# 8. Emotional and Psychological Assessment
class PsychologicalAssessment(BaseModel):
    current_emotional_state: Optional[str] = None
    has_trusted_support: Optional[YesNoUnsure] = None
    support_person_details: Optional[str] = None
    previous_trauma: Optional[YesNoUnsure] = None
    feels_safe_going_home: Optional[YesNoUnsure] = None
    wants_counselor: Optional[YesNoUnsure] = None


# 9. Legal and Follow-Up
class LegalFollowUp(BaseModel):
    reported_to_police: Optional[YesNoUnsure] = None
    wants_reporting_explanation: Optional[YesNoUnsure] = None
    wants_evidence_collected: Optional[YesNoUnsure] = None
    contact_for_followup: Optional[YesNoUnsure] = None
    contact_information: Optional[str] = None
    needs_transportation: Optional[YesNoUnsure] = None
    needs_safe_housing: Optional[YesNoUnsure] = None


# 10. Closure and Support
class ClosureSupport(BaseModel):
    additional_questions: Optional[str] = None
    wants_next_steps_review: Optional[YesNoUnsure] = None
    wants_resources_explained: Optional[YesNoUnsure] = None


# Complete Interview Record
class SANEInterview(BaseModel):
    interview_date: datetime = Field(default_factory=datetime.now)
    interviewer_name: Optional[str] = None
    patient_id: Optional[str] = Field(None, description="Use anonymous identifier")
    
    consent: ConsentSection = Field(default_factory=ConsentSection)
    medical_history: MedicalHistory = Field(default_factory=MedicalHistory)
    incident_history: IncidentHistory = Field(default_factory=IncidentHistory)
    sexual_contact: SexualContactDetails = Field(default_factory=SexualContactDetails)
    injury_assessment: InjuryAssessment = Field(default_factory=InjuryAssessment)
    forensic_evidence: ForensicEvidence = Field(default_factory=ForensicEvidence)
    treatment: TreatmentDiscussion = Field(default_factory=TreatmentDiscussion)
    psychological: PsychologicalAssessment = Field(default_factory=PsychologicalAssessment)
    legal_followup: LegalFollowUp = Field(default_factory=LegalFollowUp)
    closure: ClosureSupport = Field(default_factory=ClosureSupport)
    
    additional_notes: Optional[str] = None


class SANEInterviewChatbot:
    """
    Interactive chatbot for conducting SANE interviews with trauma-informed approach
    """
    
    def __init__(self):
        self.interview = SANEInterview()
        self.current_section = 0
        self.sections = [
            ("Consent and Introduction", self.consent_questions),
            ("Medical History", self.medical_history_questions),
            ("Incident History", self.incident_questions),
            ("Sexual Contact Details", self.sexual_contact_questions),
            ("Injury and Pain Assessment", self.injury_questions),
            ("Forensic Evidence Collection", self.forensic_questions),
            ("Treatment Discussion", self.treatment_questions),
            ("Emotional Support", self.psychological_questions),
            ("Legal and Follow-Up", self.legal_questions),
            ("Closure and Resources", self.closure_questions)
        ]
    
    def display_header(self):
        print("\n" + "="*60)
        print("🩺 SANE INTERVIEW SYSTEM")
        print("Sexual Assault Nurse Examiner - Trauma-Informed Interview")
        print("="*60)
        print("\nKey Principles:")
        print("• Patient has the right to decline any question")
        print("• Maintain nonjudgmental, supportive tone")
        print("• Document exact words when possible")
        print("• Allow pauses and breaks as needed")
        print("="*60 + "\n")
    
    def get_response(self, question: str, allow_decline: bool = True) -> str:
        """Get response with option to decline"""
        print(f"\n{question}")
        if allow_decline:
            print("(Type 'skip' to decline answering)")
        response = input("Response: ").strip()
        return response if response.lower() != 'skip' else "decline_to_answer"
    
    def get_yes_no(self, question: str) -> YesNoUnsure:
        """Get yes/no/unsure response"""
        response = self.get_response(f"{question} (yes/no/unsure)")
        response_lower = response.lower()
        if response_lower in ['y', 'yes']:
            return YesNoUnsure.YES
        elif response_lower in ['n', 'no']:
            return YesNoUnsure.NO
        elif response_lower in ['u', 'unsure', 'not sure']:
            return YesNoUnsure.UNSURE
        else:
            return YesNoUnsure.DECLINE
    
    def consent_questions(self):
        print("\n🩺 1. INTRODUCTION AND CONSENT")
        print("-" * 60)
        
        print("\nI want to make sure you understand your rights and what will happen today.")
        self.interview.consent.understands_purpose = self.get_yes_no(
            "Do you understand the purpose of this examination and your rights during the process?"
        )
        
        self.interview.consent.wants_explanation = self.get_yes_no(
            "Would you like me to explain what will happen during the exam?"
        )
        
        if self.interview.consent.wants_explanation == YesNoUnsure.YES:
            print("\n[Provide detailed explanation of examination process]")
            input("Press Enter when explanation is complete...")
        
        self.interview.consent.gives_permission = self.get_yes_no(
            "Do I have your permission to proceed with the medical examination?"
        )
        
        if self.interview.consent.gives_permission != YesNoUnsure.YES:
            print("\nRespecting your decision. You can take time to decide.")
            return False
        
        self.interview.consent.additional_information = self.get_response(
            "Is there anything you would like me to know before we start?"
        )
        
        self.interview.consent.wants_advocate_present = self.get_yes_no(
            "Would you like someone (advocate, friend, or family member) to be with you during the exam?"
        )
        
        if self.interview.consent.wants_advocate_present == YesNoUnsure.YES:
            self.interview.consent.advocate_name = self.get_response(
                "What is their name?", allow_decline=False
            )
        
        return True
    
    def medical_history_questions(self):
        print("\n👩‍⚕️ 2. GENERAL MEDICAL HISTORY")
        print("-" * 60)
        
        self.interview.medical_history.medical_conditions = self.get_response(
            "Do you have any medical conditions I should know about?"
        )
        
        self.interview.medical_history.current_medications = self.get_response(
            "Are you currently taking any medications or using birth control?"
        )
        
        self.interview.medical_history.allergies = self.get_response(
            "Do you have any allergies, particularly to medications or latex?"
        )
        
        self.interview.medical_history.last_menstrual_period = self.get_response(
            "When was your last menstrual period?"
        )
        
        self.interview.medical_history.pregnancy_history = self.get_response(
            "Have you ever been pregnant? If yes, how many times?"
        )
        
        self.interview.medical_history.currently_pregnant = self.get_yes_no(
            "Are you currently pregnant or do you think you could be?"
        )
    
    def incident_questions(self):
        print("\n⚕️ 3. INCIDENT HISTORY")
        print("-" * 60)
        print("Remember: You may decline to answer any question.\n")
        
        print("I need to ask you some questions about what happened.")
        print("Take your time, and use your own words.")
        self.interview.incident_history.narrative = self.get_response(
            "Can you tell me, in your own words, what happened?"
        )
        
        self.interview.incident_history.incident_date = self.get_response(
            "When did the assault occur? (date)"
        )
        
        self.interview.incident_history.incident_time = self.get_response(
            "What time did it occur? (approximate is fine)"
        )
        
        self.interview.incident_history.location = self.get_response(
            "Where did it happen? (location, indoors/outdoors, bed, car, etc.)"
        )
        
        self.interview.incident_history.knows_assailant = self.get_yes_no(
            "Do you know the person(s) who assaulted you?"
        )
        
        num_response = self.get_response(
            "How many individuals were involved? (number)"
        )
        if num_response.isdigit():
            self.interview.incident_history.number_of_individuals = int(num_response)
        
        self.interview.incident_history.weapons_used = self.get_yes_no(
            "Were any weapons used or threats made?"
        )
        
        if self.interview.incident_history.weapons_used == YesNoUnsure.YES:
            self.interview.incident_history.weapon_details = self.get_response(
                "Can you describe the weapon(s) or threats?"
            )
        
        self.interview.incident_history.physically_restrained = self.get_yes_no(
            "Were you physically restrained (hands, ropes, clothing, etc.)?"
        )
        
        if self.interview.incident_history.physically_restrained == YesNoUnsure.YES:
            self.interview.incident_history.restraint_details = self.get_response(
                "How were you restrained?"
            )
        
        self.interview.incident_history.lost_consciousness = self.get_yes_no(
            "Did you lose consciousness at any point?"
        )
        
        self.interview.incident_history.forced_substances = self.get_yes_no(
            "Were you forced to drink alcohol, take drugs, or any substances?"
        )
        
        if self.interview.incident_history.forced_substances == YesNoUnsure.YES:
            self.interview.incident_history.substance_details = self.get_response(
                "What substances were involved?"
            )
        
        self.interview.incident_history.witnesses = self.get_yes_no(
            "Were there any witnesses or anyone who helped afterward?"
        )
        
        if self.interview.incident_history.witnesses == YesNoUnsure.YES:
            self.interview.incident_history.witness_details = self.get_response(
                "Can you provide details about witnesses or helpers?"
            )
    
    def sexual_contact_questions(self):
        print("\n🧬 4. SEXUAL CONTACT DETAILS")
        print("-" * 60)
        print("These questions help us collect appropriate forensic evidence.\n")
        
        contact_response = self.get_response(
            "What type(s) of sexual contact occurred? (vaginal, oral, anal, digital, other)"
        )
        if contact_response != "decline_to_answer":
            types = []
            if "vaginal" in contact_response.lower():
                types.append(SexualContactType.VAGINAL)
            if "oral" in contact_response.lower():
                types.append(SexualContactType.ORAL)
            if "anal" in contact_response.lower():
                types.append(SexualContactType.ANAL)
            if "digital" in contact_response.lower():
                types.append(SexualContactType.DIGITAL)
            if "other" in contact_response.lower():
                types.append(SexualContactType.OTHER)
            self.interview.sexual_contact.contact_types = types if types else None
        
        self.interview.sexual_contact.condom_used = self.get_yes_no(
            "Was a condom or any barrier used?"
        )
        
        self.interview.sexual_contact.ejaculation_noted = self.get_yes_no(
            "Was ejaculation noted?"
        )
        
        if self.interview.sexual_contact.ejaculation_noted == YesNoUnsure.YES:
            self.interview.sexual_contact.ejaculation_location = self.get_response(
                "Where did ejaculation occur?"
            )
        
        self.interview.sexual_contact.objects_used = self.get_yes_no(
            "Did the assailant use any object(s)?"
        )
        
        if self.interview.sexual_contact.objects_used == YesNoUnsure.YES:
            self.interview.sexual_contact.object_details = self.get_response(
                "Can you describe the object(s)?"
            )
        
        self.interview.sexual_contact.able_to_resist = self.get_yes_no(
            "Were you able to resist?"
        )
        
        if self.interview.sexual_contact.able_to_resist == YesNoUnsure.YES:
            self.interview.sexual_contact.resistance_details = self.get_response(
                "How did you resist?"
            )
        
        self.interview.sexual_contact.clothing_removed_torn = self.get_yes_no(
            "Did the assailant remove or tear any of your clothing?"
        )
        
        activities_response = self.get_response(
            "Since the incident, have you: bathed, changed clothes, urinated, eaten, or brushed teeth? (list all that apply)"
        )
        if activities_response != "decline_to_answer":
            self.interview.sexual_contact.post_incident_activities = [
                act.strip() for act in activities_response.split(',')
            ]
        
        self.interview.sexual_contact.items_cleaned_disposed = self.get_yes_no(
            "Have you cleaned or disposed of any items related to the incident?"
        )
    
    def injury_questions(self):
        print("\n👁️ 5. INJURY AND PAIN ASSESSMENT")
        print("-" * 60)
        
        self.interview.injury_assessment.has_pain = self.get_yes_no(
            "Do you have any pain right now?"
        )
        
        if self.interview.injury_assessment.has_pain == YesNoUnsure.YES:
            self.interview.injury_assessment.pain_locations = self.get_response(
                "Where is the pain located?"
            )
            
            pain_response = self.get_response(
                "How severe is the pain on a scale of 1-10? (1=minimal, 10=worst possible)"
            )
            if pain_response.isdigit():
                level = int(pain_response)
                if 0 <= level <= 10:
                    self.interview.injury_assessment.pain_level = level
        
        assault_response = self.get_response(
            "Did the assailant hit, slap, kick, bite, or strangle you? (list all that apply)"
        )
        if assault_response != "decline_to_answer":
            self.interview.injury_assessment.physical_assault_types = [
                act.strip() for act in assault_response.split(',')
            ]
        
        self.interview.injury_assessment.visible_injuries = self.get_response(
            "Do you have any bruises, scratches, or bleeding? Please describe locations."
        )
        
        symptoms_response = self.get_response(
            "Are you experiencing: dizziness, nausea, or headaches? (list all that apply)"
        )
        if symptoms_response != "decline_to_answer":
            self.interview.injury_assessment.symptoms = [
                sym.strip() for sym in symptoms_response.split(',')
            ]
        
        self.interview.injury_assessment.genital_anal_symptoms = self.get_response(
            "Are you experiencing pain, discharge, or bleeding in genital or anal areas?"
        )
    
    def forensic_questions(self):
        print("\n🧫 6. FORENSIC EVIDENCE COLLECTION")
        print("-" * 60)
        
        self.interview.forensic_evidence.urinated_since = self.get_yes_no(
            "Have you urinated since the assault?"
        )
        
        self.interview.forensic_evidence.defecated_since = self.get_yes_no(
            "Have you defecated since the assault?"
        )
        
        self.interview.forensic_evidence.changed_sanitary_products = self.get_yes_no(
            "Have you changed sanitary products since the assault?"
        )
        
        self.interview.forensic_evidence.eaten_drunk_smoked = self.get_yes_no(
            "Have you eaten, drunk, or smoked since the incident?"
        )
        
        self.interview.forensic_evidence.items_left_behind = self.get_yes_no(
            "Did the assailant leave any items behind (hair, condom, tissues, etc.)?"
        )
        
        if self.interview.forensic_evidence.items_left_behind == YesNoUnsure.YES:
            self.interview.forensic_evidence.items_description = self.get_response(
                "Can you describe the items?"
            )
        
        self.interview.forensic_evidence.wearing_same_clothes = self.get_yes_no(
            "Are you wearing the same clothes from the assault?"
        )
        
        self.interview.forensic_evidence.wants_items_collected = self.get_yes_no(
            "Would you like these items collected for evidence?"
        )
    
    def treatment_questions(self):
        print("\n💊 7. PROPHYLAXIS AND TREATMENT DISCUSSION")
        print("-" * 60)
        
        print("\nWe can provide preventive treatment for infections and pregnancy.")
        
        self.interview.treatment.accepts_sti_prophylaxis = self.get_yes_no(
            "Are you willing to take medication to prevent sexually transmitted infections (STIs)?"
        )
        
        self.interview.treatment.wants_emergency_contraception = self.get_yes_no(
            "Would you like emergency contraception (if applicable)?"
        )
        
        self.interview.treatment.recent_hiv_test = self.get_yes_no(
            "Have you had a recent HIV test?"
        )
        
        self.interview.treatment.wants_hiv_test = self.get_yes_no(
            "Would you like to have an HIV test now?"
        )
        
        self.interview.treatment.medication_concerns = self.get_response(
            "Do you have any concerns about medications or treatment options?"
        )
    
    def psychological_questions(self):
        print("\n🧠 8. EMOTIONAL AND PSYCHOLOGICAL ASSESSMENT")
        print("-" * 60)
        
        self.interview.psychological.current_emotional_state = self.get_response(
            "How are you feeling emotionally right now?"
        )
        
        self.interview.psychological.has_trusted_support = self.get_yes_no(
            "Do you have someone you trust to talk to about this?"
        )
        
        if self.interview.psychological.has_trusted_support == YesNoUnsure.YES:
            self.interview.psychological.support_person_details = self.get_response(
                "Who is your support person?"
            )
        
        self.interview.psychological.previous_trauma = self.get_yes_no(
            "Have you ever experienced anything like this before?"
        )
        
        self.interview.psychological.feels_safe_going_home = self.get_yes_no(
            "Do you feel safe going home today?"
        )
        
        self.interview.psychological.wants_counselor = self.get_yes_no(
            "Would you like to speak with a counselor or advocate?"
        )
    
    def legal_questions(self):
        print("\n📄 9. LEGAL AND FOLLOW-UP QUESTIONS")
        print("-" * 60)
        
        self.interview.legal_followup.reported_to_police = self.get_yes_no(
            "Have you already reported this assault to the police?"
        )
        
        self.interview.legal_followup.wants_reporting_explanation = self.get_yes_no(
            "Would you like me to explain how reporting works?"
        )
        
        if self.interview.legal_followup.wants_reporting_explanation == YesNoUnsure.YES:
            print("\n[Provide explanation of reporting process]")
            input("Press Enter when explanation is complete...")
        
        self.interview.legal_followup.wants_evidence_collected = self.get_yes_no(
            "Do you want forensic evidence collected even if you're undecided about reporting?"
        )
        
        self.interview.legal_followup.contact_for_followup = self.get_yes_no(
            "Can we contact you for follow-up medical results?"
        )
        
        if self.interview.legal_followup.contact_for_followup == YesNoUnsure.YES:
            self.interview.legal_followup.contact_information = self.get_response(
                "What is the best way to contact you? (phone/email)", allow_decline=False
            )
        
        self.interview.legal_followup.needs_transportation = self.get_yes_no(
            "Do you need help with transportation tonight?"
        )
        
        self.interview.legal_followup.needs_safe_housing = self.get_yes_no(
            "Do you need help with safe housing tonight?"
        )
    
    def closure_questions(self):
        print("\n🩹 10. CLOSURE AND SUPPORT")
        print("-" * 60)
        
        self.interview.closure.additional_questions = self.get_response(
            "Do you have any questions or concerns before we finish?"
        )
        
        self.interview.closure.wants_next_steps_review = self.get_yes_no(
            "Would you like me to review your next steps (medical, legal, counseling)?"
        )
        
        if self.interview.closure.wants_next_steps_review == YesNoUnsure.YES:
            print("\n[Review next steps with patient]")
            input("Press Enter when review is complete...")
        
        self.interview.closure.wants_resources_explained = self.get_yes_no(
            "I have resources and hotlines you can contact for help. Would you like me to explain them?"
        )
        
        if self.interview.closure.wants_resources_explained == YesNoUnsure.YES:
            print("\n📞 IMPORTANT RESOURCES:")
            print("• National Sexual Assault Hotline: 1-800-656-HOPE (4673)")
            print("• Crisis Text Line: Text HOME to 741741")
            print("• RAINN Online Chat: www.rainn.org")
            print("• National Domestic Violence Hotline: 1-800-799-7233")
            input("\nPress Enter to continue...")
    
    def conduct_interview(self):
        """Run the complete interview process"""
        self.display_header()
        
        interviewer = input("Enter interviewer name: ").strip()
        self.interview.interviewer_name = interviewer
        
        patient_id = input("Enter patient identifier (anonymous): ").strip()
        self.interview.patient_id = patient_id
        
        for section_name, section_func in self.sections:
            print(f"\n{'='*60}")
            result = section_func()
            
            # Check if consent was declined
            if section_name == "Consent and Introduction" and result is False:
                print("\n⚠️  Exam cannot proceed without consent.")
                return None
            
            cont = input("\nContinue to next section? (yes/no): ").strip().lower()
            if cont not in ['y', 'yes', '']:
                print("\nInterview paused. Patient needs break.")
                break
        
        print("\n" + "="*60)
        print("✅ INTERVIEW COMPLETE")
        print("="*60)
        
        return self.interview
    
    def save_interview(self, filename: str = "interview_record.json"):
        """Save interview to JSON file"""
        with open(filename, 'w') as f:
            f.write(self.interview.model_dump_json(indent=2))
        print(f"\n💾 Interview saved to {filename}")


def cli():
    """Main entry point"""
    chatbot = SANEInterviewChatbot()
    
    try:
        interview = chatbot.conduct_interview()
        
        if interview:
            save = input("\nWould you like to save this interview record? (yes/no): ").strip().lower()
            if save in ['y', 'yes']:
                filename = input("Enter filename (default: interview_record.json): ").strip()
                if not filename:
                    filename = "interview_record.json"
                chatbot.save_interview(filename)
                print("\n✅ Interview record saved successfully.")
            
            print("\n🙏 Thank you for your courage and trust.")
            print("Remember: This was not your fault.")
            print("Support is available 24/7.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interview interrupted by user.")
        print("Patient safety is priority. Provide immediate support.")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        print("Ensure patient safety and wellbeing first.")


if __name__ == "__main__":
    cli()
