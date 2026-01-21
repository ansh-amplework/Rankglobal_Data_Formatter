import json
from typing import List, Dict, Any

# ---------------------------------
# Configuration
# ---------------------------------
INPUT_FILES = [
    "extract-data-2026-01-20(3).json"
]

OUTPUT_FILE = "finalized_companies.json"


# ---------------------------------
# Deduplication
# ---------------------------------
def remove_duplicate_dicts(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove exact duplicate dictionaries while preserving order.
    Handles nested structures safely.
    """
    seen = set()
    unique: List[Dict[str, Any]] = []

    for item in data:
        if not isinstance(item, dict):
            continue  # defensive guard

        key = json.dumps(item, sort_keys=True, ensure_ascii=False)

        if key not in seen:
            seen.add(key)
            unique.append(item)

    return unique


# ---------------------------------
# Load + Merge
# ---------------------------------
def load_companies(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print("Excaption:",e)

    companies = data.get("companies", [])
    if not isinstance(companies, list):
        raise ValueError(f"`companies` must be a list in {file_path}")

    # Ensure only dicts pass through
    return [c for c in companies if isinstance(c, dict)]


# ---------------------------------
# Main
# ---------------------------------
def main() -> None:
    all_companies: List[Dict[str, Any]] = []

    for file_path in INPUT_FILES:
        all_companies.extend(load_companies(file_path))

    finalized_companies = remove_duplicate_dicts(all_companies)

    output = {
        "companies": finalized_companies
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)

    print(f"Finalized companies written to: {OUTPUT_FILE}")
    print(f"Total unique companies: {len(finalized_companies)}")


if __name__ == "__main__":
    main()
