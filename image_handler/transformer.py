from PIL import Image
import logging

from PIL import Image, ImageEnhance

from base_classes import Transformer
from .operations import ImageResizer, ColorModeConverter


class ImageTransformer(Transformer):
    def transform(self, image: Image.Image, instructions: dict) -> Image.Image:
        self.item = image
        self.instructions = instructions

        for operation, parameters in self.instructions.items():
            match operation:
                case 'rotate': self.item = self.item.rotate(parameters)
                case 'resize': self.item = ImageResizer(self.item, parameters).run()
                case 'color_mode': self.item = ColorModeConverter(self.item, parameters).run()
                case 'color_balance':
                    if isinstance(parameters, float):
                        enh = ImageEnhance.Color(self.item)
                        self.item = enh.enhance(parameters)
                case 'contrast':
                    if isinstance(parameters, float):
                        enh = ImageEnhance.Contrast(self.item)
                        self.item = enh.enhance(parameters)
                case 'brightness':
                    if isinstance(parameters, float):
                        enh = ImageEnhance.Brightness(self.item)
                        self.item = enh.enhance(parameters)
                case 'sharpness':
                    if isinstance(parameters, float):
                        enh = ImageEnhance.Sharpness(self.item)
                        self.item = enh.enhance(parameters)
                case _: raise ValueError(f"Unsupported operation {operation}")

        return self.item

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, new):
        if not isinstance(new, Image.Image):
            raise TypeError("IE: image must be an instance of PIL.Image.Image")
        self._item = new

