import re
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)


# Define patterns to match department-related phrases
patterns = [
    [{"LOWER": "lecturer"}, {"LOWER": "in"}, {"POS": "PROPN", "OP": "+"}],  # Matches "Lecturer in [Department]"
    [{"LOWER": "professor"}, {"LOWER": "at"}, {"POS": "PROPN", "OP": "+"}],  # Matches "professor at [Department]"
    [{"LOWER": "professor"}, {"LOWER": "in"}, {"POS": "PROPN", "OP": "+"}],  # Matches "professor in [Department]"
    [{"LOWER": "professor"}, {"LOWER": "of"}, {"POS": "PROPN", "OP": "+"}],  # Matches "professor of [Department]"
    [{"LOWER": "department"}, {"LOWER": "of"}, {"POS": "PROPN", "OP": "+"}],  # Matches "department of [Department]"
    [{"LOWER": "in"}, {"LOWER": "the"}, {"POS": "PROPN", "OP": "+"}, {"LOWER": "department"}]  # Matches "in the [Department] department"
]

# Add the patterns to the matcher
matcher.add("DEPARTMENT_PATTERNS", patterns)

def populate_faculty_columns(rawText: list[str]):
    department = extract_department(rawText)
    isFaculty = extract_professor_in_text(rawText)
    return isFaculty, department

def extract_professor_in_text(rawText: list[str]) -> str:
    if rawText is None: return False
    for text in rawText:
        if 'professor' in text.lower(): return True
    return False

def extract_department(rawText: list[str]) -> str:
    """
    Extracts the academic department from the given text using specific patterns,
    with case insensitivity for keywords and stopping conditions (e.g., punctuation or prepositions).
    
    Args:
        text (list[str]): The raw text to search for department patterns.

    Returns:
        str: The extracted department or an empty string if no match is found.
    """
    return extract_department_regex(rawText)

def extract_department_regex(rawText):
    primary_patterns = [
        r'professor of ([A-Za-z]+)',              # Professor of + first word
        r'department of ([A-Za-z]+)',             # Department of + first word
        r'professor in the ([A-Za-z]+)'           # Professor in the + first word
    ]

    backup_patterns = [
        r'school of ([A-Za-z]+)',                 # School of + first word
        r'college of ([A-Za-z]+)',                # College of + first word
        r'book on ([A-Za-z]+)',                   # Book on + first word
        r'in the area of ([A-Za-z]+)',            # In the area of + first word
        r'research primarily focused on ([A-Za-z]+)'  # Research primarily focused on + first word
    ]

    if rawText is None: return "MISSING"

    # Iterating over snapshots and trying primary patterns
    for text in rawText:
        for pattern in primary_patterns:
            match = re.match(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()

    # Iterating over snapshots and trying backup patterns
    for text in rawText:
        for pattern in backup_patterns:
            match = re.match(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()

    return "MISSING"    

def extract_department_spacy(rawText):
    if rawText is None: return "MISSING"
    for text in rawText:
        doc = nlp(text)  # Process the text with SpaCy
        
        # Find matches in the processed doc
        matches = matcher(doc)
        if matches:
            for match_id, start, end in matches:
                matched_span = doc[start:end]  # Extract the matched span
                department = " ".join([token.text for token in matched_span if token.dep_ in ('pobj', 'attr')]).strip()
                
                if department:  # Check if a valid department was extracted
                    return department  # Return the department if valid
    
    return "MISSING"  # No matches found in any text