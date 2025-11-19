import re
# import phonenumbers

# ========== REGEX DEFINITIONS ==========

# Names: Capitalized first name + Capitalized last name (both required)
NAME_RE = re.compile(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b')

EMAIL_RE = re.compile(
    r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
)

PHONE_RE = re.compile(r'''(?x)               # verbose
    (?<!\w)                                  # not part of a word
    (?!\d{4}-\d{2}-\d{2})                    # reject YYYY-MM-DD dates
    (?=(?:.*\d){7,15})                       # total digits between 7 and 15
    (?:\+?\d{1,3}[\s\-\.]?)?                 # optional country code +91, +44, etc.
    (?:\(?\d{1,4}\)?[\s\-\.]?)?              # optional area/zone code (e.g. (212), 020)
    (?:\d{2,5}[\s\-\.]?){2,6}                # 2–6 groups of 2–5 digits
    (?!\w)
''')

DATE_RE = re.compile(
    r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b|'
    r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b|'
    r'\b\d{4}-\d{2}-\d{2}\b|'
    r'\b\d{1,2}/\d{1,2}/\d{4}\b',
    re.IGNORECASE
)

ADDRESS_RE = re.compile(
    r'\b\d+[A-Z]?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+'
    r'(?:Street|St|Road|Rd|Avenue|Ave|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Parkway|Pkwy|Way)\b'
    r'(?:\s*,\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)*'
)

# ========== HELPER FUNCTIONS ==========

def get_line_col(text, index):
    lines = text[:index].split('\n')
    line_num = len(lines)
    col = len(lines[-1])
    return line_num, col

def find_pattern(pattern, text):
    results = []
    for m in pattern.finditer(text):
        match_text = m.group()
        line, col = get_line_col(text, m.start())
        results.append((match_text, line, col, col + len(match_text)))
    return results

# ========== MAIN FUNCTIONS ==========

def find_names(text):
    """Extract person names using regex and filter out street/location names"""
    results = []
    seen = set()
    
    # Words to exclude (street/location keywords)
    exclude_keywords = [
        'Street', 'St', 'Road', 'Rd', 'Avenue', 'Ave', 'Boulevard', 'Blvd',
        'Lane', 'Ln', 'Drive', 'Dr', 'Court', 'Ct', 'Parkway', 'Pkwy', 'Way',
        'Baker', 'Wall', 'Evergreen', 'Pennsylvania', 'Downing',
        'New', 'York', 'City', 'London', 'Washington'
    ]
    
    for m in NAME_RE.finditer(text):
        name = m.group().strip()
        
        # Skip if name contains any exclude keyword
        if any(keyword in name for keyword in exclude_keywords):
            continue
        
        # Skip if already seen
        if name in seen:
            continue
        
        seen.add(name)
        line, col = get_line_col(text, m.start())
        results.append((name, line, col, col + len(name)))
    
    return results

def find_emails(text):
    return find_pattern(EMAIL_RE, text)

def find_phones(text):
    return find_pattern(PHONE_RE, text)

def find_dates(text):
    return find_pattern(DATE_RE, text)

def find_addresses(text):
    return find_pattern(ADDRESS_RE, text)