import pytest
from pydantic import ValidationError
from .nobel_prize_models import PrizeWinner, PersonalBackground, CareerPosition, BroaderRecognition, FAQItem, GlossaryItem

def test_faq_item():
    faq = FAQItem(question="What is the discovery?", answer="It's a new particle.")
    assert faq.question == "What is the discovery?"
    assert faq.answer == "It's a new particle."

def test_glossary_item():
    glossary = GlossaryItem(term="Particle", definition="A small portion of matter.")
    assert glossary.term == "Particle"
    assert glossary.definition == "A small portion of matter."

def test_personal_background():
    pb = PersonalBackground(
        birth_date="1950-01-01",
        birth_place="City, Country",
        nationality="Country",
        family_background="Parents were scientists.",
        education=["B.Sc. Physics, University X (1970)"],
        early_influences="Mentors at University X."
    )
    assert pb.birth_date == "1950-01-01"
    assert len(pb.education) == 1

def test_career_position():
    cp = CareerPosition(
        title="Professor",
        institution="University Y",
        location="City, Country",
        start_year=1980,
        end_year=2000,
        description="Teaching and research."
    )
    assert cp.start_year == 1980
    assert cp.end_year == 2000

def test_broader_recognition():
    br = BroaderRecognition(
        honors_and_awards=["Award A"],
        academy_memberships=["Academy B"],
        editorial_roles=["Journal C"],
        mentorship_contributions="Mentored many students.",
        leadership_roles=["Dept Head"],
        public_engagement="Public lectures."
    )
    assert "Award A" in br.honors_and_awards
    assert "Academy B" in br.academy_memberships

def test_prize_winner_validation_error():
    with pytest.raises(ValidationError):
        # Missing required fields
        PrizeWinner(name="John Doe", year=2020, category="Physics")

def test_full_prize_winner():
    pb = PersonalBackground(
        birth_date="1950-01-01",
        birth_place="City, Country",
        nationality="Country",
        family_background="Parents were scientists.",
        education=["B.Sc. Physics, University X (1970)"],
        early_influences="Mentors at University X."
    )
    cp = CareerPosition(
        title="Professor",
        institution="University Y",
        location="City, Country",
        start_year=1980,
        end_year=2000,
        description="Teaching and research."
    )
    br = BroaderRecognition(
        honors_and_awards=["Award A"],
        academy_memberships=["Academy B"],
        editorial_roles=["Journal C"],
        mentorship_contributions="Mentored many students.",
        leadership_roles=["Dept Head"],
        public_engagement="Public lectures."
    )
    faq = FAQItem(question="Q", answer="A")
    glossary = GlossaryItem(term="T", definition="D")

    winner = PrizeWinner(
        name="John Doe",
        year=2020,
        category="Physics",
        contribution="Discovered something new.",
        personal_background=pb,
        career_timeline=[cp],
        broader_recognition=br,
        history="Detailed history of the discovery that is long enough to meet the 50 characters requirement.",
        impact="Measurable impact of the discovery that is long enough to meet the 50 characters requirement.",
        foundation="Cross-disciplinary influence that is long enough to meet the 50 characters requirement.",
        applications=["App 1"],
        relevancy="Current relevance of the idea that is long enough to meet the 50 characters requirement.",
        advancements=["Adv 1"],
        refinements=["Ref 1"],
        gaps=["Gap 1"],
        keywords=["Key 1"],
        learning_objectives=["Obj 1"],
        faq=[faq],
        glossary=[glossary]
    )
    assert winner.name == "John Doe"
    assert winner.year == 2020
