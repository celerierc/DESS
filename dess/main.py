import pandas as pd
import numpy as np
from search import *

'''
Given the dataframe df containing the name of the professor and the university as columns,
create a new column called raw_text that contains the text scraped from the first 3 search results
'''
def create_chrome_driver():
   
    options = Options()
    options.add_argument("--headless")
    #options.add_experimental_option("detach", True)
    service = Service('/opt/homebrew/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def main(df: pd.DataFrame):
    name_list = df['Name'].tolist()
    university_list = df['University'].tolist()
    driver = create_chrome_driver()
    raw_text_vector = []
    for i in range(len(name_list)):
        raw_text = search_google(driver,name_list[i], university_list[i], 2)
        #raw_text is a list of strings
        raw_text_vector.append(raw_text)
    df['raw_text'] = raw_text_vector
    
    return df

def test_main():
    df = pd.DataFrame({'Name': ['Tyler Holden', 'Arnold Rosenbloom','Anant Agarwal'], 'University': ['University of Toronto', 'University of Toronto','Massachusetts Institute of Technology']})
    df = main(df)
    print(df['raw_text'].tolist())
    
test_main()
    
    