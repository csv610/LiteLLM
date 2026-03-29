# StudyGuide Agentic: Rigorous Academic Deconstruction

A sophisticated 11-agent AI pipeline designed to generate exhaustive, scholarly study guides for any book. Unlike simple summaries, this system performs a deep "academic deconstruction," combining plot analysis with logical mapping, live research updates (up to 2026), and cognitive challenges.

## 🚀 Features

- **Direct-Streaming Architecture**: Processes books in batches to prevent LLM truncation, ensuring 100% chapter coverage regardless of book length.
- **11-Agent Scholarly Pipeline**:
  - **Planner**: Maps the intellectual landscape and identifies every chapter/part.
  - **Prerequisite Agent**: Scaffolds foundational knowledge and essential vocabulary before reading.
  - **Research Agent**: Injects 2026 academic breakthroughs, news, and scholarly critiques.
  - **Logic Mapping**: Generates Mermaid.js visualizations of the author's argument architecture.
  - **Deep-Dive Deconstruction**: Provides dual **Summary + Subtext Analysis** for every chapter.
  - **Cognitive Challenges**: Generates application-based MCQs with hidden rationalizations.
  - **Contrarian Perspectives**: Analyzes the text through multiple critical lenses (Feminist, Marxist, etc.) and counter-arguments.
  - **Essay Architect**: Provides high-yield thesis statements and paragraph-by-paragraph evidence strategies.
  - **Intellectual Horizon**: Recommends rival theories, primary sources, and media connections (podcasts, films).
- **Pure Markdown Output**: High-quality, formatted reports saved automatically to the `outputs/` folder.

## 🛠️ Installation

1. Ensure you have Python 3.8+ installed.
2. Install the required Pydantic library:
   ```bash
   pip install pydantic
   ```
   *(Note: This project relies on a local `lite` orchestration library for LLM communication.)*

## 📖 Usage

Generate a study guide via the CLI:

```bash
# Basic usage
python studyguide_cli.py "The Great Gatsby"

# With author and specific model
python studyguide_cli.py "Thinking, Fast and Slow" -a "Daniel Kahneman" -m "ollama/gemma3"
```

### Options:
- `title`: (Required) The title of the book to summarize.
- `-a`, `--author`: (Optional) The author of the book for better accuracy.
- `-m`, `--model`: (Optional) The LLM model to use (default: `ollama/gemma3`).

## 📁 Project Structure

- `studyguide_cli.py`: Entry point for the command-line interface.
- `studyguide_generator.py`: The core orchestration engine managing agent handoffs and file streaming.
- `studyguide_models.py`: Pydantic definitions ensuring strict data integrity across agents.
- `studyguide_prompts.py`: The analytical "brain" containing system prompts for all 11 agents.
- `outputs/`: Destination for generated Markdown study guides.
- `logs/`: Application execution logs for debugging and auditing.

## 🧠 The "Eleven-Agent" Workflow

The system utilizes a specialized workflow to ensure academic rigor:
1. **Intellectual Scaffolding**: Before summarizing, it identifies the "entry keys" (theories/vocabulary) needed to understand the work.
2. **Contextual Injection**: It fetches live research to challenge or support the book's claims with modern data.
3. **Recursive Batching**: To maintain high density, chapters are processed in focused batches, preventing the "skimming" effect common in standard AI summaries.
4. **Scholarly Synthesis**: The final sections provide tools for further research, essay writing, and critical debate.

---
*Engineered for high-rigor academic analysis.*
