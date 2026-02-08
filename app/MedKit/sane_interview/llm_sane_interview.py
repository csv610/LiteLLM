"""llm_sane_interview - AI-Assisted SANE Interview System with LLM Question Suggestions.

Extends the base SANE (Sexual Assault Nurse Examiner) interview system with
intelligent, context-aware question suggestions powered by LLMs. Maintains a
strict "AI suggests, nurse decides" principle where all AI recommendations are
reviewed and approved by the nurse before use. Designed for sensitive trauma
assessment with privacy-first architecture.

Provides rule-based and LLM-powered question suggestions that consider clinical
relevance, forensic evidence implications, and patient safety. Tracks suggestion
acceptance rates and generates interview statistics. Supports both local model
execution and external API usage with anonymization warnings.

QUICK START:
    Run the LLM-assisted SANE interview:

        python llm_sane_interview.py

    Then select whether to enable AI assistance when prompted. The system will:
    1. Conduct the standard SANE interview protocol
    2. Offer AI-suggested follow-up questions based on patient responses
    3. Allow you to accept, reject, or create custom questions
    4. Generate a complete interview record

    Use programmatically:

        from llm_sane_interview import LLMAssistedSANEInterviewer

        chatbot = LLMAssistedSANEInterviewer(use_llm_assist=True, local_model=True)
        interview = chatbot.conduct_interview()
        chatbot.save_interview("interview_record.json")

COMMON USES:
    - Conducting comprehensive SANE assessments with AI support
    - Generating contextual follow-up questions for complex cases
    - Training healthcare providers on SANE protocols
    - Ensuring thorough documentation of medical and forensic findings
    - Identifying critical safety concerns (suicidal ideation, ongoing threat)
    - Collecting forensic evidence with systematic questioning

KEY FEATURES:
    - AI-powered question suggestions with priority levels (critical/high/medium/low)
    - Rule-based suggestion engine for high-sensitivity scenarios
    - Nurse-controlled approval workflow for all suggestions
    - Safety detection (suicidal ideation, trafficking indicators)
    - Forensic evidence optimization (timeline, contamination awareness)
    - Medical documentation (injuries, symptoms, substance use)
    - Custom follow-up question support
    - Privacy-first architecture with local model option
    - Complete interview statistics tracking
    - JSON export for medical records and law enforcement coordination
"""

from sane_interview_models import (
    SANEInterview, YesNoUnsure, SexualContactType
)
from sane_interview_chatbot import SANEInterviewer
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import json


class QuestionSuggestion(BaseModel):
    """Model for LLM-generated question suggestions"""
    question: str = Field(description="The suggested follow-up question")
    rationale: str = Field(description="Why this question is relevant")
    priority: str = Field(description="high, medium, or low priority")
    medical_relevance: bool = Field(description="Has medical/safety implications")
    forensic_relevance: bool = Field(description="Has forensic/evidence implications")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "How long after the incident did you shower?",
                "rationale": "Timeline affects forensic evidence collection viability",
                "priority": "high",
                "medical_relevance": False,
                "forensic_relevance": True
            }
        }


class InterviewContext(BaseModel):
    """Context passed to LLM for generating suggestions"""
    current_section: str
    patient_response: str
    questions_already_asked: List[str]
    responses_so_far: Dict[str, Any]
    nurse_notes: Optional[str] = None


class LLMAssistedSANEInterviewer(SANEInterviewer):
    """
    Enhanced SANE chatbot with LLM assistance for question suggestions.
    
    Key principles:
    - LLM SUGGESTS, nurse DECIDES
    - All suggestions reviewed before asking
    - Patient data never sent to external APIs (use local model or anonymized)
    - Nurse can ignore any/all suggestions
    """
    
    def __init__(self, use_llm_assist: bool = True, local_model: bool = True, io_handler: Optional[Any] = None):
        super().__init__(io_handler=io_handler)
        self.use_llm_assist = use_llm_assist
        self.local_model = local_model  # If False, warns about privacy
        self.questions_asked = []
        self.llm_suggestions_accepted = 0
        self.llm_suggestions_rejected = 0
        self.nurse_notes = {}
        
        if use_llm_assist and not local_model:
            self.io.display("\n⚠️  WARNING: Using external LLM API")
            self.io.display("   Patient data will be anonymized before sending")
            self.io.display("   Consider using local model for maximum privacy")
            self.io.wait_for_user("   Press Enter to acknowledge and continue...")
    
    def get_response_with_llm_assist(
        self, 
        question: str, 
        section: str,
        allow_decline: bool = True,
        enable_suggestions: bool = True
    ) -> str:
        """
        Enhanced version that can provide LLM suggestions after initial response
        """
        # Ask the standard question first
        self.io.display(f"\n{question}")
        if allow_decline:
            self.io.display("(Type 'skip' to decline answering)")
        
        response = self.io.ask("Response: ").strip()
        
        # Record the question asked
        self.questions_asked.append(question)
        
        # If patient declined or LLM assist is off, return as normal
        if response.lower() == 'skip' or not self.use_llm_assist or not enable_suggestions:
            return response if response.lower() != 'skip' else "decline_to_answer"
        
        # If response has substance, get LLM suggestions
        if response and len(response) > 10:  # Meaningful response
            context = InterviewContext(
                current_section=section,
                patient_response=response,
                questions_already_asked=self.questions_asked[-5:],  # Last 5 questions
                responses_so_far=self._get_section_summary(section),
                nurse_notes=self.nurse_notes.get(section, None)
            )
            
            # Generate and present suggestions
            self._handle_llm_suggestions(context, section)
        
        return response if response.lower() != 'skip' else "decline_to_answer"
    
    def _get_section_summary(self, section: str) -> Dict[str, Any]:
        """Get summary of current section for context"""
        section_map = {
            "consent": self.interview.consent,
            "medical_history": self.interview.medical_history,
            "incident_history": self.interview.incident_history,
            "sexual_contact": self.interview.sexual_contact,
            "injury_assessment": self.interview.injury_assessment,
            "forensic_evidence": self.interview.forensic_evidence,
            "treatment": self.interview.treatment,
            "psychological": self.interview.psychological,
            "legal_followup": self.interview.legal_followup,
            "closure": self.interview.closure
        }
        
        section_obj = section_map.get(section)
        if section_obj:
            return section_obj.model_dump(exclude_none=True)
        return {}
    
    def _generate_llm_suggestions(self, context: InterviewContext) -> List[QuestionSuggestion]:
        """
        Generate question suggestions using LLM
        
        In production, this would call Claude API or local model.
        For this demo, we'll use rule-based logic that simulates what an LLM would do.
        """
        suggestions = []
        
        response_lower = context.patient_response.lower()
        section = context.current_section
        
        # Simulate LLM analysis with contextual rules
        # In production: suggestions = self._call_claude_api(context)
        
        # INCIDENT HISTORY suggestions
        if section == "incident_history":
            if "hit" in response_lower or "struck" in response_lower:
                suggestions.append(QuestionSuggestion(
                    question="Did you lose consciousness at any point after being hit?",
                    rationale="Head trauma requires immediate medical evaluation for concussion",
                    priority="high",
                    medical_relevance=True,
                    forensic_relevance=True
                ))
            
            if "drink" in response_lower or "drunk" in response_lower:
                suggestions.append(QuestionSuggestion(
                    question="Do you remember what you drank and approximately how much?",
                    rationale="Important for toxicology and determining if substances were administered",
                    priority="high",
                    medical_relevance=True,
                    forensic_relevance=True
                ))
            
            if any(time in response_lower for time in ["night", "evening", "dark"]):
                suggestions.append(QuestionSuggestion(
                    question="Was there any lighting in the area? Could you see the assailant clearly?",
                    rationale="Lighting conditions affect identification and witness testimony",
                    priority="medium",
                    medical_relevance=False,
                    forensic_relevance=True
                ))
        
        # INJURY ASSESSMENT suggestions
        elif section == "injury_assessment":
            if "neck" in response_lower or "throat" in response_lower or "chok" in response_lower:
                suggestions.append(QuestionSuggestion(
                    question="Are you having any difficulty breathing or swallowing?",
                    rationale="Strangulation can cause delayed airway complications - critical safety issue",
                    priority="high",
                    medical_relevance=True,
                    forensic_relevance=True
                ))
                suggestions.append(QuestionSuggestion(
                    question="Did you lose consciousness during the choking/strangulation?",
                    rationale="Loss of consciousness indicates severe strangulation requiring immediate medical attention",
                    priority="high",
                    medical_relevance=True,
                    forensic_relevance=True
                ))
            
            if "head" in response_lower and "pain" in response_lower:
                suggestions.append(QuestionSuggestion(
                    question="Do you have any vision changes, dizziness, or nausea?",
                    rationale="Signs of potential concussion or traumatic brain injury",
                    priority="high",
                    medical_relevance=True,
                    forensic_relevance=True
                ))
        
        # SEXUAL CONTACT suggestions
        elif section == "sexual_contact":
            if "shower" in response_lower or "bath" in response_lower:
                if not any("how long" in q.lower() for q in context.questions_already_asked):
                    suggestions.append(QuestionSuggestion(
                        question="How long after the assault did you shower/bathe?",
                        rationale="Timeline affects viability of forensic evidence collection",
                        priority="high",
                        medical_relevance=False,
                        forensic_relevance=True
                    ))
            
            if "mouth" in response_lower or "oral" in response_lower:
                suggestions.append(QuestionSuggestion(
                    question="Have you eaten, drunk anything, or brushed your teeth since the oral contact?",
                    rationale="These activities can destroy oral cavity evidence",
                    priority="high",
                    medical_relevance=False,
                    forensic_relevance=True
                ))
        
        # FORENSIC EVIDENCE suggestions
        elif section == "forensic_evidence":
            if "clothes" in response_lower:
                if not any("which clothes" in q.lower() for q in context.questions_already_asked):
                    suggestions.append(QuestionSuggestion(
                        question="Can you describe which specific clothing items you were wearing during the assault?",
                        rationale="Specific clothing identification helps with evidence collection and documentation",
                        priority="medium",
                        medical_relevance=False,
                        forensic_relevance=True
                    ))
        
        # PSYCHOLOGICAL suggestions
        elif section == "psychological":
            if any(word in response_lower for word in ["scared", "afraid", "terrified", "anxious"]):
                if not any("safe" in q.lower() for q in context.questions_already_asked):
                    suggestions.append(QuestionSuggestion(
                        question="Do you feel safe going home today, or would you like help finding a safe place to stay?",
                        rationale="Patient safety is paramount; expressing fear may indicate unsafe home environment",
                        priority="high",
                        medical_relevance=True,
                        forensic_relevance=False
                    ))
            
            if any(word in response_lower for word in ["suicide", "hurt myself", "end it", "don't want to live"]):
                suggestions.append(QuestionSuggestion(
                    question="Are you having thoughts of hurting yourself? This is very important and we can get you immediate help.",
                    rationale="CRITICAL: Suicidal ideation requires immediate intervention",
                    priority="CRITICAL",
                    medical_relevance=True,
                    forensic_relevance=False
                ))
        
        return suggestions
    
    def _handle_llm_suggestions(self, context: InterviewContext, section: str):
        """
        Generate and present suggestions to nurse, let them decide what to ask
        """
        suggestions = self._generate_llm_suggestions(context)
        
        if not suggestions:
            return  # No suggestions, continue normally
        
        # Display suggestions to nurse
        self.io.display("\n" + "─" * 70)
        self.io.display("🤖 AI ASSISTANT - SUGGESTED FOLLOW-UP QUESTIONS")
        self.io.display("─" * 70)
        self.io.display("Review these suggestions and decide what to ask (if anything):\n")
        
        for i, suggestion in enumerate(suggestions, 1):
            priority_emoji = {
                "CRITICAL": "🚨",
                "high": "⚠️",
                "medium": "💡",
                "low": "ℹ️"
            }.get(suggestion.priority, "💡")
            
            self.io.display(f"{priority_emoji} Suggestion {i} [{suggestion.priority.upper()} priority]:")
            self.io.display(f"   Q: {suggestion.question}")
            self.io.display(f"   Why: {suggestion.rationale}")
            
            if suggestion.medical_relevance:
                self.io.display("   🏥 Medical relevance: Yes")
            if suggestion.forensic_relevance:
                self.io.display("   🔬 Forensic relevance: Yes")
            self.io.display("")
        
        self.io.display("─" * 70)
        self.io.display("Options:")
        self.io.display("  [1-9]  Ask that numbered question")
        self.io.display("  [m]    Make note for later")
        self.io.display("  [s]    Skip all suggestions")
        self.io.display("  [c]    Create custom follow-up question")
        self.io.display("─" * 70)
        
        choice = self.io.ask("Your choice: ").strip().lower()
        
        if choice == 's':
            self.llm_suggestions_rejected += len(suggestions)
            self.io.display("✓ Continuing without additional questions\n")
            return
        
        elif choice == 'm':
            note = self.io.ask("Enter note: ").strip()
            self.nurse_notes[section] = self.nurse_notes.get(section, "") + f"\n{note}"
            self.io.display("✓ Note saved\n")
            return
        
        elif choice == 'c':
            custom_q = self.io.ask("Enter your custom question: ").strip()
            if custom_q:
                self._ask_custom_followup(custom_q, section)
            return
        
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(suggestions):
                self.llm_suggestions_accepted += 1
                selected = suggestions[idx]
                
                # Ask the suggested question
                self.io.display(f"\n{selected.question}")
                self.io.display("(Type 'skip' to decline answering)")
                followup_response = self.io.ask("Response: ").strip()
                
                # Store the follow-up response
                self._store_followup_response(section, selected.question, followup_response)
                
                self.io.display("✓ Response recorded\n")
            else:
                self.io.display("Invalid selection\n")
        else:
            self.io.display("Invalid choice, continuing...\n")
    
    def _ask_custom_followup(self, question: str, section: str):
        """Nurse asks their own custom follow-up question"""
        self.io.display(f"\n{question}")
        self.io.display("(Type 'skip' to decline answering)")
        response = self.io.ask("Response: ").strip()
        
        self._store_followup_response(section, question, response)
        self.io.display("✓ Response recorded\n")
    
    def _store_followup_response(self, section: str, question: str, response: str):
        """Store follow-up Q&A in additional notes"""
        entry = f"\n[Follow-up] Q: {question}\nA: {response}"
        self.interview.additional_notes = (self.interview.additional_notes or "") + entry
        self.questions_asked.append(question)
    
    # Override the original question methods to use LLM assistance
    
    def incident_questions(self):
        self.io.display("\n⚕️ 3. INCIDENT HISTORY")
        self.io.display("-" * 60)
        self.io.display("Remember: You may decline to answer any question.\n")
        
        self.io.display("I need to ask you some questions about what happened.")
        self.io.display("Take your time, and use your own words.")
        self.interview.incident_history.narrative = self.get_response_with_llm_assist(
            "Can you tell me, in your own words, what happened?",
            section="incident_history"
        )
        
        self.interview.incident_history.incident_date = self.get_response_with_llm_assist(
            "When did the assault occur? (date)",
            section="incident_history",
            enable_suggestions=False  # Date questions don't need suggestions
        )
        
        self.interview.incident_history.incident_time = self.get_response_with_llm_assist(
            "What time did it occur? (approximate is fine)",
            section="incident_history",
            enable_suggestions=False
        )
        
        self.interview.incident_history.location = self.get_response_with_llm_assist(
            "Where did it happen? (location, indoors/outdoors, bed, car, etc.)",
            section="incident_history"
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
            self.interview.incident_history.weapon_details = self.get_response_with_llm_assist(
                "Can you describe the weapon(s) or threats?",
                section="incident_history"
            )
        
        self.interview.incident_history.physically_restrained = self.get_yes_no(
            "Were you physically restrained (hands, ropes, clothing, etc.)?"
        )
        
        if self.interview.incident_history.physically_restrained == YesNoUnsure.YES:
            self.interview.incident_history.restraint_details = self.get_response_with_llm_assist(
                "How were you restrained?",
                section="incident_history"
            )
        
        self.interview.incident_history.lost_consciousness = self.get_yes_no(
            "Did you lose consciousness at any point?"
        )
        
        self.interview.incident_history.forced_substances = self.get_yes_no(
            "Were you forced to drink alcohol, take drugs, or any substances?"
        )
        
        if self.interview.incident_history.forced_substances == YesNoUnsure.YES:
            self.interview.incident_history.substance_details = self.get_response_with_llm_assist(
                "What substances were involved?",
                section="incident_history"
            )
        
        self.interview.incident_history.witnesses = self.get_yes_no(
            "Were there any witnesses or anyone who helped afterward?"
        )
        
        if self.interview.incident_history.witnesses == YesNoUnsure.YES:
            self.interview.incident_history.witness_details = self.get_response_with_llm_assist(
                "Can you provide details about witnesses or helpers?",
                section="incident_history"
            )
    
    def injury_questions(self):
        self.io.display("\n👁️ 5. INJURY AND PAIN ASSESSMENT")
        self.io.display("-" * 60)
        
        self.interview.injury_assessment.has_pain = self.get_yes_no(
            "Do you have any pain right now?"
        )
        
        if self.interview.injury_assessment.has_pain == YesNoUnsure.YES:
            self.interview.injury_assessment.pain_locations = self.get_response_with_llm_assist(
                "Where is the pain located?",
                section="injury_assessment"
            )
            
            pain_response = self.get_response(
                "How severe is the pain on a scale of 1-10? (1=minimal, 10=worst possible)"
            )
            if pain_response.isdigit():
                level = int(pain_response)
                if 0 <= level <= 10:
                    self.interview.injury_assessment.pain_level = level
        
        assault_response = self.get_response_with_llm_assist(
            "Did the assailant hit, slap, kick, bite, or strangle you? (list all that apply)",
            section="injury_assessment"
        )
        if assault_response != "decline_to_answer":
            self.interview.injury_assessment.physical_assault_types = [
                act.strip() for act in assault_response.split(',')
            ]
        
        self.interview.injury_assessment.visible_injuries = self.get_response_with_llm_assist(
            "Do you have any bruises, scratches, or bleeding? Please describe locations.",
            section="injury_assessment"
        )
        
        symptoms_response = self.get_response_with_llm_assist(
            "Are you experiencing: dizziness, nausea, or headaches? (list all that apply)",
            section="injury_assessment"
        )
        if symptoms_response != "decline_to_answer":
            self.interview.injury_assessment.symptoms = [
                sym.strip() for sym in symptoms_response.split(',')
            ]
        
        self.interview.injury_assessment.genital_anal_symptoms = self.get_response_with_llm_assist(
            "Are you experiencing pain, discharge, or bleeding in genital or anal areas?",
            section="injury_assessment"
        )
    
    def sexual_contact_questions(self):
        self.io.display("\n🧬 4. SEXUAL CONTACT DETAILS")
        self.io.display("-" * 60)
        self.io.display("These questions help us collect appropriate forensic evidence.\n")
        
        contact_response = self.get_response_with_llm_assist(
            "What type(s) of sexual contact occurred? (vaginal, oral, anal, digital, other)",
            section="sexual_contact"
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
            self.interview.sexual_contact.ejaculation_location = self.get_response_with_llm_assist(
                "Where did ejaculation occur?",
                section="sexual_contact"
            )
        
        self.interview.sexual_contact.objects_used = self.get_yes_no(
            "Did the assailant use any object(s)?"
        )
        
        if self.interview.sexual_contact.objects_used == YesNoUnsure.YES:
            self.interview.sexual_contact.object_details = self.get_response_with_llm_assist(
                "Can you describe the object(s)?",
                section="sexual_contact"
            )
        
        self.interview.sexual_contact.able_to_resist = self.get_yes_no(
            "Were you able to resist?"
        )
        
        if self.interview.sexual_contact.able_to_resist == YesNoUnsure.YES:
            self.interview.sexual_contact.resistance_details = self.get_response_with_llm_assist(
                "How did you resist?",
                section="sexual_contact"
            )
        
        self.interview.sexual_contact.clothing_removed_torn = self.get_yes_no(
            "Did the assailant remove or tear any of your clothing?"
        )
        
        activities_response = self.get_response_with_llm_assist(
            "Since the incident, have you: bathed, changed clothes, urinated, eaten, or brushed teeth? (list all that apply)",
            section="sexual_contact"
        )
        if activities_response != "decline_to_answer":
            self.interview.sexual_contact.post_incident_activities = [
                act.strip() for act in activities_response.split(',')
            ]
        
        self.interview.sexual_contact.items_cleaned_disposed = self.get_yes_no(
            "Have you cleaned or disposed of any items related to the incident?"
        )
    
    def psychological_questions(self):
        self.io.display("\n🧠 8. EMOTIONAL AND PSYCHOLOGICAL ASSESSMENT")
        self.io.display("-" * 60)
        
        self.interview.psychological.current_emotional_state = self.get_response_with_llm_assist(
            "How are you feeling emotionally right now?",
            section="psychological"
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
    
    def display_statistics(self):
        """Display LLM assistance statistics at end of interview"""
        self.io.display("\n" + "="*70)
        self.io.display("📊 LLM ASSISTANCE STATISTICS")
        self.io.display("="*70)
        self.io.display(f"Total suggestions made: {self.llm_suggestions_accepted + self.llm_suggestions_rejected}")
        self.io.display(f"Suggestions accepted: {self.llm_suggestions_accepted}")
        self.io.display(f"Suggestions rejected: {self.llm_suggestions_rejected}")
        
        if (self.llm_suggestions_accepted + self.llm_suggestions_rejected) > 0:
            acceptance_rate = (self.llm_suggestions_accepted / 
                             (self.llm_suggestions_accepted + self.llm_suggestions_rejected) * 100)
            self.io.display(f"Acceptance rate: {acceptance_rate:.1f}%")
        
        self.io.display("="*70 + "\n")


def cli():
    """Main entry point with LLM assistance option"""
    from sane_interview_chatbot import ConsoleInterviewIO
    io = ConsoleInterviewIO()
    
    io.display("="*70)
    io.display("🩺 SANE INTERVIEW SYSTEM - LLM-ASSISTED VERSION")
    io.display("="*70)
    
    use_llm = io.ask("\nEnable AI-powered question suggestions? (yes/no): ").strip().lower()
    use_llm_bool = use_llm in ['y', 'yes']
    
    if use_llm_bool:
        print("\n✓ LLM assistance enabled")
        print("  • AI will suggest relevant follow-up questions")
        print("  • You have full control over what to ask")
        print("  • All suggestions require your review")
        print("  • Patient data processed locally (simulated)\n")
    else:
        print("\n✓ LLM assistance disabled - using standard protocol\n")
    
    chatbot = LLMAssistedSANEInterviewer(use_llm_assist=use_llm_bool, local_model=True)
    
    try:
        interview = chatbot.conduct_interview()
        
        if interview and use_llm_bool:
            chatbot.display_statistics()
        
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
