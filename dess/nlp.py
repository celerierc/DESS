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
    isFaculty = department != "MISSING"
    return isFaculty, department

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
        # Define the patterns to search for, case-insensitive keywords
    patterns = {
        "professor": r'professor ([A-Za-z\s]+)',
        "professor_of": r'professor of ([A-Za-z\s]+)',
        "professor_of_the_department": r'professor of the ([A-Za-z\s]+) department',
        "professor_in": r'professor in ([A-Za-z\s]+)',
        "professor_in_the_department": r'professor in ([A-Za-z\s]+) department',
        "department_of": r'department of ([A-Za-z\s]+)',
        "in_the_department": r'in the ([A-Za-z\s]+) department',
        "the_department": r'the ([A-Za-z\s]+) department',
        "the_department_of_at": r'the department of ([A-Za-z\s]+) at'
    }
    if rawText is None: return "MISSING"

    # Check each pattern and return the first matched department
    for text in rawText:
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()  # Return the captured department name

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