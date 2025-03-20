"""
Processing InRelease metadata.
"""

import re

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator
from dateutil import parser

from libapt.apt import AptConfig


class FileHash(BaseModel):
    """
    Model for Release file hashes.
    """

    hash: str
    size: int
    file: str

    def __str__(self) -> str:
        return f"{self.hash} {self.size} {self.file}"

    def __repr__(self) -> str:
        return str(self)


def _parse_hash_entires(raw: str) -> list[FileHash]:
    """
    Parse the hash entries of the Release file.

    :param raw: Raw data form the Release file.
    :return: Entires as list of string tuples.
    """
    entries: list[FileHash] = []
    for line in raw.strip().split("\n"):
        line = line.strip()
        parts = re.split(r"[ ]+", line, maxsplit=2)
        entries.append(FileHash(hash=parts[0], size=int(parts[1]), file=parts[2]))
    return entries


class Release(BaseModel):
    """
    Model for APT Release data.
    """

    Origin: Optional[str] = None
    Label: Optional[str] = None
    Suite: Optional[str] = None
    Version: Optional[str] = None
    Codename: Optional[str] = None
    Date: datetime
    Architectures: list[str]
    Components: list[str]
    Description: Optional[str] = None
    MD5Sum: Optional[list[FileHash]] = None
    SHA1: Optional[list[FileHash]] = None
    SHA256: Optional[list[FileHash]] = None
    SHA512: Optional[list[FileHash]] = None
    base_url: str
    repo: Optional[AptConfig] = None

    @property
    def stanza(self) -> str:
        """
        Generate a stanza representing this Release.

        :returns: Stanza for the Release as str.
        """
        stanza = ""

        for key, value in self.model_dump().items():
            key = str(key)
            if not key[0].isupper():
                continue

            if not value:
                continue

            value = getattr(self, key)

            if isinstance(value, list):
                if isinstance(value[0], FileHash):
                    value = "\n" + "\n".join([str(entry) for entry in value])
                else:
                    value = " ".join([str(entry) for entry in value])
            elif isinstance(value, datetime):
                value = value.strftime("%a, %d %b %Y %H:%M:%S UTC")
            else:
                value = str(value)

            value = str(value).replace("\n", "\n  ")

            key = key.replace("_", "-")

            stanza += f"{key}: {str(value)}\n"

        return stanza

    @field_validator("Architectures", mode="before")
    @classmethod
    def transform_arch(cls, raw: str | list[str]) -> list[str]:
        if isinstance(raw, list):
            return raw
        return raw.split(" ")

    @field_validator("Components", mode="before")
    @classmethod
    def transform_comp(cls, raw: str | list[str]) -> list[str]:
        if isinstance(raw, list):
            return raw
        return raw.split(" ")

    @field_validator("MD5Sum", mode="before")
    @classmethod
    def transform_md5(cls, raw: str | list[FileHash]) -> list[FileHash]:
        if isinstance(raw, list):
            return raw
        return _parse_hash_entires(raw)

    @field_validator("SHA1", mode="before")
    @classmethod
    def transform_sha1(cls, raw: str | list[FileHash]) -> list[FileHash]:
        if isinstance(raw, list):
            return raw
        return _parse_hash_entires(raw)

    @field_validator("SHA256", mode="before")
    @classmethod
    def transform_sha256(cls, raw: str | list[FileHash]) -> list[FileHash]:
        if isinstance(raw, list):
            return raw
        return _parse_hash_entires(raw)

    @field_validator("SHA512", mode="before")
    @classmethod
    def transform_sha512(cls, raw: str | list[FileHash]) -> list[FileHash]:
        if isinstance(raw, list):
            return raw
        return _parse_hash_entires(raw)

    @field_validator("Date", mode="before")
    @classmethod
    def transform_date(cls, raw: str | datetime) -> datetime:
        if isinstance(raw, datetime):
            return raw
        return parser.parse(raw)
