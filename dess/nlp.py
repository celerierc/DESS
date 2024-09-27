import re

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

    # Define the patterns to search for, case-insensitive keywords
    patterns = [
        r'professor of ([A-Za-z\s]+?)(?:,|\.|\s+at|\s+in|\s+from|$)',  
        r'professor in ([A-Za-z\s]+?)(?:,|\.|\s+at|\s+in|\s+from|$)',  
        r'department of ([A-Za-z\s]+?)(?:,|\.|\s+at|\s+in|\s+from|$)', 
        r'in the ([A-Za-z\s]+?) department(?:,|\.|\s+at|\s+in|\s+from|$)'
    ]

    # Loop through patterns and search for matches, case-insensitive search
    if rawText is None: return "MISSING"
    for text in rawText:
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)  # re.IGNORECASE makes it case-insensitive
            if match:
                # Return the first captured group (the department name)
                return match.group(1).strip()

    # Return an empty string if no patterns match
    return "MISSING"