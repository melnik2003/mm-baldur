import logging
from pathlib import Path

from PIL import Image

from base_classes import Saver


class ImageSaver(Saver):
    def save(self, image: Image.Image, target_path: Path) -> None:
        self.item = image
        self.target_path = target_path

        self.item.save(self.target_path)

        logging.debug(f"Image saved to {self.target_path}")

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, new):
        if not isinstance(new, Image.Image):
            raise TypeError("IE: image must be an instance of PIL.Image.Image")
        self._item = new
