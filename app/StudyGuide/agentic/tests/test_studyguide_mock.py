import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
import os
import shutil

from studyguide_models import (
    BookInput,
    SummaryPlanModel,
    ResearchModel,
    ResearchUpdate,
    PrerequisiteModel,
    VocabularyItem,
    RelevancyModel,
    ModernPerspective,
    CriticalLens,
    MindMapModel,
    EssayArchitectModel,
    EssayTopic,
    EssayBodyParagraph,
    BatchSummaryResponse,
    ChapterSummaryAndAnalysis,
    BatchQuizResponse,
    ChapterQuiz,
    MultipleChoiceQuestion,
    FollowUpModel,
    ReadingRecommendation,
    MediaItem
)
from studyguide_generator import StudyGuideGenerator
from lite.config import ModelConfig

@pytest.fixture
def mock_lite_client():
    with patch('studyguide_generator.LiteClient') as mock:
        yield mock

@pytest.fixture
def temp_outputs(tmp_path):
    # Mocking the parent directory to use a temporary one for outputs
    with patch('studyguide_generator.Path') as mock_path:
        # We need to make sure Path(__file__).parent / "outputs" works
        mock_path.return_value.parent.__truediv__.return_value = tmp_path
        yield tmp_path

def test_studyguide_generator_init(mock_lite_client):
    config = ModelConfig(model="test-model")
    generator = StudyGuideGenerator(config)
    assert generator.model == "test-model"
    mock_lite_client.assert_called_once_with(model_config=config)

def test_generate_and_save_mock(mock_lite_client, tmp_path):
    # Setup mock responses
    mock_instance = mock_lite_client.return_value
    
    def mock_generate_text(model_input):
        fmt = model_input.response_format
        if fmt == SummaryPlanModel:
            return SummaryPlanModel(
                title="Test Book",
                author="Test Author",
                planning_notes="Test Notes",
                sections=["Chapter 1", "Chapter 2"]
            )
        elif fmt == PrerequisiteModel:
            return PrerequisiteModel(
                knowledge_scaffolding=["Concept 1"],
                historical_priming="Priming text",
                entry_vocabulary=[VocabularyItem(term="Term 1", definition="Def 1")]
            )
        elif fmt == ResearchModel:
            return ResearchModel(
                latest_updates=[ResearchUpdate(title="Update 1", summary="Sum 1", source_citation="Cit 1")],
                academic_critiques=["Critique 1"]
            )
        elif fmt == MindMapModel:
            return MindMapModel(
                mermaid_code="graph TD; A-->B",
                map_description="Map Desc"
            )
        elif fmt == BatchSummaryResponse:
            return BatchSummaryResponse(
                chapters=[
                    ChapterSummaryAndAnalysis(chapter_title="Chapter 1", summary="Sum 1", analysis="Ana 1"),
                    ChapterSummaryAndAnalysis(chapter_title="Chapter 2", summary="Sum 2", analysis="Ana 2")
                ]
            )
        elif fmt == BatchQuizResponse:
            return BatchQuizResponse(
                quizzes=[
                    ChapterQuiz(chapter_title="Chapter 1", questions=[
                        MultipleChoiceQuestion(question="Q1", options=["A", "B"], correct_option="A", explanation="E1")
                    ]),
                    ChapterQuiz(chapter_title="Chapter 2", questions=[
                        MultipleChoiceQuestion(question="Q2", options=["C", "D"], correct_option="C", explanation="E2")
                    ])
                ]
            )
        elif fmt == RelevancyModel:
            return RelevancyModel(
                modern_perspectives=[ModernPerspective(point="Point 1", explanation="Exp 1")],
                critical_lenses=[CriticalLens(lens_name="Lens 1", analysis="Ana 1")],
                cross_curricular_connections=["Conn 1"]
            )
        elif fmt == EssayArchitectModel:
            return EssayArchitectModel(
                essay_topics=[EssayTopic(
                    prompt="Prompt 1",
                    thesis_statement="Thesis 1",
                    introduction_hooks=["Hook 1"],
                    body_paragraphs=[EssayBodyParagraph(sub_thesis="Sub 1", supporting_evidence=["Ev 1"], suggested_quotes=["Quote 1"])],
                    conclusion_strategy="Strat 1"
                )]
            )
        elif fmt == FollowUpModel:
            return FollowUpModel(
                further_reading=[ReadingRecommendation(title="Rec 1", author="Aut 1", why_it_relates="Why 1")],
                actionable_next_steps=["Step 1"],
                media_connections=[MediaItem(type="Film", title="Film 1", description="Desc 1")]
            )
        return None

    mock_instance.generate_text.side_effect = mock_generate_text
    
    # Mocking Path in StudyGuideGenerator to point to tmp_path
    with patch('studyguide_generator.Path') as mock_path_class:
        # This is tricky because we use Path(__file__).parent
        # Let's mock it so that output_dir = tmp_path / "outputs"
        mock_parent = MagicMock()
        mock_path_class.return_value.parent = mock_parent
        mock_outputs = tmp_path / "outputs"
        mock_parent.__truediv__.return_value = mock_outputs
        
        config = ModelConfig(model="test-model")
        generator = StudyGuideGenerator(config)
        book_input = BookInput(title="Test Book", author="Test Author")
        
        output_file_str = generator.generate_and_save(book_input)
        output_file = Path(output_file_str)
        
        assert output_file.exists()
        content = output_file.read_text()
        
        assert "# Comprehensive Academic Deconstruction: Test Book" in content
        assert "Test Author" in content
        assert "## 0. Executive Summary & Strategy" in content
        assert "Test Notes" in content
        assert "## I. Foundations for Critical Thought" in content
        assert "Concept 1" in content
        assert "Term 1" in content
        assert "## II. Live Research & Academic Updates (2026)" in content
        assert "Update 1" in content
        assert "## III. Logic & Argument Architecture" in content
        assert "mermaid" in content
        assert "graph TD; A-->B" in content
        assert "## IV. Chapter-by-Chapter Deep Deconstruction" in content
        assert "Chapter 1" in content
        assert "Chapter 2" in content
        assert "Q1" in content
        assert "Q2" in content
        assert "## V. Contrarian Perspectives & Modern Relevancy" in content
        assert "Lens 1" in content
        assert "Conn 1" in content
        assert "## VI. Scholarly Essay Architectures" in content
        assert "Thesis 1" in content
        assert "## VII. The Intellectual Horizon (Beyond the Book)" in content
        assert "Rec 1" in content
        assert "Film 1" in content
        assert "## VIII. Metadata & Agent Trace" in content
        assert "test-model" in content
