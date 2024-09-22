import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def search_google(name: str, university: str,snapshots:int):
    # Have options
    options = Options()
    options.headless = True
    # options.add_experimental_option("detach", True)
    service = Service('/opt/homebrew/bin/chromedriver')

    # pass options to driver
    driver = webdriver.Chrome(service=service, options=options)
    search_query = f'"{name}" {university} department'
    google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
    # print(f'Using URL = {google_url}')

    driver.get(google_url)

    time.sleep(3)  # Adjust sleep time as needed depending on page load time

    # Find the first 3 search results
    try:
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
                parse_text(div_text)
                completed += 1
            except:
                index += 1
                continue

            index += 1

    except Exception as e:
        print(f'Error while scraping', e)
        # driver.quit()

    # Close the driver
    driver.quit()


def parse_text(text: str):
    text = text.split('\n')
    # use enumerate
    for idx, t in enumerate(text):
        print(f'Index {idx}, text: {t}')


if __name__ == '__main__':
    search_google("Arnold Rosenbloom", "University of Toronto",4)
