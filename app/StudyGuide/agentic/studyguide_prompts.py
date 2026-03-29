"""PromptBuilder for the 11-agent Rigorous Academic Analysis workflow."""

from typing import List

class PromptBuilder:
    """Builder class for high-rigor, analytical study guide prompts."""
    
    @staticmethod
    def get_planner_prompt(title: str, author: str = None) -> str:
        """Prompt for the planner agent: Strategy & Intellectual Mapping."""
        author_info = f" by {author}" if author else ""
        return f"""You are the planner agent in an 11-agent intellectual deconstruction system.

Your job is to outline the structure of a rigorous academic analysis for "{title}"{author_info}.

CORE MANDATE: 100% CHAPTER COVERAGE.
1.  Identify EVERY single chapter or part in this book. Your plan MUST include a numbered list of all chapters (e.g., Chapter 1 to Chapter 13). DO NOT group them.
2.  For each chapter, identify the core logical argument or narrative arc.
3.  Identify the major characters (for novels) or key entities (for non-fiction).
4.  Identify 3-5 major themes, motifs, and symbols.
5.  Plan for Research Updates, Foundational Scaffolding, Logic Mapping, and Contrarian Perspectives.

Your goal is to build a roadmap that ensures NO detail is missed and every chapter gets its own analytical spotlight."""

    @staticmethod
    def get_research_prompt(title: str, author: str, search_results: str) -> str:
        """Prompt for the research agent: Challenging the Text with 2026 Data."""
        return f"""You are the research agent. Analyze these 2024-2026 search results for "{title}".

Focus on:
1.  **Direct Challenges**: Recent breakthroughs or news that DISPROVE or complicate the author's claims.
2.  **Modern Context**: How current (2026) global or scientific events alter the significance of this book.
3.  **Scholarly Pushback**: Strong, recent academic critiques from the last 2 years.

Provide a dense, cited report."""

    @staticmethod
    def get_prerequisite_prompt(title: str, author: str = None) -> str:
        """Prompt for the foundational agent: Scaffolding the Brain."""
        return f"""Provide the "Intellectual Scaffolding" for "{title}".

What are the 3-5 foundational theories, scientific laws, or philosophical frameworks the reader MUST master to even begin analyzing this work? 
Explain these concepts deeply and why they are the "entry keys" to this book."""

    @staticmethod
    def get_batch_generator_prompt(title: str, author: str, chapters_to_process: List[str], plan_json: str) -> str:
        """Prompt for the generator agent to process a specific batch of chapters."""
        return f"""You are the Deep-Dive Agent. Generate a deconstruction of specific chapters for "{title}" by {author}.

Chapters to process in this batch: {", ".join(chapters_to_process)}

Original Plan Context:
{plan_json}

CORE RULES:
1.  **SUMMARY/ANALYSIS SPLIT**: For EVERY chapter in this batch, provide:
    - **Detailed Summary**: A dense paragraph explaining WHAT happens or WHAT is argued.
    - **Logic & Subtext Analysis**: A dense paragraph explaining HOW the author builds the argument, rhetorical moves, and unspoken biases.
2.  **Rigor**: Maintain a high-level academic tone. No fluff.

Focus only on the chapters assigned to this batch."""

    @staticmethod
    def get_batch_quiz_prompt(title: str, author: str, batch_draft_json: str) -> str:
        """Prompt for the quiz agent to process a specific batch of chapters."""
        return f"""You are the quiz agent. Generate cognitive challenge quizzes for the following chapters of "{title}".

Chapters content:
{batch_draft_json}

Your task:
For EVERY chapter in this batch, provide 3-5 Multiple Choice Questions (MCQs).
RULE: ALL QUESTIONS MUST BE APPLICATION-BASED. No simple recall.
Include the question, 4 options, correct letter, and logical rationalization."""

    @staticmethod
    def get_critique_prompt(title: str, plan_json: str, draft_json: str) -> str:
        """Prompt for the inquisitor agent: Brutal Academic Audit."""
        return f"""You are the Inquisitor. Audit the generated draft for "{title}".

Check for:
1.  **Completeness**: Did the generator skip any chapters from the plan? If even one is missing, flag it as a CRITICAL FAILURE.
2.  **Analytical Depth**: Is the 'Analysis' section just repeating the summary, or is it actually analyzing the subtext and logic?
3.  **Rigor**: Is the language too simple? Demand higher-level academic terminology.

Reject anything that feels like a 'CliffNotes' summary. Demand scholarship."""

    @staticmethod
    def get_relevancy_prompt(title: str, author: str, draft_json: str) -> str:
        """Prompt for the relevancy agent: Alternative Lenses & Counter-Arguments."""
        return f"""Provide the "Contrarian Perspectives" for "{title}".

1.  **Alternative Critical Lenses**: Analyze the text through Feminist, Marxist, or Post-Colonial lenses.
2.  **The Counter-Thesis**: Present the strongest possible academic argument that contradicts the author's main point.
3.  **2026 Application**: How does this logic fail or succeed in a 2026 context?"""

    @staticmethod
    def get_mindmap_prompt(title: str, author: str, draft_json: str) -> str:
        """Prompt for the mindmap agent: Visualizing the Argument."""
        return f"""Generate a Mermaid.js logic map for "{title}".

Map the LOGICAL PROGRESSION of the author's argument. Use `graph TD`. Ensure the causal links between chapters are visualized."""

    @staticmethod
    def get_essay_prompt(title: str, author: str, draft_json: str) -> str:
        """Prompt for the thesis architect: Grade-Boosting Strategy."""
        return f"""Generate 3-5 "Provocative Essay Architectures" for "{title}".

Include a Scholarly Prompt, a 3-Point Thesis, and a paragraph-by-paragraph evidence strategy for each."""

    @staticmethod
    def get_followup_prompt(title: str, author: str, draft_json: str) -> str:
        """Prompt for the growth roadmap agent: The Intellectual Horizon."""
        return f"""Provide the "Intellectual Horizon" for "{title}".

List primary sources, 3 rival theories (books that argue the opposite), and 3 prompts for further independent research."""

    @staticmethod
    def get_reviewer_prompt(title: str, plan_json: str, research_json: str, prereq_json: str, draft_json: str, critique_json: str, relevancy_json: str, mindmap_json: str, essay_json: str, quiz_json: str, followup_json: str) -> str:
        """Prompt for the final auditor agent: Integration & Rigor."""
        return f"""Produce the final **Academic Deconstruction & Scholarly Roadmap** for "{title}".

Your Goal:
1.  **Audit Chapter Coverage**: Ensure EVERY chapter from the plan is included with BOTH summary and analysis.
2.  **Academic Tone**: Ensure the tone is that of a high-level academic journal.
3.  **Structural Integrity**: Ensure the "Logic Map", "Essay Architectures", and "Cognitive Challenges" are integrated for a seamless, high-rigor experience.

The final output must be so comprehensive that the student feels they have mastered the entire intellectual landscape of the book."""
