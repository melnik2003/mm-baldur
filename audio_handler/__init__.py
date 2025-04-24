from base_classes import MediaHandler
from pathlib import Path


class AudioHandler(MediaHandler):
    def run(self, input_path: Path, target_path: Path, params: dict) -> bool:
        pass

    def load(self):
        pass

    def transform(self):
        pass

    def save(self):
        pass