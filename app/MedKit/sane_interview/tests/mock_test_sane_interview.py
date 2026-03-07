import os
import sys
import pytest

# Add parent directory to sys.path to allow imports when running from within tests/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sane_interview import SANEInterview, Question
from sane_interview_models import YesNoUnsure, SANEInterviewRecord, SexualContactType

def test_parse_yes_no():
    interview = SANEInterview()
    assert interview._parse_yes_no("yes") == YesNoUnsure.YES
    assert interview._parse_yes_no("y") == YesNoUnsure.YES
    assert interview._parse_yes_no("no") == YesNoUnsure.NO
    assert interview._parse_yes_no("n") == YesNoUnsure.NO
    assert interview._parse_yes_no("u") == YesNoUnsure.UNSURE
    assert interview._parse_yes_no("unsure") == YesNoUnsure.UNSURE
    assert interview._parse_yes_no("not sure") == YesNoUnsure.UNSURE
    assert interview._parse_yes_no("skip") == YesNoUnsure.DECLINE
    assert interview._parse_yes_no("explain") == YesNoUnsure.EXPLAIN
    assert interview._parse_yes_no("") == YesNoUnsure.DECLINE
    assert interview._parse_yes_no("random") == YesNoUnsure.DECLINE

def test_interview_initial_flow():
    interview = SANEInterview()
    
    # First question: interviewer name
    q1 = interview.get_next_question()
    assert isinstance(q1, Question)
    assert "Enter interviewer name" in q1.text
    
    # Second question: patient identifier
    q2 = interview.get_next_question("Nurse Jane")
    assert "Enter patient identifier" in q2.text
    assert interview.interview.interviewer_name == "Nurse Jane"
    
    # Third: Info about Consent
    q3 = interview.get_next_question("P123")
    assert "🩺 1. INTRODUCTION AND CONSENT" in q3.text
    assert q3.type == "info"
    assert interview.interview.patient_id == "P123"
    
    # Fourth: Consent question
    q4 = interview.get_next_question()
    assert "Do you understand the purpose" in q4.text
    assert q4.type == "yes_no"

def test_consent_denied():
    interview = SANEInterview()
    interview.get_next_question() # Returns Interviewer name Q
    interview.get_next_question("Nurse Jane") # Returns Patient ID Q
    interview.get_next_question("P123") # Returns Consent Info Q
    q_purpose = interview.get_next_question() # Returns Understands Purpose Q
    assert "Do you understand the purpose" in q_purpose.text
    
    # Deny permission
    q_permission = interview.get_next_question("yes") # Returns Permission Q
    assert "Do I have your permission" in q_permission.text
    
    q_denied_info = interview.get_next_question("no") # Returns Denied Info Q
    assert "Exam cannot proceed without consent" in q_denied_info.text
    
    next_q = interview.get_next_question()
    assert next_q is None
    assert interview._interview_complete is True

def test_consent_full_flow():
    interview = SANEInterview()
    interview.get_next_question() # Interviewer
    interview.get_next_question("Nurse Jane") # Patient ID
    interview.get_next_question("P123") # Info
    
    interview.get_next_question() # Returns Understands purpose
    q_permission = interview.get_next_question("yes") # Returns Permission Q
    assert "Do I have your permission" in q_permission.text
    
    q_medical_info_intro = interview.get_next_question("yes") # Returns Info: To provide best medical care...
    assert "To provide the best medical care" in q_medical_info_intro.text
    
    q_age_yn = interview.get_next_question()
    assert "May I ask your age?" in q_age_yn.text
    
    q_age_val = interview.get_next_question("yes")
    assert "What is your age in years?" in q_age_val.text
    
    q_sex_yn = interview.get_next_question("25")
    assert interview.interview.consent.age == 25
    assert "May I ask your sex assigned at birth?" in q_sex_yn.text
    
    q_sex_val = interview.get_next_question("yes")
    assert "What sex were you assigned at birth?" in q_sex_val.text
    
    q_gender_yn = interview.get_next_question("female")
    assert interview.interview.consent.sex == "female"
    assert "Do you identify as transgender" in q_gender_yn.text
    
    q_info_know = interview.get_next_question("no")
    assert "Is there anything you would like me to know" in q_info_know.text
    
    q_advocate_yn = interview.get_next_question("None")
    assert interview.interview.consent.additional_information == "None"
    assert "Would you like someone" in q_advocate_yn.text
    
    q_advocate_name = interview.get_next_question("yes")
    assert "What is their name?" in q_advocate_name.text
    
    q_medical_intro = interview.get_next_question("Friend")
    assert interview.interview.consent.advocate_name == "Friend"
    assert "👩‍⚕️ 2. GENERAL MEDICAL HISTORY" in q_medical_intro.text

def test_sexual_contact_parsing():
    interview = SANEInterview()
    flow = interview.sexual_contact_questions()
    next(flow) # Info
    q = flow.send("") # What parts of your body...
    assert "parts of your body" in q.text
    
    # Simulate sending "vagina and mouth"
    try:
        flow.send("vagina and mouth")
    except StopIteration:
        pass
    
    assert SexualContactType.VAGINAL in interview.interview.sexual_contact.contact_types
    assert SexualContactType.ORAL in interview.interview.sexual_contact.contact_types
    assert SexualContactType.ANAL not in interview.interview.sexual_contact.contact_types

def test_medical_history_conditional_age():
    # Test that menstrual questions are skipped if age < 12
    interview = SANEInterview()
    interview.interview.consent.age = 10
    
    flow = interview.medical_history_questions()
    next(flow) # Info
    flow.send("") # conditions
    flow.send("") # medications
    q_last = flow.send("") # allergies -> if age < 12, this should raise StopIteration after this send
    
    try:
        flow.send("")
        assert False, "Should have stopped"
    except StopIteration:
        pass
    
    # last_menstrual_period should be None
    assert interview.interview.medical_history.last_menstrual_period is None
    
    # Now test with age > 12
    interview2 = SANEInterview()
    interview2.interview.consent.age = 20
    flow2 = interview2.medical_history_questions()
    next(flow2) # Info
    flow2.send("") # conditions
    flow2.send("") # medications
    flow2.send("") # allergies
    q_menstrual = flow2.send("") # result of allergies answer
    assert "last menstrual period" in q_menstrual.text
