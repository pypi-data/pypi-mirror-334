"""Debian package pool implementation."""

import logging
import lzma
import gzip
import hashlib

from pathlib import Path

from libapt.apt import AptConfig, AptRepo, AptDebRepo, AptFlatRepo
from libapt.deb import Package, DebianVersion, Source
from libapt.download import Downloader, DownloadFailed
from libapt.release import Release, FileHash
from libapt.stanza import stanza_to_dict, stanzas_to_list
from libapt.signature import strip_signature, verify_signature
from libapt.version import matches


class ComponentPool:
    """Package pool for one component."""

    def __init__(self, packages: list[Package], sources: list[Source]) -> None:
        self._packages: dict[str, list[Package]] = {}
        self._sources: dict[str, list[Source]] = {}

        for package in packages:
            if package.Package in self._packages:
                self._packages[package.Package].append(package)
            else:
                self._packages[package.Package] = [package]

        for source in sources:
            if source.Package in self._sources:
                self._sources[source.Package].append(source)
            else:
                self._sources[source.Package] = [source]

    @property
    def packages(self) -> list[Package]:
        """
        Get all packages in the pool.

        :returns: List of packages.
        """
        packages: list[Package] = []
        for pl in self._packages.values():
            packages.extend(pl)
        return packages

    @property
    def sources(self) -> list[Source]:
        """
        Get all packages in the pool.

        :returns: List of Source packages.
        """
        sources: list[Source] = []
        for pl in self._sources.values():
            sources.extend(pl)
        return sources

    def find_binary_package(
        self, package: str, version: DebianVersion | None = None, relation: str | None = None, arch: str | None = None
    ) -> list[Package]:
        """
        Search for a matching binary package.

        :param package: Name of the package.
        :param version: Version of the package.
        :param relation: Version relation for comparison.
        :param arch: Architecture of the package.
        :returns: List of matching packages. The newest package is the first element of the list.
        """
        if package not in self._packages:
            return []

        packages: list[Package]

        if arch is not None:
            packages = list(filter(lambda pkg: pkg.Architecture == arch, self._packages[package]))
        else:
            packages = self._packages[package].copy()

        if version is not None:
            packages = list(filter(lambda pkg: matches(relation, version, pkg.Version), packages))

        packages.sort(key=lambda package: package.Version, reverse=True)

        return packages

    def find_source_package(
        self, package: str, version: DebianVersion | None = None, relation: str | None = None, arch: str | None = None
    ) -> list[Source]:
        """
        Search for matching source package.

        :param package: Name of the package.
        :param version: Version of the package.
        :param relation: Version relation for comparison.
        :param arch: Architecture of the package.
        :returns: List of matching source packages. The newest source package is the first element of the list.
        """
        if package not in self._sources:
            return []

        sources: list[Source]

        if arch is not None:
            sources = list(filter(lambda pkg: pkg.Architecture == arch, self._sources[package]))
        else:
            sources = self._sources[package].copy()

        if version is not None:
            sources = list(filter(lambda src: matches(relation, version, src.Version), sources))

        sources.sort(key=lambda package: package.Version, reverse=True)

        return sources


class RepoPool:
    """Package pool for one apt repository."""

    def __init__(self) -> None:
        """
        Create a new RepoPool.
        """
        self.DEFAULT_COMPONENT = "main"
        self._component_pools: dict[str, ComponentPool] = {}

    def _update_component(self, component: str | None, cmp_pool: ComponentPool) -> None:
        """
        Update the packages of an component.

        :param component: Name of the component.
        :param cmp_pool: New packages and sources.
        """
        if component is None:
            component = self.DEFAULT_COMPONENT
        self._component_pools[component] = cmp_pool

    @property
    def packages(self) -> list[Package]:
        """
        Get all packages in the pool.

        :returns: List of packages.
        """
        packages: list[Package] = []
        for comp_pool in self._component_pools.values():
            packages.extend(comp_pool.packages)
        return packages

    @property
    def sources(self) -> list[Source]:
        """
        Get all packages in the pool.

        :returns: List of Source packages.
        """
        sources: list[Source] = []
        for comp_pool in self._component_pools.values():
            sources.extend(comp_pool.sources)
        return sources

    def get_packages(self, component: str | None = None) -> list[Package]:
        """
        Get all packages of this repository and component, if component is given.

        :param component: Component name.
        :returns: Packages of the given apt repository (and component).
        """
        if component is None:
            component = self.DEFAULT_COMPONENT

        if component not in self._component_pools:
            return []

        return self._component_pools[component].packages

    def get_sources(self, component: str | None = None) -> list[Source]:
        """
        Get all packages of the repository and component, if component is given.

        :param component: Component name.
        :returns: Packages of the given apt repository (and component).
        """
        if component is None:
            component = self.DEFAULT_COMPONENT

        if component not in self._component_pools:
            return []

        return self._component_pools[component].sources

    def find_binary_package(
        self, package: str, version: DebianVersion | None = None, relation: str | None = None, arch: str | None = None
    ) -> list[Package]:
        """
        Search for a matching binary package.

        :param package: Name of the package.
        :param version: Version of the package.
        :param relation: Version relation for comparison.
        :param arch: Architecture of the package.
        :returns: List of matching packages. The newest package is the first element of the list.
        """
        packages: list[Package] = []
        for cmp_pool in self._component_pools.values():
            pkgs = cmp_pool.find_binary_package(package, version, relation, arch)
            packages.extend(pkgs)

        packages.sort(key=lambda package: package.Version, reverse=True)

        return packages

    def find_source_package(
        self, package: str, version: DebianVersion | None = None, relation: str | None = None, arch: str | None = None
    ) -> list[Source]:
        """
        Search for matching source package.

        :param package: Name of the package.
        :param version: Version of the package.
        :param relation: Version relation for comparison.
        :param arch: Architecture of the package.
        :returns: List of matching source packages. The newest source package is the first element of the list.
        """
        sources: list[Source] = []
        for cmp_pool in self._component_pools.values():
            srcs = cmp_pool.find_source_package(package, version, relation, arch)
            sources.extend(srcs)

        sources.sort(key=lambda source: source.Version, reverse=True)

        return sources


def _get_package_index_hash(url: str, release: Release) -> tuple[str, str] | None:
    """
    Get the hash for the given package index file.

    :param url: URL to the package index hash file.
    :param release: InRelease metadata.
    :returns: Tuple of hash and algorithm name, or None if hash is not found.
    """
    hash_lists: list[tuple[list[FileHash] | None, str]] = [
        (release.SHA512, "SHA512"),
        (release.SHA256, "SHA256"),
        (release.SHA1, "SHA1"),
        (release.MD5Sum, "MD5Sum"),
    ]

    for hash_list, hash_name in hash_lists:
        if hash_list is None:
            continue

        hashes = list(filter(lambda h: url.endswith(h.file), hash_list))
        if len(hashes) > 1:
            logging.error("Multiple entries found for url %s: %s", url, hashes)
        if len(hashes) > 0:
            return (hashes[0].hash, hash_name)

    return None


class Pool:
    """Querying apt repositories."""

    def __init__(self, downloader: Downloader):
        """
        Setup the pool.

        :param downloader: Downloader implementation.
        """
        self._downloader = downloader
        self._apt_repos: dict[str, AptRepo] = {}
        self._pools: dict[str, RepoPool] = {}
        self._repo_metadata: dict[str, Release] = {}

    @property
    def downloader(self) -> Downloader:
        """
        Get the downloader.

        :returns: The downloader.
        """
        return self._downloader

    @property
    def apt_repo_ids(self) -> list[str]:
        """
        Get the IDs of all apt repos.

        :returns: List of apt repository IDs.
        """
        return [str(key) for key in self._apt_repos.keys()]

    @property
    def apt_repos(self) -> list[AptRepo]:
        """
        Get all apt repos.

        :returns: List of apt repositories.
        """
        return [repo for repo in self._apt_repos.values()]

    @property
    def packages(self) -> list[Package]:
        """
        Get all packages in the pool.

        :returns: List of packages.
        """
        packages = []
        for repo_pool in self._pools.values():
            packages.extend(repo_pool.packages)
        return packages

    @property
    def sources(self) -> list[Source]:
        """
        Get all packages in the pool.

        :returns: List of Source packages.
        """
        sources = []
        for repo_pool in self._pools.values():
            sources.extend(repo_pool.sources)
        return sources

    def get_packages(self, apt_repo_id: str, component: str | None = None) -> list[Package]:
        """
        Get all packages of the repository and component, if component is given.

        :param apt_repo_id: Apt repo id.
        :param component: Component name.
        :returns: Packages of the given apt repository (and component).
        """
        if apt_repo_id in self._pools:
            repo_pool = self._pools[apt_repo_id]
            return repo_pool.get_packages(component)
        return []

    def get_sources(self, apt_repo_id: str, component: str | None = None) -> list[Source]:
        """
        Get all packages of the repository and component, if component is given.

        :param apt_repo_id: Apt repo id.
        :param component: Component name.
        :returns: Packages of the given apt repository (and component).
        """
        if apt_repo_id in self._pools:
            repo_pool = self._pools[apt_repo_id]
            return repo_pool.get_sources(component)
        return []

    def add_repository(self, config: AptConfig, arch: str) -> bool:
        """
        Add a new apt repository.

        :param config: Apt repository config.
        :param arch: CPU architecture.
        :returns: True if repo was added, false if repo already exists.
        """
        repo: AptRepo
        if config.distro is None:
            repo = AptFlatRepo(config=config, arch=arch)
        else:
            repo = AptDebRepo(config=config, arch=arch)
        if repo.id in self._apt_repos:
            return False

        self._apt_repos[repo.id] = repo
        return True

    def _get_repo_signing_key(self, repo: AptRepo) -> Path | None:
        """
        Get the signing key of the repo.

        :param repo: Repository.
        :returns: Signing key path or None.
        """
        pub_key: Path | None = None
        if repo.key:
            key = str(repo.key)
            if key.startswith("http://") or key.startswith("https://"):
                pub_key = self._downloader.download_file(key)
            else:
                pub_key = Path(repo.key)
        return pub_key

    def _check_needs_update(self, repo: AptRepo) -> tuple[bool, Release]:
        """
        Check if the repo metadata needs to be updated.

        :param repo: Repository.
        :returns: True if the repo metadata needs and update.
        """
        inrelease_data = self._downloader.download(repo.in_release_url, bypass_cache=True)
        inrelease_content = inrelease_data.decode(encoding="utf-8")
        pub_key = self._get_repo_signing_key(repo)

        if pub_key:
            logging.debug("Using key %s for repo %s.", pub_key, repo)
            content = verify_signature(inrelease_content, pub_key)
        else:
            # Skip signature check.
            logging.warning("The repository %s has no key. Signature check is skipped.", repo)
            content = strip_signature(inrelease_content)

        data = stanza_to_dict(content.split("\n"))
        release = Release(base_url=repo.url, repo=repo.apt_config, **data)

        if repo.id in self._repo_metadata and self._repo_metadata[repo.id].Date == release.Date:
            # No update needed
            logging.debug("No update needed for repo %s.", repo)
            return (False, release)

        self._repo_metadata[repo.id] = release

        return (True, release)

    def _verify_package_index_hash(self, data: bytes, hash: str, algo: str) -> bool:
        """
        Verify that the hash of the data matches.

        :param data: Data for hash calculation.
        :param hash: Hash string to compare with.
        :param algo: Hash algorithm.
        :returns: True if the hash matches.
        """
        algos = {
            "MD5Sum": hashlib.md5,
            "SHA1": hashlib.sha1,
            "SHA256": hashlib.sha256,
            "SHA512": hashlib.sha512,
        }
        data_hash = algos[algo](data).hexdigest()
        return data_hash == str(hash)

    def _download_package_index(self, urls: list[str], release: Release) -> str | None:
        content = None
        for url in urls:
            try:
                data = self._downloader.download(url)

                res = _get_package_index_hash(url, release)
                if res:
                    (hash, algo) = res
                    if not self._verify_package_index_hash(data, hash, algo):
                        logging.error("Hash mismatch for URL %s, hash %s and algorithm %s!", url, hash, algo)
                        continue
                else:
                    logging.error("No hash found for URL %s! Skipping data verification.", url)

                if url.endswith(".xz"):
                    data = lzma.decompress(data)
                elif url.endswith(".gz"):
                    data = gzip.decompress(data)
                else:
                    # Assume uncompressed index
                    data = data

                content = data.decode(encoding="utf-8")
            except DownloadFailed:
                continue
            except UnicodeDecodeError as e:  # pragma: no cover
                logging.error("%s\nDecoding of content of URL %s failed!", e, url)
                continue
            break
        return content

    def _get_component_pool(
        self, pkg_urls: list[str], src_urls: list[str], release: Release, component: str | None
    ) -> ComponentPool:
        package_content = self._download_package_index(pkg_urls, release=release)
        packages = []
        if not package_content:
            logging.error("Download of package index for urls %s failed!", pkg_urls)
        else:
            stanzas = stanzas_to_list(package_content)
            packages = [
                Package(base_url=release.base_url, repo=release.repo, component=component, **stanza)
                for stanza in stanzas
            ]

        source_content = self._download_package_index(src_urls, release=release)
        sources = []
        if not source_content:
            logging.error("Download of source package index for urls %s failed!", src_urls)
        else:
            stanzas = stanzas_to_list(source_content)
            sources = [
                Source(base_url=release.base_url, repo=release.repo, component=component, **stanza)
                for stanza in stanzas
            ]

        return ComponentPool(packages, sources)

    def _update_package_indices(self, repo: AptRepo, release: Release) -> None:
        """
        Update the packages and sources of the given repository.

        :param repo: Repository.
        :param release: Apt repository InRelease metadata.
        """
        if repo.id not in self._pools:  # pragma: no branch
            self._pools[repo.id] = RepoPool()

        if isinstance(repo, AptFlatRepo):
            cmp_pool = self._get_component_pool(
                repo.packages_urls(), repo.source_urls(), release=release, component=None
            )
            self._pools[repo.id]._update_component(None, cmp_pool)
        else:
            assert isinstance(repo, AptDebRepo)
            for cmp in repo.components:
                cmp_pool = self._get_component_pool(
                    repo.packages_urls(cmp), repo.source_urls(cmp), release=release, component=cmp
                )
                self._pools[repo.id]._update_component(cmp, cmp_pool)

    def update(self) -> None:
        """Update apt repository metadata."""
        for repo in self._apt_repos.values():
            (needs_update, release) = self._check_needs_update(repo)
            if needs_update:
                self._update_package_indices(repo, release)

    def find_binary_package(
        self, package: str, version: DebianVersion | None = None, relation: str | None = None, arch: str | None = None
    ) -> list[Package]:
        """
        Search for a matching binary package.

        :param package: Name of the package.
        :param version: Version of the package.
        :param relation: Version relation for comparison.
        :param arch: Architecture of the package.
        :returns: List of matching packages. The newest package is the first element of the list.
        """
        packages: list[Package] = []
        for pool in self._pools.values():
            pkgs = pool.find_binary_package(package, version, relation, arch)
            packages.extend(pkgs)

        packages.sort(key=lambda package: package.Version, reverse=True)

        return packages

    def find_source_package(
        self, package: str, version: DebianVersion | None = None, relation: str | None = None, arch: str | None = None
    ) -> list[Source]:
        """
        Search for matching source package.

        :param package: Name of the package.
        :param version: Version of the package.
        :param relation: Version relation for comparison.
        :param arch: Architecture of the package.
        :returns: List of matching source packages. The newest source package is the first element of the list.
        """
        sources: list[Source] = []
        for pool in self._pools.values():
            srcs = pool.find_source_package(package, version, relation, arch)
            sources.extend(srcs)

        sources.sort(key=lambda source: source.Version)

        return sources
