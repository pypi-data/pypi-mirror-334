import csv
from typing import List, Dict


def export_to_csv(filename: str, data: List[Dict]):
    """Exports paper data to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "PubmedID",
                "Title",
                "Publication Date",
                "Non-academic Author(s)",
                "Company Affiliation(s)",
                "Corresponding Author Email",
            ],
        )
        writer.writeheader()
        writer.writerows(data)
