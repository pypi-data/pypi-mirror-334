import requests
from typing import List, Dict


def fetch_papers(query: str, max_results: int = 10) -> List[Dict]:
    """Fetches research papers from PubMed based on a user query."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmax": max_results, "retmode": "json"}

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    paper_ids = response.json().get("esearchresult", {}).get("idlist", [])

    # Fetch details for each paper
    details_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    details_params = {"db": "pubmed", "id": ",".join(paper_ids), "retmode": "json"}
    details_response = requests.get(details_url, params=details_params)
    details_response.raise_for_status()
    papers = details_response.json().get("result", {})

    results = []
    for paper_id in paper_ids:
        paper_info = papers.get(paper_id, {})
        results.append(
            {
                "PubmedID": paper_id,
                "Title": paper_info.get("title", "N/A"),
                "Publication Date": paper_info.get("pubdate", "N/A"),
            }
        )

    return results
