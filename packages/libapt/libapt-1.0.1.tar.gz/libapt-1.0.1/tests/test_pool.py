"""Tests for the Pool class."""

import tempfile
import shutil
import hashlib
import logging

from pathlib import Path

import pytest

from pydantic import BaseModel
from libyamlconf.verify import load_and_verify  # type: ignore[import-untyped]

from libapt.apt import AptConfig
from libapt.deb import _parse_version
from libapt.cache import DefaultCache
from libapt.download import DefaultDownloader, Downloader, DownloadFailed
from libapt.pool import Pool, _get_package_index_hash
from libapt.release import Release
from libapt.signature import verify_signature
from libapt.stanza import stanza_to_dict


test_data = Path(__file__).parent / "data"


class Config(BaseModel):
    """Config for testing"""

    apt_repos: list[AptConfig]


class TestDownloader(Downloader):
    def __init__(self):
        self._cache = DefaultCache()
        self._data = {
            "http://testreposigned/dists/local/InRelease": test_data / "InRelease",
            "http://testreposigned/dists/local/main/binary-amd64/Packages.xz": test_data / "Packages.xz",
            "http://testrepo/dists/local/InRelease": test_data / "InReleaseLocal",
            "http://testrepo/dists/local/main/binary-amd64/Packages.xz": test_data / "Packages.xz",
            "http://testrepo/dists/local/main/source/Sources.xz": test_data / "Sources.xz",
            "http://testrepo/dists/local/other/binary-amd64/Packages.gz": test_data / "PackagesLocalOther.gz",
            "http://testrepo/dists/local/other/source/Sources": test_data / "SourcesLocalOther",
            "http://testrepo/InRelease": test_data / "InRelease",
            "http://testrepo/Packages.xz": test_data / "Packages.xz",
            "http://testrepo/Sources.xz": test_data / "Sources.xz",
            "http://testrepo/ubuntu-keyring-2018-archive.gpg": test_data / "ubuntu-keyring-2018-archive.gpg",
        }
        self._tmpdir = Path(tempfile.mkdtemp())

    def __del__(self):
        shutil.rmtree(self._tmpdir)

    def download_file(
        self, url: str, folder: Path | None = None, name: str | None = None, bypass_cache: bool = False
    ) -> Path:
        """
        Download the given url as temporary file.

        :param url: URL of the artifact to download.
        :returns:   Path to the downloaded file.
        """
        if self._cache.contains(url):
            return self._cache.get_file(url)

        if url in self._data:
            name = hashlib.md5(url.encode()).hexdigest()
            file = self._tmpdir / name
            shutil.copy(self._data[url], file)
            return file
        else:
            raise DownloadFailed("Url %s not contained in the test data!")

    def download(self, url: str, bypass_cache: bool = False) -> bytes:
        """
        Download the given url.

        :param url: URL of the artifact to download.
        :returns: Data of the URL.
        """
        if self._cache.contains(url):
            return self._cache.get_data(url)

        if url in self._data:
            with open(self._data[url], "rb") as f:
                return f.read()
        else:
            raise DownloadFailed("Url %s not contained in the test data!")


class TestPool:
    """Tests for the package pool."""

    def test_pool_downloader(self) -> None:
        """Test the downloader property."""
        downloader = TestDownloader()
        pool = Pool(downloader)

        assert pool.downloader == downloader

    def test_pool_local(self, caplog) -> None:
        """Test for straight forward using the pool."""
        downloader = TestDownloader()
        pool = Pool(downloader)
        config = AptConfig(apt_repo="http://testrepo", distro="local", components={"main"})

        pool.add_repository(config, "amd64")

        with caplog.at_level(logging.ERROR):
            pool.update()
            assert "Multiple entries found for url" in caplog.text

        (_rel, version) = _parse_version("2.0.9-1ubuntu0.1")
        pkg = pool.find_binary_package(package="anope", arch="amd64", version=version, relation="==")
        assert pkg
        assert pkg[0].Package == "anope"
        assert pkg[0].Architecture == "amd64"

        (_rel, version) = _parse_version("2.0.9")
        pkg = pool.find_binary_package(package="anope", arch="amd64", version=version, relation=">=")
        assert pkg
        assert pkg[0].Package == "anope"
        assert pkg[0].Architecture == "amd64"

        src = pool.find_source_package(package="acl", arch="any")
        assert src
        assert src[0].Package == "acl"
        assert src[0].Architecture == "any"

    def test_pool_not_found(self) -> None:
        """Test for straight forward using the pool."""
        downloader = TestDownloader()
        pool = Pool(downloader)
        config = AptConfig(apt_repo="http://testrepo", distro="local", components={"main"})

        pool.add_repository(config, "amd64")

        pool.update()

        (_rel, version) = _parse_version("2.0.9-1ubuntu2")
        pkg = pool.find_binary_package(package="anope", arch="amd64", version=version, relation="==")
        assert not pkg

        pkg = pool.find_binary_package(package="anope", arch="arm64")
        assert not pkg

        pkg = pool.find_binary_package(package="no_package", arch="arm64")
        assert not pkg

    @pytest.mark.requires_download
    @pytest.mark.long_running
    def test_pool_jammy_online(self) -> None:
        """Test for straight forward using the pool."""
        downloader = DefaultDownloader()
        pool = Pool(downloader)

        file = test_data / "jammy.yaml"

        config: Config = load_and_verify(file, Config)

        pool.add_repository(config.apt_repos[0], "amd64")

        pool.update()

        bb = pool.find_binary_package(package="busybox-static", arch="amd64")
        assert bb != []
        assert bb[0].Package == "busybox-static"
        assert bb[0].Architecture == "amd64"

    @pytest.mark.requires_download
    @pytest.mark.long_running
    def test_pool_noble_online(self) -> None:
        """Test for straight forward using the pool."""
        downloader = DefaultDownloader()
        pool = Pool(downloader)

        file = test_data / "noble.yaml"

        config: Config = load_and_verify(file, Config)

        pool.add_repository(config.apt_repos[0], "amd64")

        pool.update()

        bb = pool.find_binary_package(package="busybox-static", arch="amd64")
        assert bb != []
        assert bb[0].Package == "busybox-static"
        assert bb[0].Architecture == "amd64"

    @pytest.mark.requires_download
    @pytest.mark.long_running
    def test_pool_bookworm_online(self) -> None:
        """Test for straight forward using the pool."""
        downloader = DefaultDownloader()
        pool = Pool(downloader)

        file = test_data / "bookworm.yaml"

        config: Config = load_and_verify(file, Config)

        pool.add_repository(config.apt_repos[0], "amd64")

        pool.update()

        bb = pool.find_binary_package(package="busybox-static", arch="amd64")
        assert bb != []
        assert bb[0].Package == "busybox-static"
        assert bb[0].Architecture == "amd64"

    def test_pool_local_other(self) -> None:
        """Test multiple package versions."""
        downloader = TestDownloader()
        pool = Pool(downloader)
        config = AptConfig(apt_repo="http://testrepo", distro="local", components={"other"})

        pool.add_repository(config, "amd64")

        pool.update()

        (_rel, version) = _parse_version("22.07.5-2ubuntu1.5")
        pkg = pool.find_binary_package(package="accountsservice", arch="amd64", version=version, relation="==")
        assert pkg
        assert pkg[0].Package == "accountsservice"
        assert pkg[0].Architecture == "amd64"

        (_rel, version) = _parse_version("22.07.5-2ubuntu1.7")
        pkg = pool.find_binary_package(package="accountsservice", arch="amd64", version=version, relation=">=")
        assert pkg
        assert pkg[0].Package == "accountsservice"
        assert pkg[0].Architecture == "amd64"
        assert pkg[0].repo == config
        assert pkg[0].component == "other"
        assert pkg[0].base_url == "http://testrepo/"

        pkg = pool.find_binary_package(package="accountsservice", arch="amd64")
        assert pkg
        assert pkg[0].Package == "accountsservice"
        assert pkg[0].Architecture == "amd64"
        assert pkg[0].Version == version

        pkg = pool.find_binary_package(package="accountsservice")
        assert pkg
        assert pkg[0].Package == "accountsservice"
        assert pkg[0].Architecture == "amd64"
        assert pkg[0].Version == version

        (_rel, version) = _parse_version("20220623.1-3.1ubuntu3")
        src = pool.find_source_package(package="abseil", arch="any", version=version, relation="==")
        assert src
        assert src[0].Package == "abseil"
        assert src[0].Architecture == "any"

        (_rel, version) = _parse_version("20220623.1-3.1ubuntu4")
        src = pool.find_source_package(package="abseil", arch="any", version=version, relation=">=")
        assert src
        assert src[0].Package == "abseil"
        assert src[0].Architecture == "any"

        src = pool.find_source_package(package="abseil", arch="any")
        assert src
        assert len(src) == 2
        assert src[1].Package == "abseil"
        assert src[1].Architecture == "any"
        assert src[1].Version == version

        src = pool.find_source_package(package="abseil")
        assert src
        assert len(src) == 2
        assert src[1].Package == "abseil"
        assert src[1].Architecture == "any"
        assert src[1].Version == version

        src = pool.find_source_package(package="abseil", arch="all")
        assert not src

        src = pool.find_source_package(package="other")
        assert not src

    def test_pool_local_other_packages(self) -> None:
        """Test multiple package versions."""
        downloader = TestDownloader()
        pool = Pool(downloader)
        config = AptConfig(apt_repo="http://testrepo", distro="local", components={"other"})

        pool.add_repository(config, "amd64")

        pool.update()

        packages = pool.packages
        assert len(packages) == 2
        assert packages[0].Package == "accountsservice"
        assert packages[1].Package == "accountsservice"

        sources = pool.sources
        assert len(sources) == 2
        assert sources[0].Package == "abseil"
        assert sources[1].Package == "abseil"

    def test_pool_local_flat(self) -> None:
        """Test flat apt repository."""
        downloader = TestDownloader()
        pool = Pool(downloader)
        config = AptConfig(apt_repo="http://testrepo")

        pool.add_repository(config, "amd64")

        pool.update()

        (_rel, version) = _parse_version("2.0.9-1ubuntu0.1")
        pkg = pool.find_binary_package(package="anope", arch="amd64", version=version, relation="==")
        assert pkg
        assert pkg[0].Package == "anope"
        assert pkg[0].Architecture == "amd64"

        (_rel, version) = _parse_version("2.0.9")
        pkg = pool.find_binary_package(package="anope", arch="amd64", version=version, relation=">=")
        assert pkg
        assert pkg[0].Package == "anope"
        assert pkg[0].Architecture == "amd64"

        src = pool.find_source_package(package="acl", arch="any")
        assert src is not None
        assert src[0].Package == "acl"
        assert src[0].Architecture == "any"

    def test_pool_flat_get_packages(self) -> None:
        """Test for get packages and get sources."""
        downloader = TestDownloader()
        pool = Pool(downloader)
        config = AptConfig(apt_repo="http://testrepo")

        pool.add_repository(config, "amd64")

        pool.update()

        repo_ids = pool.apt_repo_ids
        assert len(repo_ids) == 1

        srcs = pool.get_sources(apt_repo_id=repo_ids[0], component=None)
        assert len(srcs) == 52

        pkgs = pool.get_packages(apt_repo_id=repo_ids[0], component=None)
        assert len(pkgs) == 43

    def test_pool_get_packages(self) -> None:
        """Test for get packages and get sources."""
        downloader = TestDownloader()
        pool = Pool(downloader)
        config = AptConfig(apt_repo="http://testrepo", distro="local", components={"main"})

        pool.add_repository(config, "amd64")

        pool.update()

        repo_ids = pool.apt_repo_ids
        assert len(repo_ids) == 1

        srcs = pool.get_sources(apt_repo_id=repo_ids[0], component="main")
        assert len(srcs) == 52

        pkgs = pool.get_packages(apt_repo_id=repo_ids[0], component="main")
        assert len(pkgs) == 43

        srcs = pool.get_sources(apt_repo_id=repo_ids[0], component="wrong")
        assert len(srcs) == 0

        pkgs = pool.get_packages(apt_repo_id=repo_ids[0], component="wrong")
        assert len(pkgs) == 0

    def test_pool_apt_repos(self) -> None:
        """Test for apt_repos property."""
        downloader = TestDownloader()
        pool = Pool(downloader)
        config = AptConfig(apt_repo="http://testrepo", distro="local", components={"main"})

        pool.add_repository(config, "amd64")

        assert len(pool.apt_repos) == 1

    def test_no_repo(self) -> None:
        """Test for get packages and get sources."""
        downloader = TestDownloader()
        pool = Pool(downloader)

        srcs = pool.get_sources(apt_repo_id="wrong", component=None)
        assert len(srcs) == 0

        pkgs = pool.get_packages(apt_repo_id="wrong", component="main")
        assert len(pkgs) == 0

    def test_duplicate_repo(self) -> None:
        """Test adding a repo twice."""
        downloader = TestDownloader()
        pool = Pool(downloader)
        config = AptConfig(apt_repo="http://testrepo", distro="local", components={"main"})

        assert pool.add_repository(config, "amd64") is True
        assert pool.add_repository(config, "amd64") is False
        assert len(pool.apt_repos) == 1

    def test_signed_repo(self, caplog) -> None:
        """Test adding a repo twice."""
        downloader = TestDownloader()
        pool = Pool(downloader)
        key = test_data / "ubuntu-keyring-2018-archive.gpg"
        config = AptConfig(apt_repo="http://testreposigned", distro="local", components={"main"}, key=str(key))

        pool.add_repository(config, "amd64")

        with caplog.at_level(logging.ERROR):
            pool.update()
            assert "Hash mismatch for URL" in caplog.text

        assert len(pool._repo_metadata) == 1
        # The packages are not loaded because of the hash mismatch.
        assert len(pool.packages) == 0

    def test_package_index_hash(self):
        """Test the package index hash verification."""
        inrelease = test_data / "InRelease"
        key = test_data / "ubuntu-keyring-2018-archive.gpg"

        with open(inrelease, "r", encoding="utf-8") as f:
            data = f.read()

        content = verify_signature(data, key)
        content_dict = stanza_to_dict(content.split("\n"))
        release = Release(base_url="http://myrepo.com", **content_dict)

        downloader = TestDownloader()
        pool = Pool(downloader)

        url = "http://archive.ubuntu.com/ubuntu/dists/jammy/main/binary-amd64/Packages.xz"
        res = _get_package_index_hash(url, release)
        assert res is not None
        (hash, algo) = res
        assert algo == "SHA256"
        assert hash == "2a6a199e1031a5c279cb346646d594993f35b1c03dd4a82aaa0323980dd92451"

        package_index = test_data / "Packages.xz"
        with open(package_index, "rb") as f:
            data = f.read()

        hash = "1868c4dadae62783838ff2a59f6d86d9ee82ff27c05c9b294f0efc043f49a9b4"

        assert pool._verify_package_index_hash(data, hash, algo) is True

    def test_signed_repo_key_from_url(self) -> None:
        """Test adding a repo twice."""
        downloader = TestDownloader()
        pool = Pool(downloader)
        config = AptConfig(
            apt_repo="http://testreposigned",
            distro="local",
            components={"main"},
            key="http://testrepo/ubuntu-keyring-2018-archive.gpg",
        )

        pool.add_repository(config, "amd64")

        pool.update()

        assert len(pool._repo_metadata) == 1
        # The download of the package indices failed.
        assert len(pool.packages) == 0

    def test_signed_repo_key_from_cache(self) -> None:
        """Test adding a repo twice."""
        downloader = TestDownloader()

        downloader._cache.store_file(
            "http://wrong/ubuntu-keyring-2018-archive.gpg", test_data / "ubuntu-keyring-2018-archive.gpg"
        )

        pool = Pool(downloader)
        config = AptConfig(
            apt_repo="http://testreposigned",
            distro="local",
            components={"main"},
            key="http://wrong/ubuntu-keyring-2018-archive.gpg",
        )

        pool.add_repository(config, "amd64")

        pool.update()

        assert len(pool._repo_metadata) == 1
        # The download of the package indices failed.
        assert len(pool.packages) == 0

    def test_update_not_needed(self) -> None:
        """Test adding a repo twice."""
        downloader = TestDownloader()

        downloader._cache.store_file(
            "http://wrong/ubuntu-keyring-2018-archive.gpg", test_data / "ubuntu-keyring-2018-archive.gpg"
        )

        pool = Pool(downloader)
        config = AptConfig(
            apt_repo="http://testreposigned",
            distro="local",
            components={"main"},
            key="http://wrong/ubuntu-keyring-2018-archive.gpg",
        )

        pool.add_repository(config, "amd64")

        pool.update()

        pool.update()

        assert len(pool._repo_metadata) == 1
        # The download of the package indices failed.
        assert len(pool.packages) == 0
