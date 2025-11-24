import csv
from patterns import (
    find_emails, find_dates, find_phones,
    find_addresses, find_names
)

def read_txt(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def process_text(text):
    results = {
        "names": find_names(text),
        "emails": find_emails(text),
        "phones": find_phones(text),
        "dates": find_dates(text),
        "addresses": find_addresses(text)
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
    # Export to CSV
    export_to_csv(results)

def export_to_csv(results, output_file="output.csv"):
    """Export results to CSV file ordered by line number"""
    rows = []
    
    # Collect all matches with their type
    for type_name, matches in results.items():
        for match_text, line_num, start_col, end_col in matches:
            rows.append({
                "ln": line_num,
                "match": match_text,
                "type": type_name,
                "start_col": start_col,
                "end_col": end_col
            })
    
    # Sort by line number
    rows.sort(key=lambda x: (x["ln"], x["start_col"]))
    
    # Write to CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ln", "match", "type", "start_col", "end_col"])
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"\n=== CSV EXPORT ===")
    print(f"Results exported to {output_file}")
    print(f"Total entries: {len(rows)}")

if __name__ == "__main__":
    text = read_txt("sample.txt")
    process_text(text)
    # 11 names
    # 4 emails
    # 6 phone numbers
    # 3 dates
    # 5 addresses