import sys
import argparse

from .google_image_scraper import GoogleImageScraper
from .image_downloader import ImageDownloader


class ImageScraperCLI:
    def __init__(self) -> None:
        self.__parser = argparse.ArgumentParser(description = 'Image Scraper CLI')
        self.__subparsers = self.__parser.add_subparsers()
        self.__settings()

    def __settings(self):
        parser_run = self.__subparsers.add_parser('run', help = 'Run a scrap routine')
        parser_run.add_argument(
            '-q', '--query', 
            type = str, 
            help = 'Write one or more word (dont forget to use ""), separated by space and without punctuation or accentuation.',
            required = True
        )
        parser_run.add_argument(
            '-l', 
            '--limit', 
            type = int, 
            help = 'Set the limit of downloaded images (default: 30).',
            default = 30
        )
        parser_run.add_argument(
            '-p', 
            '--prefix', 
            type = str, 
            help = 'Set downloaded image name prefix (default: image).',
        )
        parser_run.add_argument(
            '-v', 
            '--verbose',
            type = bool,
            help = 'Set to see logs.',
            action = 'store_true'
        )
        parser_run.set_defaults(func = self.__run_scrap_routine)

    def __run_scrap_routine(self, args):
        if not args.query:
            raise Exception('The argument "--query" is required.')
        image_scraper = GoogleImageScraper()
        hrefs = image_scraper.extract_hrefs_from_google_image_page(args.query, args.limit)
        if args.verbose:
            print(f'Images hrefs found: {len(hrefs)}')
        img_urls = image_scraper.extract_img_urls_from_hrefs(hrefs)
        if args.verbose:
            print(f'Images URLs extracted: {len(img_urls)}')
        img_downloader = ImageDownloader()
        img_downloader.download_images(img_urls, prefix = args.prefix)

    def main(self, argsv = None):
        args = self.__parser.parse_args(argsv)
        if hasattr(args, 'func'):
            args.func(args)
        else:
            self.__parser.print_help()

