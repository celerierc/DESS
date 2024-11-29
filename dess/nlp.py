import re
import pandas as pd
import pickle

isProfessor_criteria = ["professor","faculty","chair","dean","head"]
isInstructor_criteria = ["instructor","educator","adjunct"]
isEmeritus_criteria = ["emiritus","emerita"]
isAssistantProf_criteria = ["assistant"]
isAssociateProf_criteria = ["associate"]
isFullProf_criteria = ["full"]
isClinicalProf_criteria = ["clinical"]
isResearcher_criteria = ["research","citations","examine","investigate"]

def extract_department_information(df: pd.DataFrame):
    """Populates the isFaculty and department columns in the DataFrame."""
    df[['isProfessor', 'isInstructor', 'isEmeritus', 'isAssistantProf', 
        'isAssociateProf', 'isFullProf', 'isClinicalProf', 'isResearcher', 
        'teaching_intensity', 'isProfessor2', 'department']] =  df.apply(
        lambda row: populate_faculty_columns(row['rawText']),
        axis=1,
        result_type='expand'
    )

def populate_faculty_columns(rawText: list[str]):
    department, isProfessor2 = extract_department_regex(rawText)
    flags = extract_professor_in_text(rawText)
    return  (*flags, isProfessor2, department)

def extract_professor_in_text(rawText: list[str]) -> str:
    if rawText is None:
        return False, False, False, False, False, False, False, False, 0
    # Define criteria and their corresponding flags
    criteria_flags = {
        "isProfessor": isProfessor_criteria,
        "isInstructor": isInstructor_criteria,
        "isEmeritus": isEmeritus_criteria,
        "isAssistantProf": isAssistantProf_criteria,
        "isAssociateProf": isAssociateProf_criteria,
        "isFullProf": isFullProf_criteria,
        "isClinicalProf": isClinicalProf_criteria,
        "isResearcher": isResearcher_criteria,
    }

    flags = {key: False for key in criteria_flags.keys()}
    teaching_intensity = 0

    for text in rawText:
        teaching_intensity += count_teaching_intensity(text)
        for flag, criteria in criteria_flags.items():
            if flags[flag] == False and lookup_criteria(text, criteria):
                flags[flag] = True

    return  tuple(flags.values()) + (teaching_intensity,)

def count_teaching_intensity(text: str) -> int:
    '''
    Counts the number of times the word teach appears in the text using regex
    '''
    matches = re.findall(r'\bteach\w*', text, re.IGNORECASE)
    return len(matches)
    
def lookup_criteria(text: str, criteria: list[str]) -> bool:
    for criterion in criteria:
        if criterion in text.lower():
            return True
    return False

def extract_department_regex(rawText):
    #  todo: figure out conditional matching (?:the)?(?department)
    primary_patterns = [
        r'professor of the ([A-Za-z]+)',         # Matches "professor of the X" or "professor of X"
        r'professor of ([A-Za-z]+)',         # Matches "professor of the X" or "professor of X"
        r'professor in the ([A-Za-z]+)',         # Matches "professor in the X" or "professor in X"
        r'professor in ([A-Za-z]+)',         # Matches "professor in the X" or "professor in X"
        r'Chair in the ([A-Za-z]+)',             # Matches "Chair in the X" or "Chair in X"
        r'Chair in ([A-Za-z]+)',             # Matches "Chair in the X" or "Chair in X"
        r'professor emeritus of the ([A-Za-z]+)', # Matches "professor emeritus of the X" or "professor emeritus of X"
        r'professor emeritus of ([A-Za-z]+)', # Matches "professor emeritus of the X" or "professor emeritus of X"
        r'professor emerita of the ([A-Za-z]+)',  # Matches "professor emerita of the X" or "professor emerita of X"
        r'professor emerita of ([A-Za-z]+)',  # Matches "professor emerita of the X" or "professor emerita of X"
        r'Faculty of the ([A-Za-z]+)'
        r'Faculty of ([A-Za-z]+)'
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
        for pattern in primary_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                isProfessor2 = True #Found in primary pattern
                return match.group(1).strip(),isProfessor2
            
    # Iterating over snapshots and trying backup patterns
    for text in rawText:
        for pattern in backup_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip(), isProfessor2
            
    # Iterating over snapshots and trying to match with whitelist files
    return extract_with_fuzzy_matching(rawText)

def _load_department_names(file_path):
    with open(file_path, 'rb') as f:
        department_names = pickle.load(f)
    return department_names

def extract_with_fuzzy_matching(rawText):
    DEPARTMENT_WHITELIST = _load_department_names("storage/department-whitelist.pkl")

    for text in rawText:
        for department in DEPARTMENT_WHITELIST:
            if department in text.lower(): return department, False
    return "MISSING", False