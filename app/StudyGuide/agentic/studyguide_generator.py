"""Direct-streaming book summary generator: prevents truncation by writing batches directly to disk."""

import json
from pathlib import Path
import sys
from typing import List

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lite.lite_client import LiteClient
from lite.config import ModelConfig, ModelInput
from studyguide_models import (
    AgentTrace,
    StudyGuideModel,
    BookInput,
    SummaryPlanModel,
    ResearchModel,
    PrerequisiteModel,
    CritiqueModel,
    RelevancyModel,
    MindMapModel,
    EssayArchitectModel,
    QuizModel,
    BatchSummaryResponse,
    BatchQuizResponse,
    ChapterQuiz,
    ChapterSummaryAndAnalysis,
    FollowUpModel,
    ReviewedStudyGuideModel,
)
from studyguide_prompts import PromptBuilder


class StudyGuideGenerator:
    """Generator class for the eleven-agent direct-streaming workflow."""
    
    def __init__(self, model_config: ModelConfig):
        """
        Initialize the generator with model configuration.
        """
        self.model_config = model_config
        self.model = model_config.model or "ollama/gemma3"
        self.client = LiteClient(model_config=model_config)

    def _run_planner_agent(self, book_input: BookInput) -> SummaryPlanModel:
        """Run the planner agent."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_planner_prompt(book_input.title, book_input.author),
            response_format=SummaryPlanModel,
        )
        response = self.client.generate_text(model_input=model_input)
        if isinstance(response, SummaryPlanModel): return response
        raise ValueError(f"Expected SummaryPlanModel, got {type(response).__name__}")

    def _run_research_agent(self, book_input: BookInput) -> ResearchModel:
        """Run the research agent."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_research_prompt(book_input.title, book_input.author, "Live academic search results 2024-2026."),
            response_format=ResearchModel,
        )
        response = self.client.generate_text(model_input=model_input)
        if isinstance(response, ResearchModel): return response
        return ResearchModel(latest_updates=[], academic_critiques=[])

    def _run_prerequisite_agent(self, book_input: BookInput) -> PrerequisiteModel:
        """Run the prerequisite agent."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_prerequisite_prompt(book_input.title, book_input.author),
            response_format=PrerequisiteModel,
        )
        response = self.client.generate_text(model_input=model_input)
        if isinstance(response, PrerequisiteModel): return response
        raise ValueError(f"Expected PrerequisiteModel, got {type(response).__name__}")

    def _run_batch_generator(self, book_input: BookInput, chapters: List[str], plan: SummaryPlanModel) -> List[ChapterSummaryAndAnalysis]:
        """Run the generator agent for a batch."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_batch_generator_prompt(book_input.title, book_input.author, chapters, json.dumps(plan.model_dump(), indent=2)),
            response_format=BatchSummaryResponse,
        )
        response = self.client.generate_text(model_input=model_input)
        if isinstance(response, BatchSummaryResponse): return response.chapters
        raise ValueError(f"Expected BatchSummaryResponse, got {type(response).__name__}")

    def _run_batch_quiz(self, book_input: BookInput, batch_content: List[ChapterSummaryAndAnalysis]) -> List[ChapterQuiz]:
        """Run the quiz agent for a batch."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_batch_quiz_prompt(book_input.title, book_input.author, json.dumps([x.model_dump() for x in batch_content], indent=2)),
            response_format=BatchQuizResponse,
        )
        response = self.client.generate_text(model_input=model_input)
        if isinstance(response, BatchQuizResponse): return response.quizzes
        raise ValueError(f"Expected BatchQuizResponse, got {type(response).__name__}")

    def _run_mindmap_agent(self, book_input: BookInput, plan: SummaryPlanModel) -> MindMapModel:
        """Run the mindmap agent."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_mindmap_prompt(book_input.title, book_input.author, json.dumps(plan.model_dump(), indent=2)),
            response_format=MindMapModel,
        )
        response = self.client.generate_text(model_input=model_input)
        if isinstance(response, MindMapModel): return response
        raise ValueError(f"Expected MindMapModel, got {type(response).__name__}")

    def _run_relevancy_agent(self, book_input: BookInput, plan: SummaryPlanModel) -> RelevancyModel:
        """Run the relevancy agent."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_relevancy_prompt(book_input.title, book_input.author, json.dumps(plan.model_dump(), indent=2)),
            response_format=RelevancyModel,
        )
        response = self.client.generate_text(model_input=model_input)
        if isinstance(response, RelevancyModel): return response
        raise ValueError(f"Expected RelevancyModel, got {type(response).__name__}")

    def _run_essay_agent(self, book_input: BookInput, plan: SummaryPlanModel) -> EssayArchitectModel:
        """Run the essay agent."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_essay_prompt(book_input.title, book_input.author, json.dumps(plan.model_dump(), indent=2)),
            response_format=EssayArchitectModel,
        )
        response = self.client.generate_text(model_input=model_input)
        if isinstance(response, EssayArchitectModel): return response
        raise ValueError(f"Expected EssayArchitectModel, got {type(response).__name__}")

    def _run_followup_agent(self, book_input: BookInput, plan: SummaryPlanModel) -> FollowUpModel:
        """Run the follow-up agent."""
        model_input = ModelInput(
            user_prompt=PromptBuilder.get_followup_prompt(book_input.title, book_input.author, json.dumps(plan.model_dump(), indent=2)),
            response_format=FollowUpModel,
        )
        response = self.client.generate_text(model_input=model_input)
        if isinstance(response, FollowUpModel): return response
        raise ValueError(f"Expected FollowUpModel, got {type(response).__name__}")

    def generate_and_save(self, book_input: BookInput) -> str:
        """Main orchestrator: Streams content directly to Markdown file."""
        title_norm = book_input.title.replace(' ', '_').lower()
        filename = f"{title_norm}_summary.md"
        
        # Start fresh
        with open(filename, 'w') as f:
            f.write(f"# Comprehensive Academic Deconstruction: {book_input.title}\n")
            if book_input.author: f.write(f"**Author:** {book_input.author}\n\n")

        print(f"Step 1: Planning...")
        plan = self._run_planner_agent(book_input)
        
        print(f"Step 2: Intellectual Scaffolding...")
        prereq = self._run_prerequisite_agent(book_input)
        with open(filename, 'a') as f:
            f.write("## I. Foundations for Critical Thought\n")
            f.write("### Knowledge Scaffolding\n")
            for item in prereq.knowledge_scaffolding:
                f.write(f"- {item}\n")
            f.write(f"\n### Historical Priming\n{prereq.historical_priming}\n\n")
            f.write("### Core Intellectual Vocabulary\n")
            for vocab in prereq.entry_vocabulary:
                f.write(f"- **{vocab.term}:** {vocab.definition}\n")
            f.write("\n")

        print(f"Step 3: Live Research...")
        research = self._run_research_agent(book_input)
        with open(filename, 'a') as f:
            f.write("## II. Live Research & Academic Updates (2026)\n")
            for update in research.latest_updates:
                f.write(f"- **{update.title}:** {update.summary} (*Source: {update.source_citation}*)\n")
            if research.academic_critiques:
                f.write("\n#### Recent Academic Critiques\n")
                for critique in research.academic_critiques:
                    f.write(f"- {critique}\n")
            f.write("\n")

        print(f"Step 4: Logic Mapping...")
        mindmap = self._run_mindmap_agent(book_input, plan)
        with open(filename, 'a') as f:
            f.write("## III. Logic & Argument Architecture\n")
            f.write(f"{mindmap.map_description}\n\n")
            clean_code = mindmap.mermaid_code.replace("```mermaid", "").replace("```", "").strip()
            f.write(f"```mermaid\n{clean_code}\n```\n\n")

        print(f"Step 5: Chapter-by-Chapter Deep Dive (Batch Streaming)...")
        with open(filename, 'a') as f:
            f.write("## IV. Chapter-by-Chapter Deep Deconstruction\n")
            
        all_chapters = plan.sections
        batch_size = 2
        for i in range(0, len(all_chapters), batch_size):
            batch = all_chapters[i:i + batch_size]
            print(f"  Processing: {', '.join(batch)}")
            summaries = self._run_batch_generator(book_input, batch, plan)
            quizzes = self._run_batch_quiz(book_input, summaries)
            
            quiz_map = {q.chapter_title: q for q in quizzes}
            with open(filename, 'a') as f:
                for ch in summaries:
                    f.write(f"### {ch.chapter_title}\n")
                    f.write(f"**Summary:**\n{ch.summary}\n\n")
                    f.write(f"**Logic & Subtext Analysis:**\n{ch.analysis}\n\n")
                    if ch.chapter_title in quiz_map:
                        f.write("---\n**🧠 Cognitive Challenge: " + ch.chapter_title + "**\n\n")
                        for idx, q in enumerate(quiz_map[ch.chapter_title].questions):
                            f.write(f"{idx+1}. {q.question}\n")
                            for opt in q.options: f.write(f"   - {opt}\n")
                            f.write(f"\n   <details>\n   <summary>View Rationalization</summary>\n\n   **Correct Answer: {q.correct_option}**\n\n   {q.explanation}\n   </details>\n\n")
                        f.write("---\n\n")

        print(f"Step 6: Contrarian Perspectives...")
        relevancy = self._run_relevancy_agent(book_input, plan)
        with open(filename, 'a') as f:
            f.write("## V. Contrarian Perspectives & Modern Relevancy\n")
            for p in relevancy.modern_perspectives:
                f.write(f"- **{p.point}:** {p.explanation}\n")
            f.write("\n### Alternative Critical Lenses\n")
            for lens in relevancy.critical_lenses:
                f.write(f"- **{lens.lens_name} Analysis:** {lens.analysis}\n")
            f.write("\n")

        print(f"Step 7: Essay Architect...")
        essay = self._run_essay_agent(book_input, plan)
        with open(filename, 'a') as f:
            f.write("## VI. Scholarly Essay Architectures\n")
            for topic in essay.essay_topics:
                f.write(f"### Topic: {topic.prompt}\n")
                f.write(f"**Thesis:** {topic.thesis_statement}\n\n")
                f.write("**Introduction Hooks:**\n")
                for hook in topic.introduction_hooks: f.write(f"- {hook}\n")
                f.write("\n**Paragraph-by-Paragraph Strategy:**\n")
                for idx, bp in enumerate(topic.body_paragraphs):
                    f.write(f"{idx+1}. *{bp.sub_thesis}*\n")
                    for arg in bp.supporting_evidence: f.write(f"   - {arg}\n")
                    f.write("   - **Suggested Quotes:** " + ", ".join(bp.suggested_quotes) + "\n")
                f.write(f"\n**Conclusion Strategy:** {topic.conclusion_strategy}\n\n")

        print(f"Step 8: Intellectual Horizon...")
        followup = self._run_followup_agent(book_input, plan)
        with open(filename, 'a') as f:
            f.write("## VII. The Intellectual Horizon (Beyond the Book)\n")
            f.write("### Further Reading & Rival Theories\n")
            for book in followup.further_reading:
                f.write(f"- **{book.title}** by {book.author}: {book.why_it_relates}\n")
            f.write("\n### Actionable Next Steps & Research Inquiries\n")
            for step in followup.actionable_next_steps:
                f.write(f"- {step}\n")
            f.write("\n")

        print(f"Academic Deconstruction Complete: {filename}")
        return filename
