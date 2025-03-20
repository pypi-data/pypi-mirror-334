"""Tests for APT repo generator."""

import os
import shutil

from pathlib import Path

from libapt.generator import generate_repo_metadata, RepositoryMetadata
from libapt.signature import verify_signature, strip_signature, generate_key
from libapt.deb import load_packages, load_sources


test_data = Path(__file__).parent / "data"


class TestGenerator:
    """Tests for generator."""

    def test_generate_repo(self, tmp_path) -> None:
        """Test the apt repo generator."""
        pool_folder = tmp_path / "pool"
        os.makedirs(pool_folder, exist_ok=True)
        shutil.copy(test_data / "bash_5.2.15-2+b7_amd64.deb", pool_folder)
        shutil.copy(test_data / "accountsservice_22.07.5-2ubuntu1.5_amd64.deb", pool_folder)
        shutil.copy(test_data / "abseil_20220623.1-3.1ubuntu3.dsc", pool_folder)

        meta = RepositoryMetadata(
            suite="local",
            version="1.0",
            packages_folder=tmp_path / "pool",
            base_folder=tmp_path,
        )
        repo = generate_repo_metadata(metadata=meta, base_url="http://localhost")

        assert repo.apt_repo == "http://localhost"
        assert repo.arch == "amd64"
        assert repo.components == {"main"}
        assert repo.distro == "local"
        assert repo.key is not None
        assert os.path.isfile(repo.key)

        inrelease = tmp_path / "dists" / repo.distro / "InRelease"
        assert os.path.isfile(inrelease)

        with open(inrelease, "r", encoding="utf-8") as f:
            inrelease_content = f.read()

        assert "Packages.xz" in inrelease_content
        assert "Packages.gz" in inrelease_content
        assert "Packages" in inrelease_content
        assert "Sources.xz" in inrelease_content
        assert "Sources.gz" in inrelease_content
        assert "Sources" in inrelease_content

        verify_signature(inrelease_content, Path(repo.key))

        assert os.path.isfile(tmp_path / "dists" / repo.distro / "main" / "binary-amd64" / "Packages.xz")
        assert os.path.isfile(tmp_path / "dists" / repo.distro / "main" / "binary-amd64" / "Packages.gz")

        package_index = tmp_path / "dists" / repo.distro / "main" / "binary-amd64" / "Packages"

        assert os.path.isfile(package_index)

        with open(package_index, "r", encoding="utf-8") as f:
            package_index_content = f.read()

        pkgs = load_packages(package_index_content, base_url="http://localhost")
        assert len(pkgs) == 2
        assert pkgs[0].Package == "accountsservice"
        assert pkgs[1].Package == "bash"

        assert os.path.isfile(tmp_path / "dists" / repo.distro / "main" / "source" / "Sources.xz")
        assert os.path.isfile(tmp_path / "dists" / repo.distro / "main" / "source" / "Sources.gz")

        source_index = tmp_path / "dists" / repo.distro / "main" / "source" / "Sources"

        assert os.path.isfile(source_index)

        with open(source_index, "r", encoding="utf-8") as f:
            source_index_content = f.read()

        srcs = load_sources(source_index_content, base_url="http://localhost")
        assert len(srcs) == 1
        assert srcs[0].Package == "abseil"

    def test_generate_repo_unsigned_source(self, tmp_path) -> None:
        """Test the apt repo generator."""
        pool_folder = tmp_path / "pool"
        os.makedirs(pool_folder, exist_ok=True)

        with open(test_data / "abseil_20220623.1-3.1ubuntu3.dsc", "r", encoding="utf-8") as f:
            content = f.read()
            content = strip_signature(content)
            with open(pool_folder / "abseil_20220623.1-3.1ubuntu3.dsc", "w", encoding="utf-8") as f:
                f.write(content)

        meta = RepositoryMetadata(
            suite="myrepo",
            version="1.0",
            packages_folder=tmp_path / "pool",
            base_folder=tmp_path,
        )
        repo = generate_repo_metadata(metadata=meta, base_url="http://localhost")

        assert repo.distro == "myrepo"

        assert os.path.isfile(tmp_path / "dists" / repo.distro / "main" / "source" / "Sources.xz")
        assert os.path.isfile(tmp_path / "dists" / repo.distro / "main" / "source" / "Sources.gz")

        source_index = tmp_path / "dists" / repo.distro / "main" / "source" / "Sources"

        assert os.path.isfile(source_index)

        with open(source_index, "r", encoding="utf-8") as f:
            source_index_content = f.read()

        srcs = load_sources(source_index_content, base_url="http://localhost")
        assert len(srcs) == 1
        assert srcs[0].Package == "abseil"

    def test_generate_repo_own_key(self, tmp_path) -> None:
        """Test the apt repo generator."""
        pool_folder = tmp_path / "pool"
        os.makedirs(pool_folder, exist_ok=True)
        shutil.copy(test_data / "accountsservice_22.07.5-2ubuntu1.5_amd64.deb", pool_folder)
        shutil.copy(test_data / "abseil_20220623.1-3.1ubuntu3.dsc", pool_folder)

        import getpass

        user = getpass.getuser()
        (priv, pub) = generate_key(owner=user, owner_mail=f"{user}@localhost", folder=tmp_path)

        meta = RepositoryMetadata(
            suite="local",
            version="1.0",
            packages_folder=tmp_path / "pool",
            base_folder=tmp_path,
            private_key=priv,
            public_key=pub,
        )
        repo = generate_repo_metadata(metadata=meta, base_url="http://localhost")

        assert repo.apt_repo == "http://localhost"
        assert repo.arch == "amd64"
        assert repo.components == {"main"}
        assert repo.distro == "local"
        assert repo.key == pub

        inrelease = tmp_path / "dists" / repo.distro / "InRelease"
        assert os.path.isfile(inrelease)

        with open(inrelease, "r", encoding="utf-8") as f:
            inrelease_content = f.read()

        verify_signature(inrelease_content, pub)
