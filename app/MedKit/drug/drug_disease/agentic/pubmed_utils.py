import requests
import logging
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

class PubMedTool:
    """Tool for searching and fetching abstracts from PubMed (NCBI Entrez API)."""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    
    @staticmethod
    def search_pubmed(query: str, max_results: int = 5) -> List[str]:
        """Search PubMed for a query and return a list of PMIDs."""
        search_url = f"{PubMedTool.BASE_URL}esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json"
        }
        
        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("esearchresult", {}).get("idlist", [])
        except Exception as e:
            logger.error(f"PubMed search failed: {e}")
            return []

    @staticmethod
    def fetch_details(pmids: List[str]) -> str:
        """Fetch titles and abstracts for a list of PMIDs."""
        if not pmids:
            return "No PubMed results found."
            
        fetch_url = f"{PubMedTool.BASE_URL}efetch.fcgi"
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml"
        }
        
        try:
            response = requests.get(fetch_url, params=params)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            
            results = []
            for article in root.findall(".//PubmedArticle"):
                title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "No Title"
                abstract_elem = article.find(".//AbstractText")
                abstract = abstract_elem.text if abstract_elem is not None else "No Abstract available"
                
                # Some abstracts are split into multiple elements
                if abstract_elem is not None and not abstract:
                    abstract = " ".join([elem.text for elem in article.findall(".//AbstractText") if elem.text])
                
                results.append(f"Title: {title}\nAbstract: {abstract}\n---")
                
            return "\n".join(results)
        except Exception as e:
            logger.error(f"PubMed fetch failed: {e}")
            return "Failed to fetch PubMed details."

    @staticmethod
    def get_evidence(medicine: str, condition: str) -> str:
        """Helper to search and fetch in one go."""
        query = f"({medicine}[Title/Abstract]) AND ({condition}[Title/Abstract]) AND (interaction OR safety OR contraindication)"
        pmids = PubMedTool.search_pubmed(query)
        return PubMedTool.fetch_details(pmids)
