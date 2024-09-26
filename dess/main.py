#!python3
"""
This module provides functionality for populating a pandas DataFrame with data 
scraped from Google search results, as well as the NLP-analysis performed by the spaCy library
to ascertain department. 
"""
import pandas as pd
import dess.search as search
import dess.nlp as nlp

def populate_raw_text(df: pd.DataFrame, driver, snapshots: int) -> pd.Series:
    """Populates the rawText column in the DataFrame."""
    def fetch_raw_text(row):
        return search.get_snapshots_from_google(driver, row['Name'], row['University'], snapshots)
    
    return df.apply(fetch_raw_text, axis=1)


def populate_faculty_columns(df: pd.DataFrame):
    """Populates the isFaculty and department columns in the DataFrame."""
    df[['isFaculty', 'department']] = df.apply(
        lambda row: nlp.populate_faculty_columns(row['rawText']),
        axis=1,
        result_type='expand'
    )

def main(df: pd.DataFrame, driver_type: str, snapshots: int) -> pd.DataFrame:
    """
    Populates the DataFrame's rawText, isFaculty, and department columns.

    Args:
        df (pd.DataFrame): DataFrame containing the name and university columns.
        driver_type (str): Type of web driver to use ('chrome' or 'firefox').
        snapshots (int): The number of search results to retrieve for rawText.

    Returns:
        pd.DataFrame: Updated DataFrame with additional columns populated.
    """
    
    driver = search.setup_driver(driver_type)

    df['rawText'] = populate_raw_text(df, driver, snapshots)

    driver.quit()
    
    # populate_faculty_columns(df)

    return df

def test_main():
    df = pd.DataFrame({'Name': ['Tyler Holden', 'Arnold Rosenbloom','Anant Agarwal'], 
                       'University': ['University of Toronto', 'University of Toronto','Massachusetts Institute of Technology']})
    df = main(df, 'firefox', 2)
    print(df['rawText'].to_list())
    
if __name__ == '__main__':
    test_main()