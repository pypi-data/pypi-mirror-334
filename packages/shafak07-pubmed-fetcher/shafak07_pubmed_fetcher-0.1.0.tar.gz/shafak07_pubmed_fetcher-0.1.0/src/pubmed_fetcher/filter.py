from typing import List, Dict


def filter_non_academic(authors: List[Dict]) -> List[Dict]:
    """Filters out university-affiliated authors and keeps pharma/biotech authors."""
    non_academic_authors = []
    for author in authors:
        affiliation = author.get("affiliation", "").lower()
        if "pharma" in affiliation or "biotech" in affiliation:
            non_academic_authors.append(author)
    return non_academic_authors
