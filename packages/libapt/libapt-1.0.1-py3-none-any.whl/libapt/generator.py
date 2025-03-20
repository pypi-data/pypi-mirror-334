"""Apt repository generator"""

import glob
import logging
import os
import lzma
import gzip
import hashlib
import datetime

from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from libapt.apt import AptConfig
from libapt.deb import Package, Source, extract_deb_meta, load_sources
from libapt.signature import strip_signature, sign_content, generate_key
from libapt.release import Release, FileHash


class RepositoryMetadata(BaseModel):
    """Metadata for repository creation."""

    suite: str
    version: str
    packages_folder: Path
    base_folder: Path
    origin: Optional[str] = None
    label: Optional[str] = None
    codename: Optional[str] = None
    description: Optional[str] = None
    private_key: Optional[str | Path] = None
    public_key: Optional[str | Path] = None


def generate_repo_metadata(metadata: RepositoryMetadata, base_url: str) -> AptConfig:
    """
    Generate valid apt repository metadata.

    If no key is provided, a key will be generated.
    If a public key is provided, the metadata will be verified using the key.
    Existing metadata will be overwritten!

    :param metadata: Repository specification.
    :param base_url: Base URL of the repository.
    :returns: AptConfig for the new repository.
    """
    packages: list[Package] = []
    for match in glob.glob("*.deb", root_dir=metadata.packages_folder):
        file = metadata.packages_folder / match
        deb_meta = extract_deb_meta(file)
        if deb_meta and deb_meta.package:
            pkg = deb_meta.package
            pkg.base_url = base_url
            pkg.Filename = match
            logging.debug("Adding package %s (%s)", match, pkg.Package)
            packages.append(pkg)
        else:  # pragma: no cover
            # Should never happen for a valid deb file.
            logging.info("Invalid deb package: %s", file)

    packages_by_arch: dict[str, list[Package]] = {}
    for pkg in packages:
        if pkg.Architecture not in packages_by_arch:
            packages_by_arch[pkg.Architecture] = [pkg]
        else:
            packages_by_arch[pkg.Architecture].append(pkg)

    sources: list[Source] = []
    for match in glob.glob("*.dsc", root_dir=metadata.packages_folder):
        file = metadata.packages_folder / match

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        if "BEGIN PGP SIGNED MESSAGE" in content:
            content = strip_signature(content)

        # Add required Directory field
        content_lines = [line for line in content.split("\n") if line.strip() != ""]
        content_lines.append(f"Directory: {file.parent}")
        content = "\n".join(content_lines)

        # Rename Source field to package field
        content = content.replace("Source: ", "Package: ")

        srcs = load_sources(content, base_url="")
        if len(srcs) == 0:  # pragma: no cover
            # Should never happen for a valid dsc file.
            logging.info("Invalid dsc package: %s", file)
            continue
        else:
            sources.append(srcs[0])

    base_folder = Path(metadata.base_folder)

    dist_folder = base_folder / "dists" / metadata.suite
    os.makedirs(dist_folder, exist_ok=True)

    COMPONENT = "main"

    for arch in packages_by_arch.keys():
        pkgs_folder = dist_folder / COMPONENT / f"binary-{arch}"
        os.makedirs(pkgs_folder, exist_ok=True)

        pkg_index_content = "".join([pkg.stanza for pkg in packages_by_arch[arch]])
        pkg_index_file = pkgs_folder / "Packages"

        with open(pkg_index_file, "w", encoding="utf-8") as f:
            f.write(pkg_index_content)

        pkg_index_file_xz = pkgs_folder / "Packages.xz"
        with open(pkg_index_file_xz, "wb") as f:
            f.write(lzma.compress(pkg_index_content.encode(encoding="utf-8")))

        pkg_index_file_gz = pkgs_folder / "Packages.gz"
        with open(pkg_index_file_gz, "wb") as f:
            f.write(gzip.compress(pkg_index_content.encode(encoding="utf-8")))

    srcs_folder = dist_folder / COMPONENT / "source"
    os.makedirs(srcs_folder, exist_ok=True)

    src_index_content = "".join([src.stanza for src in sources])
    src_index_file = srcs_folder / "Sources"

    with open(src_index_file, "w", encoding="utf-8") as f:
        f.write(src_index_content)

    src_index_file_xz = srcs_folder / "Sources.xz"
    with open(src_index_file_xz, "wb") as f:
        f.write(lzma.compress(src_index_content.encode(encoding="utf-8")))

    src_index_file_gz = srcs_folder / "Sources.gz"
    with open(src_index_file_gz, "wb") as f:
        f.write(gzip.compress(src_index_content.encode(encoding="utf-8")))

    file_hashes: dict[str, list[FileHash]] = {}
    hashes = [
        ("SHA512", hashlib.sha512),
        ("SHA256", hashlib.sha256),
        ("SHA1", hashlib.sha1),
        ("MD5Sum", hashlib.md5),
    ]

    for name, _algo in hashes:
        file_hashes[name] = []

    for match in glob.glob("**/Packages*", root_dir=dist_folder, recursive=True):
        file = dist_folder / match

        with open(file, "rb") as f:
            file_data = f.read()

        file_size = os.path.getsize(file)

        for hash_name, hash_algo in hashes:
            file_hash = hash_algo(file_data).hexdigest()
            file_hashes[hash_name].append(FileHash(hash=file_hash, size=file_size, file=match))

    for match in glob.glob("**/Source*", root_dir=dist_folder, recursive=True):
        file = dist_folder / match

        with open(file, "rb") as f:
            file_data = f.read()

        file_size = os.path.getsize(file)

        for hash_name, hash_algo in hashes:
            file_hash = hash_algo(file_data).hexdigest()
            file_hashes[hash_name].append(FileHash(hash=file_hash, size=file_size, file=match))

    architectures = [arch for arch in packages_by_arch.keys()]

    release = Release(
        Origin=metadata.origin,
        Label=metadata.label,
        Suite=metadata.suite,
        Version=metadata.version,
        Codename=metadata.codename,
        Date=datetime.datetime.now(),
        Architectures=architectures,
        Components=[COMPONENT],
        Description=metadata.description,
        MD5Sum=file_hashes["MD5Sum"],
        SHA1=file_hashes["SHA1"],
        SHA256=file_hashes["SHA256"],
        SHA512=file_hashes["SHA512"],
        base_url=base_url,
        repo=None,
    )

    release_content = release.stanza

    release_file = dist_folder / "Release"
    with open(release_file, "w", encoding="utf-8") as f:
        f.write(release_content)

    if not metadata.private_key:
        import getpass

        user = getpass.getuser()
        (priv, pub) = generate_key(owner=user, owner_mail=f"{user}@localhost", folder=base_folder)
        metadata.private_key = priv
        metadata.public_key = pub

    assert metadata.private_key
    release_content = sign_content(release_content, Path(metadata.private_key))

    inrelease_file = dist_folder / "InRelease"
    with open(inrelease_file, "w", encoding="utf-8") as f:
        f.write(release_content)

    if len(packages_by_arch.keys()) == 1:
        repo_arch: str | None = list(packages_by_arch.keys())[0]
    else:
        repo_arch = None

    config = AptConfig(
        apt_repo=base_url, arch=repo_arch, distro=metadata.suite, components={COMPONENT}, key=metadata.public_key
    )

    return config
