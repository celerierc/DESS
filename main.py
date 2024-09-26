#!python3

"""
main.py

This module serves as the entry point for the DESS application. It is responsible for loading 
data, processing it through the `prune_dataframe` function, and passing the processed DataFrame 
to the DESS module for further operations.
"""

import os
import fileio
import pandas as pd
from dess.main import main as dess

LOCAL_PARQUET_PATH = 'storage/ds.parquet'

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
    df = df[['AgyTitle', 'Name']].copy() 
    # Add new empty columns directly to the DataFrame
    df['isFaculty'] = None           
    df['rawText'] = None               
    df['department'] = ""
    return df

def main():
    # Step 1: Loading the data structure
    if os.path.exists(LOCAL_PARQUET_PATH):
        print("Loading DataFrame from local ...")
        df = pd.read_parquet(LOCAL_PARQUET_PATH)
    else:
        print("Loading data from Dropbox (and caching parquet file)...")
        df = fileio.load_data_from_dropbox() 
    df = prune_dataframe(df)
    df_last = df.tail(3)
    print(df_last)

    # Step 2: pass data to DESS module
    dess(df, 'firefox', 2)


if __name__ == "__main__":
    main()