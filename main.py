import re
import json
from collections import defaultdict
import pdfplumber
import docx
import phonenumbers
import dateparser

# ---------- regex patterns ----------
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
CARD_RE  = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
DATE_RE  = re.compile(r"\b(?:\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4}|\d{4}[\/\-.]\d{1,2}[\/\-.]\d{1,2}|\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s\d{2,4})\b", re.I)
# Arabic name heuristic
AR_NAME_RE = re.compile(r"\b[ء-ي]{2,}\s+[ء-ي]{2,}(?:\s+[ء-ي]{2,})?\b")

# ---------- helper: read files ----------
def read_txt(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def read_docx(path):
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def read_pdf(path):
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

# ---------- extraction ----------
def find_regex(pattern, text):
    return [(m.group(), m.start(), m.end()) for m in pattern.finditer(text)]

def find_emails(text):
    return find_regex(EMAIL_RE, text)

def find_cards(text):
    return find_regex(CARD_RE, text)

def find_dates(text):
    # return raw matches + parsed date
    out = []
    for m in DATE_RE.finditer(text):
        s = m.group()
        parsed = dateparser.parse(s)
        out.append((s, m.start(), m.end(), str(parsed) if parsed else None))
    return out

def find_phones(text, region="EG"):
    out = []
    for match in phonenumbers.PhoneNumberMatcher(text, region):
        num = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
        out.append((num, match.start, match.end))
    return out

def find_ar_names(text):
    return find_regex(AR_NAME_RE, text)

# ---------- run on a text ----------
def process_text(text):
    results = defaultdict(list)
    results['emails'] = find_emails(text)
    results['cards']  = find_cards(text)
    results['dates']  = find_dates(text)
    results['phones'] = find_phones(text)
    results['arabic_names'] = find_ar_names(text)
    # counts
    summary = {k: len(v) for k, v in results.items()}
    return results, summary

# ---------- example usage with a sample text ----------
if __name__ == "__main__":
    sample = open("sample_input.txt", "r", encoding="utf-8").read()
    results, summary = process_text(sample)
    print("Summary:", json.dumps(summary, ensure_ascii=False, indent=2))
    for k, items in results.items():
        print("\n===", k, "===")
        for it in items:
            print(it)
