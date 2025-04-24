import logging
from pathlib import Path

from PIL import Image

from base_classes import Loader


class ImageLoader(Loader):
    def load(self, input_path: Path) -> Image.Image:
        self.input_path = input_path
        with Image.open(self.input_path) as file:
            image = file.copy()
            logging.debug(f"Image loaded from {self.input_path}")
            return image
