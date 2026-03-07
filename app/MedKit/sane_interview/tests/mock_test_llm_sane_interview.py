import os
import sys
import pytest
from unittest.mock import MagicMock, patch

# Add parent directory to sys.path to allow imports when running from within tests/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm_sane_interview import (
    LLMAssistedSANEInterviewer, InterviewContext, QuestionSuggestion
)
from sane_interview_models import YesNoUnsure

class MockIO:
    def __init__(self, responses=None):
        self.responses = responses or []
        self.output = []
    
    def display(self, text):
        self.output.append(text)
    
    def ask(self, prompt):
        if self.responses:
            return self.responses.pop(0)
        return ""
    
    def wait_for_user(self, text):
        pass

def test_llm_suggestions_generation():
    interviewer = LLMAssistedSANEInterviewer(use_llm_assist=True)
    
    # Test incident_history suggestions for "choking" (strangulation)
    # Wait, "choking" logic is in injury_assessment
    context = InterviewContext(
        current_section="injury_assessment",
        patient_response="The person tried to choke me.",
        questions_already_asked=[],
        responses_so_far={}
    )
    
    suggestions = interviewer._generate_llm_suggestions(context)
    assert len(suggestions) >= 2
    assert any("breathing" in s.question.lower() for s in suggestions)
    assert any("consciousness" in s.question.lower() for s in suggestions)
    assert suggestions[0].priority == "high"

def test_llm_suggestions_generation_psychological():
    interviewer = LLMAssistedSANEInterviewer(use_llm_assist=True)
    
    # Test for suicidal ideation
    context = InterviewContext(
        current_section="psychological",
        patient_response="I don't want to live anymore.",
        questions_already_asked=[],
        responses_so_far={}
    )
    
    suggestions = interviewer._generate_llm_suggestions(context)
    assert len(suggestions) >= 1
    assert any("hurting yourself" in s.question.lower() for s in suggestions)
    assert suggestions[0].priority == "CRITICAL"

def test_get_response_with_llm_assist_accepted():
    mock_io = MockIO(responses=["I was choked.", "1"]) # 1. Response, 2. Accept first suggestion
    interviewer = LLMAssistedSANEInterviewer(use_llm_assist=True, io_handler=mock_io)
    
    # Mock the follow-up response
    with patch.object(mock_io, 'ask', side_effect=["I was choked.", "1", "No, I can breathe fine."]):
        response = interviewer.get_response_with_llm_assist(
            "What happened to you?",
            section="injury_assessment"
        )
    
    assert response == "I was choked."
    assert interviewer.llm_suggestions_accepted == 1
    assert "breathing" in interviewer.interview.additional_notes

def test_get_response_with_llm_assist_skipped():
    mock_io = MockIO(responses=["I was choked.", "s"]) # 1. Response, 2. Skip suggestions
    interviewer = LLMAssistedSANEInterviewer(use_llm_assist=True, io_handler=mock_io)
    
    response = interviewer.get_response_with_llm_assist(
        "What happened to you?",
        section="injury_assessment"
    )
    
    assert response == "I was choked."
    assert interviewer.llm_suggestions_rejected >= 1
    assert interviewer.interview.additional_notes is None
