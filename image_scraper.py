import re
from time import sleep
import urllib.parse
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

class ImageScraper:
    def __init__(self) -> None:
        self.__driver = webdriver.Chrome(
            service = Service(ChromeDriverManager().install()),
            options = self.__select_options()
        )

    def __select_options(self) -> Options:
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
        container = self.__driver.find_element(By.ID, 'search')
        titles = container.find_elements(By.TAG_NAME, 'h3')[:limit]
        hrefs = []
        for title in titles:
            try:
                title.find_element(By.TAG_NAME, 'img').click()
                sleep(0.1)
                hrefs.append(title.find_element(By.TAG_NAME, 'a').get_attribute('href'))
            except:
                pass
        self.__driver.close()
        print(f'Images hrefs found: {len(hrefs)}')
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
        print(f'Images URLs extracted: {len(img_urls)}')
        return img_urls
    
    def download_images(self, img_urls: list[str]) -> None:
        dir_name = datetime.now().strftime('%Y_%m_%d_%H%M')
        os.mkdir(dir_name)
        counter = 0
        for url in img_urls:
            try:
                img_data = requests.get(url, stream = True, timeout = 5).content
                with open(f'{dir_name}/image_{counter}.jpg', 'wb') as file:
                    file.write(img_data)
                counter += 1
            except:
                pass
        print(f'Downloaded Images: {counter}')

if __name__ == '__main__':
    image_scraper = ImageScraper()
    hrefs = image_scraper.extract_hrefs_from_google_image_page('Yoga Pose Cobra', 100)
    img_urls = image_scraper.extract_img_urls_from_hrefs(hrefs)
    image_scraper.download_images(img_urls)