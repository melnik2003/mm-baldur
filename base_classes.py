from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Any


class MediaHandler(ABC):
    @abstractmethod
    def run(self, input_path: Path, target_path: Path, params: dict) -> bool:
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def save(self):
        pass


class Loader(ABC):
    def __init__(self):
        self._input_path: Optional[Path] = None

    @abstractmethod
    def load(self, input_path: Path) -> Any:  # Ensure path is validated
        pass

    @property
    def input_path(self):
        return self._input_path

    @input_path.setter
    def input_path(self, new):
        if not isinstance(new, Path):
            raise TypeError("IE: input_path must be an instance of Path and validated beforehand")
        if not new.is_file():
            raise ValueError("IE: input_path must be a valid file path and validated beforehand")
        self._input_path = new


class Transformer(ABC):
    def __init__(self):
        self._item: Any = None
        self._instructions: Optional[dict] = None

    @abstractmethod
    def transform(self, item, instructions) -> Any:
        pass

    @property
    def instructions(self):
        return self._instructions.copy()

    @instructions.setter
    def instructions(self, new):
        if not isinstance(new, dict):
            raise TypeError("IE: instructions must be a dictionary")
        self._instructions = new


class Saver(ABC):
    def __init__(self):
        self._item: Any = None
        self._target_path: Optional[Path] = None

    @abstractmethod
    def save(self, item, target_path) -> None:
        pass

    @property
    def target_path(self):
        return self._target_path

    @target_path.setter
    def target_path(self, new):
        if not isinstance(new, Path):
            raise TypeError("IE: target_path must be an instance of Path")
        self._target_path = new