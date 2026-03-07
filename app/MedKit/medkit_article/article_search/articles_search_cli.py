import argparse
import json
import sys
from pathlib import Path

# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

try:
    from .biomcp_articles_search import MedicalArticleSearch
except (ImportError, ValueError):
    from biomcp_articles_search import MedicalArticleSearch


def main():
    parser = argparse.ArgumentParser(description="MedKit Medical Article Search CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Search
    search_p = subparsers.add_parser(
        "search", help="Search for medical articles by disease"
    )
    search_p.add_argument("disease", help="Name of the disease to search articles for")
    search_p.add_argument(
        "-n", "--num", type=int, default=10, help="Maximum number of articles to return"
    )
    search_p.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )

    # Citations
    cite_p = subparsers.add_parser("cite", help="Get formatted citations for articles")
    cite_p.add_argument("disease", help="Name of the disease")

    args = parser.parse_args()
    searcher = MedicalArticleSearch()

    try:
        if args.command == "search":
            articles = searcher.search_articles(args.disease)
            if not articles:
                print(f"No articles found for '{args.disease}'.")
                return

            # Limit results
            articles = articles[: args.num]

            if args.json:
                print(json.dumps(articles, indent=2))
            else:
                print(f"\n📚 Found {len(articles)} articles for '{args.disease}':\n")
                for i, art in enumerate(articles, 1):
                    print(f"{i}. {art['title']}")
                    print(f"   Journal: {art['journal']} ({art['date']})")
                    print(f"   PMID: {art['pmid']} | DOI: {art.get('doi', 'N/A')}")
                    print("-" * 40)

        elif args.command == "cite":
            articles = searcher.search_articles(args.disease)
            if not articles:
                print(f"No articles found for '{args.disease}'.")
                return

            citations = searcher.get_article_citations()
            print(f"\n📑 Citations for '{args.disease}':\n")
            for cite in citations:
                print(cite)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
