#!python3

"""
main.py

This module serves as the entry point for the DESS application. It is responsible for loading 
data, processing it through the `prune_dataframe` function, and passing the processed DataFrame 
to the DESS module for further operations.
"""

import os
import time
import pandas as pd
import fileio
from dess.main import main as dess

LOCAL_PARQUET_PATH = 'storage/ds.parquet'
CHUNK_SIZE = 200

def prune_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters and prepares the DataFrame for further processing.

    This function extracts the relevant columns from the DataFrame and adds new columns that 
    will be populated later in the workflow. The structure of this function may evolve as 
    the application's requirements change.

    Args:
        df (pd.DataFrame): The input DataFrame containing various columns.

    Returns:
        pd.DataFrame: A new DataFrame with selected columns (name, university) and additional 
                      empty columns for isFaculty, rawText, and department.
    """
    print(df.columns)
    # df = df[['id_text']].copy() 
    # Add new empty columns directly to the DataFrame
    df['isProfessor'] = None           
    df['rawText'] = None               
    df['department'] = ""
    return df

def process_and_cache(df):
    print('begun processing')
    start = time.time()
    for i in range(3400, len(df), CHUNK_SIZE):
        chunk = df.iloc[i:i + CHUNK_SIZE].copy()
        chunk = dess(chunk, 'firefox', 4)
        df.iloc[i:i + CHUNK_SIZE, df.columns.get_loc('rawText')] = chunk['rawText']
        df.to_parquet(LOCAL_PARQUET_PATH, index=False)
        current_time = time.time()
        time_taken = current_time - start
        start = current_time
        print(f"[{time_taken:.2f}] Processed and updated chunk {i // CHUNK_SIZE} of {df.shape[0] // CHUNK_SIZE}")

def main():
    # Step 1: Loading the data structure
    if os.path.exists(LOCAL_PARQUET_PATH):
        print("Loading DataFrame from local ...")
        df = pd.read_parquet(LOCAL_PARQUET_PATH)
    else:
        print("Loading data from Dropbox (and caching parquet file)...")
        df = fileio.load_data_from_dropbox() 
    # df = prune_dataframe(df)
    # df.to_parquet(LOCAL_PARQUET_PATH, index=False)
    # print(df)
    process_and_cache(df)

    # # Step 2: pass data to DESS module
    # df = dess(df, 'firefox', 4)

def examine_results():
    # df = pd.read_csv('storage/ds_100_spacy.csv')
    # present_df = df[df['department'] != "MISSING"]
    # # print(f"Count of 'MISSING': {missing_df.shape[0]}")
    # pd.set_option('display.max_rows', None)  
    # pd.set_option('display.max_colwidth', None)
    # pd.set_option('display.max_colwidth', None)
    # print(present_df['department'])
    df = pd.read_parquet(LOCAL_PARQUET_PATH)
    df.to_csv('storage/ds.csv')

if __name__ == "__main__":
    # main()
    examine_results()