import asyncio
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from . import riemann_problems as guide_module
from . import riemann_problems_agent as agent_module
from . import riemann_problems_cli as cli_module
from .riemann_problems_models import (
    RiemannAppliedImpactModel,
    RiemannOverviewModel,
    RiemannTechnicalModel,
    RiemannTheoryModel,
)


class DummyClient:
    def __init__(self, config, responses=None):
        self.config = config
        self.responses = list(responses or [])
        self.calls = []

    def generate_text(self, model_input):
        self.calls.append(model_input)
        if not self.responses:
            raise AssertionError("No fake response configured for generate_text()")
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


@pytest.fixture
def sample_theory():
    return RiemannTheoryModel(
        name="Riemann Hypothesis",
        layperson_explanation="A conjecture about where special zeros appear.",
        intuition="It reveals hidden structure in prime numbers.",
        historical_context="It was proposed in 1859.",
        motivation="Understand the distribution of primes.",
        definition="All nontrivial zeros of zeta have real part one half.",
        misconceptions=["It is already proved."],
        limitations="It remains unproved.",
        modern_developments="Computational checks support it.",
        key_properties=["Critical line"],
        related_concepts=["Riemann zeta function"],
        applications=["Analytic number theory"],
        significance="It is a central open problem.",
        counterfactual_impact="Modern number theory would look different.",
    )


def test_generate_text_builds_structured_request(monkeypatch, sample_theory):
    fake_client = DummyClient(None, responses=[sample_theory])
    monkeypatch.setattr(guide_module, "LiteClient", lambda config: fake_client)

    guide = guide_module.RiemannTheoryGuide()
    result = guide.generate_text("Riemann Hypothesis")

    assert result == sample_theory
    assert len(fake_client.calls) == 1
    model_input = fake_client.calls[0]
    assert "Riemann theory" in model_input.user_prompt
    assert model_input.response_format is RiemannTheoryModel


def test_generate_text_returns_none_on_non_structured_response(monkeypatch):
    fake_client = DummyClient(None, responses=["plain text"])
    monkeypatch.setattr(guide_module, "LiteClient", lambda config: fake_client)

    guide = guide_module.RiemannTheoryGuide()

    assert guide.generate_text("Riemann Hypothesis") is None


def test_save_to_file_persists_json(monkeypatch, tmp_path, sample_theory):
    monkeypatch.setattr(guide_module, "LiteClient", lambda config: DummyClient(config))
    guide = guide_module.RiemannTheoryGuide()

    saved_path = Path(guide.save_to_file(sample_theory, str(tmp_path)))

    assert saved_path.exists()
    assert saved_path.name == "riemann_riemann_hypothesis.json"
    assert json.loads(saved_path.read_text(encoding="utf-8"))["name"] == sample_theory.name


def test_display_theory_prints_sections(capsys, sample_theory):
    guide_module.RiemannTheoryGuide.display_theory(sample_theory)

    output = capsys.readouterr().out
    assert "RIEMANN THEORY: RIEMANN HYPOTHESIS" in output
    assert "COMMON MISCONCEPTIONS:" in output
    assert "APPLICATIONS:" in output


def test_display_summary_uses_available_theories(monkeypatch, capsys):
    fake_client = DummyClient(None, responses=["Grouped summary"])
    monkeypatch.setattr(guide_module, "LiteClient", lambda config: fake_client)

    guide = guide_module.RiemannTheoryGuide()
    guide.available_theories = ["Riemann surface", "Riemann hypothesis"]
    guide.display_summary()

    output = capsys.readouterr().out
    assert "SUMMARY OF RIEMANN THEORIES AND CONCEPTS" in output
    assert "Grouped summary" in output
    assert len(fake_client.calls) == 1
    assert "Riemann surface" in fake_client.calls[0].user_prompt


def test_display_summary_handles_client_error(monkeypatch, capsys):
    fake_client = DummyClient(None, responses=[RuntimeError("backend unavailable")])
    monkeypatch.setattr(guide_module, "LiteClient", lambda config: fake_client)

    guide = guide_module.RiemannTheoryGuide()
    guide.available_theories = ["Riemann surface"]
    guide.display_summary()

    output = capsys.readouterr().out
    assert "Error fetching summary" in output


def test_run_pipeline_orchestrates_all_agents(monkeypatch):
    overview = RiemannOverviewModel(
        name="Riemann surface",
        layperson_explanation="A shaped space for complex values.",
        intuition="It turns branching into geometry.",
        historical_context="Developed in the 19th century.",
        motivation="Handle multivalued complex functions cleanly.",
    )
    technical = RiemannTechnicalModel(
        definition="A connected one-dimensional complex manifold.",
        misconceptions=["It is just a 2D surface in space."],
        limitations="Classification can be hard in general.",
        modern_developments="It remains central in geometry and physics.",
        key_properties=["Complex structure"],
        related_concepts=["Complex manifold"],
    )
    applied = RiemannAppliedImpactModel(
        applications=["String theory"],
        significance="It connects analysis, topology, and geometry.",
        counterfactual_impact="Several modern fields would have developed differently.",
    )

    fake_client = DummyClient(None, responses=[
        "historical brief",
        overview,
        technical,
        applied,
        "PASS",
    ])
    monkeypatch.setattr(agent_module, "LiteClient", lambda config: fake_client)

    result = asyncio.run(agent_module.run_riemann_agent("Riemann surface"))

    assert isinstance(result, RiemannTheoryModel)
    assert result.name == "Riemann surface"
    assert result.applications == ["String theory"]
    assert len(fake_client.calls) == 5


def test_run_pipeline_surfaces_critic_failure(monkeypatch, capsys):
    fake_client = DummyClient(None, responses=[
        "brief",
        RiemannOverviewModel(
            name="X",
            layperson_explanation="lp",
            intuition="int",
            historical_context="hist",
            motivation="mot",
        ),
        RiemannTechnicalModel(
            definition="def",
            misconceptions=["m"],
            limitations="lim",
            modern_developments="mod",
            key_properties=["k"],
            related_concepts=["r"],
        ),
        RiemannAppliedImpactModel(
            applications=["app"],
            significance="sig",
            counterfactual_impact="cf",
        ),
        "Needs consistency fixes",
    ])
    monkeypatch.setattr(agent_module, "LiteClient", lambda config: fake_client)

    asyncio.run(agent_module.run_riemann_agent("X"))

    output = capsys.readouterr().out
    assert "Critic Feedback" in output


def test_cli_list_mode_prints_available_theories(monkeypatch, capsys):
    class FakeGuide:
        def __init__(self, config):
            self.available_theories = ["A", "B"]

        def display_summary(self):
            raise AssertionError("display_summary should not run in list mode")

    monkeypatch.setattr(cli_module, "RiemannTheoryGuide", FakeGuide)
    monkeypatch.setattr(cli_module.sys, "argv", ["riemann_problems_cli.py", "--list"])

    cli_module.main()

    output = capsys.readouterr().out
    assert "Available Riemann Theories" in output
    assert " - A" in output


def test_cli_default_summary_mode(monkeypatch):
    called = {"summary": False}

    class FakeGuide:
        def __init__(self, config):
            self.available_theories = ["A"]

        def display_summary(self):
            called["summary"] = True

    monkeypatch.setattr(cli_module, "RiemannTheoryGuide", FakeGuide)
    monkeypatch.setattr(cli_module.sys, "argv", ["riemann_problems_cli.py"])

    cli_module.main()

    assert called["summary"] is True


def test_cli_theory_mode_runs_async_agent(monkeypatch):
    captured = {}

    async def fake_run_agent_generation(theory_name, model):
        captured["theory_name"] = theory_name
        captured["model"] = model

    monkeypatch.setattr(cli_module, "run_agent_generation", fake_run_agent_generation)
    monkeypatch.setattr(cli_module, "RiemannTheoryGuide", lambda config: type("FakeGuide", (), {"available_theories": []})())
    monkeypatch.setattr(cli_module.sys, "argv", ["riemann_problems_cli.py", "-t", "Riemann surface", "-m", "demo/model"])

    cli_module.main()

    assert captured == {"theory_name": "Riemann surface", "model": "demo/model"}
