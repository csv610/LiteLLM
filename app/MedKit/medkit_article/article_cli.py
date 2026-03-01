import argparse
import sys
import os
from pathlib import Path

# Add the project root to sys.path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

def display_module_list():
    """Display available article modules."""
    print("\n📚 MedKit Article Module Catalog\n")
    
    modules = {
        "search": "Search for medical articles using PubMed (biomcp) and visualize results.",
        "review": "Perform structured reviews of medical articles using LLMs.",
        "compare": "Side-by-side comparison of two medical articles.",
        "summarize": "Generate cohesive summaries for long medical articles.",
        "keywords": "Extract precise medical keywords and terminology from articles."
    }

    for cmd, desc in modules.items():
        print(f"  - {cmd.ljust(12)}: {desc}")
    
    print("\nUsage: medkit-article <subcommand> [args]")
    print("Example: medkit-article search 'Diabetes'")

def main():
    parser = argparse.ArgumentParser(description="MedKit Article Unified CLI")
    subparsers = parser.add_subparsers(dest="command", required=False) # Not required to allow 'list' as default or handle it manually

    # List command
    list_p = subparsers.add_parser("list", help="List all available article modules")

    # Search (delegation)
    search_p = subparsers.add_parser("search", help="Search for medical articles")
    search_p.add_argument("query", help="Search query (e.g., disease name)")
    search_p.add_argument("-n", "--num", type=int, default=5, help="Number of articles to return")

    # Review
    review_p = subparsers.add_parser("review", help="Review a medical article")
    review_p.add_argument("-f", "--file", required=True, help="Path to the article file")
    review_p.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use")

    # Summarize
    summarize_p = subparsers.add_parser("summarize", help="Summarize a medical article")
    summarize_p.add_argument("-f", "--file", required=True, help="Path to the article file")
    summarize_p.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use")

    # Compare
    compare_p = subparsers.add_parser("compare", help="Compare two medical articles")
    compare_p.add_argument("-f1", "--file1", required=True, help="Path to the first article")
    compare_p.add_argument("-f2", "--file2", required=True, help="Path to the second article")
    compare_p.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use")

    # Keywords
    keywords_p = subparsers.add_parser("keywords", help="Extract keywords from a medical article")
    keywords_p.add_argument("-f", "--file", required=True, help="Path to the article file")
    keywords_p.add_argument("-m", "--model", default="ollama/gemma3", help="Model to use")

    if len(sys.argv) == 1:
        display_module_list()
        return

    args, unknown = parser.parse_known_args()

    if args.command == "list":
        display_module_list()
    
    elif args.command == "search":
        from medkit_article.article_search.articles_search_cli import main as search_main
        sys.argv = [sys.argv[0], "search", args.query, "-n", str(args.num)] + unknown
        search_main()

    elif args.command == "review":
        from medkit_article.article_review.article_review_cli import main as review_main
        sys.argv = [sys.argv[0], "-f", args.file, "-m", args.model] + unknown
        review_main()

    elif args.command == "summarize":
        from medkit_article.article_summary.article_summary_cli import main as summarize_main
        sys.argv = [sys.argv[0], "-f", args.file, "-m", args.model] + unknown
        summarize_main()

    elif args.command == "compare":
        from medkit_article.article_comparison.article_comparison_cli import main as compare_main
        sys.argv = [sys.argv[0], "-f1", args.file1, "-f2", args.file2, "-m", args.model] + unknown
        compare_main()

    elif args.command == "keywords":
        from medkit_article.article_keywords.cli import main as keywords_main
        sys.argv = [sys.argv[0], "-f", args.file, "-m", args.model] + unknown
        keywords_main()
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
