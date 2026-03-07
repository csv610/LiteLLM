import os
import sys

import pytest
from pydantic import ValidationError

# Add parent directory to sys.path to allow imports when running from within tests/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sane_interview_models import (
    ConsentSection,
    SANEInterviewRecord,
    SexualContactType,
    YesNoUnsure,
)


def test_consent_section_validation():
    # Valid age
    consent = ConsentSection(age=25)
    assert consent.age == 25

    # Invalid age (too high)
    with pytest.raises(ValidationError):
        ConsentSection(age=200)

    # Invalid age (negative)
    with pytest.raises(ValidationError):
        ConsentSection(age=-1)


def test_interview_record_defaults():
    record = SANEInterviewRecord()
    assert record.interview_date is not None
    assert record.consent is not None
    assert record.medical_history is not None
    assert record.incident_history is not None
    assert record.sexual_contact is not None
    assert record.injury_assessment is not None
    assert record.forensic_evidence is not None
    assert record.treatment is not None
    assert record.psychological is not None
    assert record.legal_followup is not None
    assert record.closure is not None


def test_sexual_contact_details():
    from sane_interview_models import SexualContactDetails

    details = SexualContactDetails(
        contact_types=[SexualContactType.VAGINAL, SexualContactType.ORAL],
        condom_used=YesNoUnsure.NO,
    )
    assert len(details.contact_types) == 2
    assert SexualContactType.VAGINAL in details.contact_types
    assert details.condom_used == YesNoUnsure.NO


def test_injury_assessment_pain_level():
    from sane_interview_models import InjuryAssessment

    # Valid pain level
    ia = InjuryAssessment(pain_level=5)
    assert ia.pain_level == 5

    # Invalid pain level
    with pytest.raises(ValidationError):
        InjuryAssessment(pain_level=11)
