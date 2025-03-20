"""Tests for InRelease processing."""

from pathlib import Path

import pytest

from pydantic import BaseModel
from libyamlconf.verify import load_and_verify  # type: ignore[import-untyped]

from libapt.apt import AptConfig, AptFlatRepo, AptDebRepo, InvalidAptConfig

test_data = Path(__file__).parent / "data"


class Config(BaseModel):
    """Config for testing"""

    arch: str
    apt_repos: list[AptConfig]


class TestRelease:
    """Tests for InRelease processing."""

    def test_apt_metadata(self) -> None:
        """Test converting an APT stanza to a Python dict."""
        file = test_data / "apt.yaml"

        config: Config = load_and_verify(file, Config)
        apt_config = config.apt_repos[0]

        assert apt_config.apt_repo == "http://archive.ubuntu.com/ubuntu"
        assert apt_config.distro == "jammy"
        assert apt_config.components == {"main", "universe"}

    def test_apt_metadata_id(self) -> None:
        """Test the generated ID for the apt metadata."""
        file = test_data / "apt.yaml"

        config: Config = load_and_verify(file, Config)
        apt_config = config.apt_repos[0]

        assert apt_config.components is not None
        assert apt_config.get_id() == f"{apt_config.apt_repo}_{apt_config.distro}_{'-'.join(apt_config.components)}"

    def test_aptdebrepo(self) -> None:
        """Test the AptDebRepo initialization."""
        file = test_data / "apt.yaml"

        config: Config = load_and_verify(file, Config)
        apt_config = config.apt_repos[0]

        repo = AptDebRepo(apt_config, "amd64")

        assert repo.dist == "jammy"
        assert repo.arch == "amd64"
        assert repo.components == {"main", "universe"}
        assert repo.in_release_url == "http://archive.ubuntu.com/ubuntu/dists/jammy/InRelease"
        assert repo.id == f"{repo._config.apt_repo}_{repo._get_id()}"
        assert repo._get_id() == repo._get_id()
        assert repo._meta_path == f"dists/{apt_config.distro}/"
        assert repo.url == apt_config.apt_repo
        assert apt_config.components is not None
        assert (
            repo.apt_list_deb_entry(trusted=True)
            == f"deb [arch=amd64 trusted=yes] {apt_config.apt_repo} {apt_config.distro} {' '.join(apt_config.components)}"
        )
        assert (
            repo.apt_list_deb_entry(trusted=False)
            == f"deb [arch=amd64] {apt_config.apt_repo} {apt_config.distro} {' '.join(apt_config.components)}"
        )
        assert (
            repo.apt_list_deb_src_entry()
            == f"deb-src {apt_config.apt_repo} {apt_config.distro} {' '.join(apt_config.components)}"
        )
        assert repo.packages_urls("main") == [
            f"{apt_config.apt_repo}/dists/{apt_config.distro}/main/binary-amd64/Packages.xz",
            f"{apt_config.apt_repo}/dists/{apt_config.distro}/main/binary-amd64/Packages.gz",
            f"{apt_config.apt_repo}/dists/{apt_config.distro}/main/binary-amd64/Packages",
        ]
        assert repo.source_urls("main") == [
            f"{apt_config.apt_repo}/dists/{apt_config.distro}/main/source/Sources.xz",
            f"{apt_config.apt_repo}/dists/{apt_config.distro}/main/source/Sources.gz",
            f"{apt_config.apt_repo}/dists/{apt_config.distro}/main/source/Sources",
        ]
        assert repo.key is None
        assert repo._get_repr() == f"AptDebRepo<{apt_config}>"
        assert str(repo) == f"AptDebRepo<{apt_config}>"

    def test_aptdebrepo_no_dist(self) -> None:
        """AptDebRepo shall raise an InvalidAptConfig exception if distro is missing."""
        file = test_data / "apt_no_dist.yaml"

        config: Config = load_and_verify(file, Config)
        apt_config = config.apt_repos[0]

        with pytest.raises(InvalidAptConfig):
            AptDebRepo(apt_config, "amd64")

    def test_aptdebrepo_no_comp(self) -> None:
        """AptDebRepo shall raise an InvalidAptConfig exception if components are missing."""
        file = test_data / "apt_no_comp.yaml"

        config: Config = load_and_verify(file, Config)
        apt_config = config.apt_repos[0]

        with pytest.raises(InvalidAptConfig):
            AptDebRepo(apt_config, "amd64")

    def test_aptdebrepo_eq(self) -> None:
        """Test comparing aptdebrepos"""
        file = test_data / "apt.yaml"

        config: Config = load_and_verify(file, Config)
        apt_config = config.apt_repos[0]
        apt_config2 = config.apt_repos[1]

        repo1 = AptDebRepo(apt_config, "amd64")
        repo2 = AptDebRepo(apt_config2, "amd64")
        repo3 = AptDebRepo(apt_config, "arm64")

        assert repo1 == repo1
        assert repo2 == repo2
        assert repo3 == repo3
        assert repo1 != repo2
        assert repo1 != repo3

    def test_aptflatrepo(self) -> None:
        """Test the AptFlatRepo initialization."""
        file = test_data / "apt_flat.yaml"

        config: Config = load_and_verify(file, Config)
        apt_config = config.apt_repos[0]

        repo = AptFlatRepo(apt_config, "amd64")

        assert repo.arch == "amd64"
        assert repo.in_release_url == "http://archive.ubuntu.com/ubuntu/InRelease"
        assert repo.id == f"{repo._config.apt_repo}_{repo._get_id()}"
        assert repo._get_id() == repo._get_id()
        assert repo._meta_path == ""
        assert repo.url == apt_config.apt_repo
        assert repo.apt_list_deb_entry(trusted=True) == f"deb [arch=amd64 trusted=yes] {apt_config.apt_repo} /"
        assert repo.apt_list_deb_entry(trusted=False) == f"deb [arch=amd64] {apt_config.apt_repo} /"
        assert repo.apt_list_deb_src_entry() == f"deb-src {apt_config.apt_repo} /"
        assert repo.packages_urls() == [
            f"{apt_config.apt_repo}/Packages.xz",
            f"{apt_config.apt_repo}/Packages.gz",
            f"{apt_config.apt_repo}/Packages",
        ]
        assert repo.source_urls() == [
            f"{apt_config.apt_repo}/Sources.xz",
            f"{apt_config.apt_repo}/Sources.gz",
            f"{apt_config.apt_repo}/Sources",
        ]
        assert repo.key == "http://archive.ubuntu.com/ubuntu/key.pub"
        assert repo._get_repr() == f"AptFlatRepo<{apt_config}>"
        assert str(repo) == f"AptFlatRepo<{apt_config}>"

        apt_config = config.apt_repos[1]
        repo = AptFlatRepo(apt_config, "amd64")
        assert repo.arch == "arm64"

    def test_aptflatrepo_dist(self) -> None:
        """ApFlatRepo shall raise an InvalidAptConfig exception if distro is provided."""
        file = test_data / "apt_no_comp.yaml"

        config: Config = load_and_verify(file, Config)
        apt_config = config.apt_repos[0]

        with pytest.raises(InvalidAptConfig):
            AptFlatRepo(apt_config, "amd64")

    def test_aptflatrepo_comp(self) -> None:
        """AptFlatRepo shall raise an InvalidAptConfig exception if components are provided."""
        file = test_data / "apt_no_dist.yaml"

        config: Config = load_and_verify(file, Config)
        apt_config = config.apt_repos[0]

        with pytest.raises(InvalidAptConfig):
            AptFlatRepo(apt_config, "amd64")

    def test_aptflatrepo_eq(self) -> None:
        """Test comparing aptflatrepos"""
        file = test_data / "apt_flat.yaml"

        config: Config = load_and_verify(file, Config)
        apt_config = config.apt_repos[0]
        apt_config2 = config.apt_repos[1]

        repo1 = AptFlatRepo(apt_config, "amd64")
        repo2 = AptFlatRepo(apt_config2, "amd64")
        repo3 = AptFlatRepo(apt_config, "arm64")

        assert repo1 == repo1
        assert repo2 == repo2
        assert repo3 == repo3
        assert repo1 != repo2
        assert repo1 != repo3

    def test_compare_aptdebrepo_aptflatrepo(self) -> None:
        """Test comparing aptdebrepos"""
        file = test_data / "apt_flat.yaml"
        file2 = test_data / "apt.yaml"

        config: Config = load_and_verify(file, Config)
        config2: Config = load_and_verify(file2, Config)
        apt_config = config.apt_repos[0]
        apt_config2 = config2.apt_repos[0]

        repo1 = AptFlatRepo(apt_config, "amd64")
        repo2 = AptDebRepo(apt_config2, "amd64")

        assert repo1 != repo2
