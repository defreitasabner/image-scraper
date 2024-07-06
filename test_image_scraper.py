import os

import pytest

from image_scraper import ImageScraper

class TestImageScraper:

    def test_extract_img_urls_from_hrefs(self):
        hrefs_example = ['https://www.google.com/imgres?q=caliscelidae&imgurl=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Ff%2Fff%2FOmmadissW.jpg&imgrefurl=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FCaliscelidae&docid=Ee383zb8Cv7QMM&tbnid=vHC-nB0oRjdY8M&vet=12ahUKEwiKmLjR1JCHAxWXFbkGHcRFA4UQM3oECGoQAA..i&w=569&h=694&hcb=2&ved=2ahUKEwiKmLjR1JCHAxWXFbkGHcRFA4UQM3oECGoQAA']
        img_scraper = ImageScraper()

        img_urls = img_scraper.extract_img_urls_from_hrefs(hrefs_example)

        assert img_urls[0] == 'https://upload.wikimedia.org/wikipedia/commons/f/ff/OmmadissW.jpg'

