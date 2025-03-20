"""APT Repository metadata processing."""

from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path

from pydantic import BaseModel


class InvalidAptConfig(Exception):
    """Raised if a invalid apt repo configuration is given."""


class AptConfig(BaseModel):
    """
    Model for APT repository metadata.
    """

    apt_repo: str
    distro: Optional[str] = None
    components: Optional[set[str]] = None
    primary: Optional[bool] = None
    arch: Optional[str] = None
    key: Optional[Path | str] = None

    def get_id(self) -> str:
        """
        Generate and ID representing this configuration.

        :returns: Unique identifier for the APT repository.
        """
        if self.components:
            components = "-".join(self.components)
        else:
            components = ""
        return f"{self.apt_repo}_{self.distro}_{components}"

    def __repr__(self) -> str:
        return f"APT<url: {self.apt_repo}, distro: {self.distro}, components: {str(self.components)}>"


class AptRepo(ABC):
    """
    Base class for repository description.
    """

    PACKAGES_FILES = ["Packages.xz", "Packages.gz", "Packages"]
    SOURCES_FILES = ["Sources.xz", "Sources.gz", "Sources"]

    def __init__(self, config: AptConfig, arch: str) -> None:
        self._config: AptConfig = config
        if config.arch is not None:
            self._arch: str = config.arch
        else:
            self._arch = arch

    @property
    @abstractmethod
    def _meta_path(self) -> str:
        """
        Get path to the directory containing the metadata.

        :returns: Returns the path/url to the directory where the metadata files (InRelease) are located.
        """
        raise NotImplementedError()

    @property
    def id(self) -> str:
        """
        Get unique ID string for this apt repository.

        :returns: Returns a string that uniquely identified this repository.
        """
        return f"{self._config.apt_repo}_{self._get_id()}"

    @property
    def apt_config(self) -> AptConfig:
        """
        Get AptConfig for repository.

        :returns: AptConfig for repo.
        """
        return self._config

    @property
    def url(self) -> str:
        return self._config.apt_repo

    @property
    def arch(self) -> str:
        return self._arch

    @property
    def in_release_url(self) -> str:
        return f"{self._config.apt_repo}/{self._meta_path}InRelease"

    @property
    def key(self) -> str | Path | None:
        """
        URL or path to the public armored GPG key used for signing.

        :returns: URL or path to the GPG key.
        """
        return self._config.key

    @abstractmethod
    def apt_list_deb_entry(self, trusted: bool = False) -> str:
        """
        APT sources list entry for binary packages.

        :param trusted: If true, the apt signature check is disabled for the entry.
        :returns: Returns a string that can be used to define the repo in an apt sources list.
        """
        raise NotImplementedError()

    @abstractmethod
    def apt_list_deb_src_entry(self) -> str:
        """
        APT sources list entry for binary packages.

        :returns: Returns a string that can be used to define the source repo in an apt sources list.
        """
        raise NotImplementedError()

    @abstractmethod
    def _get_id(self) -> str:
        """Returns the repo id part specific for the derived repository type."""
        raise NotImplementedError()

    @abstractmethod
    def _get_repr(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def packages_urls(self, component: str) -> list[str]:
        """
        Get URLs for package index file.

        :param component: Name of the component.
        :returns: List of URLs to the package index of the given component.
        """
        raise NotImplementedError()

    @abstractmethod
    def source_urls(self, component: str) -> list[str]:
        """
        Get URLs for source index file.

        :param component: Name of the component.
        :returns: List of URLs to the source index of the given component.
        """
        raise NotImplementedError()

    def __repr__(self) -> str:
        return self._get_repr()

    def __str__(self) -> str:
        return repr(self)

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self._arch == other._arch and self._config == other._config

    def _apt_source_parameters(self, trusted: bool = False) -> str:
        """
        Get the deb binary apt flags for the apt sources list.

        :param trusted: Trust the repository, i.e. skip signature verification.
        :returns: Returns the parameters for the apt sources.list entry.
        """
        if trusted:
            return f"[arch={self.arch} trusted=yes]"
        else:
            return f"[arch={self.arch}]"


class AptFlatRepo(AptRepo):
    """
    Implementation of a flat apt repo.

    A flat repo has no distribution folder.
    See: https://wiki.debian.org/DebianRepository/Format#Flat_Repository_Format
    """

    def __init__(self, config: AptConfig, arch: str) -> None:
        super().__init__(config, arch)
        if config.distro is not None:
            raise InvalidAptConfig("Flat repositories does not support the distro parameter.")
        if config.components is not None:
            raise InvalidAptConfig("Flat repositories does not support components.")

    @property
    def _meta_path(self) -> str:
        return ""

    def apt_list_deb_entry(self, trusted: bool = False) -> str:
        """
        APT sources list entry for binary packages.

        :param trusted: If true, the apt signature check is disabled for the entry.
        :returns: Returns a string that can be used to define the repo in an apt sources list.
        """
        params = self._apt_source_parameters(trusted)
        return f"deb {params} {self._config.apt_repo} /"

    def apt_list_deb_src_entry(self) -> str:
        """
        APT sources list entry for binary packages.

        :returns: Returns a string that can be used to define the source repo in an apt sources list.
        """
        return f"deb-src {self._config.apt_repo} /"

    def _get_id(self) -> str:
        return self._config.get_id()

    def _get_repr(self) -> str:
        return f"AptFlatRepo<{self._config}>"

    def packages_urls(self, component: str = "") -> list[str]:
        """
        Get URLs for package index file.

        :param component: Name of the component.
        :returns: List of URLs to the package index of the given component.
        """
        urls = []
        for packages in self.PACKAGES_FILES:
            urls.append(f"{self._config.apt_repo}/{self._meta_path}{packages}")
        return urls

    def source_urls(self, component: str = "") -> list[str]:
        """
        Get URLs for source index file.

        :param component: Name of the component.
        :returns: List of URLs to the source index of the given component.
        """
        urls = []
        for sources in self.SOURCES_FILES:
            urls.append(f"{self._config.apt_repo}/{self._meta_path}{sources}")
        return urls


class AptDebRepo(AptRepo):
    """
    Implementation of a normal apt repo.

    See: https://wiki.debian.org/DebianRepository/Format#Debian_Repository_Format
    """

    def __init__(self, config: AptConfig, arch: str):
        super().__init__(config, arch)
        if config.distro is None:
            raise InvalidAptConfig("Deb repositories require the distro parameter.")
        if config.components is None:
            raise InvalidAptConfig("Deb repositories require components.")

    @property
    def _meta_path(self) -> str:
        return f"dists/{self._config.distro}/"

    @property
    def dist(self) -> str:
        assert self._config.distro is not None
        return self._config.distro

    @property
    def components(self) -> set[str]:
        assert self._config.components is not None
        return self._config.components

    def apt_list_deb_entry(self, trusted: bool = False) -> str:
        """
        APT sources list entry for binary packages.

        :param trusted: If true, the apt signature check is disabled for the entry.
        :returns: Returns a string that can be used to define the repo in an apt sources list.
        """
        assert self._config.components is not None
        params = super(AptDebRepo, self)._apt_source_parameters(trusted)
        return f"deb {params} {self._config.apt_repo} {self._config.distro} {' '.join(self._config.components)}"

    def apt_list_deb_src_entry(self) -> str:
        """
        APT sources list entry for binary packages.

        :returns: Returns a string that can be used to define the source repo in an apt sources list.
        """
        assert self._config.components is not None
        return f"deb-src {self._config.apt_repo} {self._config.distro} {' '.join(self._config.components)}"

    def _get_id(self) -> str:
        assert self._config.components is not None
        return f"{self._config.distro}_{'_'.join(self._config.components)}"

    def _get_repr(self) -> str:
        return f"AptDebRepo<{self._config}>"

    def packages_urls(self, component: str) -> list[str]:
        """
        Get URLs for package index file.

        :param component: Name of the component.
        :returns: List of URLs to the package index of the given component.
        """
        urls = []
        for packages in self.PACKAGES_FILES:
            urls.append(f"{self._config.apt_repo}/{self._meta_path}{component}/binary-{self.arch}/{packages}")
        return urls

    def source_urls(self, component: str) -> list[str]:
        """
        Get URLs for source index file.

        :param component: Name of the component.
        :returns: List of URLs to the source index of the given component.
        """
        urls = []
        for sources in self.SOURCES_FILES:
            urls.append(f"{self._config.apt_repo}/{self._meta_path}{component}/source/{sources}")
        return urls
