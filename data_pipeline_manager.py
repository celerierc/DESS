import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import dropbox

load_dotenv()

STORAGE_DIR = "storage/"

def get_new_rows():
    """Reads the master (stata) dataset and returns new rows not present in 'complete' or 'reprocess' files."""
    df_master = pd.read_stata(f"{STORAGE_DIR}/input.dta")
    df_c = pd.read_parquet(f"{STORAGE_DIR}/complete.parquet")
    df_r = pd.read_parquet(f"{STORAGE_DIR}/reprocess.parquet")

    df_u = df_master[
        ~df_master['id_text'].isin(df_c['id_text']) & 
        ~df_master['id_text'].isin(df_r['id_text'])
    ]

    return df_u

def append_to_file(FILE_PATH: str, df: pd.DataFrame):
    """Appends new rows to the specified Parquet file. If the file doesn't exist, creates it."""
    if os.path.exists(FILE_PATH):
        print(f"APPENDING TO FILE: {FILE_PATH}")
        existing_df = pd.read_parquet(FILE_PATH)
        df = pd.concat([existing_df, df], ignore_index=True)
    else:
        print(f"CREATING NEW FILE: {FILE_PATH}")

    df.to_parquet(FILE_PATH, version=118)


def add_dess_columns(df: pd.DataFrame):
    """Adds custom DESS-related columns to the given DataFrame. This may change
    but generally includes: 'isProfessor', 'isProfessor2', 'rawText', and 'department'."""
    print(df.columns)
    # Add new empty columns directly to the DataFrame
    df['isProfessor'] = None
    df['isProfessor2'] = None
    df['rawText'] = None           
    df['department'] = ""
    return df


def get_merged_data_from_parallel_scrape(df1: pd.DataFrame, df2: pd.DataFrame, split_ratio: float =0.5):
    """Merges two DataFrames that were scraped in parallel to populate different sections of rawText."""
    if df1.shape != df2.shape or not df1.columns.equals(df2.columns):
        raise ValueError("DataFrames must have the same shape and columns to be merged.")
    
    split_index = int(len(df1) * split_ratio)
    merged_df = df1.copy()
    merged_df.loc[split_index:, 'rawText'] = df2.loc[split_index:, 'rawText']
    return merged_df

def update_internal_files(df_c: pd.DataFrame, df_r: pd.DataFrame, df_u: pd.DataFrame):
    """Updates the internal files with the given DataFrames."""
    # TODO: Test
    new_non_empty_rawText_rows = df_u[df_u['rawText'].apply(lambda x: isinstance(x, np.ndarray) and len(x) > 0)]
    new_empty_rawText_rows = df_u[~df_u['id_text'].isin(new_non_empty_rawText_rows['id_text'])]

    # Merging to complete.parquet + error checking
    updated_df_c, completed_conflicts = _safe_merge(df_c, new_non_empty_rawText_rows)
    if completed_conflicts:
        error_file_path = os.path.join(STORAGE_DIR, 'completed_conflicts.csv')
        completed_conflicts.to_csv(error_file_path, index = False)
        print(f"{len(completed_conflicts)} conflicts found updating complete.parquet. Conflicting rows saved to {error_file_path}.")

    # Merging to reprocess.parquet + error checking
    updated_df_r, reprocess_conflicts = _safe_merge(df_r, new_empty_rawText_rows)
    if reprocess_conflicts:
        error_file_path = os.path.join(STORAGE_DIR, 'reprocess_conflicts.csv')
        reprocess_conflicts.to_csv(error_file_path, index = False)
        print(f"{len(reprocess_conflicts)} conflicts found updating complete.parquet. Conflicting rows saved to {error_file_path}.")

    return updated_df_c, updated_df_r

def _safe_merge(df_master: pd.DataFrame, df: pd.DataFrame, col_name: str = 'id_text'):
    """Concatenates df to df_master, avoiding duplicate id_text entries."""
    conflicting_ids = df[col_name].isin(df_master[col_name])
    conflicts = df.loc[conflicting_ids, col_name].tolist()
    
    # Filter df to only non-conflicting rows
    df_to_add = df[~df[col_name].isin(conflicts)]
    
    # Concatenate safely
    df_combined = pd.concat([df_master, df_to_add], ignore_index=True)
    
    return df_combined, conflicts

def orchestrate_upload_workflow():
    # TODO: test & document
    for file_name in os.listdir(STORAGE_DIR):
        if file_name.endswith('.parquet'):
            file_path = os.path.join(STORAGE_DIR, file_name)
        
        _upload_file_to_dropbox(file_path)
        if file_name == 'complete.parquet':
            stata_file_path = _get_output_file()
            _upload_file_to_dropbox(stata_file_path)

def _upload_file_to_dropbox(file_path):
    """Uploads a file to Dropbox."""
    # TODO: test this function.
    access_token = os.getenv("DROPBOX_ACCESS_TOKEN")
    dropbox_folder = os.getenv("DROPBOX_FOLDER")
    file_name = os.path.basename(file_path)

    upload_path = f"/{dropbox_folder}/{file_name}"

    if not access_token or not dropbox_folder:
        raise ValueError("Access token and Dropbox folder must be set in the .env file.")
    
    dbx = dropbox.Dropbox(access_token) # dropbox client

    try:
        with open(file_path, 'rb') as f:
            dbx.files_upload(f.read(), upload_path)
        print(f"Successfully uploaded {file_name} to {upload_path}")
    except Exception as e:
        print(f"Error uploading {file_name} to Dropbox: {e}")
    

def _get_output_file():
    """Reads the complete Parquet file and does some post-processing to ensure stata conversion is optimized."""
    df = pd.read_parquet(f"{STORAGE_DIR}/complete.parquet")
    df = df.drop(columns='rawText')
    df = df[df['department'] != 'MISSING']
    stata_file_path = os.path.join(STORAGE_DIR, 'complete.dta')
    df.to_stata(stata_file_path)
    print(f"Successfully generated {stata_file_path}")
    return stata_file_path