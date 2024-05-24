from abc import ABC, abstractmethod
from pathlib import Path


class AbstractExcelParser(ABC):
    @classmethod
    @abstractmethod
    def read_file(cls, path: Path | str):
        raise NotImplementedError
