import os
from datetime import datetime

import requests
from PIL import Image

class ImageDownloader:
    def __init__(self, root_dir: str | None = None) -> None:
        self.__allowed_formats = ['jpg', 'jpeg', 'png', 'webp']

    def download_images(
        self,
        img_urls: list[str], 
        limit: int,
        dir_name: str | None = None,
        prefix: str | None = None,
    ) -> None:
        if not dir_name:
            dir_name = datetime.now().strftime('%Y_%m_%d_%H%M')
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        prefix = prefix if prefix else 'image'
        downloaded_imgs = 0
        not_allowed_imgs = 0
        broken_imgs = 0
        for url in img_urls:
            if downloaded_imgs == limit:
                break
            try:
                img_format = url.split('.')[-1].split('?')[0]
                if img_format not in self.__allowed_formats:
                    not_allowed_imgs += 1
                    raise Exception(f'Not allowed format: {img_format}')
                img_data = requests.get(url, stream = True, timeout = 5).content
                img_path = os.path.join(dir_name, f'{prefix}_{downloaded_imgs}.{img_format}')
                with open(img_path, 'wb') as file:
                    file.write(img_data)
                img = Image.open(img_path)
                img.verify()
                downloaded_imgs += 1
            except (IOError, SyntaxError):
                broken_imgs += 1
            except:
                pass
        return downloaded_imgs, not_allowed_imgs, broken_imgs

