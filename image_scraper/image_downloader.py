import os
from datetime import datetime

import requests


class ImageDownloader:
    def __init__(self, root_dir: str | None = None) -> None:
        self.__ROOT_DIR = self.__set_root_dir(root_dir)

    def __set_root_dir(self, root_dir):
        return root_dir if root_dir else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def download_images(
        self, 
        img_urls: list[str], 
        dir_name: str | None = None,
        prefix: str | None = None,
    ) -> None:
        if not dir_name:
            dir_name = datetime.now().strftime('%Y_%m_%d_%H%M')
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        prefix = prefix if prefix else 'image'
        counter = 0
        for url in img_urls:
            try:
                img_data = requests.get(url, stream = True, timeout = 5).content
                img_path = os.path.join(self.__ROOT_DIR, dir_name, f'{prefix}_{counter}.jpg') 
                with open(img_path, 'wb') as file:
                    file.write(img_data)
                counter += 1
            except:
                pass

