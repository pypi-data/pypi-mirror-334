"""Tests for InRelease processing."""

import os
import logging
import shutil

from pathlib import Path

import pytest

from libapt.cache import DefaultCache
from libapt.deb import (
    load_packages,
    load_sources,
    DebianVersion,
    _parse_dependencies,
    _parse_person,
    _parse_version,
    _parse_package_list,
    extract_deb,
    extract_deb_data,
    extract_deb_meta,
    Package,
    Source,
    PackageDependency,
    Person,
)
from libapt.download import DefaultDownloader, DownloadFailed
from libapt.release import FileHash

test_data = Path(__file__).parent / "data"


class TestDeb:
    """Tests for Package metadata processing."""

    def test_parse_version(self) -> None:
        """Test parsing a version."""

        version_str = "= 0:22.07.5-2ubuntu1.5"
        (relation, version) = _parse_version(version_str)
        assert relation == "="
        assert version.epoch == 0
        assert version.version == "22.07.5"
        assert version.revision == "2ubuntu1.5"

        version_str = "22.07.5-2ubuntu1.5"
        (relation, version) = _parse_version(version_str)
        assert relation is None
        assert version.epoch == 0
        assert version.version == "22.07.5"
        assert version.revision == "2ubuntu1.5"

        version_str = "22.07.5"
        (relation, version) = _parse_version(version=version_str)
        assert relation is None
        assert version.epoch == 0
        assert version.version == "22.07.5"
        assert version.revision is None

    def test_parse_dependencies(self) -> None:
        """Test parsing dependencies."""

        depends_str = "dbus (>= 1.9.18), libaccountsservice0 (= 22.07.5-2ubuntu1.5), libc6 (>= 2.34) | libglib2.0-0 (>= 2.63.5), default-logind | logind"
        depends = _parse_dependencies(dependencies=depends_str)
        assert len(depends) == 4
        assert len(depends[0].alternatives) == 1
        assert depends[0].alternatives[0].package == "dbus"
        assert depends[0].alternatives[0].version == DebianVersion(epoch=None, version="1.9.18", revision=None)
        assert depends[0].alternatives[0].relation == ">="
        assert len(depends[1].alternatives) == 1
        assert depends[1].alternatives[0].package == "libaccountsservice0"
        assert depends[1].alternatives[0].version == DebianVersion(epoch=None, version="22.07.5", revision="2ubuntu1.5")
        assert depends[1].alternatives[0].relation == "="
        assert len(depends[2].alternatives) == 2
        assert depends[2].alternatives[0].package == "libc6"
        assert depends[2].alternatives[0].version == DebianVersion(epoch=None, version="2.34", revision=None)
        assert depends[2].alternatives[0].relation == ">="
        assert depends[2].alternatives[1].package == "libglib2.0-0"
        assert depends[2].alternatives[1].version == DebianVersion(epoch=None, version="2.63.5", revision=None)
        assert depends[2].alternatives[1].relation == ">="
        assert len(depends[3].alternatives) == 2
        assert depends[3].alternatives[0].package == "default-logind"
        assert depends[3].alternatives[0].version is None
        assert depends[3].alternatives[0].relation is None
        assert depends[3].alternatives[1].package == "logind"
        assert depends[3].alternatives[1].version is None
        assert depends[3].alternatives[1].relation is None

    def test_parse_person(self) -> None:
        """Test parsing a maintainer."""
        maintainer = "Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>"
        person = _parse_person(person=maintainer)
        assert person.name == "Ubuntu Developers"
        assert person.email == "ubuntu-devel-discuss@lists.ubuntu.com"

    def test_parse_person_no_mail(self) -> None:
        """Test parsing a maintainer."""
        maintainer = "Ubuntu Developers"
        person = _parse_person(person=maintainer)
        assert person.name == "Ubuntu Developers"
        assert person.email == ""

    def test_deb_metadata(self) -> None:
        """Test converting an package stanza to a package."""
        file = test_data / "Package"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        packages = load_packages(content, base_url="http://myrepo.org")

        assert len(packages) == 1

        package = packages[0]

        assert package.Package == "accountsservice"
        assert package.Architecture == "amd64"
        (_rel, version) = _parse_version("22.07.5-2ubuntu1.5")
        assert package.Version == version
        assert package.Priority == "optional"
        assert package.Section == "gnome"
        assert package.Origin == "Ubuntu"
        assert package.Maintainer == _parse_person("Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>")
        assert package.Original_Maintainer == _parse_person(
            "Debian freedesktop.org maintainers <pkg-freedesktop-maintainers@lists.alioth.debian.org>"
        )
        assert package.Bugs == "https://bugs.launchpad.net/ubuntu/+filebug"
        assert package.Installed_Size == 500
        assert package.Depends == _parse_dependencies(
            "dbus (>= 1.9.18), libaccountsservice0 (= 22.07.5-2ubuntu1.5), libc6 (>= 2.34), libglib2.0-0 (>= 2.63.5), libpolkit-gobject-1-0 (>= 0.99)"
        )
        assert package.Recommends == _parse_dependencies("default-logind | logind")
        assert package.Suggests == _parse_dependencies("gnome-control-center")
        assert package.Filename == "pool/main/a/accountsservice/accountsservice_22.07.5-2ubuntu1.5_amd64.deb"
        assert package.Size == 69982
        assert package.MD5sum == "0db1637dad9ed76d01563fdc1b74a3c7"
        assert package.SHA1 == "9af1ee126f99a9c2aecd268af8445a4af71b08fb"
        assert package.SHA256 == "95ef667f9ada1acb2629bb98d3aa004dcf49a694430ac46b72d9add43adc569d"
        assert (
            package.SHA512
            == "4520da486daebf911df64d856892f7ba51eaf71660c9247d0d0bc5bcfbe3c80f444befce51d431d85315dd2ca2c843e075cfe8e71ac26db12ee3acbbae1a6178"
        )
        assert package.Homepage == "https://www.freedesktop.org/wiki/Software/AccountsService/"
        assert package.Description == "query and manipulate user account information"
        assert package.Task == [
            "ubuntu-desktop-minimal",
            "ubuntu-desktop",
            "ubuntu-desktop-raspi",
            "kubuntu-desktop",
            "xubuntu-core",
            "xubuntu-desktop",
            "lubuntu-desktop",
            "ubuntustudio-desktop-core",
            "ubuntustudio-desktop",
            "ubuntukylin-desktop",
            "ubuntu-mate-core",
            "ubuntu-mate-desktop",
            "ubuntu-budgie-desktop",
            "ubuntu-budgie-desktop-raspi",
        ]
        assert package.Description_md5 == "8aeed0a03c7cd494f0c4b8d977483d7e"

    def test_deb_metadata_short(self) -> None:
        """Test converting an package stanza to a package."""
        file = test_data / "Package2"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        packages = load_packages(content, base_url="http://myrepo.org")

        assert len(packages) == 1

        package = packages[0]

        assert package.Package == "accountsservice"
        assert package.Architecture == "amd64"
        (_rel, version) = _parse_version("22.07.5-2ubuntu1.5")
        assert package.Version == version
        assert package.Priority is None
        assert package.Section is None
        assert package.Origin is None
        assert package.Maintainer is None
        assert package.Original_Maintainer is None
        assert package.Bugs is None
        assert package.Installed_Size is None
        assert package.Depends is None
        assert package.Recommends is None
        assert package.Suggests is None
        assert package.Filename == "pool/main/a/accountsservice/accountsservice_22.07.5-2ubuntu1.5_amd64.deb"
        assert package.Size is None
        assert package.MD5sum is None
        assert package.SHA1 is None
        assert package.SHA256 is None
        assert package.SHA512 is None
        assert package.Homepage is None
        assert package.Description is None
        assert package.Task is None
        assert package.Description_md5 is None

    def test_load_package_index(self) -> None:
        """Test converting an package index to a packages list."""
        file = test_data / "Packages"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        packages = load_packages(content, base_url="http://myrepo.org")

        assert len(packages) == 43

    def test_parse_package_list(self) -> None:
        """Test parsing of the package list metadata."""
        package_list_metadata = """
        libaa-bin deb text optional arch=any
        libaa1 deb libs optional arch=any more
        libaa1-dev deb libdevel other arch=arm64
        """
        entries = _parse_package_list(package_list_metadata)
        assert len(entries) == 3
        assert entries[0].package == "libaa-bin"
        assert entries[0].package_type == "deb"
        assert entries[0].section == "text"
        assert entries[0].priority == "optional"
        assert entries[0].additional == {"arch": "any"}
        assert entries[1].package == "libaa1"
        assert entries[1].package_type == "deb"
        assert entries[1].section == "libs"
        assert entries[1].priority == "optional"
        assert entries[1].additional == {"arch": "any", "more": ""}
        assert entries[2].package == "libaa1-dev"
        assert entries[2].package_type == "deb"
        assert entries[2].section == "libdevel"
        assert entries[2].priority == "other"
        assert entries[2].additional == {"arch": "arm64"}

    def test_source_metadata(self) -> None:
        """Test parsing a source metadata stanza."""
        file = test_data / "Source"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        sources = load_sources(content, base_url="http://myrepo.org")

        assert len(sources) == 1

        source = sources[0]

        assert source.Package == "abseil"
        assert source.Format == "3.0 (quilt)"
        assert source.Binary == ["libabsl-dev", "libabsl20220623t64"]
        assert source.Architecture == "any"
        (_rel, version) = _parse_version("20220623.1-3.1ubuntu3")
        assert source.Version == version
        assert source.Priority == "optional"
        assert source.Section == "misc"
        assert source.Maintainer == _parse_person("Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>")
        assert source.Original_Maintainer == _parse_person("Benjamin Barenblat <bbaren@debian.org>")
        assert source.Standards_Version == "4.6.1"
        assert source.Build_Depends == _parse_dependencies(
            "dpkg-dev (>= 1.22.5), cmake (>= 3.5), debhelper-compat (= 12), g++-12, googletest (>= 1.12) [!mipsel !ppc64] <!nocheck>"
        )
        assert source.Testsuite == "autopkgtest"
        assert source.Testsuite_Triggers == ["cmake", "g++", "libgtest-dev", "make", "pkg-config"]
        assert source.Homepage == "https://abseil.io/"
        assert source.Description is not None
        assert source.Description.startswith("extensions to the C++ standard library")
        assert "provides alternatives to the standard for special needs." in source.Description
        assert source.Vcs_Browser == "https://salsa.debian.org/debian/abseil"
        assert source.Vcs_Git == "https://salsa.debian.org/debian/abseil.git"
        assert source.Directory == "pool/main/a/abseil"
        assert source.Package_List == _parse_package_list("""
        libabsl-dev deb libdevel optional arch=any
        libabsl20220623t64 deb libs optional arch=any
        """)
        assert source.Files == [
            FileHash(hash="0bdff2b9ae7d7682edb73619d90ff09e", size=2627, file="abseil_20220623.1-3.1ubuntu3.dsc"),
            FileHash(hash="3c40838276f6e5f67acf9a3e5a5e0bd1", size=1957272, file="abseil_20220623.1.orig.tar.gz"),
            FileHash(
                hash="1a5a4d628664aea1355429fc76e683e9", size=8412, file="abseil_20220623.1-3.1ubuntu3.debian.tar.xz"
            ),
        ]
        assert source.Checksums_Sha1 == [
            FileHash(
                hash="6c0d98cc24721badfb32aae562b00bc754502a54", size=2627, file="abseil_20220623.1-3.1ubuntu3.dsc"
            ),
            FileHash(
                hash="60f52f4d90cebd82fc77dae1119590ef96e01ed5", size=1957272, file="abseil_20220623.1.orig.tar.gz"
            ),
            FileHash(
                hash="fd95bd8e6fa7168f7f82f4a1a367243666045b49",
                size=8412,
                file="abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
            ),
        ]
        assert source.Checksums_Sha256 == [
            FileHash(
                hash="f96c82b5cacdc312050bb46cc346adae5d3080d4bab151b7f91561173042fe32",
                size=2627,
                file="abseil_20220623.1-3.1ubuntu3.dsc",
            ),
            FileHash(
                hash="abfe2897f3a30edaa74bc34365afe3c2a3cd012091a97dc7e008f7016adcd5fe",
                size=1957272,
                file="abseil_20220623.1.orig.tar.gz",
            ),
            FileHash(
                hash="9d427fae687587f47ff6b3e9d83d396300463572e0af342129a9498a1ed82284",
                size=8412,
                file="abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
            ),
        ]
        assert source.Checksums_Sha512 == [
            FileHash(
                hash="fc3fa76b206948b66725f1de3c8998a4614ef78a7d9b6629d016a218dc04f0bae7390ede38d561bc3487da18235e0be309f89c0db0eaf191096d18b1d81cb3a1",
                size=2627,
                file="abseil_20220623.1-3.1ubuntu3.dsc",
            ),
            FileHash(
                hash="3c7fca91a9bda39a43cbdbd855577f58a988a7dc214ac93ef7e4cb2cc6ec24149bd7a414b4f7caf35511eaaa296260051a3d02b69ee5fd6e3247100b0b12258e",
                size=1957272,
                file="abseil_20220623.1.orig.tar.gz",
            ),
            FileHash(
                hash="0a666f60c5d8bd89ebb9ff99de9b120c0ec8858ca199b1236de31f834007facbd896257bde2efbfadc828b5ccf9e8472b0ba89dcb70af89d49db3763258c070e",
                size=8412,
                file="abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
            ),
        ]

    def test_source_metadata_minimal(self) -> None:
        """Test parsing a source metadata stanza."""
        file = test_data / "Source2"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        sources = load_sources(content, base_url="http://myrepo.org")

        assert len(sources) == 1

        source = sources[0]

        assert source.Package == "abseil"
        assert source.Format == "3.0 (quilt)"
        assert source.Binary is None
        assert source.Architecture is None
        (_rel, version) = _parse_version("20220623.1-3.1ubuntu3")
        assert source.Version == version
        assert source.Priority is None
        assert source.Section is None
        assert source.Maintainer == _parse_person("Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>")
        assert source.Original_Maintainer is None
        assert source.Standards_Version == "4.6.1"
        assert source.Build_Depends is None
        assert source.Testsuite is None
        assert source.Testsuite_Triggers is None
        assert source.Homepage is None
        assert source.Description is None
        assert source.Vcs_Browser is None
        assert source.Vcs_Git is None
        assert source.Directory == "pool/main/a/abseil"
        assert source.Package_List is None
        assert source.Files == [
            FileHash(hash="0bdff2b9ae7d7682edb73619d90ff09e", size=2627, file="abseil_20220623.1-3.1ubuntu3.dsc"),
            FileHash(hash="3c40838276f6e5f67acf9a3e5a5e0bd1", size=1957272, file="abseil_20220623.1.orig.tar.gz"),
            FileHash(
                hash="1a5a4d628664aea1355429fc76e683e9", size=8412, file="abseil_20220623.1-3.1ubuntu3.debian.tar.xz"
            ),
        ]
        assert source.Checksums_Sha1 == [
            FileHash(
                hash="6c0d98cc24721badfb32aae562b00bc754502a54", size=2627, file="abseil_20220623.1-3.1ubuntu3.dsc"
            ),
            FileHash(
                hash="60f52f4d90cebd82fc77dae1119590ef96e01ed5", size=1957272, file="abseil_20220623.1.orig.tar.gz"
            ),
            FileHash(
                hash="fd95bd8e6fa7168f7f82f4a1a367243666045b49",
                size=8412,
                file="abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
            ),
        ]
        assert source.Checksums_Sha256 == [
            FileHash(
                hash="f96c82b5cacdc312050bb46cc346adae5d3080d4bab151b7f91561173042fe32",
                size=2627,
                file="abseil_20220623.1-3.1ubuntu3.dsc",
            ),
            FileHash(
                hash="abfe2897f3a30edaa74bc34365afe3c2a3cd012091a97dc7e008f7016adcd5fe",
                size=1957272,
                file="abseil_20220623.1.orig.tar.gz",
            ),
            FileHash(
                hash="9d427fae687587f47ff6b3e9d83d396300463572e0af342129a9498a1ed82284",
                size=8412,
                file="abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
            ),
        ]
        assert source.Checksums_Sha512 is None

    def test_load_source_index(self) -> None:
        """Test parsing a source package index."""
        file = test_data / "Sources"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        sources = load_sources(content, base_url="http://myrepo.org")

        assert len(sources) == 52

    def test_download_package(self) -> None:
        """Test downloading a Debian file."""
        file = test_data / "Package"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        packages = load_packages(content, base_url="http://archive.ubuntu.com/ubuntu")

        assert len(packages) == 1

        package = packages[0]

        cache = DefaultCache()
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/accountsservice/accountsservice_22.07.5-2ubuntu1.5_amd64.deb",
            test_data / "accountsservice_22.07.5-2ubuntu1.5_amd64.deb",
        )

        downloader = DefaultDownloader(cache=cache)

        pkg_file = package.download(downloader=downloader)

        assert pkg_file
        assert os.path.exists(pkg_file)

    def test_download_package_sha256(self) -> None:
        """Test downloading a Debian file."""
        file = test_data / "Package_SHA256"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        packages = load_packages(content, base_url="http://archive.ubuntu.com/ubuntu")

        assert len(packages) == 1

        package = packages[0]

        cache = DefaultCache()
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/accountsservice/accountsservice_22.07.5-2ubuntu1.5_amd64.deb",
            test_data / "accountsservice_22.07.5-2ubuntu1.5_amd64.deb",
        )

        downloader = DefaultDownloader(cache=cache)

        pkg_file = package.download(downloader=downloader)

        assert pkg_file
        assert os.path.exists(pkg_file)

    def test_download_package_sha1(self) -> None:
        """Test downloading a Debian file."""
        file = test_data / "Package_SHA1"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        packages = load_packages(content, base_url="http://archive.ubuntu.com/ubuntu")

        assert len(packages) == 1

        package = packages[0]

        cache = DefaultCache()
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/accountsservice/accountsservice_22.07.5-2ubuntu1.5_amd64.deb",
            test_data / "accountsservice_22.07.5-2ubuntu1.5_amd64.deb",
        )

        downloader = DefaultDownloader(cache=cache)

        pkg_file = package.download(downloader=downloader)

        assert pkg_file
        assert os.path.exists(pkg_file)

    def test_download_package_md5(self) -> None:
        """Test downloading a Debian file."""
        file = test_data / "Package_MD5"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        packages = load_packages(content, base_url="http://archive.ubuntu.com/ubuntu/")

        assert len(packages) == 1

        package = packages[0]

        cache = DefaultCache()
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/accountsservice/accountsservice_22.07.5-2ubuntu1.5_amd64.deb",
            test_data / "accountsservice_22.07.5-2ubuntu1.5_amd64.deb",
        )

        downloader = DefaultDownloader(cache=cache)

        pkg_file = package.download(downloader=downloader)

        assert pkg_file
        assert os.path.exists(pkg_file)

    def test_download_package_no_hash(self, caplog) -> None:
        """Test downloading a Debian file."""
        file = test_data / "Package_NO_HASH"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        packages = load_packages(content, base_url="http://archive.ubuntu.com/ubuntu")

        assert len(packages) == 1

        package = packages[0]

        cache = DefaultCache()
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/accountsservice/accountsservice_22.07.5-2ubuntu1.5_amd64.deb",
            test_data / "accountsservice_22.07.5-2ubuntu1.5_amd64.deb",
        )

        downloader = DefaultDownloader(cache=cache)

        with caplog.at_level(logging.ERROR):
            pkg_file = package.download(downloader=downloader)
            assert "The package accountsservice has no hash." in caplog.text

        assert pkg_file
        assert os.path.exists(pkg_file)

    def test_download_package_wrong_hash(self, caplog) -> None:
        """Test downloading a Debian file."""
        file = test_data / "Package_WRONG_HASH"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        packages = load_packages(content, base_url="http://archive.ubuntu.com/ubuntu")

        assert len(packages) == 1

        package = packages[0]

        cache = DefaultCache()
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/accountsservice/accountsservice_22.07.5-2ubuntu1.5_amd64.deb",
            test_data / "accountsservice_22.07.5-2ubuntu1.5_amd64.deb",
        )

        downloader = DefaultDownloader(cache=cache)

        with pytest.raises(DownloadFailed):
            package.download(downloader=downloader)

    def test_download_source_package(self) -> None:
        """Test downloading a Debian file."""
        file = test_data / "Source"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        sources = load_sources(content, base_url="http://archive.ubuntu.com/ubuntu")

        assert len(sources) == 1

        source = sources[0]

        cache = DefaultCache()
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1-3.1ubuntu3.dsc",
            test_data / "abseil_20220623.1-3.1ubuntu3.dsc",
        )
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1.orig.tar.gz",
            test_data / "abseil_20220623.1.orig.tar.gz",
        )
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
            test_data / "abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
        )

        downloader = DefaultDownloader(cache=cache)

        src_file = source.download(downloader=downloader)

        assert src_file
        assert os.path.exists(src_file)
        assert str(src_file).endswith(".dsc")

    def test_download_source_package_sha256(self) -> None:
        """Test downloading a Debian file."""
        file = test_data / "Source_SHA256"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        sources = load_sources(content, base_url="http://archive.ubuntu.com/ubuntu")

        assert len(sources) == 1

        source = sources[0]

        cache = DefaultCache()
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1-3.1ubuntu3.dsc",
            test_data / "abseil_20220623.1-3.1ubuntu3.dsc",
        )
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1.orig.tar.gz",
            test_data / "abseil_20220623.1.orig.tar.gz",
        )
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
            test_data / "abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
        )

        downloader = DefaultDownloader(cache=cache)

        src_file = source.download(downloader=downloader)

        assert src_file
        assert os.path.exists(src_file)
        assert str(src_file).endswith(".dsc")

    def test_download_source_package_sha1(self) -> None:
        """Test downloading a Debian file."""
        file = test_data / "Source_SHA1"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        sources = load_sources(content, base_url="http://archive.ubuntu.com/ubuntu/")

        assert len(sources) == 1

        source = sources[0]

        cache = DefaultCache()
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1-3.1ubuntu3.dsc",
            test_data / "abseil_20220623.1-3.1ubuntu3.dsc",
        )
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1.orig.tar.gz",
            test_data / "abseil_20220623.1.orig.tar.gz",
        )
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
            test_data / "abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
        )

        downloader = DefaultDownloader(cache=cache)

        src_file = source.download(downloader=downloader)

        assert src_file
        assert os.path.exists(src_file)
        assert str(src_file).endswith(".dsc")

    def test_download_source_package_md5(self) -> None:
        """Test downloading a Debian file."""
        file = test_data / "Source_MD5"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        sources = load_sources(content, base_url="http://archive.ubuntu.com/ubuntu/")

        assert len(sources) == 1

        source = sources[0]

        cache = DefaultCache()
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1-3.1ubuntu3.dsc",
            test_data / "abseil_20220623.1-3.1ubuntu3.dsc",
        )
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1.orig.tar.gz",
            test_data / "abseil_20220623.1.orig.tar.gz",
        )
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
            test_data / "abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
        )

        downloader = DefaultDownloader(cache=cache)

        src_file = source.download(downloader=downloader)

        assert src_file
        assert os.path.exists(src_file)
        assert str(src_file).endswith(".dsc")

    def test_download_source_wrong_hash(self, caplog) -> None:
        """Test downloading a Debian file."""
        file = test_data / "Source_WRONG_HASH"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        sources = load_sources(content, base_url="http://archive.ubuntu.com/ubuntu")

        assert len(sources) == 1

        source = sources[0]

        cache = DefaultCache()
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1-3.1ubuntu3.dsc",
            test_data / "abseil_20220623.1-3.1ubuntu3.dsc",
        )
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1.orig.tar.gz",
            test_data / "abseil_20220623.1.orig.tar.gz",
        )
        cache.store_file(
            "http://archive.ubuntu.com/ubuntu/pool/main/a/abseil/abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
            test_data / "abseil_20220623.1-3.1ubuntu3.debian.tar.xz",
        )

        downloader = DefaultDownloader(cache=cache)

        with pytest.raises(DownloadFailed):
            source.download(downloader=downloader)

    def test_extract_deb(self) -> None:
        """Test for extracting a Debian package."""
        deb = test_data / "accountsservice_22.07.5-2ubuntu1.5_amd64.deb"

        assert os.path.isfile(deb)

        content = extract_deb(deb)

        assert content
        assert os.path.isfile(content / "debian-binary")
        assert os.path.isfile(content / "control.tar.zst")
        assert os.path.isfile(content / "data.tar.zst")

        shutil.rmtree(content)

    def test_extract_deb_broken(self, caplog) -> None:
        """Test for extracting a broken Debian package."""
        deb = test_data / "abseil_20220623.1-3.1ubuntu3.debian.tar.xz"

        assert os.path.isfile(deb)

        with caplog.at_level(logging.ERROR):
            content = extract_deb(deb)
            assert f"Extraction of deb {str(deb)} failed:" in caplog.text

        assert content is None

    def test_extract_deb_to_folder(self, tmp_path) -> None:
        """Test for extracting a Debian package."""
        deb = test_data / "accountsservice_22.07.5-2ubuntu1.5_amd64.deb"

        assert os.path.isfile(deb)

        content = extract_deb(deb, tmp_path)

        assert content
        assert content == tmp_path
        assert os.path.isfile(tmp_path / "debian-binary")
        assert os.path.isfile(tmp_path / "control.tar.zst")
        assert os.path.isfile(tmp_path / "data.tar.zst")

    def test_extract_deb_data_zstd(self) -> None:
        """Test for extracting a Debian package data."""
        deb = test_data / "accountsservice_22.07.5-2ubuntu1.5_amd64.deb"

        assert os.path.isfile(deb)

        content = extract_deb_data(deb)

        assert content
        assert os.path.isfile(content / "lib/systemd/system/accounts-daemon.service")
        assert os.path.isfile(content / "usr/libexec/accounts-daemon")

        shutil.rmtree(content)

    def test_extract_deb_data_xz(self) -> None:
        """Test for extracting a Debian package data."""
        deb = test_data / "bash_5.2.15-2+b7_amd64.deb"

        assert os.path.isfile(deb)

        content = extract_deb_data(deb)

        assert content
        assert os.path.isfile(content / "bin/bash")

        shutil.rmtree(content)

    def test_extract_deb_data_to_dir(self, tmp_path) -> None:
        """Test for extracting a Debian package data."""
        deb = test_data / "bash_5.2.15-2+b7_amd64.deb"

        assert os.path.isfile(deb)

        content = extract_deb_data(deb, tmp_path)

        assert content
        assert content == tmp_path
        assert os.path.isfile(tmp_path / "bin/bash")

    def test_extract_deb_data_broken(self) -> None:
        """Test for extracting a Debian package data."""
        deb = test_data / "abseil_20220623.1-3.1ubuntu3.debian.tar.xz"

        assert os.path.isfile(deb)

        content = extract_deb_data(deb)

        assert content is None

    def test_extract_deb_meta_xz(self) -> None:
        """Test for extracting a Debian package metadata."""
        deb = test_data / "bash_5.2.15-2+b7_amd64.deb"

        assert os.path.isfile(deb)

        meta = extract_deb_meta(deb)

        assert meta
        assert meta.package

        assert meta.package.Package == "bash"

        assert len(meta.md5sums) > 0
        bash = list(filter(lambda entry: entry[1] == "bin/bash", meta.md5sums))
        assert len(bash) == 1

        assert "postinst" in meta.scripts
        assert "postrm" in meta.scripts
        assert "prerm" in meta.scripts

    def test_extract_deb_meta_zstd(self) -> None:
        """Test for extracting a Debian package metadata."""
        deb = test_data / "accountsservice_22.07.5-2ubuntu1.5_amd64.deb"

        assert os.path.isfile(deb)

        meta = extract_deb_meta(deb)

        assert meta
        assert meta.package

        assert meta.package.Package == "accountsservice"

        assert len(meta.md5sums) > 0
        bash = list(filter(lambda entry: entry[1] == "lib/systemd/system/accounts-daemon.service", meta.md5sums))
        assert len(bash) == 1

        assert "postinst" in meta.scripts
        assert "preinst" in meta.scripts
        assert "postrm" in meta.scripts
        assert "prerm" in meta.scripts

    def test_extract_deb_meta_broken(self) -> None:
        """Test for extracting a Debian package metadata."""
        deb = test_data / "abseil_20220623.1-3.1ubuntu3.debian.tar.xz"

        assert os.path.isfile(deb)

        meta = extract_deb_meta(deb)

        assert meta is None

    def test_deb_stanza(self) -> None:
        """Test package stanza generation."""
        file = test_data / "Package"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        pkgs = load_packages(content, base_url="http:/myrepo.com")

        assert len(pkgs) > 0

        pkg: Package = pkgs[0]

        stanza = pkg.stanza

        assert "Package: accountsservice" in stanza
        assert "base_url" not in stanza
        assert "Original-Maintainer" in stanza

        pkgs = load_packages(stanza, base_url="http:/myrepo.com")

        assert len(pkgs) > 0
        assert pkg == pkgs[0]

    def test_src_stanza(self) -> None:
        """Test source package stanza generation."""
        file = test_data / "Source"

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        srcs = load_sources(content, base_url="http://myrepo.com")

        assert len(srcs) > 0

        src: Source = srcs[0]

        assert "libabsl-dev deb libdevel optional arch=any" in str(src.Package_List)

        stanza = src.stanza

        assert "Package: abseil" in stanza
        assert "base_url" not in stanza
        assert (
            "Description: extensions to the C++ standard library\n  Abseil is an open-source collection of C++ library code designed to augment the"
            in stanza
        )
        assert "Package-List: \n  libabsl-dev deb libdevel optional arch=any" in stanza
        assert "Files: \n  0bdff2b9ae7d7682edb73619d90ff09e 2627 abseil_20220623.1-3.1ubuntu3.dsc" in stanza

        srcs = load_sources(stanza, base_url="http://myrepo.com")

        assert len(srcs) > 0
        assert src == srcs[0]

    def test_package_dependency_no_relation(self) -> None:
        """Test representation of a package dependency without relation."""
        (_rel, version) = _parse_version("22.07.5-2ubuntu1.5")
        dep = PackageDependency(package="mypackage", version=version, relation=None, additional=None)
        assert str(dep) == "mypackage (22.07.5-2ubuntu1.5)"

    def test_person_no_mail(self) -> None:
        """Test representation of a person without email."""
        pers = Person(name="Max Mustermann", email="")
        assert str(pers) == "Max Mustermann"
