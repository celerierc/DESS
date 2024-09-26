"""
Provides functionality to create web drivers for Chrome and Firefox using Selenium, perform Google 
searches, and parse the search results.

Dependencies:
- Selenium: A browser automation framework. Ensure that the appropriate browser driver (ChromeDriver or GeckoDriver) 
is installed and accessible in your PATH.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FireFoxOptions
import time

def setup_driver(driver_type: str) -> webdriver:
    """Sets up the web driver based on the specified type."""
    if driver_type == 'chrome':
        return create_chrome_driver()
    elif driver_type == 'firefox':
        return create_firefox_driver()
    else:
        raise ValueError("Invalid driver type specified. Use 'chrome' or 'firefox'.")


def create_chrome_driver():
    """
    Initializes and returns a Chrome web driver with specified options.

    Returns:
        webdriver.Chrome: An instance of the Chrome web driver configured with headless options.
    """
    options = Options()
    options.add_argument("--headless")
    #options.add_experimental_option("detach", True)
    service = Service('/opt/homebrew/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def create_firefox_driver():
    """
    Initializes and returns a Firefox web driver with specified options.

    Returns:
        webdriver.Firefox: An instance of the Chrome web driver configured with headless options.
    """
    # Set up Selenium options
    options = FireFoxOptions()
    options.set_preference("dom.popup_maximum", 0)
    options.set_preference("privacy.popups.disable_from_plugins", 3)
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    return driver

def get_snapshots_from_google(driver: webdriver,name: str, university: str,snapshots:int):
    """
    Performs a Google search for the given name and university, and retrieves specified snapshots of the search results.

    Args:
        driver (webdriver): The web driver instance to use for the search.
        name (str): The name to search for.
        university (str): The university to include in the search query.
        snapshots (int): The number of result snapshots to retrieve.

    Returns:
        list: A list containing the parsed text of the search result snapshots.

    Raises:
        Exception: Raises an exception if there is an error during the search or result retrieval.
    """
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
        return feature_vector

    except Exception as e:
        print(f'Error while scraping', e)
        # driver.quit()

def parse_text(text: str):
    text = text.split('\n')
    # use enumerate
    # for idx, t in enumerate(text):
    #     #print(f'Index {idx}, text: {t}')
    return text[-1].strip()

if __name__ == '__main__':
    get_snapshots_from_google("Tyler Holden", "University of Toronto",4)
