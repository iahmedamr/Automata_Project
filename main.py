from patterns import (
    find_emails, find_cards, find_dates, find_phones,
    find_addresses, find_names
)
"""dsfdlsnflsd"""


""" fffff"""

def read_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def process_text(text):
    results = {
        "names": find_names(text),
        "emails": find_emails(text),
        "phones": find_phones(text),
        "dates": find_dates(text),
        "addresses": find_addresses(text),
        "cards": find_cards(text),
    }

    print("\n=== SUMMARY ===")
    for k, v in results.items():
        print(f"{k}: {len(v)} found")

    print("\n=== DETAILS ===")
    for k, v in results.items():
        if not v: 
            continue
        print(f"\n-- {k.upper()} --")
        for match in v:
            print(match)

if __name__ == "__main__":
    text = read_txt("sample.txt")
    process_text(text)
