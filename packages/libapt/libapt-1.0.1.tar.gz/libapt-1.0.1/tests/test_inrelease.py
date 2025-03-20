"""Tests for InRelease processing."""

import logging

from pathlib import Path

import deepdiff

from libapt.release import _parse_hash_entires, Release, FileHash
from libapt.signature import strip_signature
from libapt.stanza import stanza_to_dict


test_data = Path(__file__).parent / "data"


class TestRelease:
    """Tests for InRelease processing."""

    def test__parse_hash_entires(self) -> None:
        """Test the file metadata parsing."""
        files_metadata = """
        1ae40621b32609d6251d09b2a47ef936        829119597 Contents-amd64
        2fc7d01e0a1c7b351738abcd571eec59         51301092 Contents-amd64.gz
        a78c03f162892e93e91366e0ec2a4f13        826443945 Contents-arm64
        """
        files = _parse_hash_entires(files_metadata)
        assert len(files) == 3
        assert files[0].hash == "1ae40621b32609d6251d09b2a47ef936"
        assert files[0].size == 829119597
        assert files[0].file == "Contents-amd64"
        assert files[1].hash == "2fc7d01e0a1c7b351738abcd571eec59"
        assert files[1].size == 51301092
        assert files[1].file == "Contents-amd64.gz"
        assert files[2].hash == "a78c03f162892e93e91366e0ec2a4f13"
        assert files[2].size == 826443945
        assert files[2].file == "Contents-arm64"

    def test_hashes_SHA512(self) -> None:
        """Test SHA512 hashes are parsed.."""
        inrelease = test_data / "InRelease2"

        with open(inrelease, "r", encoding="utf-8") as f:
            data = f.read()

        content = strip_signature(data)
        content_dict = stanza_to_dict(content.split("\n"))
        release = Release(base_url="http://myrepo.com", **content_dict)

        assert release.SHA512 is not None
        assert release.SHA512[:2] == [
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

    def test_release_stanza(self) -> None:
        """Test source package stanza generation."""
        inrelease = test_data / "InRelease3"

        with open(inrelease, "r", encoding="utf-8") as f:
            data = f.read()

        content = strip_signature(data)
        content_dict = stanza_to_dict(content.split("\n"))
        release = Release(base_url="http://myrepo.com", **content_dict)

        stanza = release.stanza

        assert "Origin: Ubuntu" in stanza
        assert "Version: 24.04" in stanza
        assert "base_url" not in stanza
        assert "Date: Thu, 25 Apr 2024 15:10:33 UTC" in stanza
        assert "MD5Sum: \n  1ae40621b32609d6251d09b2a47ef936 829119597 Contents-amd64" in stanza
        assert (
            "SHA256: \n  e945cdeadad8067c9b569e66c058f709d5aa4cd11d8099cc088dc192705e7bc7 829119597 Contents-amd64"
            in stanza
        )

        content_dict = stanza_to_dict(stanza.split("\n"))
        release2 = Release(base_url="http://myrepo.com", **content_dict)

        if release != release2:
            logging.error("Difference: %s", deepdiff.DeepDiff(release.model_dump(), release2.model_dump()))
            assert False
