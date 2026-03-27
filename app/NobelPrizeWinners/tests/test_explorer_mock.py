from unittest.mock import MagicMock, patch

import pytest

import nobel_prize_explorer
from nobel_prize_models import (
    BroaderRecognition,
    CareerPosition,
    FAQItem,
    GlossaryItem,
    PersonalBackground,
    PrizeResponse,
    PrizeWinner,
)


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


@pytest.fixture
def mock_explorer():
    with patch("nobel_prize_explorer.LiteClient") as mock_client_cls, \
         patch("nobel_prize_explorer.logging_config.configure_logging", return_value=MagicMock()):
        model_config = MagicMock()
        model_config.model = "test-model"
        model_config.temperature = 0.2
        explorer = nobel_prize_explorer.NobelPrizeWinnerInfo(model_config)
        yield explorer, mock_client_cls.return_value


def test_validate_model_name(mock_explorer):
    explorer, _ = mock_explorer

    explorer._validate_model_name("gpt-4")
    explorer._validate_model_name("gemini/gemini-1.5-pro")

    with pytest.raises(ValueError):
        explorer._validate_model_name("invalid model!")


def test_fetch_winners_runs_generation_then_validation_agent(mock_explorer):
    explorer, mock_client = mock_explorer
    generated_response = make_prize_response()
    validated_response = make_prize_response()
    validated_response.winners[0].name = "Validated Winner"

    mock_client.generate_text.side_effect = [generated_response, validated_response]

    winners = explorer.fetch_winners("Physics", "2023", "test-model")

    assert len(winners) == 1
    assert winners[0].name == "Validated Winner"
    assert mock_client.generate_text.call_count == 2

    first_call = mock_client.generate_text.call_args_list[0]
    first_model_input = first_call.kwargs["model_input"]
    first_model_config = first_call.kwargs["model_config"]
    assert first_model_input.system_prompt == nobel_prize_explorer.PromptBuilder.create_agent_system_prompt("generation_agent")
    assert "Physics" in first_model_input.user_prompt
    assert "2023" in first_model_input.user_prompt
    assert first_model_config.temperature == 0.2

    second_call = mock_client.generate_text.call_args_list[1]
    second_model_input = second_call.kwargs["model_input"]
    second_model_config = second_call.kwargs["model_config"]
    assert second_model_input.system_prompt == nobel_prize_explorer.PromptBuilder.create_agent_system_prompt("validation_agent")
    assert "Candidate JSON" in second_model_input.user_prompt
    assert second_model_config.temperature == 0.0


def test_run_agent_raises_on_invalid_response(mock_explorer):
    explorer, mock_client = mock_explorer
    mock_client.generate_text.return_value = "not-structured-data"

    with pytest.raises(RuntimeError, match="generation_agent returned invalid response"):
        explorer._run_agent(
            agent_name="generation_agent",
            prompt="test prompt",
            model_config=MagicMock(model="test-model"),
        )
