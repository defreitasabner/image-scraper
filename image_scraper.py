import re
from time import sleep
import urllib.parse
import os

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
        self.chrome_options = Options()
        self.chrome_options.add_argument('no--sandbox')
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('disable-extensions')
        
        self.browser = webdriver.Chrome(
            service = Service(ChromeDriverManager().install()),
            options = self.chrome_options
        )

    def extract_hrefs_from_google_image_page(self, keyword: str, quantity: int):
        self.browser.get(f'https://www.google.com/search?q={keyword}')
        nav_menu = self.browser.find_element(By.XPATH, '//*[@id="cnt"]/div[4]')
        img_button = nav_menu.find_element(By.XPATH, '//*[@id="hdtb-sc"]/div/div/div[1]/div/div[2]/a')
        img_button.click()
        container = self.browser.find_element(By.XPATH, '//*[@id="rcnt"]')
        titles = container.find_elements(By.TAG_NAME, 'h3')[:quantity]
        hrefs = []
        for title in titles:
            try:
                title.find_element(By.TAG_NAME, 'img').click()
                sleep(0.1)
                hrefs.append(title.find_element(By.TAG_NAME, 'a').get_attribute('href'))
            except:
                pass
        return hrefs
    
    def extract_img_urls_from_hrefs(self, hrefs):
        pattern = re.compile(r"imgurl=([^&]+)")
        img_urls = []
        for href in hrefs:
            result = pattern.search(href)
            if result:
                extracted_url = result.group(1)
                decoded_url = urllib.parse.unquote(extracted_url)
                img_urls.append(decoded_url)
        return img_urls
    
    def download_images(self, img_urls):
        for url in img_urls:
            img_data = requests.get(url, stream = True).content
            counter = 0
            with open(f'image_{counter}.jpg', 'wb') as file:
                file.write(img_data)
                counter += 1

if __name__ == '__main__':
    image_scraper = ImageScraper()
    hrefs = image_scraper.extract_hrefs_from_google_image_page('caliscelidae', 1)
    img_urls = image_scraper.extract_img_urls_from_hrefs(hrefs)
    image_scraper.download_images(img_urls)