from nobel_prize_models import (
    BroaderRecognition,
    CareerPosition,
    FAQItem,
    GlossaryItem,
    PersonalBackground,
    PrizeResponse,
    PrizeWinner,
)
from nobel_prize_prompts import PromptBuilder


def make_prize_response() -> PrizeResponse:
    return PrizeResponse(
        winners=[
            PrizeWinner(
                name="Test Winner",
                year=2023,
                category="Physics",
                contribution="Measured electron dynamics in matter using attosecond pulse techniques.",
                personal_background=PersonalBackground(
                    birth_date="1960-01-01",
                    birth_place="City, Country",
                    nationality="Country",
                    family_background="Family background with early academic influences.",
                    education=["B.Sc. Physics, University X (1982)"],
                    early_influences="Mentors and laboratory training shaped the research direction.",
                ),
                career_timeline=[
                    CareerPosition(
                        title="Professor",
                        institution="University Y",
                        location="City, Country",
                        start_year=1995,
                        end_year=None,
                        description="Research and teaching in ultrafast science.",
                    )
                ],
                broader_recognition=BroaderRecognition(
                    honors_and_awards=["Award A"],
                    academy_memberships=["Academy B"],
                    editorial_roles=["Journal C"],
                    mentorship_contributions="Mentored students and postdoctoral researchers.",
                    leadership_roles=["Institute Director"],
                    public_engagement="Delivered public lectures on ultrafast measurement methods.",
                ),
                history="This history section is intentionally long enough to satisfy schema validation and describe chronology.",
                impact="This impact section is intentionally long enough to satisfy schema validation and stay objective.",
                foundation="This foundation section is intentionally long enough to satisfy schema validation with specifics.",
                applications=["Application A"],
                relevancy="This relevancy section is intentionally long enough to satisfy schema validation today.",
                advancements=["Advancement A"],
                refinements=["Refinement A"],
                gaps=["Gap A"],
                keywords=["attosecond physics"],
                learning_objectives=["Understand ultrafast measurement methods."],
                faq=[FAQItem(question="What is attosecond science?", answer="It studies processes on attosecond timescales.")],
                glossary=[GlossaryItem(term="Attosecond", definition="One quintillionth of a second.")],
            )
        ]
    )

def test_create_nobel_prize_prompt():
    category = "Physics"
    year = "2020"
    prompt = PromptBuilder.create_nobel_prize_prompt(category, year)
    assert category in prompt
    assert year in prompt
    assert "BIOGRAPHICAL INFORMATION" in prompt
    assert "SCIENTIFIC WORK" in prompt
    assert "EDUCATIONAL CONTENT" in prompt

def test_create_agent_system_prompt():
    generation_prompt = PromptBuilder.create_agent_system_prompt("generation_agent")
    validation_prompt = PromptBuilder.create_agent_system_prompt("validation_agent")

    assert "generation agent" in generation_prompt.lower()
    assert "validation agent" in validation_prompt.lower()

def test_create_validation_prompt():
    response = make_prize_response()
    prompt = PromptBuilder.create_validation_prompt("Physics", "2023", response)

    assert "accuracy" in prompt.lower()
    assert "complete coverage" in prompt.lower()
    assert "Candidate JSON" in prompt
    assert '"name": "Test Winner"' in prompt
