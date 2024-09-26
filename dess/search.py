import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def search_google(driver,name: str, university: str,snapshots:int):
    search_query = f'"{name}" {university}'
    google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
    driver.get(google_url)

    time.sleep(2)  

    # Find the first snapshot search results
    try:
        #This will contain the raw text from the search results
        feature_vector = []
        results = driver.find_elements(By.XPATH, '//div[@class="MjjYud"]')
        no_of_wanted_results = snapshots
        completed = 0
        index = 0
        while completed != no_of_wanted_results:
            div_element = results[index]
            try:
                span_text = div_element.find_element(By.XPATH, './/span').text
                if span_text == 'People also ask':
                    index += 1
                    continue
                div_text = div_element.text
                feature_vector.append(parse_text(div_text))
                completed += 1
            except:
                index += 1
                continue

            index += 1
        #print(f'Feature vector: {feature_vector}')
        return feature_vector

    except Exception as e:
        print(f'Error while scraping', e)
        # driver.quit()

    # Close the driver
    #driver.quit()


def parse_text(text: str):
    text = text.split('\n')
    # use enumerate
    # for idx, t in enumerate(text):
    #     #print(f'Index {idx}, text: {t}')
    return text[-1].strip()

if __name__ == '__main__':
    search_google("Tyler Holden", "University of Toronto",4)
