"""APT package metadata processing."""

import os
import logging
import hashlib
import tempfile
import glob
import tarfile
import shutil
import zstandard

from typing import Optional
from pathlib import Path
from dataclasses import dataclass

import unix_ar  # type: ignore

from pydantic import BaseModel, field_validator

from libapt.apt import AptConfig
from libapt.download import Downloader, DownloadFailed
from libapt.stanza import stanza_to_dict
from libapt.release import _parse_hash_entires, FileHash
from libapt.version import DebianVersion


class InvalidPackageMetadata(Exception):
    """Raised if invalid package metadata is detected."""


class PackageDependency(BaseModel):
    """Single package dependency."""

    package: str
    version: Optional[DebianVersion]
    relation: Optional[str]
    additional: Optional[str] = None

    def __str__(self) -> str:
        version_str = f"{self.package}"
        if self.version:
            if self.relation:
                version_str += f" ({self.relation} {self.version})"
            else:
                version_str += f" ({self.version})"

        if self.additional:
            version_str += " " + self.additional

        return version_str

    def __repr__(self) -> str:
        return str(self)


class Dependency(BaseModel):
    """Debian package dependency."""

    alternatives: list[PackageDependency]

    def __str__(self) -> str:
        alts = [str(alt) for alt in self.alternatives]
        return " | ".join(alts)

    def __repr__(self) -> str:
        return str(self)


class Person(BaseModel):
    """Debian package maintainer"""

    name: str
    email: str

    def __str__(self) -> str:
        if self.email != "":
            return f"{self.name} <{self.email}>"
        else:
            return f"{self.name}"

    def __repr__(self) -> str:
        return str(self)


def _parse_version(version: str) -> tuple[str | None, DebianVersion]:
    """
    Parse a Debian package version dependency string.

    :param version: Version string.
    :returns: Version object.
    """
    if " " in version:
        parts = version.split(" ", maxsplit=1)
        relation = parts[0].strip()
        version = parts[1].strip()
    else:
        relation = None

    if ":" in version:
        parts = version.split(":", maxsplit=1)
        epoch = int(parts[0])
        version = parts[1]
    else:
        epoch = 0

    if "-" in version:
        parts = version.rsplit("-", maxsplit=1)
        version = parts[0]
        revision = parts[1]
    else:
        revision = None

    return (relation, DebianVersion(epoch=epoch, version=version, revision=revision))


def _parse_dependencies(dependencies: str) -> list[Dependency]:
    """
    Parse a dependency string from a package stanza.

    :param dependencies: Dependencies string.
    :returns: List of Dependency objects
    """
    deps: list[Dependency] = []

    packages = dependencies.strip().split(",")

    for package in packages:
        package = package.strip()

        alternatives: list[PackageDependency] = []

        for alternative in package.split("|"):
            alternative = alternative.strip()
            if "(" in alternative:
                parts = alternative.split("(", maxsplit=1)
                name = parts[0].strip()
                remainder = parts[1].strip()
                if ") " in remainder:
                    parts = remainder.split(")", maxsplit=1)
                    version_str = parts[0]
                    additional = parts[1].strip()
                else:
                    version_str = remainder[:-1]
                    additional = None

                (relation, version) = _parse_version(version_str)
                alternatives.append(
                    PackageDependency(package=name, version=version, relation=relation, additional=additional)
                )
            else:
                alternatives.append(
                    PackageDependency(package=alternative, version=None, relation=None, additional=None)
                )

        deps.append(Dependency(alternatives=alternatives))

    return deps


def _parse_person(person: str) -> Person:
    """
    Parse a maintainer string from a package stanza.

    :param person: Maintainer string.
    :returns: Person object
    """
    person = person.strip()
    if "<" in person:
        parts = person.split("<", maxsplit=1)
        name = parts[0].strip()
        email = parts[1].strip()[:-1]
    else:
        name = person
        email = ""
    return Person(name=name, email=email)


class Package(BaseModel):
    """APT package information."""

    Package: str
    Architecture: str
    Version: DebianVersion
    Built_Using: Optional[list[Dependency]] = None
    Priority: Optional[str] = None
    Section: Optional[str] = None
    Origin: Optional[str] = None
    Maintainer: Optional[Person] = None
    Original_Maintainer: Optional[Person] = None
    Bugs: Optional[str] = None
    Installed_Size: Optional[int] = None
    Depends: Optional[list[Dependency]] = None
    Recommends: Optional[list[Dependency]] = None
    Suggests: Optional[list[Dependency]] = None
    Filename: str
    Size: Optional[int] = None
    MD5sum: Optional[str] = None
    SHA1: Optional[str] = None
    SHA256: Optional[str] = None
    SHA512: Optional[str] = None
    Homepage: Optional[str] = None
    Task: Optional[list[str]] = None
    Description: Optional[str] = None
    Description_md5: Optional[str] = None
    base_url: str
    component: Optional[str] = None
    repo: Optional[AptConfig] = None

    @property
    def stanza(self) -> str:
        """
        Generate a stanza representing this package.

        :returns: Stanza for the package as str.
        """
        stanza = ""

        for key, value in self.model_dump().items():
            key = str(key)
            if not key[0].isupper():
                continue

            if value is None:
                continue

            value = getattr(self, key)

            if isinstance(value, list):
                value = ", ".join([str(entry) for entry in value])
            else:
                value = str(value)

            value = str(value).replace("\n", "\n  ")

            key = key.replace("_", "-")

            stanza += f"{key}: {str(value)}\n"

        return stanza + "\n"

    @field_validator("Version", mode="before")
    @classmethod
    def transform_version(cls, raw: str) -> DebianVersion:
        (_rel, version) = _parse_version(raw)
        return version

    @field_validator("Built_Using", mode="before")
    @classmethod
    def transform_built_using(cls, raw: str) -> list[Dependency]:
        return _parse_dependencies(raw)

    @field_validator("Maintainer", mode="before")
    @classmethod
    def transform_maintainer(cls, raw: str) -> Person:
        return _parse_person(raw)

    @field_validator("Original_Maintainer", mode="before")
    @classmethod
    def transform_original_maintainer(cls, raw: str) -> Person:
        return _parse_person(raw)

    @field_validator("Depends", mode="before")
    @classmethod
    def transform_depends(cls, raw: str) -> list[Dependency]:
        return _parse_dependencies(raw)

    @field_validator("Recommends", mode="before")
    @classmethod
    def transform_recommends(cls, raw: str) -> list[Dependency]:
        return _parse_dependencies(raw)

    @field_validator("Suggests", mode="before")
    @classmethod
    def transform_suggests(cls, raw: str) -> list[Dependency]:
        return _parse_dependencies(raw)

    @field_validator("Task", mode="before")
    @classmethod
    def transform_task(cls, raw: str) -> list[str]:
        return [task.strip() for task in raw.split(",")]

    @field_validator("base_url", mode="before")
    @classmethod
    def transform_base_url(cls, raw: str) -> str:
        if len(raw) > 0 and raw[-1] != "/":
            raw += "/"
        return raw

    def download(self, downloader: Downloader, folder: Path | None = None) -> Path | None:
        """
        Download the package.

        :param folder: Where to put the package.
        :param downloader: Downloader for package download.
        :returns: Path to the downloaded package file, or None if download fails.
        :raises DownloadFailed: Raises and DownloadFailed exception in case of hash mismatch.
        """
        assert self.Filename != ""

        url = f"{self.base_url}{self.Filename}"
        logging.debug("Downloading package %s from %s...", self.Package, url)

        file = downloader.download_file(url, folder, Path(self.Filename).name)

        with open(file, "rb") as f:
            data = f.read()

        hash_algo = None
        expected_hash = ""

        if self.SHA512:
            hash_algo = hashlib.sha512
            expected_hash = self.SHA512
        elif self.SHA256:
            hash_algo = hashlib.sha256
            expected_hash = self.SHA256
        elif self.SHA1:
            hash_algo = hashlib.sha1
            expected_hash = self.SHA1
        elif self.MD5sum:
            hash_algo = hashlib.md5
            expected_hash = self.MD5sum
        else:
            logging.error("The package %s has no hash. Cannot verify the integrity of the package.", self.Package)

        if hash_algo:
            hash = hash_algo(data).hexdigest()
            if hash != expected_hash:
                raise DownloadFailed(
                    f"The hash of the package {self.Package} downloaded form URL {url} is {hash} and does not match {self.SHA512}!"
                )

        return file


class PackageListEntry(BaseModel):
    """Debian source metadata package list entry."""

    package: str
    package_type: str
    section: str
    priority: str
    additional: dict

    def __str__(self) -> str:
        pls = f"{self.package} {self.package_type} {self.section} {self.priority}"
        for key, value in self.additional.items():
            pls += f" {key}={value}"
        return pls

    def __repr__(self) -> str:
        return str(self)


def _parse_package_list(package_list: str) -> list[PackageListEntry]:
    """
    Parse the package list metadata.

    :param package_list: Package list text from metadata file.
    :returns: List of PackageListEntry objects.
    """
    entries: list[PackageListEntry] = []

    lines = [line.strip() for line in package_list.strip().split("\n")]

    for line in lines:
        line = line.strip()
        parts = [part.strip() for part in line.split(" ")]
        package = parts[0]
        package_type = parts[1]
        section = parts[2]
        priority = parts[3]
        additional: dict[str, str] = {}
        for more in parts[4:]:
            if "=" in more:
                parts = more.split("=", maxsplit=1)
                additional[parts[0].strip()] = parts[1].strip()
            else:
                additional[more.strip()] = ""
        entries.append(
            PackageListEntry(
                package=package, package_type=package_type, section=section, priority=priority, additional=additional
            )
        )

    return entries


class Source(BaseModel):
    """Debian source package metadata."""

    Package: str
    Format: str
    Binary: Optional[list[str]] = None
    Architecture: Optional[str] = None
    Version: DebianVersion
    Priority: Optional[str] = None
    Section: Optional[str] = None
    Maintainer: Person
    Original_Maintainer: Optional[Person] = None
    Uploaders: Optional[list[Person]] = None
    Standards_Version: Optional[str] = None
    Build_Depends: Optional[list[Dependency]] = None
    Testsuite: Optional[str] = None
    Testsuite_Triggers: Optional[list[str]] = None
    Homepage: Optional[str] = None
    Description: Optional[str] = None
    Vcs_Browser: Optional[str] = None
    Vcs_Git: Optional[str] = None
    Vcs_Svn: Optional[str] = None
    Vcs_Arch: Optional[str] = None
    Vcs_Bzr: Optional[str] = None
    Vcs_Cvs: Optional[str] = None
    Vcs_Darcs: Optional[str] = None
    Vcs_Hg: Optional[str] = None
    Vcs_Mtn: Optional[str] = None
    Directory: Optional[str] = None
    Package_List: Optional[list[PackageListEntry]] = None
    Files: list[FileHash]
    Checksums_Sha1: Optional[list[FileHash]] = None
    Checksums_Sha256: Optional[list[FileHash]] = None
    Checksums_Sha512: Optional[list[FileHash]] = None
    Debian_Vcs_Browser: Optional[str] = None
    Debian_Vcs_Svn: Optional[str] = None
    base_url: str
    component: Optional[str] = None
    repo: Optional[AptConfig] = None

    @property
    def stanza(self) -> str:
        """
        Generate a stanza representing this source package.

        :returns: Stanza for the package as str.
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
                if isinstance(value[0], FileHash) or isinstance(value[0], PackageListEntry):
                    value = "\n" + "\n".join([str(entry) for entry in value])
                else:
                    value = ", ".join([str(entry) for entry in value])
            else:
                value = str(value)

            value = str(value).replace("\n", "\n  ")

            key = key.replace("_", "-")

            stanza += f"{key}: {str(value)}\n"

        return stanza + "\n"

    @field_validator("Binary", mode="before")
    @classmethod
    def transform_binary(cls, raw: str) -> list[str]:
        return [binary.strip() for binary in raw.split(",")]

    @field_validator("Version", mode="before")
    @classmethod
    def transform_version(cls, raw: str) -> DebianVersion:
        (_rel, version) = _parse_version(raw)
        return version

    @field_validator("Maintainer", mode="before")
    @classmethod
    def transform_maintainer(cls, raw: str) -> Person:
        return _parse_person(raw)

    @field_validator("Original_Maintainer", mode="before")
    @classmethod
    def transform_original_maintainer(cls, raw: str) -> Person:
        return _parse_person(raw)

    @field_validator("Uploaders", mode="before")
    @classmethod
    def transform_uploaders(cls, raw: str) -> list[Person]:
        return [_parse_person(entry.strip()) for entry in raw.strip().split(",") if entry.strip()]

    @field_validator("Build_Depends", mode="before")
    @classmethod
    def transform_build_depends(cls, raw: str) -> list[Dependency]:
        return _parse_dependencies(raw)

    @field_validator("Testsuite_Triggers", mode="before")
    @classmethod
    def transform_testsuite_triggers(cls, raw: str) -> list[str]:
        return [entry.strip() for entry in raw.split(",")]

    @field_validator("Package_List", mode="before")
    @classmethod
    def transform_package_list(cls, raw: str) -> list[PackageListEntry]:
        return _parse_package_list(raw)

    @field_validator("Files", mode="before")
    @classmethod
    def transform_files(cls, raw: str) -> list[FileHash]:
        return _parse_hash_entires(raw)

    @field_validator("Checksums_Sha1", mode="before")
    @classmethod
    def transform_sha1(cls, raw: str) -> list[FileHash]:
        return _parse_hash_entires(raw)

    @field_validator("Checksums_Sha256", mode="before")
    @classmethod
    def transform_sha256(cls, raw: str) -> list[FileHash]:
        return _parse_hash_entires(raw)

    @field_validator("Checksums_Sha512", mode="before")
    @classmethod
    def transform_sha512(cls, raw: str) -> list[FileHash]:
        return _parse_hash_entires(raw)

    @field_validator("base_url", mode="before")
    @classmethod
    def transform_base_url(cls, raw: str) -> str:
        if len(raw) > 0 and raw[-1] != "/":
            raw += "/"
        return raw

    def download(self, downloader: Downloader, folder: Path | None = None) -> Path | None:
        """
        Download the source package.

        :param folder: Where to put the source package files.
        :param downloader: Downloader for package download.
        :returns: Path to the downloaded dsc file, or None if download fails.
        :raises DownloadFailed: Raises and DownloadFailed exception in case of hash mismatch.
        """
        files: list[FileHash] = []
        hash_algo = None

        if self.Checksums_Sha512:
            files = self.Checksums_Sha512
            hash_algo = hashlib.sha512
        elif self.Checksums_Sha256:
            files = self.Checksums_Sha256
            hash_algo = hashlib.sha256
        elif self.Checksums_Sha1:
            files = self.Checksums_Sha1
            hash_algo = hashlib.sha1
        else:
            files = self.Files
            hash_algo = hashlib.md5

        dsc_file = None

        for file_meta in files:
            url = f"{self.base_url}{self.Directory}/{file_meta.file}"
            logging.debug("Downloading file of source package %s from %s...", self.Package, url)

            file = downloader.download_file(url, folder, Path(file_meta.file).name)

            with open(file, "rb") as f:
                data = f.read()

            hash = hash_algo(data).hexdigest()
            if hash != file_meta.hash:
                raise DownloadFailed(
                    f"The hash of the package {self.Package} downloaded form URL {url} is {hash} and does not match {file_meta.hash}!"
                )

            if file_meta.file.endswith(".dsc"):
                dsc_file = file

        return dsc_file


def load_packages(
    content: str, base_url: str, repo: AptConfig | None = None, component: str | None = None
) -> list[Package]:
    """
    Load the Debian package metadata.

    :param content: Content of the package index file.
    :param base_url: Prefix URL to complete the file URL.
    :param repo: Apt repository containing the package.
    :param component: Component containing the package.
    :returns: List if package metadata objects.
    """
    packages: list[Package] = []

    stanzas = content.split("\n\n")

    for stanza in stanzas:
        stanza = stanza.strip()
        if not stanza:
            continue

        data = stanza_to_dict(stanza.split("\n"))
        package = Package(base_url=base_url, repo=repo, component=component, **data)
        packages.append(package)

    return packages


def load_sources(
    content: str, base_url: str, repo: AptConfig | None = None, component: str | None = None
) -> list[Source]:
    """
    Load the Debian source metadata.

    :param content: Content of the source index file.
    :param base_url: Prefix URL to complete the file URLs.
    :param repo: Apt repository containing the package.
    :param component: Component containing the package.
    :returns: List if source metadata objects.
    """
    sources: list[Source] = []

    stanzas = content.split("\n\n")

    for stanza in stanzas:
        stanza = stanza.strip()
        if not stanza:
            continue

        data = stanza_to_dict(stanza.split("\n"))
        source = Source(base_url=base_url, repo=repo, component=component, **data)
        sources.append(source)

    return sources


def extract_deb(deb: Path, target: Path | None = None) -> Path | None:
    """
    Extract the deb package to the given folder.

    If no folder is given, a temporary folder is used.

    :param deb: Path to the deb file.
    :param target: Folder to put the files.
    :returns: Path to the folder containing the content or None if extraction failed.
    """
    if target is None:
        target = Path(tempfile.mkdtemp())

    logging.debug("Extracting content of %s to %s.", deb, target)

    os.makedirs(target, exist_ok=True)

    try:
        file = unix_ar.open(deb)
        file.extractall(str(target))
    except Exception as e:
        logging.error("Extraction of deb %s failed: %s", deb, e)
        return None

    return target


def _extract_zst(archive: Path, extracted_file: Path) -> None:
    """
    Extract a .zst file.

    :param archive: Path to .zst file.
    :param extracted_file: Directory to extract file
    """

    zstd = zstandard.ZstdDecompressor()

    with open(extracted_file, "wb") as out_file:
        with archive.open("rb") as zst_file:
            zstd.copy_stream(zst_file, out_file)


def extract_deb_data(deb: Path, target: Path | None = None) -> Path | None:
    """
    Extract the deb package data to the given folder.

    If no folder is given, a temporary folder is used.

    :param deb: Path to the deb file.
    :param target: Folder to put the data files of the deb.
    :returns: Path to the folder containing the package data or None if extraction failed.
    """
    content = extract_deb(deb)
    if content is None:
        return None

    matches = glob.glob("data.*", root_dir=content)
    if len(matches) == 0:  # pragma: no cover
        # Should not happen for proper Debian binary archives.
        logging.error("Package %s has not data content!", deb)
        return None

    if target is None:
        target = Path(tempfile.mkdtemp())

    logging.debug("Data archives of package %s: %s", deb, matches)

    for match in matches:
        archive = content / match
        logging.debug("Extracting tar %s...", archive)

        if match.endswith(".zst"):
            out = content / match[:-4]
            logging.debug("Extracting zstd file %s as %s...", archive, out)
            _extract_zst(archive, out)
            archive = out

        tar = tarfile.open(archive)
        tar.extractall(path=target)
        tar.close()

    shutil.rmtree(content)

    return target


@dataclass
class DebMetadata:
    package: Package | None
    md5sums: list[tuple[str, str]]
    scripts: dict[str, str]


def extract_deb_meta(deb: Path) -> DebMetadata | None:
    """
    Extract the deb package metadata.

    :param deb: Path to the deb file.
    :returns: a DebMetadata object or None.
    """
    content = extract_deb(deb)
    if content is None:
        return None

    matches = glob.glob("control.*", root_dir=content)
    if len(matches) == 0:  # pragma: no cover
        # Should not happen for proper Debian binary archives.
        logging.error("Package %s has not control content!", deb)
        return None

    target = Path(tempfile.mkdtemp())

    logging.debug("Control archives of package %s: %s", deb, matches)

    for match in matches:
        archive = content / match
        logging.debug("Extracting tar %s...")

        if match.endswith(".zst"):
            out = content / match[:-4]
            logging.debug("Extracting zstd file %s as %s...", archive, out)
            _extract_zst(archive, out)
            archive = out

        tar = tarfile.open(archive)
        tar.extractall(path=target)
        tar.close()

    shutil.rmtree(content)

    control = target / "control"
    pkg: Package | None = None

    if os.path.isfile(control):  # pragma: no branch
        # Should always exist for a valid Debian binary package.
        with open(control, "r", encoding="utf-8") as f:
            control_content = f.read()

        control_content += f"Filename: {str(deb)}"

        pkgs = load_packages(control_content, base_url="")
        if len(pkgs) == 0:  # pragma: no cover
            # Should not happen for proper Debian binary archives.
            logging.error("Parsing control content failed! Content:\n%s", control_content)
        else:
            if len(pkgs) > 1:  # pragma: no cover
                # Should not happen for proper Debian binary archives.
                logging.error("Control describes multiple packages! Packages:\n%s", pkgs)
            pkg = pkgs[0]

    md5sums = target / "md5sums"
    files: list[tuple[str, str]] = []
    if os.path.isfile(md5sums):  # pragma: no branch
        # Should always exist for a valid Debian binary package.
        with open(md5sums, "r", encoding="utf-8") as f:
            md5sums_content = f.readlines()
        for line in md5sums_content:
            line = line.strip()
            if line == "":  # pragma: no cover
                # Should never happen for a valid Debian binary package.
                continue

            parts = [part for part in line.split(" ") if part.strip() != ""]

            if not len(parts) == 2:  # pragma: no cover
                # Should not happen for proper Debian binary archives.
                logging.error("Invalid line in md5sums: %s (%s)", line, parts)
                continue

            files.append((parts[0].strip(), parts[1].strip()))

    scripts = [
        ("postinst", target / "postinst"),
        ("postrm", target / "postrm"),
        ("preinst", target / "preinst"),
        ("prerm", target / "prerm"),
    ]
    package_scripts: dict[str, str] = {}

    for name, script in scripts:
        if os.path.isfile(script):
            with open(script, "r", encoding="utf-8") as f:
                script_content = f.read()
            package_scripts[name] = script_content

    shutil.rmtree(target)

    return DebMetadata(package=pkg, md5sums=files, scripts=package_scripts)
