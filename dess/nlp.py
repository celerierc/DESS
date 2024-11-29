import re
import pandas as pd

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
    df[['isProfessor', 'isInstructor', 'isEmeritus', 'isAssistantProf', 'isAssociateProf', 'isFullProf', 'isClinicalProf', 'isResearcher', 'teaching_intensity', 'isProfessor2', 'department']] = df.apply(
        lambda row: populate_faculty_columns(row['rawText']),
        axis=1,
        result_type='expand'
    )

def populate_faculty_columns(rawText: list[str]):
    department, isProfessor2 = extract_department_regex(rawText)
    # isProfessor, = extract_professor_in_text(rawText)
    return  extract_professor_in_text(rawText), isProfessor2, department

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
                
    return (*flags.values(), teaching_intensity)

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
                return match.group(1).strip(),isProfessor2
    return "MISSING", isProfessor2