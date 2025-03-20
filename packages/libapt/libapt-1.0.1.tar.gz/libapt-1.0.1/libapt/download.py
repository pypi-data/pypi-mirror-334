"""Interfaces for downloading assets."""

import hashlib
import logging
import tempfile
import shutil

from abc import ABC, abstractmethod
from pathlib import Path

import requests

from libapt.cache import Cache


class Downloader(ABC):
    """Generic interface for downloading resources."""

    @abstractmethod
    def download_file(
        self, url: str, folder: Path | None = None, name: str | None = None, bypass_cache: bool = False
    ) -> Path:
        """
        Download the given url as temporary file.

        :param url: URL of the artifact to download.
        :param folder: Folder to place the downloaded file.
        :param name: Filename for the downloaded file.
        :param bypass_cache: Bypass the cache.
        :returns:   Path to the downloaded file.
        """

    @abstractmethod
    def download(self, url: str, bypass_cache: bool = False) -> bytes:
        """
        Download the given url.

        :param url: URL of the artifact to download.
        :param bypass_cache: Bypass the cache.
        :returns: Data of the URL.
        """


class DownloadFailed(Exception):
    """Raised if a download failed."""


class DefaultDownloader(Downloader):
    """Default downloader implementation."""

    def __init__(self, cache: Cache | None = None):
        self._tmpdir = Path(tempfile.mkdtemp())
        self._cache = cache

    def __del__(self):
        shutil.rmtree(self._tmpdir)

    def download_file(
        self, url: str, folder: Path | None = None, name: str | None = None, bypass_cache: bool = False
    ) -> Path:
        """
        Download the given url as temporary file.

        :param url: URL of the artifact to download.
        :param folder: Folder to place the downloaded file.
        :param name: Filename for the downloaded file.
        :param bypass_cache: Bypass the cache.
        :returns: Path to the downloaded file.
        :raises DownloadFailed: Raises an DownloadFailed exception if the download fails.
        """
        if not name:
            name = hashlib.md5(url.encode()).hexdigest()

        if folder:
            file = folder / name
        else:
            file = self._tmpdir / name

        if not bypass_cache and self._cache:
            cache_file = self._cache.get_file(url, file=file)
            if cache_file:
                return cache_file

        response = requests.get(url)

        if response.status_code >= 400:
            logging.info("Download of %s failed. Return code: %s.", url, response.status_code)
            raise DownloadFailed(f"Download of {url} failed. Return code: {response.status_code}.")

        with open(file, "wb") as f:
            f.write(response.content)

        return file

    def download(self, url: str, bypass_cache: bool = False) -> bytes:
        """
        Download the given url.

        :param url: URL of the artifact to download.
        :param bypass_cache: Bypass the cache.
        :returns: Data of the URL.
        :raises DownloadFailed: Raises an DownloadFailed exception if the download fails.
        """
        if not bypass_cache and self._cache:
            data = self._cache.get_data(url)
            if data:
                return data

        response = requests.get(url)

        if response.status_code >= 400:
            logging.info("Download of %s failed. Return code: %s.", url, response.status_code)
            raise DownloadFailed(f"Download of {url} failed. Return code: {response.status_code}.")

        return response.content
