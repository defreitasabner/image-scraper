import re
from time import sleep
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class GoogleImageScraper:
    def __init__(self) -> None:
        self.__driver = webdriver.Chrome(
            service = Service(ChromeDriverManager().install()),
            options = self.__set_options()
        )

    def __set_options(self) -> Options:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('disable-extensions')
        options.add_argument("--window-size=1920x1080")
        return options

    def extract_hrefs_from_google_image_page(self, query: str, limit: int) -> list[str]:
        treated_query = query.strip().replace(' ', '+').lower()
        self.__driver.get(f'https://www.google.com/search?q={treated_query}')
        nav_menu = self.__driver.find_element(By.CLASS_NAME, 'crJ18e')
        nav_items = nav_menu.find_elements(By.TAG_NAME, 'div')
        img_button = next(filter(lambda item: item.text.startswith('Im') , nav_items), None)
        img_button.click()
        WebDriverWait(self.__driver, 10).until(
            EC.presence_of_element_located((By.ID, 'search'))
        )
        self.__driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        sleep(1)
        container = self.__driver.find_element(By.ID, 'search')
        titles = container.find_elements(By.TAG_NAME, 'h3')[:int(limit * 1.25)]
        hrefs = []
        for title in titles:
            try:
                title.find_element(By.TAG_NAME, 'img').click()
                sleep(0.1)
                hrefs.append(title.find_element(By.TAG_NAME, 'a').get_attribute('href'))
            except:
                pass
        self.__driver.close()
        return hrefs
    
    def extract_img_urls_from_hrefs(self, hrefs: list[str]) -> list[str]:
        pattern = re.compile(r"imgurl=([^&]+)")
        img_urls = []
        for href in hrefs:
            result = pattern.search(href)
            if result:
                extracted_url = result.group(1)
                decoded_url = urllib.parse.unquote(extracted_url)
                img_urls.append(decoded_url)
        return img_urls

