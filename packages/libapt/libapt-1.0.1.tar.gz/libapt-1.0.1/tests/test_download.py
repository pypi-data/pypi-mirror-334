"""Tests for Downloader."""

import os

from pathlib import Path

import pytest

from libapt.cache import DefaultCache
from libapt.download import DefaultDownloader, DownloadFailed


test_data = Path(__file__).parent / "data"


class TestDownloader:
    """Tests for Downloader."""

    def test_cleanup_temporary_folder(self) -> None:
        """Test that the downloader deletes the temporary folder."""
        downloader = DefaultDownloader()
        tmpdir = downloader._tmpdir
        assert tmpdir is not None
        assert os.path.isdir(tmpdir)
        del downloader
        assert not os.path.isdir(tmpdir)

    def test_download_file(self):
        """Test downloading a file."""
        url = "https://raw.githubusercontent.com/eLiSCHe/libapt/903fcbaa956129d67ed2db1f6925af954bb07717/tests/data/Package"
        reference = test_data / "Package"

        downloader = DefaultDownloader(cache=DefaultCache())
        file = downloader.download_file(url)

        assert file.parent == downloader._tmpdir

        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        with open(reference, "r", encoding="utf-8") as f:
            reference_content = f.read()

        assert content == reference_content

    def test_download_file_failed(self):
        """Test downloading a file."""
        url = (
            "https://raw.githubusercontent.com/eLiSCHe/libapt/903fcbaa956129d67ed2db1f6925af954bb07717/tests/data/None"
        )

        downloader = DefaultDownloader()

        with pytest.raises(DownloadFailed):
            downloader.download_file(url)

    def test_download(self):
        """Test downloading a file."""
        url = "https://raw.githubusercontent.com/eLiSCHe/libapt/903fcbaa956129d67ed2db1f6925af954bb07717/tests/data/Package"
        reference = test_data / "Package"

        downloader = DefaultDownloader(cache=DefaultCache())
        content = downloader.download(url).decode(encoding="utf-8")

        with open(reference, "r", encoding="utf-8") as f:
            reference_content = f.read()

        assert content == reference_content

    def test_download_failed(self):
        """Test downloading a file."""
        url = (
            "https://raw.githubusercontent.com/eLiSCHe/libapt/903fcbaa956129d67ed2db1f6925af954bb07717/tests/data/None"
        )

        downloader = DefaultDownloader()

        with pytest.raises(DownloadFailed):
            downloader.download(url)

    def test_download_cache_hit(self):
        """Test downloading a file from the cache."""

        url = "https://wrong/tests/data/Package"
        reference = test_data / "Package"

        cache = DefaultCache()
        cache.store_file(url, reference)

        downloader = DefaultDownloader(cache=cache)
        file = downloader.download_file(url)

        assert file.parent == downloader._tmpdir

        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        with open(reference, "r", encoding="utf-8") as f:
            reference_content = f.read()

        assert content == reference_content

    def test_download_to_folder(self, tmp_path):
        """Test downloading a file to a given folder."""

        url = "https://some.url"
        reference = test_data / "Package"

        cache = DefaultCache()
        cache.store_file(url, reference)

        downloader = DefaultDownloader(cache=cache)

        file = downloader.download_file(url, folder=tmp_path)

        assert file.parent == tmp_path

        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        with open(reference, "r", encoding="utf-8") as f:
            reference_content = f.read()

        assert content == reference_content

    def test_download_to_file(self, tmp_path):
        """Test downloading a file to a given name."""

        url = "https://some-other.url"
        reference = test_data / "Package"

        cache = DefaultCache()
        cache.store_file(url, reference)

        downloader = DefaultDownloader(cache=cache)

        name = "myfile"

        file = downloader.download_file(url, folder=tmp_path, name=name)

        assert file == tmp_path / name

        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        with open(reference, "r", encoding="utf-8") as f:
            reference_content = f.read()

        assert content == reference_content

    def test_download_data_cache_hit(self):
        """Test downloading data from the cache."""

        url = "https://wrong/tests/data/Package"
        reference = test_data / "Package"

        cache = DefaultCache()
        cache.store_file(url, reference)

        downloader = DefaultDownloader(cache=cache)
        data = downloader.download(url)
        content = data.decode(encoding="utf-8")

        with open(reference, "r", encoding="utf-8") as f:
            reference_content = f.read()

        assert content == reference_content
