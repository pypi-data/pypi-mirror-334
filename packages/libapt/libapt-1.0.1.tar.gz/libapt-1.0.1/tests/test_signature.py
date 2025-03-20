"""Tests for InRelease processing."""

import os

from pathlib import Path

import pytest

from dateutil import parser

import pgpy

from libapt.signature import strip_signature, verify_signature, InvalidSignature, generate_key, sign_content
from libapt.release import Release, FileHash
from libapt.stanza import stanza_to_dict

test_data = Path(__file__).parent / "data"


class TestSignature:
    """Tests for Release signature processing."""

    def test_strip_signature(self) -> None:
        """Test removing the signature from InRelease content."""
        inrelease = test_data / "InRelease"

        with open(inrelease, "r", encoding="utf-8") as file:
            content = file.read()

        stripped = strip_signature(content)

        assert "BEGIN PGP SIGNED MESSAGE" not in stripped
        assert "\nHash: " not in stripped
        assert "BEGIN PGP SIGNATURE" not in stripped
        assert "ENDs PGP SIGNATURE" not in stripped

    def test_verify_signature(self) -> None:
        """Test InRelease signature verification."""
        inrelease = test_data / "InRelease"
        key = test_data / "ubuntu-keyring-2018-archive.gpg"

        with open(inrelease, "r", encoding="utf-8") as f:
            data = f.read()

        content = verify_signature(data, key)
        content_dict = stanza_to_dict(content.split("\n"))
        release = Release(base_url="http://myrepo.com", **content_dict)

        assert release.Origin == "Ubuntu"
        assert release.Label == "Ubuntu"
        assert release.Suite == "noble"
        assert release.Version == "24.04"
        assert release.Codename == "noble"
        assert release.Date == parser.parse("Thu, 25 Apr 2024 15:10:33 UTC")
        assert release.Architectures == "amd64 arm64 armhf i386 ppc64el riscv64 s390x".split(" ")
        assert release.Components == "main restricted universe multiverse".split(" ")
        assert release.Description == "Ubuntu Noble 24.04"
        assert release.SHA256 is not None
        assert release.SHA256[:2] == [
            FileHash(
                hash="e945cdeadad8067c9b569e66c058f709d5aa4cd11d8099cc088dc192705e7bc7",
                size=829119597,
                file="Contents-amd64",
            ),
            FileHash(
                hash="c8718dbbacd1ab72675513cf0674ff9921fcf781d9f49c4c0eaf68a49c18adc1",
                size=51301092,
                file="Contents-amd64.gz",
            ),
        ]

    def test_verify_signature_invalid(self) -> None:
        """Test InRelease signature verification."""
        inrelease = test_data / "InReleaseInvalid"
        key = test_data / "ubuntu-keyring-2018-archive.gpg"

        with open(inrelease, "r", encoding="utf-8") as f:
            data = f.read()

        with pytest.raises(InvalidSignature):
            verify_signature(data, key)

    def test_verify_signature_wrong_key(self) -> None:
        """Test InRelease signature verification."""
        inrelease = test_data / "InRelease"
        key = test_data / "ubuntu-keyring-2012-cdimage.gpg"

        with open(inrelease, "r", encoding="utf-8") as f:
            data = f.read()

        with pytest.raises(InvalidSignature):
            verify_signature(data, key)

    def test_generate_key_no_folder(self) -> None:
        """Test GPG key generation."""
        (priv, pub) = generate_key("Max Mustermann", "max@mustermann.de")
        assert priv
        assert pub
        assert os.path.isfile(priv)
        assert os.path.isfile(pub)

        priv_key, _ = pgpy.PGPKey.from_file(priv)
        assert not priv_key.is_public
        uid = priv_key.get_uid("max@mustermann.de")
        assert uid

        pub_key, _ = pgpy.PGPKey.from_file(pub)
        assert pub_key.is_public
        uid = pub_key.get_uid("max@mustermann.de")
        assert uid

    def test_generate_key_with_folder(self, tmp_path) -> None:
        """Test GPG key generation."""
        (priv, pub) = generate_key("Max Mustermann", "max@mustermann.de", folder=tmp_path)
        assert priv
        assert pub
        assert os.path.isfile(priv)
        assert os.path.isfile(pub)
        assert priv.parent == tmp_path
        assert pub.parent == tmp_path

    def test_sign_content(self, tmp_path) -> None:
        """Test signing content."""
        (priv, pub) = generate_key("Max Mustermann", "max@mustermann.de", folder=tmp_path)

        content = sign_content("Hello, world!", priv)

        assert "BEGIN PGP SIGNED MESSAGE" in content

        verify_signature(content, pub)
