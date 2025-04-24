from pathlib import Path
from typing import Optional

from PIL import Image

from logging_tools import get_logger
from base_classes import MediaHandler
from .loader import ImageLoader
from .transformer import ImageTransformer
from .saver import ImageSaver


logger = get_logger()

class ImageHandler(MediaHandler):
    def __init__(self):
        self.loader = ImageLoader()
        self.transformer = ImageTransformer()
        self.saver = ImageSaver()

        self.input_path: Optional[Path] = None
        self.target_path: Optional[Path] = None
        self.operations: Optional[dict] = None

        self.image: Optional[Image.Image] = None

    def run(self, input_path: Path, target_path: Path, operations: dict) -> bool: # True if success
        self.input_path = input_path
        self.target_path = target_path
        self.operations = operations

        try:
            self.load()
        except Exception as e:
            logger.error(f"Error loading image {self.input_path}: {e}")
            raise

        try:
            self.transform()
        except Exception as e:
            logger.error(f"Error transforming image {self.input_path}: {e}")
            raise

        try:
            self.save()
        except Exception as e:
            logger.error(f"Error saving image {self.input_path}: {e}")
            raise

        logger.debug(f"Successfully processed image: {self.input_path} -> {self.target_path}")
        return True

    def load(self) -> None:
        self.image = self.loader.load(self.input_path)

    def transform(self) -> None:
        self.image = self.transformer.transform(self.image, self.operations)

    def save(self) -> None:
        self.saver.save(self.image, self.target_path)

