"""
article_gradio.py - Gradio interface for the MedKit Article application.
"""

import gradio as gr
import json
import sys
import os
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Import article modules
try:
    from medkit_article.article_search.biomcp_articles_search import (
        MedicalArticleSearch,
    )
    from medkit_article.article_review.article_review_cli import main as review_main
    from medkit_article.article_summary.article_summary_cli import (
        main as summarize_main,
    )
    from medkit_article.article_comparison.article_comparison_cli import (
        main as compare_main,
    )
    from medkit_article.article_keywords.cli import main as keywords_main
except (ImportError, ValueError):
    try:
# Add the project root to sys.path
path = Path(__file__).parent
while path.name != "app" and path.parent != path:
    path = path.parent
if path.name == "app":
    root = path.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

        from .article_search.biomcp_articles_search import MedicalArticleSearch
        from .article_review.article_review_cli import main as review_main
        from .article_summary.article_summary_cli import main as summarize_main
        from .article_comparison.article_comparison_cli import main as compare_main
        from .article_keywords.cli import main as keywords_main
    except (ImportError, ValueError):
        from article_search.biomcp_articles_search import MedicalArticleSearch
        from article_review.article_review_cli import main as review_main
        from article_summary.article_summary_cli import main as summarize_main
        from article_comparison.article_comparison_cli import main as compare_main
        from article_keywords.cli import main as keywords_main


def search_medical_articles(disease: str, num_articles: int, output_json: bool):
    """Search for medical articles."""
    if not disease.strip():
        return "Please enter a disease name to search for articles."

    try:
        searcher = MedicalArticleSearch()
        articles = searcher.search_articles(disease.strip())

        if not articles:
            return f"No articles found for '{disease}'."

        # Limit results
        articles = articles[:num_articles]

        if output_json:
            return json.dumps(articles, indent=2)
        else:
            result = f"## 📚 Found {len(articles)} articles for '{disease}':\n\n"
            for i, art in enumerate(articles, 1):
                result += f"{i}. **{art['title']}**\n"
                result += f"   *Journal:* {art['journal']} ({art['date']})\n"
                result += f"   *PMID:* {art['pmid']} | *DOI:* {art.get('doi', 'N/A')}\n"
                result += "---\n"
            return result

    except Exception as e:
        return f"Error searching for medical articles: {str(e)}"


def get_medical_citations(disease: str):
    """Get formatted citations for medical articles."""
    if not disease.strip():
        return "Please enter a disease name to get citations."

    try:
        searcher = MedicalArticleSearch()
        articles = searcher.search_articles(disease.strip())

        if not articles:
            return f"No articles found for '{disease}'."

        citations = searcher.get_article_citations()

        if not citations:
            return f"No citations could be generated for '{disease}'."

        result = f"## 📑 Citations for '{disease}':\n\n"
        for cite in citations:
            result += f"{cite}\n\n"
        return result

    except Exception as e:
        return f"Error getting medical citations: {str(e)}"


def process_article_file(file_path, operation: str, model_name: str):
    """Process an article file with various operations."""
    if not file_path:
        return "Please upload an article file."

    if not os.path.exists(file_path.name):
        return f"File not found: {file_path.name}"

    try:
        # Set up sys.argv for the CLI functions
        original_argv = sys.argv.copy()

        if operation == "review":
            sys.argv = [sys.argv[0], "-f", file_path.name, "-m", model_name]
            # Capture output by redirecting stdout
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                review_main()
            output = f.getvalue()
            sys.argv = original_argv
            return (
                f"## 📋 Article Review\n\n{output}"
                if output
                else "Review completed but no output generated."
            )

        elif operation == "summarize":
            sys.argv = [sys.argv[0], "-f", file_path.name, "-m", model_name]
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                summarize_main()
            output = f.getvalue()
            sys.argv = original_argv
            return (
                f"## 📄 Article Summary\n\n{output}"
                if output
                else "Summarization completed but no output generated."
            )

        elif operation == "keywords":
            sys.argv = [sys.argv[0], "-f", file_path.name, "-m", model_name]
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                keywords_main()
            output = f.getvalue()
            sys.argv = original_argv
            return (
                f"## 🔍 Extracted Keywords\n\n{output}"
                if output
                else "Keyword extraction completed but no output generated."
            )

        else:
            return f"Unknown operation: {operation}"

    except Exception as e:
        # Restore argv in case of error
        sys.argv = original_argv
        return f"Error processing article: {str(e)}"


def compare_article_files(file1_path, file2_path, model_name: str):
    """Compare two article files."""
    if not file1_path or not file2_path:
        return "Please upload both article files for comparison."

    if not os.path.exists(file1_path.name):
        return f"First file not found: {file1_path.name}"

    if not os.path.exists(file2_path.name):
        return f"Second file not found: {file2_path.name}"

    try:
        # Set up sys.argv for the CLI function
        original_argv = sys.argv.copy()
        sys.argv = [
            sys.argv[0],
            "-f1",
            file1_path.name,
            "-f2",
            file2_path.name,
            "-m",
            model_name,
        ]

        # Capture output by redirecting stdout
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            compare_main()
        output = f.getvalue()
        sys.argv = original_argv

        return (
            f"## ⚖️ Article Comparison\n\n{output}"
            if output
            else "Comparison completed but no output generated."
        )

    except Exception as e:
        # Restore argv in case of error
        sys.argv = original_argv
        return f"Error comparing articles: {str(e)}"


def create_gradio_interface():
    """Create and return the Gradio interface."""
    with gr.Blocks(
        title="MedKit Article - Medical Article Analysis Suite"
    ) as interface:
        gr.Markdown("# 📚 MedKit Article Suite")
        gr.Markdown(
            "Comprehensive tools for searching, reviewing, summarizing, comparing, and extracting keywords from medical articles."
        )

        with gr.Tabs():
            # Article Search Tab
            with gr.TabItem("🔍 Article Search"):
                with gr.Row():
                    with gr.Column():
                        search_disease = gr.Textbox(
                            label="Disease Name",
                            placeholder="Enter disease name to search for articles (e.g., 'Diabetes', 'Hypertension')",
                            lines=1,
                        )
                        search_num = gr.Slider(
                            label="Number of Articles to Return",
                            minimum=1,
                            maximum=50,
                            value=10,
                            step=1,
                        )
                        search_json = gr.Checkbox(label="Output as JSON", value=False)
                        search_btn = gr.Button("Search Articles", variant="primary")

                    with gr.Column():
                        search_output = gr.Markdown(label="Search Results")

                search_btn.click(
                    fn=search_medical_articles,
                    inputs=[search_disease, search_num, search_json],
                    outputs=search_output,
                )

                gr.Markdown("""
                ### About Article Search
                Search PubMed for medical articles using the biomcp framework:
                - Enter a disease name to find relevant articles
                - Get article details including title, journal, date, PMID, and DOI
                - Optionally output results in JSON format for further processing
                """)

            # Citations Tab
            with gr.TabItem("📑 Citations"):
                with gr.Row():
                    with gr.Column():
                        cite_disease = gr.Textbox(
                            label="Disease Name",
                            placeholder="Enter disease name to get citations (e.g., 'Diabetes', 'Hypertension')",
                            lines=1,
                        )
                        cite_btn = gr.Button("Get Citations", variant="primary")

                    with gr.Column():
                        cite_output = gr.Markdown(label="Citations")

                cite_btn.click(
                    fn=get_medical_citations, inputs=[cite_disease], outputs=cite_output
                )

                gr.Markdown("""
                ### About Medical Citations
                Get formatted citations for medical articles:
                - Enter a disease name to find articles and generate citations
                - Citations are formatted in standard academic styles
                - Useful for research papers and literature reviews
                """)

            # Article Processing Tab
            with gr.TabItem("📄 Article Processing"):
                with gr.TabbedInterface() as article_tabs:
                    # Review Tab
                    with gr.Tab("📋 Review"):
                        with gr.Row():
                            with gr.Column():
                                review_file = gr.File(
                                    label="Upload Article File",
                                    file_types=[".txt", ".md", ".pdf"],
                                    type="filepath",
                                )
                                review_model = gr.Dropdown(
                                    label="LLM Model",
                                    choices=[
                                        "ollama/gemma3",
                                        "ollama/llama3",
                                        "ollama/mistral",
                                        "gpt-3.5-turbo",
                                        "gpt-4",
                                        "claude-3-haiku-20240307",
                                        "claude-3-sonnet-20240229",
                                    ],
                                    value="ollama/gemma3",
                                )
                                review_btn = gr.Button(
                                    "Review Article", variant="primary"
                                )

                            with gr.Column():
                                review_output = gr.Markdown(label="Review Results")

                        review_btn.click(
                            fn=process_article_file,
                            inputs=[review_file, gr.State("review"), review_model],
                            outputs=review_output,
                        )

                    # Summarize Tab
                    with gr.Tab("📄 Summarize"):
                        with gr.Row():
                            with gr.Column():
                                summarize_file = gr.File(
                                    label="Upload Article File",
                                    file_types=[".txt", ".md", ".pdf"],
                                    type="filepath",
                                )
                                summarize_model = gr.Dropdown(
                                    label="LLM Model",
                                    choices=[
                                        "ollama/gemma3",
                                        "ollama/llama3",
                                        "ollama/mistral",
                                        "gpt-3.5-turbo",
                                        "gpt-4",
                                        "claude-3-haiku-20240307",
                                        "claude-3-sonnet-20240229",
                                    ],
                                    value="ollama/gemma3",
                                )
                                summarize_btn = gr.Button(
                                    "Summarize Article", variant="primary"
                                )

                            with gr.Column():
                                summarize_output = gr.Markdown(label="Summary Results")

                        summarize_btn.click(
                            fn=process_article_file,
                            inputs=[
                                summarize_file,
                                gr.State("summarize"),
                                summarize_model,
                            ],
                            outputs=summarize_output,
                        )

                    # Keywords Tab
                    with gr.Tab("🔍 Keywords"):
                        with gr.Row():
                            with gr.Column():
                                keywords_file = gr.File(
                                    label="Upload Article File",
                                    file_types=[".txt", ".md", ".pdf"],
                                    type="filepath",
                                )
                                keywords_model = gr.Dropdown(
                                    label="LLM Model",
                                    choices=[
                                        "ollama/gemma3",
                                        "ollama/llama3",
                                        "ollama/mistral",
                                        "gpt-3.5-turbo",
                                        "gpt-4",
                                        "claude-3-haiku-20240307",
                                        "claude-3-sonnet-20240229",
                                    ],
                                    value="ollama/gemma3",
                                )
                                keywords_btn = gr.Button(
                                    "Extract Keywords", variant="primary"
                                )

                            with gr.Column():
                                keywords_output = gr.Markdown(label="Keywords Results")

                        keywords_btn.click(
                            fn=process_article_file,
                            inputs=[
                                keywords_file,
                                gr.State("keywords"),
                                keywords_model,
                            ],
                            outputs=keywords_output,
                        )

                    # Compare Tab
                    with gr.Tab("⚖️ Compare"):
                        with gr.Row():
                            with gr.Column():
                                compare_file1 = gr.File(
                                    label="Upload First Article File",
                                    file_types=[".txt", ".md", ".pdf"],
                                    type="filepath",
                                )
                                compare_file2 = gr.File(
                                    label="Upload Second Article File",
                                    file_types=[".txt", ".md", ".pdf"],
                                    type="filepath",
                                )
                                compare_model = gr.Dropdown(
                                    label="LLM Model",
                                    choices=[
                                        "ollama/gemma3",
                                        "ollama/llama3",
                                        "ollama/mistral",
                                        "gpt-3.5-turbo",
                                        "gpt-4",
                                        "claude-3-haiku-20240307",
                                        "claude-3-sonnet-20240229",
                                    ],
                                    value="ollama/gemma3",
                                )
                                compare_btn = gr.Button(
                                    "Compare Articles", variant="primary"
                                )

                            with gr.Column():
                                compare_output = gr.Markdown(label="Comparison Results")

                        compare_btn.click(
                            fn=compare_article_files,
                            inputs=[compare_file1, compare_file2, compare_model],
                            outputs=compare_output,
                        )

        gr.Markdown("""
        ### How to Use
        1. **Article Search**: Enter a disease name to search PubMed for relevant medical articles
        2. **Citations**: Enter a disease name to get formatted citations for found articles
        3. **Article Processing**: Upload article files to:
           - **Review**: Get structured reviews using AI agents
           - **Summarize**: Generate concise summaries of long articles
           - **Keywords**: Extract important medical terminology and keywords
           - **Compare**: Analyze similarities and differences between two articles
        
        ### Supported File Formats
        - Text files: .txt, .md
        - PDF files: .pdf (text content will be extracted)
        
        ### About MedKit Article Suite
        This comprehensive toolkit provides AI-powered assistance for medical literature analysis:
        - Search biomedical databases for relevant articles
        - Generate structured reviews using multi-agent AI systems
        - Create summaries that preserve key medical information
        - Extract precise medical keywords and terminology
        - Compare articles to identify consensus and contradictions
        """)

    return interface


if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch(server_name="0.0.0.0", server_port=7868, share=False)
