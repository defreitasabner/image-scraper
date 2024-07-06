from google_image_scraper import GoogleImageScraper
from image_downloader import ImageDownloader


if __name__ == '__main__':
    image_scraper = GoogleImageScraper()
    hrefs = image_scraper.extract_hrefs_from_google_image_page('Yoga Pose Cobra', 100)
    img_urls = image_scraper.extract_img_urls_from_hrefs(hrefs)
    img_downloader = ImageDownloader()
    img_downloader.download_images(img_urls)