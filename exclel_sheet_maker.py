import json
import pandas as pd
from typing import Any, Dict, List

# ---------------------------------
# Configuration
# ---------------------------------
INPUT_JSON_FILE = "finalized_companies.json"
OUTPUT_EXCEL_FILE = "companies.xlsx"
DELIMITER = " | "

COLUMNS = [
    "company_name",
    "company_website_url",
    "description",
    "business_email",
    "location",
    "team_size",
    "technologies_used",
    "solutions",
    "use_cases",
    "targeted_industries",
    "category_ids",
]

# ---------------------------------
# Helpers
# ---------------------------------
def flatten_array(items: Any) -> str | None:
    if not isinstance(items, list):
        return None

    values = [
        item.get("value")
        for item in items
        if isinstance(item, dict) and item.get("value")
    ]

    # Preserve order, remove duplicates
    unique_values = list(dict.fromkeys(values))
    return DELIMITER.join(unique_values) if unique_values else None


def transform_company(company: Dict) -> Dict[str, Any]:
    return {
        "company_name": company.get("company_name"),
        "company_website_url": company.get("company_name_citation"),
        "description": company.get("description"),
        "business_email": company.get("business_email"),
        "location": company.get("location"),
        "team_size": company.get("team_size"),
        "technologies_used": flatten_array(company.get("technologies_used")),
        "solutions": flatten_array(company.get("solutions")),
        "use_cases": flatten_array(company.get("use_cases")),
        "targeted_industries": flatten_array(company.get("targeted_industries")),
        "category_ids": flatten_array(company.get("category_ids")),
    }


# ---------------------------------
# Main
# ---------------------------------
def main() -> None:
    with open(INPUT_JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data["companies"], list):
        raise ValueError("Input JSON must be a list of objects")

    rows = [transform_company(company) for company in data['companies']]

    df = pd.DataFrame(rows, columns=COLUMNS)

    # Optional but recommended
    df.drop_duplicates(subset=["company_name"], inplace=True)

    df.to_excel(OUTPUT_EXCEL_FILE, index=False)
    print(f"Spreadsheet created: {OUTPUT_EXCEL_FILE}")


if __name__ == "__main__":
    main()
