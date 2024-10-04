#!python3
"""
This module provides utilities for interacting with Dropbox to manage and process 
data files. It includes functions for retrieving `.dta` and `.xlsx` files from a 
specified Dropbox folder, loading these files into pandas DataFrames, and uploading 
processed data back to Dropbox.

Before using the functions, ensure that the `DROPBOX_ACCESS_TOKEN` is set up in 
an environment file (.env) to allow authenticated access to Dropbox.
"""
import dropbox
from dropbox.files import WriteMode
from dotenv import load_dotenv
import os
from io import BytesIO
import pandas as pd

def get_files(dbx, folder_path: str) -> list:
    """
    Finds and returns the relevant `.dta` and `.xlsx` file paths in the specified Dropbox folder.

    Args:
        folder_path (str): The Dropbox folder path where the files are located.

    Returns:
        list: A list of file paths (strings) for files with extensions `.dta` or `.xlsx`.
    """
    files_list = []
    try:
        result = dbx.files_list_folder(folder_path)

        # Loop through files and filter based on extension
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                if entry.name.endswith('.dta') or entry.name.endswith('.xlsx'):
                    files_list.append(entry.path_lower)

    except dropbox.exceptions.ApiError as e:
        print(f"Error accessing Dropbox folder: {e}")
    
    return files_list

def get_file_content(dbx, file_path: str) -> bytes:
    """
    Retrieves and returns the buffered file content from Dropbox, allowing it to be processed in-memory.

    Args:
        file_path (str): The full Dropbox path of the file to be retrieved (either `.dta` or `.xlsx`).

    Returns:
        bytes: The content of the file in a byte buffer format. 
        
        Meant to be passed to `main.py` for processing or loaded into a pandas DataFrame.
    """
    try:
        # Download file content from Dropbox as a byte stream
        _, response = dbx.files_download(file_path)
        return response.content
    
    except dropbox.exceptions.ApiError as e:
        print(f"Error downloading file: {e}")
        return b""

def upload_file(dbx, file_content: bytes, destination_path: str) -> None:
    """
    Uploads the processed file content to the "completed/" folder in Dropbox.

    Args:
        file_content (bytes): The modified file content to be uploaded to Dropbox.
        destination_path (str): The Dropbox path where the file will be stored (e.g., 'completed/data1.xlsx').

    Returns:
        None
    """
    try:
        dbx.files_upload(file_content, destination_path, mode=WriteMode('overwrite'))
        return 0
    except dropbox.exceptions.ApiError as e:
        print(f"Error uploading file: {e}")
        return 1

def load_to_dataframe(file_content: bytes):
    """
    Loads the file content into a pandas DataFrame, attempting to handle both Excel (`.xlsx`) and Stata (`.dta`) formats.
    Args:
        file_content (bytes): The binary content of the file, typically retrieved from a cloud storage service like Dropbox.
        
    Returns:
        pandas.DataFrame: The loaded DataFrame from the file content.

    Raises:
        ValueError: If the file cannot be interpreted as either an Excel or Stata file, this error is raised.
    """
    try:
        return pd.read_excel(BytesIO(file_content))
    except Exception as excel_error:
        print("Failed to load as Excel, trying Stata format...")
        try:
            return pd.read_stata(BytesIO(file_content))
        except Exception as stata_error:
            raise ValueError("The file is neither a valid Excel (.xlsx) nor Stata (.dta) file.") from stata_error

def load_data_from_dropbox():
    """
    Loads data from a specified Dropbox account into a pandas DataFrame.
    
    Returns:
        pandas.DataFrame: The DataFrame containing the data loaded from the Dropbox file.

    Raises:
        ValueError: If no files are found in the Dropbox account, a ValueError will be raised when attempting to access the first file.
        Exception: Raises any other exceptions that may occur during Dropbox client creation or file retrieval.
    """
    load_dotenv()
    DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')

    # Verify the Dropbox client instantiation
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        print("Dropbox client created successfully")
    except AttributeError as e:
        print(f"Error: {e}")
    
    file = get_files(dbx, "")[0]
    data = get_file_content(dbx, file)
    df = load_to_dataframe(data)
    return df

def test_main():
    # Load environment variables from .env file
    load_dotenv()
    DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')
    
    # Verify the Dropbox client instantiation
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        print("Dropbox client created successfully")
    except AttributeError as e:
        print(f"Error: {e}")

    # filtered = get_files(dbx, "") # func 1
    # contents = get_file_content(dbx, '/desc.md') # func 2
    with open('internalUpdates.md', 'rb') as f: 
        data = f.read()
        result = upload_file(dbx, data, '/completed/desc2.md') # func 3
    print(result)
        

if __name__ == "__main__":
    test_main()