import re
import phonenumbers
import dateparser

# ========== REGEX DEFINITIONS ==========

EMAIL_RE = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)

PHONE_RE = re.compile(
    r"(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{1,4}\)?[-.\s]?)?\d{2,4}[-.\s]?\d{2,4}[-.\s]?\d{0,4}"
)

DATE_RE = re.compile(
    r"\b(?:\d{1,2}[\/\-.]\d{1,2}[\/\-.]\d{2,4}|\d{4}[\/\-.]\d{1,2}[\/\-.]\d{1,2}|\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s\d{2,4})\b",
    re.I
)

CARD_RE = re.compile(
    r"\b(?:\d[ -]*?){13,19}\b"
)

# Very rough English address pattern
ADDRESS_RE = re.compile(
    r"\b\d{1,5}\s+[A-Z][\w.-]*(?:\s+[A-Z][\w.-]*){0,6}\b"
)

# Simplified name pattern: assumes capitalized first + last name
NAME_RE = re.compile(
    r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b"
)


# ========== EXTRACTION HELPERS ==========

def find_regex(pattern, text):
    """Return list of (match, start, end)."""
    return [(m.group(), m.start(), m.end()) for m in pattern.finditer(text)]


def find_emails(text):
    return find_regex(EMAIL_RE, text)


def find_cards(text):
    return find_regex(CARD_RE, text)


def find_dates(text):
    results = []
    for m in DATE_RE.finditer(text):
        s = m.group()
        parsed = dateparser.parse(s)
        results.append((s, m.start(), m.end(), str(parsed) if parsed else None))
    return results


def find_phones(text, region="US"):
    results = []
    for match in phonenumbers.PhoneNumberMatcher(text, region):
        num = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
        results.append((num, match.start, match.end))
    return results


def find_addresses(text):
    return find_regex(ADDRESS_RE, text)


def find_names(text):
    return find_regex(NAME_RE, text)
