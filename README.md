# DESS: Department Extraction using Search and spaCy

<div align="center">
    <img src="cover.jpeg" alt="DESS: Department Extraction using Search and spaCy" width="250"/>
</div>

## Overview
DESS is a tool designed to automate the extraction of academic department names for faculty members listed in a dataset. The tool performs automated Google searches to find relevant web pages for each faculty member, then uses a combination of regular expressions (RegEx) and natural language processing (NLP) via SpaCy to extract department information. This is particularly useful for building datasets related to academic staff, such as faculty financial compensation.

## Project Structure

```
DESS/                               
├── README.md                       # Project documentation
├── fileio.py                       # Module for handling Dropbox interactions
├── main.py                         # Entry point for running DESS
│
├── dess/                           # Core application folder
│   ├── __init__.py                 # Marks the directory as a package
│   ├── main.py                     # Main processing logic
│   ├── nlp.py                      # NLP module for extracting departments
│   └── search.py                   # Module for performing Google searches
│
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables (e.g., Dropbox API keys)
```

## Usage
As the dataset is large and requires long processing times, we suggest running DESS in the background continuously. This can be achieved on macOS using the `caffeinate` command to prevent the system from sleeping. Here's how to run this tool with run the tool with uninterrupted execution.

1. Activate Your Virtual Environment
    ```bash
    source venv/bin/activate
    ```
2. Set your file path in `main.py`
3. Ensure `main.py` is executable
    ```bash
    chmod +x main.py
    ```
4. Run the Tool with caffeinate:
    Use the caffeinate command to prevent your Mac from sleeping while DESS is running:
    ```bash
    caffeinate -i ./main.py
    ```