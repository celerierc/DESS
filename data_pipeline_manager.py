import os
import pandas as pd

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


def get_output_file():
    """Reads the complete Parquet file and does some post-processing to ensure stata conversion is optimized."""
    df = pd.read_parquet(f"{STORAGE_DIR}/complete.parquet")
    df = df.drop(columns='rawText')
    df = df[df['department'] != 'MISSING']
    return df


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
