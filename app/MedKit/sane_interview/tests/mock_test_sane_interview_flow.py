import os
import sys
import pytest

# Add parent directory to sys.path to allow imports when running from within tests/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sane_interview import SANEInterview, Question
from sane_interview_models import YesNoUnsure, SANEInterviewRecord, SexualContactType

def test_full_successful_interview_debug():
    interview = SANEInterview()
    
    answers = [
        "Dr. Smith", # 0. Enter interviewer name
        "PAT-001",   # 1. Enter patient identifier
        "",          # 2. info (Consent intro)
        "yes",       # 3. Do you understand purpose?
        "yes",       # 4. Do I have permission?
        "",          # 5. info (To provide best care...)
        "yes",       # 6. May I ask age?
        "30",        # 7. What is age?
        "yes",       # 8. May I ask sex?
        "female",    # 9. What sex?
        "no",        # 10. Transgender?
        "nothing",   # 11. Anything else?
        "no",        # 12. Advocate?
        "",          # 13. info (Medical history intro)
        "diabetes",  # 14. Medical conditions?
        "insulin",   # 15. Medications?
        "none",      # 16. Allergies?
        "last week", # 17. LMP?
        "2 kids",    # 18. Pregnancy history?
        "no",        # 19. Currently pregnant?
        "",          # 20. info (Incident history intro)
        "Attacked",  # 21. Narrative?
        "2023-10-27",# 22. Date?
        "10 PM",     # 23. Time?
        "Park",      # 24. Location?
        "no",        # 25. Knows assailant?
        "1",         # 26. Number?
        "yes",       # 27. Weapons?
        "Knife",     # 28. Weapon details?
        "yes",       # 29. Restrained?
        "Rope",      # 30. Restraint details?
        "no",        # 31. Lost consciousness?
        "no",        # 32. Forced substances?
        "no",        # 33. Witnesses?
        "",          # 34. info (Sexual contact intro)
        "vaginal",   # 35. Contact types?
        "no",        # 36. Condom?
        "yes",       # 37. Ejaculation?
        "body",      # 38. Ejaculation location?
        "no",        # 39. Objects?
        "no",        # 40. Able to resist?
        "yes",       # 41. Clothing removed?
        "showered",  # 42. Activities?
        "no",        # 43. Items cleaned?
        "",          # 44. info (Injury intro)
        "yes",       # 45. Pain right now?
        "head",      # 46. Pain locations?
        "7",         # 47. Pain level?
        "hit",       # 48. Assault types?
        "bruise",    # 49. Visible injuries?
        "headache",  # 50. Symptoms?
        "none",      # 51. Genital symptoms?
        "",          # 52. info (Forensic intro)
        "yes",       # 53. Urinated?
        "no",        # 54. Defecated?
        "no",        # 55. Changed products?
        "no",        # 56. Eaten/drunk?
        "no",        # 57. Items left?
        "no",        # 58. Same clothes?
        "yes",       # 59. Wants collected?
        "",          # 60. info (Treatment intro)
        "yes",       # 61. STI prophylaxis?
        "yes",       # 62. Emergency contraception?
        "no",        # 63. Recent HIV test?
        "yes",       # 64. Wants HIV test?
        "none",      # 65. Medication concerns?
        "",          # 66. info (Psychological intro)
        "scared",    # 67. Emotional state?
        "yes",       # 68. Support?
        "husband",   # 69. Support details?
        "no",        # 70. Previous trauma?
        "yes",       # 71. Safe home?
        "yes",       # 72. Counselor?
        "",          # 73. info (Legal intro)
        "no",        # 74. Reported?
        "no",        # 75. Explanation?
        "yes",       # 76. Evidence even if undecided?
        "yes",       # 77. Contact follow up?
        "555-0100",  # 78. Contact info?
        "no",        # 79. Transportation?
        "no",        # 80. Safe housing?
        "",          # 81. info (Closure intro)
        "none",      # 82. Add questions?
        "no",        # 83. Next steps review?
        "no",        # 84. Resources explained?
    ]
    
    last_ans = None
    q_count = 0
    while True:
        q = interview.get_next_question(last_ans)
        if q is None:
            break
        # print(f"{q_count}: {q.text[:50]}...") # For debugging
        if q_count < len(answers):
            last_ans = answers[q_count]
        else:
            last_ans = ""
        q_count += 1
    
    assert interview._interview_complete is True
    assert interview.interview.interviewer_name == "Dr. Smith"
    assert interview.interview.consent.age == 30
    assert interview.interview.medical_history.medical_conditions == "diabetes"
    assert interview.interview.incident_history.narrative == "Attacked"
