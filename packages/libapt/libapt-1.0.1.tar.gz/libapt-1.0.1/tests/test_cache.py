"""Tests for Downloader."""

import os
import hashlib

from pathlib import Path

from libapt.cache import DefaultCache


test_data = Path(__file__).parent / "data"


class TestDownloader:
    """Tests for Downloader."""

    def test_cache_folder(self) -> None:
        """Test the default cache folder location."""
        cache = DefaultCache()
        cache_dir = cache._cache_dir
        assert cache_dir is not None
        assert cache_dir == Path.home() / ".elische" / "cache"
        assert os.path.isdir(cache_dir)

    def test_custom_cache_folder(self) -> None:
        """Test the default cache folder location."""
        cache = DefaultCache(cache_folder=[".my", "cache", "dir"])
        cache_dir = cache._cache_dir
        assert cache_dir is not None
        assert cache_dir == Path.home() / ".my" / "cache" / "dir"
        assert os.path.isdir(cache_dir)

    def test_store_file(self):
        """Test storing a file."""
        file = test_data / "Package"

        cache = DefaultCache()
        cache_file = cache.store_file("MyPackages", file)

        assert cache_file

        expected_cache_file_name = hashlib.md5("MyPackages".encode()).hexdigest()
        assert cache_file == cache._cache_dir / expected_cache_file_name

        assert os.path.isfile(cache_file)

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        with open(cache_file, "r", encoding="utf-8") as f:
            cache_content = f.read()
        assert content == cache_content

    def test_store_data(self):
        """Test storing data."""
        data = "Hello, World!"

        cache = DefaultCache()
        cache_file = cache.store_data("Hello", data.encode(encoding="utf-8"))

        assert cache_file

        expected_cache_file_name = hashlib.md5("Hello".encode()).hexdigest()
        assert cache_file == cache._cache_dir / expected_cache_file_name

        assert os.path.isfile(cache_file)

        with open(cache_file, "r", encoding="utf-8") as f:
            cache_content = f.read()
        assert data == cache_content

    def test_clear_cache(self):
        """Test clearing the cache folder."""
        data = "Hello, World!"

        cache = DefaultCache()
        cache_file = cache.store_data("Hello", data.encode(encoding="utf-8"))

        assert cache_file

        expected_cache_file_name = hashlib.md5("Hello".encode()).hexdigest()
        assert cache_file == cache._cache_dir / expected_cache_file_name

        assert os.path.isfile(cache_file)

        cache.clear_cache()

        assert os.path.isdir(cache._cache_dir)
        assert not os.path.exists(cache_file)

    def test_contains(self):
        """Test contains check."""
        id = "Hello"
        data = "Hello, World!"

        cache = DefaultCache()
        cache.store_data(id, data.encode(encoding="utf-8"))

        assert cache.contains(id)

        del cache
        cache = DefaultCache()

        assert cache.contains(id)

    def test_get_data(self):
        """Test retrieving data from cache."""
        id = "Hello"
        data = "Hello, World!"

        cache = DefaultCache()
        cache.store_data(id, data.encode(encoding="utf-8"))

        cache_data = cache.get_data(id).decode(encoding="utf-8")
        assert cache_data == data

        del cache
        cache = DefaultCache()

        cache_data = cache.get_data(id).decode(encoding="utf-8")
        assert cache_data == data

    def test_get_file(self):
        """Test retrieving a file from cache."""
        id = "MyPackage"
        file = test_data / "Package"

        cache = DefaultCache()
        cache_file = cache.store_file(id, file)

        cache_file = cache.get_file(id)
        assert cache_file
        assert os.path.isfile(cache_file)

        with open(cache_file, "r", encoding="utf-8") as f:
            cache_data = f.read()
        with open(file, "r", encoding="utf-8") as f:
            data = f.read()
        assert cache_data == data

        os.remove(cache_file)

        del cache
        cache = DefaultCache()
        cache_file = cache.get_file(id)

        assert cache_file
        assert os.path.isfile(cache_file)

        with open(cache_file, "r", encoding="utf-8") as f:
            cache_data = f.read()
        with open(file, "r", encoding="utf-8") as f:
            data = f.read()
        assert cache_data == data

        os.remove(cache_file)

        custom_file = Path.home() / "cache_test_file"
        cache_file = cache.get_file(id, file=custom_file)

        assert cache_file
        assert cache_file == custom_file
        assert os.path.isfile(cache_file)

        with open(cache_file, "r", encoding="utf-8") as f:
            cache_data = f.read()
        with open(file, "r", encoding="utf-8") as f:
            data = f.read()
        assert cache_data == data

        os.remove(cache_file)

    def test_store_not_existing_file(self):
        """Test storing a not existing file."""
        file = test_data / "None"

        cache = DefaultCache()
        cache_file = cache.store_file("MyPackages", file)

        assert cache_file is None

    def test_get_not_existing_id_as_file(self):
        """Test retrieving a not existing file."""
        cache = DefaultCache()
        cache_file = cache.get_file("None")

        assert cache_file is None

    def test_get_not_existing_id_as_data(self):
        """Test retrieving not existing data."""
        cache = DefaultCache()
        cache_data = cache.get_data("None")

        assert cache_data is None
