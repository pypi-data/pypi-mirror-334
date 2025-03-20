"""Tests for InRelease processing."""

import logging

from pathlib import Path

from dateutil import parser

from libapt.stanza import stanza_to_dict, stanzas_to_list
from libapt.release import Release, FileHash

test_data = Path(__file__).parent / "data"


class TestRelease:
    """Tests for InRelease processing."""

    def test_stanza_to_dict(self) -> None:
        """Test converting an APT stanza to a Python dict."""
        inrelease = test_data / "stanza_ok.txt"

        with open(inrelease, "r", encoding="utf-8") as file:
            content = file.readlines()

        data = stanza_to_dict(content)
        release = Release(base_url="http://myrepo.com", **data)

        assert release.Origin == "Ubuntu"
        assert release.Label == "Ubuntu"
        assert release.Suite == "noble"
        assert release.Version == "24.04"
        assert release.Codename == "noble"
        assert release.Date == parser.parse("Thu, 25 Apr 2024 15:10:33 UTC")
        assert release.Architectures == "amd64 arm64 armhf i386 ppc64el riscv64 s390x".split(" ")
        assert release.Components == "main restricted universe multiverse".split(" ")
        assert release.Description == "Ubuntu Noble 24.04"
        assert release.SHA256 == [
            FileHash(hash="1ae40621b32609d6251d09b2a47ef936", size=829119597, file="Contents-amd64"),
            FileHash(hash="2fc7d01e0a1c7b351738abcd571eec59", size=51301092, file="Contents-amd64.gz"),
            FileHash(hash="a78c03f162892e93e91366e0ec2a4f13", size=826443945, file="Contents-arm64"),
        ]

    def test_stanza_to_dict_broken(self, caplog) -> None:
        """Test converting an APT stanza to a Python dict."""
        inrelease = test_data / "stanza_broken.txt"

        with open(inrelease, "r", encoding="utf-8") as file:
            content = file.readlines()

        with caplog.at_level(logging.WARNING):
            data = stanza_to_dict(content)
            assert "is dropped because key is missing" in caplog.text

        release = Release(base_url="http://myrepo.com", **data)

        assert release.Origin == "Ubuntu"
        assert release.Label == "Ubuntu"
        assert release.Suite == "noble"
        assert release.Version == "24.04"
        assert release.Codename == "noble"
        assert release.Date == parser.parse("Thu, 25 Apr 2024 15:10:33 UTC")
        assert release.Architectures == "amd64 arm64 armhf i386 ppc64el riscv64 s390x".split(" ")
        assert release.Components == "main restricted universe multiverse".split(" ")
        assert release.Description == "Ubuntu Noble 24.04"
        assert release.SHA256 == [
            FileHash(hash="1ae40621b32609d6251d09b2a47ef936", size=829119597, file="Contents-amd64"),
            FileHash(hash="2fc7d01e0a1c7b351738abcd571eec59", size=51301092, file="Contents-amd64.gz"),
            FileHash(hash="a78c03f162892e93e91366e0ec2a4f13", size=826443945, file="Contents-arm64"),
        ]

    def test_stanza_to_dict_multi_no_stop(self) -> None:
        """Test converting an APT stanza to a Python dict."""
        inrelease = test_data / "multi_stanza.txt"

        with open(inrelease, "r", encoding="utf-8") as file:
            content = file.readlines()

        data = stanza_to_dict(content, stop_on_empty_line=False)
        release = Release(base_url="http://myrepo.com", **data)

        assert release.Origin == "Ubuntu"
        assert release.Label == "Ubuntu"
        assert release.Suite == "jammy"
        assert release.Version == "22.04"
        assert release.Codename == "jammy"
        assert release.Date == parser.parse("Thu, 25 Apr 2024 15:10:33 UTC")
        assert release.Architectures == "amd64 arm64 armhf i386 ppc64el riscv64 s390x".split(" ")
        assert release.Components == "main restricted universe multiverse".split(" ")
        assert release.Description == "Ubuntu Noble 24.04"
        assert release.SHA256 == [
            FileHash(hash="1ae40621b32609d6251d09b2a47ef936", size=829119597, file="Contents-amd64"),
            FileHash(hash="2fc7d01e0a1c7b351738abcd571eec59", size=51301092, file="Contents-amd64.gz"),
            FileHash(hash="a78c03f162892e93e91366e0ec2a4f13", size=826443945, file="Contents-arm64"),
        ]

    def test_stanza_to_dict_multi_stop(self) -> None:
        """Test converting an APT stanza to a Python dict."""
        inrelease = test_data / "multi_stanza.txt"

        with open(inrelease, "r", encoding="utf-8") as file:
            content = file.readlines()

        data = stanza_to_dict(content, stop_on_empty_line=True)
        release = Release(base_url="http://myrepo.com", **data)

        assert release.Origin == "Ubuntu"
        assert release.Label == "Ubuntu"
        assert release.Suite == "noble"
        assert release.Version == "24.04"
        assert release.Codename == "noble"
        assert release.Date == parser.parse("Thu, 25 Apr 2024 15:10:33 UTC")
        assert release.Architectures == "amd64 arm64 armhf i386 ppc64el riscv64 s390x".split(" ")
        assert release.Components == "main restricted universe multiverse".split(" ")
        assert release.Description == "Ubuntu Noble 24.04"
        assert release.SHA256 == [
            FileHash(hash="1ae40621b32609d6251d09b2a47ef936", size=829119597, file="Contents-amd64"),
            FileHash(hash="2fc7d01e0a1c7b351738abcd571eec59", size=51301092, file="Contents-amd64.gz"),
            FileHash(hash="a78c03f162892e93e91366e0ec2a4f13", size=826443945, file="Contents-arm64"),
        ]

    def test_stanzas_to_list(self) -> None:
        """Test converting APT stanzas to a list of Python dict."""
        inrelease = test_data / "stanzas.txt"

        with open(inrelease, "r", encoding="utf-8") as file:
            content = file.read()

        stanzas = stanzas_to_list(content)

        assert len(stanzas) == 3
        assert stanzas[0]["Package"] == "accountsservice"
        assert stanzas[1]["Package"] == "adsys"
        assert stanzas[2]["Package"] == "adsys-windows"
