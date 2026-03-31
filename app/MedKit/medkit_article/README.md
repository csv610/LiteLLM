# MedKit Article

This package groups article-oriented MedKit modules.

## What It Includes

- `search`: article search
- `review`: article review
- `compare`: article comparison
- `summarize`: article summary
- `keywords`: keyword extraction

## Entry Point

- `article_cli.py`: unified CLI used by `medkit-article`

## Why It Matters

These modules support literature-oriented workflows without requiring users to move between unrelated tools.

## Agentic Approach Integration

These article modules are designed to be used within the MedKit agentic framework, particularly by the LiteratureAgent:

1. **LiteratureAgent Utilization**: When the MedKit agentic system identifies a literature or research query, it routes to the LiteratureAgent.
2. **Module Integration**: The LiteratureAgent can leverage these sub-modules for specific literature tasks:
   - **Search**: Finding relevant medical articles based on queries
   - **Review**: Analyzing and critiquing article content
   - **Compare**: Comparing multiple articles for similarities and differences
   - **Summarize**: Creating concise summaries of lengthy articles
   - **Keywords**: Extracting key terms and concepts from articles
3. **Workflow Integration**:
   - User query about medical literature → TriageAgent identifies research need
   - LiteratureAgent processes the query and determines which sub-module(s) to use
   - The LiteratureAgent applies the appropriate article processing function
   - ValidationAgent checks the information against source articles for accuracy
   - SynthesisAgent incorporates literature findings with other medical data into a comprehensive response

## Limitations

- The modules help with retrieval and summarization, not comprehensive evidence synthesis.
- Outputs should be checked against source articles.
