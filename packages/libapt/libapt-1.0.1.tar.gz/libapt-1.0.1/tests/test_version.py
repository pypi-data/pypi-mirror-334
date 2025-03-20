"""Unit tests for the Debian version handling."""

import pytest

from libapt.deb import _parse_version
from libapt.version import DebianVersion, matches, InvalidRelation


class TestVersion:
    """Unit tests for the Debian version handling."""

    def _to_versions(self, versions: list[str]) -> list[DebianVersion]:
        """
        Convert strings to versions.

        :param versions: Debian versions to convert.
        """
        deb_versions: list[DebianVersion] = []
        for version_string in versions:
            deb_versions.append(self._to_version(version_string))
        return deb_versions

    def _to_version(self, version_string: str) -> DebianVersion:
        """
        Convert version string to version.

        :param version_string: Debian versions to convert.
        """
        (_relation, version) = _parse_version(version_string)
        return version

    def test_version_parsing(self):
        """Tests parsing of deb versions."""
        v = self._to_version("2.0.12-1ubuntu1")
        assert v.epoch == 0
        assert v.version == "2.0.12"
        assert v.revision == "1ubuntu1"

        v = self._to_version("2.0.12-1-1ubuntu1")
        assert v.epoch == 0
        assert v.version == "2.0.12-1"
        assert v.revision == "1ubuntu1"

        v = self._to_version("1:2.0.12-1-1ubuntu1")
        assert v.epoch == 1
        assert v.version == "2.0.12-1"
        assert v.revision == "1ubuntu1"

    def test_version_compare(self):
        """Tests version sorting."""
        versions = self._to_versions(["6.8.0-39.39", "6.8.0-31.31", "6.8.0-35.31"])

        versions.sort()

        assert versions[0] == self._to_version("6.8.0-31.31")
        assert versions[-1] == self._to_version("6.8.0-39.39")

        versions = self._to_versions(["8.0.8-0ubuntu1~24.04.1", "8.0.8-0ubuntu1~24.04.2", "8.0.7-0ubuntu1~24.04.1"])
        versions.sort()

        assert versions[0] == self._to_version("8.0.7-0ubuntu1~24.04.1")
        assert versions[-1] == self._to_version("8.0.8-0ubuntu1~24.04.2")

        versions = self._to_versions(
            ["2.42.10+dfsg-3ubuntu3.1", "2.42.10+ffsg-3ubuntu3.1", "2.42.10+afsg-3ubuntu3.1", "2.42.10+ffsg-3ubuntu3"]
        )
        versions.sort()

        assert versions[0] == self._to_version("2.42.10+afsg-3ubuntu3.1")
        assert versions[1] == self._to_version("2.42.10+dfsg-3ubuntu3.1")
        assert versions[2] == self._to_version("2.42.10+ffsg-3ubuntu3")
        assert versions[3] == self._to_version("2.42.10+ffsg-3ubuntu3.1")

    def test_partial_version(self):
        """Test comparison of partial version string."""
        vp = self._to_version("1.66ubuntu1")
        vd = self._to_version("1.66~")
        assert vd < vp

    def test_matches(self):
        """Test for VersionDepends equality."""
        a = self._to_version("1.2.3")
        b = self._to_version("1.2.3")

        assert matches("==", a, b)
        assert matches(None, a, b)
        assert matches(">=", a, b)

        c = self._to_version("0:1.2.3-1ubuntu1")
        d = self._to_version("1:1.2.3-1ubuntu1")

        assert matches(">>", c, d)
        assert matches(">=", c, d)

        e = self._to_version("1.2.3-1ubuntu2")
        f = self._to_version("1.2.3-1ubuntu1")

        assert matches("<<", e, f)
        assert matches("<=", e, f)

        with pytest.raises(InvalidRelation):
            assert matches("??", e, f)

    def test_different_type(self):
        """Test comparing DebianVersions to other types."""
        v = self._to_version("1.2.3-1ubuntu2")
        assert not v < "asdf"
        assert not v <= "asdf"
        assert not v == "asdf"

    def test_different_epochs(self):
        """Test comparing DebianVersions with different epochs."""
        a = self._to_version("0:1.2.3-1ubuntu1")
        b = self._to_version("1:1.2.3-1ubuntu1")
        c = self._to_version("1.2.3-1ubuntu1")
        d = self._to_version("1.2.3-1ubuntu2")

        assert a == c
        assert a < b
        assert c < b
        assert a < d

    def test_different_revision_length(self):
        """Test comparing DebianVersions with different epochs."""
        a = self._to_version("1.2.3-1ubuntu1")
        b = self._to_version("1.2.3-1eb12")

        assert not a < b
        assert b < a

    def test_different_versions(self):
        """Test comparing DebianVersions with different epochs."""
        a = self._to_version("1.2.3-1ubuntu1")
        b = self._to_version("1.12.34-1ubuntu1")
        c = self._to_version("1.12.34-1ubuntu")
        d = self._to_version("1.12.34-ubuntu1")
        e = self._to_version("1.12.34-?ubuntu1")
        f = self._to_version("1.12.34-1~")
        g = self._to_version("1.2.3-1ubuntu1blah3")
        h = self._to_version("1.2.3-1ubuntu1blah4")

        assert not b < a
        assert a < b
        assert c < b
        assert not b < c
        assert d < c
        assert not c < d
        assert d < e
        assert not e < d
        assert f < b
        assert not b < f
        assert g < h
        assert not h < g

    def test_version_repr(self):
        """Test version to string conversion."""
        a = self._to_version("0:1.2.3-1ubuntu1")
        b = self._to_version("1.2.3")
        c = self._to_version("1:1.2.3-1ubuntu1")
        d = self._to_version("1.2.3-1ubuntu1")

        assert str(a) == "1.2.3-1ubuntu1"
        assert str(b) == "1.2.3"
        assert str(c) == "1:1.2.3-1ubuntu1"
        assert str(d) == "1.2.3-1ubuntu1"

    def test_different_revision_compare(self):
        """Test comparing DebianVersions with different revisions."""
        a = self._to_version("1.2.3")
        b = self._to_version("1.2.3-1eb12")

        assert not b < a
        assert a < b
        assert not a < a
        assert not b < b
