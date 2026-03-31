"""Pydantic models for the 11-agent Rigorous Academic Analysis workflow."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class BookInput(BaseModel):
    """Input parameters for book summary generation."""
    title: str = Field(..., description="The title of the book to summarize")
    author: Optional[str] = Field(default=None, description="The author of the book")


class SummaryPlanModel(BaseModel):
    """Output from the planner agent defining the summary structure."""
    model_config = ConfigDict(additional_properties=False)
    title: str = Field(..., description="The title of the book.")
    author: Optional[str] = Field(default=None, description="The author of the book.")
    planning_notes: str = Field(..., description="Notes on how the study guide should be structured across all 11 agents.")
    sections: List[str] = Field(..., description="Ordered list of chapters or parts to cover in the summary and analysis.")


class ResearchUpdate(BaseModel):
    """A specific academic or scientific update found via research."""
    model_config = ConfigDict(additional_properties=False)
    title: str = Field(..., description="The title or topic of the research/news update.")
    summary: str = Field(..., description="A summary of the update and its relevance to the book.")
    source_citation: str = Field(..., description="Brief citation or link to the source.")


class ResearchModel(BaseModel):
    """Output from the research agent: Live 2026 academic/scientific updates."""
    model_config = ConfigDict(additional_properties=False)
    latest_updates: List[ResearchUpdate] = Field(..., description="New breakthroughs, studies, or news since the book was published.")
    academic_critiques: List[str] = Field(..., description="Recent scholarly pushback or new interpretations.")


class VocabularyItem(BaseModel):
    """A term and its definition for the entry vocabulary."""
    model_config = ConfigDict(additional_properties=False)
    term: str = Field(..., description="The essential term or jargon.")
    definition: str = Field(..., description="Clear definition of the term.")


class PrerequisiteModel(BaseModel):
    """Output from the prerequisite agent: 'Before You Read'."""
    model_config = ConfigDict(additional_properties=False)
    knowledge_scaffolding: List[str] = Field(..., description="Core concepts needed to understand this book.")
    historical_priming: str = Field(..., description="Brief historical context needed before starting.")
    entry_vocabulary: List[VocabularyItem] = Field(..., description="Top 5-10 essential terms to know before reading.")


class KeyFigure(BaseModel):
    """Represents a key character or historical/scientific figure in the book."""
    model_config = ConfigDict(additional_properties=False)
    name: str = Field(..., description="The name of the character or figure.")
    description: str = Field(..., description="A detailed description and analysis of their role and significance.")


class ThemeMotifSymbol(BaseModel):
    """Represents a major theme, motif, or symbol in the book."""
    model_config = ConfigDict(additional_properties=False)
    name: str = Field(..., description="The name of the theme, motif, or symbol.")
    type: str = Field(..., description="Whether it is a Theme, Motif, or Symbol.")
    analysis: str = Field(..., description="In-depth analysis of how it is used throughout the book.")


class ImportantQuote(BaseModel):
    """An important quote from the book with explanation."""
    model_config = ConfigDict(additional_properties=False)
    quote: str = Field(..., description="The exact quote or a very close paraphrase.")
    speaker_or_context: str = Field(..., description="Who said it, or the context in which it appears.")
    explanation: str = Field(..., description="Detailed explanation of the quote's meaning and significance.")


class ChapterSummaryAndAnalysis(BaseModel):
    """Summary and in-depth analysis for a specific chapter or section."""
    model_config = ConfigDict(additional_properties=False)
    chapter_title: str = Field(..., description="The title of the chapter or section.")
    summary: str = Field(..., description="A detailed summary of the plot or main arguments of the chapter.")
    analysis: str = Field(..., description="A deep analysis of the chapter, explaining the 'why' and 'how', analyzing themes, character development, or logical progression.")


class BatchSummaryResponse(BaseModel):
    """Wrapper for a batch of chapter summaries and analyses."""
    model_config = ConfigDict(additional_properties=False)
    chapters: List[ChapterSummaryAndAnalysis] = Field(..., description="List of chapter summaries and analyses.")


class ModernPerspective(BaseModel):
    """A modern perspective or 'So What?' factor for the book."""
    model_config = ConfigDict(additional_properties=False)
    point: str = Field(..., description="The modern connection or relevancy point.")
    explanation: str = Field(..., description="Detailed explanation of why this matters today (e.g., in 2026).")


class CriticalLens(BaseModel):
    """A specific academic or critical lens (e.g., Feminist, Marxist, Post-colonial)."""
    model_config = ConfigDict(additional_properties=False)
    lens_name: str = Field(..., description="The name of the critical lens.")
    analysis: str = Field(..., description="How the book is interpreted through this specific lens.")


class RelevancyModel(BaseModel):
    """Output from the relevancy agent."""
    model_config = ConfigDict(additional_properties=False)
    modern_perspectives: List[ModernPerspective] = Field(..., description="Connections to modern-day issues, culture, or science.")
    critical_lenses: List[CriticalLens] = Field(..., description="Alternative academic interpretations.")
    cross_curricular_connections: List[str] = Field(..., description="How this book relates to other fields of study.")


class MindMapModel(BaseModel):
    """Output from the mindmap agent: Visual knowledge mapping."""
    model_config = ConfigDict(additional_properties=False)
    mermaid_code: str = Field(..., description="Valid Mermaid.js mindmap or flowchart syntax code.")
    map_description: str = Field(..., description="A brief explanation of what the mindmap represents and how to read it.")


class MultipleChoiceQuestion(BaseModel):
    """A single multiple choice question."""
    model_config = ConfigDict(additional_properties=False)
    question: str = Field(..., description="The question text.")
    options: List[str] = Field(..., description="Four possible options (A, B, C, D).")
    correct_option: str = Field(..., description="The letter of the correct option (e.g., 'A').")
    explanation: str = Field(..., description="Explanation of why the correct option is right and others are distractors.")


class ChapterQuiz(BaseModel):
    """A set of questions for a specific chapter."""
    model_config = ConfigDict(additional_properties=False)
    chapter_title: str = Field(..., description="The title of the chapter this quiz covers.")
    questions: List[MultipleChoiceQuestion] = Field(..., description="3-5 multiple choice questions for this chapter.")


class BatchQuizResponse(BaseModel):
    """Wrapper for a batch of chapter quizzes."""
    model_config = ConfigDict(additional_properties=False)
    quizzes: List[ChapterQuiz] = Field(..., description="List of chapter quizzes.")


class QuizModel(BaseModel):
    """Output from the quiz agent: Active recall per chapter."""
    model_config = ConfigDict(additional_properties=False)
    chapter_quizzes: List[ChapterQuiz] = Field(..., description="List of per-chapter quizzes.")


class EssayBodyParagraph(BaseModel):
    """A single body paragraph outline for an essay."""
    model_config = ConfigDict(additional_properties=False)
    sub_thesis: str = Field(..., description="The main point or topic sentence of this paragraph.")
    supporting_evidence: List[str] = Field(..., description="Key arguments or points to support the sub-thesis.")
    suggested_quotes: List[str] = Field(..., description="Specific quotes from the book to use in this paragraph.")


class EssayTopic(BaseModel):
    """A complete essay architecture for a specific prompt."""
    model_config = ConfigDict(additional_properties=False)
    prompt: str = Field(..., description="The essay prompt or question.")
    thesis_statement: str = Field(..., description="A strong, 3-point thesis statement.")
    introduction_hooks: List[str] = Field(..., description="Suggested hooks or opening strategies.")
    body_paragraphs: List[EssayBodyParagraph] = Field(..., description="Detailed outlines for 3-4 body paragraphs.")
    conclusion_strategy: str = Field(..., description="How to synthesize the arguments and end with a 'larger significance' statement.")


class EssayArchitectModel(BaseModel):
    """Output from the essay architect agent: Grade-boosting essay outlines."""
    model_config = ConfigDict(additional_properties=False)
    essay_topics: List[EssayTopic] = Field(..., description="3-5 high-yield essay architectures based on the book's major themes.")


class ReadingRecommendation(BaseModel):
    """A curated reading recommendation."""
    model_config = ConfigDict(additional_properties=False)
    title: str = Field(..., description="Title of the recommended book or article.")
    author: str = Field(..., description="Author of the recommended work.")
    why_it_relates: str = Field(..., description="Brief explanation of how it connects to the primary book.")


class MediaItem(BaseModel):
    """A recommended media connection (documentary, podcast, etc.)."""
    model_config = ConfigDict(additional_properties=False)
    type: str = Field(..., description="Type of media (e.g., Film, Podcast, Documentary).")
    title: str = Field(..., description="Title of the media connection.")
    description: str = Field(..., description="Brief overview of the media content.")


class FollowUpModel(BaseModel):
    """Output from the follow-up agent: 'Beyond the Book'."""
    model_config = ConfigDict(additional_properties=False)
    further_reading: List[ReadingRecommendation] = Field(..., description="Curated reading list.")
    actionable_next_steps: List[str] = Field(..., description="Exercises, reflection prompts, or practical applications.")
    media_connections: List[MediaItem] = Field(..., description="Documentaries, films, or podcasts.")


class PracticeQuestion(BaseModel):
    """A practice question for exam preparation."""
    model_config = ConfigDict(additional_properties=False)
    question: str = Field(..., description="A potential exam or essay question.")
    answer: str = Field(..., description="The correct answer or key points to include in an essay answer.")


class StudyGuideModel(BaseModel):
    """Complete response containing an 11-agent SparkNotes-style study guide."""
    model_config = ConfigDict(additional_properties=False)
    title: str = Field(..., description="The title of the book.")
    author: Optional[str] = Field(default=None, description="The author of the book.")
    prerequisites: Optional[PrerequisiteModel] = Field(default=None, description="Before You Read scaffolding.")
    research_updates: Optional[ResearchModel] = Field(default=None, description="Live 2026 academic/scientific updates.")
    context_and_background: str = Field(..., description="Historical, biographical, and literary/scientific context of the book.")
    plot_or_overall_summary: str = Field(..., description="A high-level executive summary or plot overview of the entire book.")
    mindmap: Optional[MindMapModel] = Field(default=None, description="Visual knowledge map in Mermaid syntax.")
    character_list: List[KeyFigure] = Field(..., description="List of key characters or important figures.")
    themes_motifs_symbols: List[ThemeMotifSymbol] = Field(..., description="The main themes, motifs, and symbols explored in the book.")
    chapter_summaries_and_analyses: List[ChapterSummaryAndAnalysis] = Field(..., description="Detailed summaries and analyses for each chapter or part.")
    relevancy_analysis: Optional[RelevancyModel] = Field(default=None, description="Modern relevancy and critical perspective updates.")
    important_quotes_explained: List[ImportantQuote] = Field(..., description="Crucial quotes from the book with in-depth explanations.")
    essay_architect: Optional[EssayArchitectModel] = Field(default=None, description="Grade-boosting essay architectures and outlines.")
    chapter_quizzes: Optional[QuizModel] = Field(default=None, description="Per-chapter active recall quizzes.")
    follow_up: Optional[FollowUpModel] = Field(default=None, description="Beyond the Book roadmap.")
    study_questions: List[PracticeQuestion] = Field(..., description="Comprehensive study and essay questions covering the entire book.")
    agent_trace: Optional["AgentTrace"] = Field(default=None, description="Metadata from the eleven-agent workflow.")


class CritiqueItem(BaseModel):
    """A specific critique or suggestion for improvement."""
    model_config = ConfigDict(additional_properties=False)
    section: str = Field(..., description="The section of the summary being critiqued.")
    issue: str = Field(..., description="Description of the flaw or area for improvement.")
    suggestion: str = Field(..., description="A concrete suggestion on how to fix the issue.")


class CritiqueModel(BaseModel):
    """Output from the critique agent."""
    model_config = ConfigDict(additional_properties=False)
    overall_score: int = Field(..., ge=1, le=10, description="Quality score from 1-10.")
    critiques: List[CritiqueItem] = Field(..., description="List of specific critiques.")
    strengths: List[str] = Field(..., description="List of what the draft did well.")


class AgentTrace(BaseModel):
    """Brief metadata showing the eleven-agent pipeline."""
    model_config = ConfigDict(additional_properties=False)
    planner_notes: str = Field(..., description="Planner summary used by the generator.")
    research_notes: Optional[str] = Field(default=None, description="Live research findings and source notes.")
    prerequisite_notes: Optional[str] = Field(default=None, description="Before-you-read scaffolding notes.")
    critique_notes: Optional[str] = Field(default=None, description="Structured feedback from the critique agent.")
    relevancy_notes: Optional[str] = Field(default=None, description="Modern context and critical lens notes.")
    mindmap_notes: Optional[str] = Field(default=None, description="Visual mapping and Mermaid syntax notes.")
    essay_notes: Optional[str] = Field(default=None, description="Essay architecture and thesis strategy notes.")
    quiz_notes: Optional[str] = Field(default=None, description="Per-chapter quiz and retrieval practice notes.")
    follow_up_notes: Optional[str] = Field(default=None, description="Post-reading roadmap notes.")
    reviewer_summary: str = Field(..., description="Reviewer summary of checks and fixes.")
    revision_count: int = Field(default=0, description="How many material corrections the reviewer made.")


class ReviewIssue(BaseModel):
    """One issue found by the reviewer."""
    model_config = ConfigDict(additional_properties=False)
    section: str = Field(..., description="The affected section of the summary.")
    severity: str = Field(..., description="Issue severity, such as low, medium, or high.")
    issue: str = Field(..., description="Description of the issue found.")
    fix: str = Field(..., description="What was changed or should be changed.")


class ReviewedStudyGuideModel(BaseModel):
    """Reviewer output containing the corrected final summary."""
    model_config = ConfigDict(additional_properties=False)
    reviewer_summary: str = Field(..., description="Summary of checks and corrections performed.")
    revision_count: int = Field(..., description="Count of meaningful fixes made by the reviewer.")
    issues_found: List[ReviewIssue] = Field(default_factory=list, description="Issues discovered during review.")
    final_summary: StudyGuideModel = Field(..., description="The corrected final book summary.")


# Handle forward reference
StudyGuideModel.model_rebuild()
