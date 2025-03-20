"""Debian version helpers."""

from __future__ import annotations

import re

from typing import Optional

from pydantic import BaseModel, field_validator


class DebianVersion(BaseModel):
    """Debian package version."""

    epoch: Optional[int] = 0
    version: str
    revision: Optional[str] = None

    @field_validator("epoch", mode="before")
    @classmethod
    def transform_arch(cls, raw: int | None) -> int:
        if raw is None:
            return 0
        return raw

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DebianVersion):
            return False

        return self.epoch == other.epoch and other.version == self.version and other.revision == self.revision

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, DebianVersion):
            return False

        if self.epoch != other.epoch:
            # Is ensured by field validator.
            assert self.epoch is not None
            assert other.epoch is not None
            return self.epoch < other.epoch

        if self.version != other.version:
            return self._lt_parts(self.version, other.version)

        return self._lt_revision(other.revision)

    def __le__(self, other: object) -> bool:
        if not isinstance(other, DebianVersion):
            return False

        if self == other:
            return True

        return self < other

    def _lt_parts(self, a: str, b: str) -> bool:
        # split to parts
        a_parts = re.findall(r"\d+|\D+", a)
        b_parts = re.findall(r"\d+|\D+", b)

        # align length
        while len(a_parts) < len(b_parts):
            a_parts.append(None)

        while len(b_parts) < len(a_parts):
            b_parts.append(None)

        # compare parts
        for x, y in zip(a_parts, b_parts):
            if x == y:
                continue

            if x is None:
                return True
            if y is None:
                return False

            if x.isdigit() and not y.isdigit():
                return False
            elif y.isdigit() and not x.isdigit():
                return True
            elif x.isdigit() and y.isdigit():
                return int(x) < int(y)

            # align length
            while len(x) < len(y):
                x += "~"
            while len(y) < len(x):
                y += "~"

            # compare letters
            for u, v in zip([*x], [*y]):  # pragma: no branch
                if u == v:
                    continue

                if u == "~":
                    return True
                if v == "~":
                    return False

                if u.isalpha() and not v.isalpha():
                    return True
                if v.isalpha() and not u.isalpha():
                    return False

                return u < v

        # Should never be reached.
        raise Exception(f"Comparison of {a} and {b} was not conclusive!")  # pragma: no cover

    def _lt_revision(self, other: Optional[str]) -> bool:
        if not self.revision and not other:
            return False

        if self.revision == other:
            return False

        if not self.revision:
            return True
        elif not other:
            return False
        else:
            assert other
            return self._lt_parts(self.revision, other)

    def __str__(self) -> str:
        repr = self.version

        if self.epoch is not None and self.epoch != 0:
            repr = f"{self.epoch}:{repr}"

        if self.revision:
            repr = f"{repr}-{self.revision}"

        return repr

    def __repr__(self) -> str:
        return self.__str__()


class InvalidRelation(Exception):
    """Raised if an invalid version relation is given."""


def matches(relation: str | None, specified_version: DebianVersion, package_version: DebianVersion) -> bool:
    """
    Compare two DebianVersions according to the given comparison string.

    :param relation: Package relation string.
    :param specified_version: Specified required version.
    :param package_version: Debian package version.
    :returns: True if relation is fulfilled.
    :raises InvalidRelation: If the version string is not known.
    """
    if relation is None:
        relation = "="

    if relation == "<<":
        return package_version < specified_version
    elif relation == "<=":
        return package_version <= specified_version
    elif relation == "=" or relation == "==":
        return package_version == specified_version
    elif relation == ">=":
        return package_version >= specified_version
    elif relation == ">>":
        return package_version > specified_version
    else:
        raise InvalidRelation(f"The relation {relation} is not implemented!")
