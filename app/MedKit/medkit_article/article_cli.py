import argparse
import sys
import json
from .biomcp_article_search import MedicalArticleSearch

def main():
    parser = argparse.ArgumentParser(description="MedKit Medical Article Search CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Search
    search_p = subparsers.add_parser("search", help="Search for medical articles by disease")
    search_p.add_argument("disease", help="Name of the disease to search articles for")
    search_p.add_argument("-n", "--num", type=int, default=10, help="Maximum number of articles to return")
    search_p.add_argument("--json", action="store_true", help="Output results in JSON format")

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
            articles = articles[:args.num]

            if args.json:
                print(json.dumps(articles, indent=2))
            else:
                print(f"
📚 Found {len(articles)} articles for '{args.disease}':
")
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
            print(f"
📑 Citations for '{args.disease}':
")
            for cite in citations:
                print(cite)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
