import json
import subprocess


class MedicalArticleSearch:
    def __init__(self):
        self.articles = []

    def search_articles(self, disease):
        self.articles = []

        if not disease.strip():
            return self.articles

        try:
            result = subprocess.run(
                ["biomcp", "article", "search", "--disease", disease, "--json"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            if result.returncode != 0:
                raise Exception(f"Error running biomcp command: {result.stderr}")

            self.articles = json.loads(result.stdout)

            # Ensure each article has the expected fields and format
            for article in self.articles:
                details = self.extract_article_details(article)
                article.update(details)

            return self.articles

        except Exception as e:
            raise e

    def get_article_count(self):
        """Get the number of articles found."""
        return len(self.articles)

    def extract_article_details(self, article):
        """Extract and format article details."""
        authors = article.get("authors", [])
        if isinstance(authors, list):
            authors_str = ", ".join(authors)
        else:
            authors_str = str(authors)

        return {
            "title": article.get("title", "N/A"),
            "authors": authors_str,
            "journal": article.get("journal", "N/A"),
            "date": article.get("date", "N/A"),
            "year": article.get("date", "N/A").split("-")[0]
            if "-" in article.get("date", "N/A")
            else article.get("date", "N/A").split(" ")[0]
            if " " in article.get("date", "N/A")
            else article.get("date", "N/A"),
            "pmid": article.get("pmid", "N/A"),
        }

    def get_article_citations(self):
        """Get formatted citations for all articles."""
        citations = []
        for i, article in enumerate(self.articles, 1):
            details = self.extract_article_details(article)
            citation = f"{i}. {details['title']}, {details['authors']}. {details['journal']}, {details['year']}. PMID: {details['pmid']}"
            citations.append(citation)

        return citations
