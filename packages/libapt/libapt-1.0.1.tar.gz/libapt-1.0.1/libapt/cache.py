"""Interfaces for caching."""

import logging
import hashlib
import os
import shutil
import tempfile

from abc import ABC, abstractmethod
from pathlib import Path


class Cache(ABC):
    """Generic interface for APT metadata cache."""

    @abstractmethod
    def store_file(self, id: str, file: Path) -> Path | None:
        """
        Store the given file in the cache.

        :param id: ID of the artifact to store.
        :param file: Path of the file to store.
        :returns: Path to the cache file.
        """

    @abstractmethod
    def store_data(self, id: str, data: bytes) -> Path:
        """
        Store the given data in the cache.

        :param id: ID of the artifact to store.
        :param data: Binary data to store.
        :returns: Path to the cache file.
        """

    @abstractmethod
    def contains(self, id: str) -> bool:
        """
        Test if an artifact with the given ID is stored.

        :param id: ID of the artifact.
        :returns: True if the artifact is available, false else.
        """

    @abstractmethod
    def get_file(self, id: str, file: Path | None = None) -> Path | None:
        """
        Get the stored data as temporary file.

        :param id: ID of the artifact to load.
        :param file: Path where to put the file.
        :returns: Path to the temporary file.
        """

    @abstractmethod
    def get_data(self, id: str) -> bytes | None:
        """
        Get the stored data as bytes.

        :param id: ID of the artifact to load.
        :returns: Data as bytes.
        """


class DefaultCache(Cache):
    """Generic interface for APT metadata cache."""

    def __init__(self, cache_folder: list[str] = [".elische", "cache"]) -> None:
        """
        Init the cache.

        :param cache_folder: Cache folder path from home folder als list of str.
        """
        self._cache_dir = Path.home()
        for d in cache_folder:
            self._cache_dir = self._cache_dir / d
        logging.info("Using cache folder %s.", self._cache_dir)
        os.makedirs(self._cache_dir, exist_ok=True)

    def _cache_file(self, id: str) -> Path:
        """
        Get cache file for ID.

        :param id: ID of the cache entry.
        :returns: Cache file as Path.
        """
        name = hashlib.md5(id.encode()).hexdigest()
        return self._cache_dir / name

    def clear_cache(self):
        """
        Delete all cached data.
        """
        shutil.rmtree(self._cache_dir)
        os.makedirs(self._cache_dir, exist_ok=True)

    def store_file(self, id: str, file: Path) -> Path | None:
        """
        Store the given file in the cache.

        :param id: ID of the artifact to store.
        :param file: Path of the file to store.
        :returns: True if the file was stored, false else.
        """
        if not os.path.exists(file) or os.path.isdir(file):
            return None

        cache_file = self._cache_file(id)
        shutil.copy(file, cache_file, follow_symlinks=True)
        return cache_file

    def store_data(self, id: str, data: bytes) -> Path:
        """
        Store the given data in the cache.

        :param id: ID of the artifact to store.
        :param data: Binary data to store.
        :returns: True if the file was stored, false else.
        """
        cache_file = self._cache_file(id)
        with open(cache_file, "wb") as f:
            f.write(data)
        return cache_file

    def contains(self, id: str) -> bool:
        """
        Test if an artifact with the given ID is stored.

        :param id: ID of the artifact.
        :returns: True if the artifact is available, false else.
        """
        cache_file = self._cache_file(id)
        return os.path.isfile(cache_file)

    def get_file(self, id: str, file: Path | None = None) -> Path | None:
        """
        Get the stored data as temporary file.

        :param id: ID of the artifact to load.
        :param file: Path where to put the file.
        :returns: Path to the temporary file.
        """
        if file is None:
            file = Path(tempfile.NamedTemporaryFile().name)

        cache_file = self._cache_file(id)
        if os.path.isfile(cache_file):
            os.makedirs(file.parent, exist_ok=True)
            shutil.copy(cache_file, file)
            return file

        return None

    def get_data(self, id: str) -> bytes | None:
        """
        Get the stored data as bytes.

        :param id: ID of the artifact to load.
        :returns: Data as bytes.
        """
        cache_file = self._cache_file(id)
        if os.path.isfile(cache_file):
            with open(cache_file, "rb") as f:
                data = f.read()
            return data

        return None
