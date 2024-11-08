import re
import pandas as pd

def extract_department_information(df: pd.DataFrame):
    """Populates the isFaculty and department columns in the DataFrame."""
    df[['isProfessor', 'isProfessor2', 'department']] = df.apply(
        lambda row: populate_faculty_columns(row['rawText']),
        axis=1,
        result_type='expand'
    )

def populate_faculty_columns(rawText: list[str]):
    department, isProfessor2 = extract_department_regex(rawText)
    isFaculty = extract_professor_in_text(rawText)
    return isFaculty, isProfessor2, department

def extract_professor_in_text(rawText: list[str]) -> str:
    if rawText is None: return False
    for text in rawText:
        if 'professor' in text.lower(): return True
    return False

def extract_department_regex(rawText):
    primary_patterns = [
        r'professor of the ([A-Za-z]+)',
        r'professor in the ([A-Za-z]+)',
        r'professor of ([A-Za-z]+)',              # Professor of + first word
        r'department of ([A-Za-z]+)',             # Department of + first word
              # Professor in the + first word
    ]

    backup_patterns = [
        r'school of ([A-Za-z]+)',                 # School of + first word
        r'college of ([A-Za-z]+)',                # College of + first word
        r'book on ([A-Za-z]+)',                   # Book on + first word
        r'in the area of ([A-Za-z]+)',            # In the area of + first word
        r'research primarily focused on ([A-Za-z]+)'  # Research primarily focused on + first word
    ]
    isProfessor2 = False
    if rawText is None: return "MISSING", isProfessor2
    
    # Iterating over snapshots and trying primary patterns
    for text in rawText:
        #print(text)
        for pattern in primary_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                isProfessor2 = True #Found in primary pattern
                return match.group(1).strip(), isProfessor2

    # Iterating over snapshots and trying backup patterns
    for text in rawText:
        for pattern in backup_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip(), isProfessor2

    return "MISSING", isProfessor2