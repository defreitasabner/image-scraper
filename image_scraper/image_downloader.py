import os
from datetime import datetime

import requests


class ImageDownloader:
    def __init__(self, root_dir: str | None = None) -> None:
        pass

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
                img_path = os.path.join(dir_name, f'{prefix}_{counter}.jpg')
                with open(img_path, 'wb') as file:
                    file.write(img_data)
                counter += 1
            except:
                pass

