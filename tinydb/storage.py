import io
import json
import os
import warnings
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import typer

print(typer.__file__)

print(os.__file__)

__all__ = ("Storage", "JSONStorage", "MemoryStorage")


def touch(path: str, create_dirs: bool) -> None:

    if create_dirs:
        base_dir = os.path.dirname(path)

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

    with open(path, "a"):
        pass


class Storage(ABC):
    @abstractmethod
    def read(self) -> Optional[Dict[str, Dict[str, Any]]]:
        raise NotImplementedError("To be overridden!")

    @abstractmethod
    def write(self, data: Dict[str, Dict[str, Any]]) -> None:
        raise NotImplementedError("To be overridden!")

    def close(self) -> None:
        pass


class JSONStorage(Storage):
    def __init__(
        self, path: str, create_dirs=False, encoding=None, access_mode="r+", **kwargs
    ):

        super().__init__()

        self._mode = access_mode
        self.kwargs = kwargs

        if access_mode not in ("r", "rb", "r+", "rb+"):
            warnings.warn(
                "Using an `access_mode` other than 'r', 'rb', 'r+' "
                "or 'rb+' can cause data loss or corruption"
            )

        if any([character in self._mode for character in ("+", "w", "a")]):
            touch(path, create_dirs=create_dirs)

        self._handle = open(path, mode=self._mode, encoding=encoding)

    def close(self) -> None:
        self._handle.close()

    def read(self) -> Optional[Dict[str, Dict[str, Any]]]:
        self._handle.seek(0, os.SEEK_END)
        size = self._handle.tell()

        if not size:
            return None
        else:
            self._handle.seek(0)

            return json.load(self._handle)

    def write(self, data: Dict[str, Dict[str, Any]]):
        self._handle.seek(0)

        serialized = json.dumps(data, **self.kwargs)

        try:
            self._handle.write(serialized)
        except io.UnsupportedOperation:
            raise IOError(
                'Cannot write to the database. Access mode is "{0}"'.format(self._mode)
            )

        self._handle.flush()
        os.fsync(self._handle.fileno())

        self._handle.truncate()


class MemoryStorage(Storage):
    pass
