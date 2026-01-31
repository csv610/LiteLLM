import json
from typing import List, Dict, Optional, Tuple
from pathlib import Path

try:
    from medkit.core.gemini_client import GeminiClient, ModelConfig, ModelInput
    from medkit.utils.privacy_compliance import PrivacyManager
except ImportError:
    # Fallback for standalone testing
    class ModelConfig:
        def __init__(self, model_name="gemini-2.5-flash", temperature=0.8, max_output_tokens=1024):
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
            return "Mock response from GeminiClient"

    class PrivacyManager:
        def create_session(self, patient_name, age, gender):
            return None
        def save_session(self, session):
            return None
        def load_session(self, session_id):
            return None

try:
    from .mental_health_assessment import MentalHealthAssessment
    from .models import ChatSession, ChatMessage
except ImportError:
    try:
        from medkit.mental_health.mental_health_assessment import MentalHealthAssessment
        from medkit.mental_health.models import ChatSession, ChatMessage
    except ImportError:
        from mental_health_assessment import MentalHealthAssessment
        from models import ChatSession, ChatMessage

# ==================== Prompt Builder ====================

class PromptBuilder:
    """Builder class for creating prompts for mental health chat."""

    @staticmethod
    def create_system_prompt() -> str:
        """
        Create the system prompt for mental health assessment.

        Returns:
            str: System prompt defining the AI's role and guidelines
        """
        return """You are a compassionate, highly trained mental health professional conducting an
evidence-based mental health assessment. Your role is to:

1. ASK PERSONALIZED QUESTIONS: Based on what the patient tells you, ask targeted follow-up questions
   to understand their specific situation and symptoms. Skip generic questions they've already answered.

2. EXPLORE PATTERNS: Listen for patterns in their responses and dig deeper into areas they mention.

3. ASSESS SEVERITY: Understand the duration, frequency, and impact of their symptoms.

4. DETECT RED FLAGS: If they mention suicidal ideation, self-harm, or thoughts of harming others,
   immediately escalate with compassion and provide resources.

5. GATHER CONTEXT: Understand their mental health history, triggers, and what's worked before.

6. BUILD RAPPORT: Be warm, non-judgmental, and validating of their experiences.

7. STRUCTURED OUTPUT: After gathering sufficient information, provide clinical assessment in JSON format.

IMPORTANT GUIDELINES:
- Ask ONE clear question at a time
- Listen more than you question
- Validate their experiences
- Don't rush - take time to understand
- If emergency red flags appear, pause assessment and provide crisis resources
- End each response with a clear question, not a statement
- Keep questions conversational and natural
- Avoid being overly clinical or robotic
- If patient shows signs of distress, slow down and express concern

TONE: Warm, empathetic, professional, never condescending or alarming
GOAL: Build a complete picture of their mental health to provide accurate assessment and recommendations"""

    @staticmethod
    def create_initial_question_prompt(chief_complaint: str) -> str:
        """
        Create the prompt for the initial question.

        Args:
            chief_complaint: The patient's chief complaint

        Returns:
            str: Formatted prompt for initial question
        """
        return f"""The patient has come seeking help for: {chief_complaint}

Start the conversation warmly and ask them to tell you more about what they're experiencing.
Ask ONE clear, open-ended question to understand their situation better."""

    @staticmethod
    def create_followup_question_prompt(conversation_summary: str) -> str:
        """
        Create the prompt for follow-up questions.

        Args:
            conversation_summary: Summary of the conversation so far

        Returns:
            str: Formatted prompt for follow-up question
        """
        return f"""CONVERSATION SO FAR:
{conversation_summary}

Based on what the patient has shared, ask the NEXT most important question to understand their mental health.
- Skip anything they've already covered
- Go deeper into areas that need clarification
- Ask ONE clear question at a time
- Be conversational and empathetic

What's the next question you would ask?"""

    @staticmethod
    def create_assessment_prompt(conversation_text: str) -> str:
        """
        Create the prompt for generating mental health assessment.

        Args:
            conversation_text: Full conversation transcript

        Returns:
            str: Formatted prompt for assessment generation
        """
        return f"""Based on this mental health conversation, generate a comprehensive
clinical mental health assessment in JSON format.

CONVERSATION:
{conversation_text}

Generate a detailed MentalHealthAssessment that includes:
1. Symptoms identified across all categories (mood, anxiety, cognitive, physical, trauma, etc.)
2. PHQ-9 and GAD-7 scores based on responses
3. Risk assessment (suicidality, self-harm, etc.)
4. Mental health history extracted from conversation
5. Social functioning assessment
6. Primary diagnosis with confidence level
7. Treatment recommendations
8. Clinical notes and summary

Return ONLY valid JSON matching the MentalHealthAssessment schema."""

    @staticmethod
    def create_assessment_system_prompt() -> str:
        """
        Create the system prompt for assessment generation.

        Returns:
            str: System prompt for assessment generation
        """
        return """You are an expert mental health clinician generating a structured assessment.
Ensure all JSON is valid and complete."""


# ==================== Configuration ====================

class ChatConfig:
    """Chat engine configuration."""

    # Model settings
    MODEL_NAME = "gemini-2.5-flash"
    TEMPERATURE = 0.8  # More conversational, less rigid
    MAX_OUTPUT_TOKENS = 1024
    MAX_QUESTIONS = 20  # Default reasonable conversation length (user configurable)
    QUESTION_TIMEOUT = 300  # 5 minutes per question

    # Assessment questionnaires
    ENABLE_PHQ9 = True
    ENABLE_GAD7 = True

    # System prompt for adaptive questioning
    SYSTEM_PROMPT = PromptBuilder.create_system_prompt()

# ==================== Mental Health Chat Engine ====================

class MentalHealthChatEngine:
    """
    Main chat engine for mental health assessment.

    Handles personalized, adaptive conversations with patients.
    """

    # Mental health red flags with emergency protocols
    RED_FLAGS = {
        "suicidal_ideation": {
            "keywords": ["suicide", "kill myself", "don't want to live", "better off dead",
                        "harm myself", "end my", "ending my", "take my own", "final goodbye",
                        "should be dead", "want to die", "thinking about ending"],
            "severity": "emergency",
            "follow_up": "How long have you been having these thoughts? Do you have a plan?"
        },
        "self_harm": {
            "keywords": ["cutting", "hurt myself", "harm myself", "burn myself", "pull hair",
                        "bang head", "self injury", "cutting myself"],
            "severity": "emergency",
            "follow_up": "How often are you hurting yourself? Have you been injured recently?"
        },
        "harm_to_others": {
            "keywords": ["kill them", "hurt someone", "attack", "violent", "harm others",
                        "going to hit", "planning to hurt"],
            "severity": "emergency",
            "follow_up": "Are you thinking about hurting a specific person? Do you have access to weapons?"
        },
        "psychotic_symptoms": {
            "keywords": ["hearing voices", "seeing things", "hallucinations", "conspiracy",
                        "aliens", "mind reading", "thoughts not mine", "government tracking"],
            "severity": "urgent",
            "follow_up": "Can you describe what you're experiencing? How long has this been happening?"
        },
        "severe_depression": {
            "keywords": ["hopeless", "nothing matters", "pointless", "can't get out of bed",
                        "give up", "no point", "never get better", "completely empty"],
            "severity": "urgent",
            "follow_up": "Have these feelings been overwhelming? How is this affecting your daily life?"
        }
    }

    def __init__(self, session_id: Optional[str] = None, max_questions: Optional[int] = None):
        """
        Initialize chat engine.

        Args:
            session_id: Existing session ID to resume (optional)
            max_questions: Maximum number of questions to ask (optional, defaults to ChatConfig.MAX_QUESTIONS)
        """
        # Initialize Gemini client
        config = ModelConfig(
            model_name=ChatConfig.MODEL_NAME,
            temperature=ChatConfig.TEMPERATURE,
            max_output_tokens=ChatConfig.MAX_OUTPUT_TOKENS
        )
        self.client = GeminiClient(config=config)

        # Initialize privacy manager
        self.privacy_manager = PrivacyManager()

        # Session management
        self.session: Optional[ChatSession] = None
        self.session_id = session_id

        # Conversation state
        self.conversation_history: List[Dict] = []
        self.collected_data: Dict = {}
        self.emergency_triggered = False
        self.max_questions = max_questions or ChatConfig.MAX_QUESTIONS
        self.question_count = 0

    # ==================== Session Initialization ====================

    def initialize_session(self, patient_name: str, age: int, gender: str,
                          chief_complaint: str) -> ChatSession:
        """
        Initialize new chat session with patient.

        Args:
            patient_name: Patient name
            age: Patient age
            gender: Patient gender
            chief_complaint: What brings them in today?

        Returns:
            ChatSession: New session
        """
        self.session = self.privacy_manager.create_session(patient_name, age, gender)

        # Store chief complaint in collected data
        self.collected_data['chief_complaint'] = chief_complaint
        self.collected_data['complaint_onset'] = "ongoing"  # Will be refined in conversation

        # Clear conversation history
        self.conversation_history = []

        return self.session

    def resume_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Resume existing chat session.

        Args:
            session_id: Session ID to resume

        Returns:
            ChatSession or None if not found
        """
        self.session = self.privacy_manager.load_session(session_id)

        if self.session:
            # Reconstruct conversation history from messages
            self.conversation_history = []
            for message in self.session.messages:
                self.conversation_history.append({
                    "role": message.role,
                    "content": message.content
                })

        return self.session

    # ==================== Red Flag Detection ====================

    def detect_red_flags(self, user_message: str) -> Tuple[bool, List[str], str]:
        """
        Detect mental health emergency red flags in user message.

        Args:
            user_message: User's message text

        Returns:
            Tuple of (has_flags, flag_names, severity_level)
        """
        message_lower = user_message.lower()
        detected_flags = []
        max_severity = "none"

        for flag_name, flag_config in self.RED_FLAGS.items():
            for keyword in flag_config["keywords"]:
                if keyword.lower() in message_lower:
                    detected_flags.append(flag_name)
                    if flag_config["severity"] == "emergency":
                        max_severity = "emergency"
                    elif flag_config["severity"] == "urgent" and max_severity != "emergency":
                        max_severity = "urgent"
                    break

        has_flags = len(detected_flags) > 0

        return has_flags, detected_flags, max_severity

    def handle_emergency(self, flags: List[str]) -> str:
        """
        Handle emergency red flags with immediate crisis resources.

        Args:
            flags: List of detected red flag names

        Returns:
            Emergency response message
        """
        self.emergency_triggered = True

        if self.session:
            self.session.emergency_triggered = True
            self.session.session_status = "emergency"

        message = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                          🚨 CRISIS ALERT - EMERGENCY 🚨                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

Based on what you've shared, you're experiencing a mental health crisis.
Your safety is our top priority.

DETECTED CONCERNS: {', '.join(flags)}

IMMEDIATE CRISIS RESOURCES:

🆘 UNITED STATES:
   National Suicide Prevention Lifeline: 988 (available 24/7)
   Crisis Text Line: Text HOME to 741741
   International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/
   Emergency Services: 911

🆘 INTERNATIONAL:
   International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/
   Befrienders International: https://www.befrienders.org/

⚠ IF YOU ARE IN IMMEDIATE DANGER:
   → Call emergency services (911 in US) or go to your nearest emergency room
   → Tell someone you trust what you're experiencing
   → Remove yourself from any potentially dangerous situation

WHAT TO DO NOW:
   1. Reach out to crisis support above
   2. Tell a trusted friend or family member
   3. Go to the nearest emergency room if needed
   4. Call emergency services if in immediate danger

This assessment cannot replace professional mental health care or emergency services.

Please reach out for help now. You matter and recovery is possible.
"""

        return message

    # ==================== Adaptive Conversation Engine ====================

    def generate_next_question(self, context: Optional[str] = None) -> str:
        """
        Generate next question based on conversation so far.

        Args:
            context: Additional context for question generation

        Returns:
            Next question to ask patient
        """
        # Build system prompt with context about what we've learned
        sys_prompt = ChatConfig.SYSTEM_PROMPT

        if context:
            sys_prompt += f"\n\nPATIENT CONTEXT: {context}"

        # Build user prompt with conversation history summary
        conversation_summary = self._summarize_conversation()

        if not conversation_summary:
            # First question - greet and ask about chief complaint
            chief_complaint = self.collected_data.get('chief_complaint', 'mental health concerns')
            user_prompt = PromptBuilder.create_initial_question_prompt(chief_complaint)
        else:
            user_prompt = PromptBuilder.create_followup_question_prompt(conversation_summary)

        # Generate question from AI
        model_input = ModelInput(
            user_prompt=user_prompt,
            sys_prompt=sys_prompt
        )

        response = self.client.generate_content(model_input)

        # Extract clean question (remove leading/trailing markers)
        question = response.strip()
        if "Doctor:" in question:
            question = question.split("Doctor:")[-1].strip()
        if "Assistant:" in question:
            question = question.split("Assistant:")[-1].strip()

        return question

    def _summarize_conversation(self) -> str:
        """
        Create a summary of conversation so far for context.

        Returns:
            Formatted conversation summary
        """
        if not self.conversation_history:
            return ""

        summary = ""
        for msg in self.conversation_history[-10:]:  # Last 10 messages for context
            role = "Patient" if msg["role"] == "user" else "Assistant"
            summary += f"\n{role}: {msg['content'][:200]}..."  # Truncate long responses

        return summary

    def _generate_conclusion(self) -> str:
        """
        Generate closing message when question limit is reached.

        Returns:
            Conclusion message
        """
        return f"""Thank you for sharing with me today. I've gathered valuable information about your mental health and experiences.

Based on our conversation, I'd like to generate a comprehensive assessment of what we've discussed. This will help provide insights into your mental health and recommendations for next steps.

Would you like me to generate a detailed mental health assessment based on our conversation?"""

    def process_user_response(self, user_input: str) -> Dict:
        """
        Process user response and return system response.

        Args:
            user_input: User's message

        Returns:
            Dict with response and metadata
        """
        # Detect red flags
        has_flags, flags, severity = self.detect_red_flags(user_input)

        # Store message in session
        message = ChatMessage(
            role="user",
            content=user_input,
            red_flags_detected=flags
        )

        if self.session:
            self.session.messages.append(message)

        # Handle emergency
        if has_flags and severity == "emergency":
            response = self.handle_emergency(flags)
            if self.session:
                self.session.messages.append(ChatMessage(
                    role="assistant",
                    content=response
                ))
            return {
                "response": response,
                "emergency": True,
                "red_flags": flags,
                "should_continue": False
            }

        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Check if question limit reached
        if self.question_count >= self.max_questions:
            conclusion_message = self._generate_conclusion()
            assistant_message = ChatMessage(
                role="assistant",
                content=conclusion_message
            )
            if self.session:
                self.session.messages.append(assistant_message)
            self.conversation_history.append({
                "role": "assistant",
                "content": conclusion_message
            })
            return {
                "response": conclusion_message,
                "emergency": False,
                "red_flags": flags,
                "should_continue": False,
                "reason": "max_questions_reached"
            }

        # Generate next question
        next_question = self.generate_next_question()
        self.question_count += 1

        # Store assistant message
        assistant_message = ChatMessage(
            role="assistant",
            content=next_question
        )

        if self.session:
            self.session.messages.append(assistant_message)

        self.conversation_history.append({
            "role": "assistant",
            "content": next_question
        })

        return {
            "response": next_question,
            "emergency": False,
            "red_flags": flags,
            "should_continue": True,
            "questions_asked": self.question_count,
            "questions_remaining": self.max_questions - self.question_count
        }

    # ==================== Assessment Generation ====================

    def generate_assessment(self) -> Optional[MentalHealthAssessment]:
        """
        Generate comprehensive mental health assessment from chat history.

        Returns:
            MentalHealthAssessment object or None if generation fails
        """
        if not self.session:
            return None

        # Prepare conversation context
        conversation_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in self.conversation_history
        ])

        # Prompt for assessment generation
        assessment_prompt = PromptBuilder.create_assessment_prompt(conversation_text)
        sys_prompt = PromptBuilder.create_assessment_system_prompt()

        try:
            model_input = ModelInput(
                user_prompt=assessment_prompt,
                sys_prompt=sys_prompt
            )

            response = self.client.generate_content(model_input)

            # Parse JSON response
            assessment_dict = self._parse_assessment_json(response)

            # Validate and create assessment
            assessment = MentalHealthAssessment(**assessment_dict)

            # Store in session
            if self.session:
                self.session.assessment_data = assessment

            return assessment

        except Exception as e:
            print(f"Error generating assessment: {e}")
            return None

    def _parse_assessment_json(self, response: str) -> Dict:
        """
        Parse JSON from assessment response.

        Args:
            response: Response from AI

        Returns:
            Parsed JSON dictionary
        """
        # Try direct JSON parse
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass

        # Try extracting from markdown
        if "```json" in response:
            json_text = response.split("```json")[1].split("```")[0].strip()
            return json.loads(json_text)

        if "```" in response:
            json_text = response.split("```")[1].split("```")[0].strip()
            return json.loads(json_text)

        # Try regex extraction
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())

        raise ValueError("Could not parse JSON from assessment response")

    # ==================== Session Persistence ====================

    def save_session(self) -> Optional[Path]:
        """
        Save current session to storage.

        Returns:
            Path to saved session file
        """
        if self.session:
            return self.privacy_manager.save_session(self.session)
        return None

    def get_session_info(self) -> Dict:
        """
        Get current session information.

        Returns:
            Session metadata dictionary
        """
        if not self.session:
            return {}

        return {
            "session_id": self.session.session_id,
            "patient_name": self.session.patient_name,
            "age": self.session.age,
            "created_at": self.session.created_at,
            "message_count": len(self.session.messages),
            "status": self.session.session_status,
            "emergency_triggered": self.session.emergency_triggered
        }
