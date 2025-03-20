"""
Demo for using libapt.
"""

import time
import timeit
import tempfile
import os
import shutil
import multiprocessing

from pathlib import Path
import http.server

from pydantic import BaseModel
from libapt.apt import AptConfig
from libyamlconf.verify import load_and_verify  # type: ignore[import-untyped]
from libapt.pool import Pool
from libapt.download import DefaultDownloader
from libapt.cache import DefaultCache
from libapt.generator import generate_repo_metadata, RepositoryMetadata


local_repo = Path(tempfile.mkdtemp())


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=local_repo, **kwargs)


def run_http_server():
    """Serve the local apt repository."""
    port = 8124
    server_address = ("", port)
    httpd = http.server.HTTPServer(server_address, Handler)
    httpd.serve_forever()


def run_parallel_http_server() -> multiprocessing.Process:
    proc = multiprocessing.Process(target=run_http_server, args=())
    proc.start()
    return proc


class Config(BaseModel):
    """Config for testing"""

    arch: str
    apt_repos: list[AptConfig]


def main(local_repo: Path) -> None:
    """
    Example for interfacing with the Ubuntu Jammy apt repository.
    """
    # Load the configuration.
    config_file = Path(__file__).parent / "apt.yaml"
    config: Config = load_and_verify(file=config_file, model=Config, relative_path_keys=[["apt_repos", "key"]])

    # Prepare the package pool.
    downloader = DefaultDownloader(cache=DefaultCache())
    pool = Pool(downloader=downloader)
    for repo in config.apt_repos:
        pool.add_repository(config=repo, arch=config.arch)

    # Load the apt repository metadata.
    print("Loading the apt repository metadata...")
    start = time.time()
    pool.update()
    end = time.time()
    print("Loading the apt repository metadata took %.2f seconds." % (end - start))

    print(f"The configured repositories provide {len(pool.packages)} binary packages.")
    print(f"The configured repositories provide {len(pool.sources)} binary packages.")

    # Search for the busybox package
    pkgs = pool.find_binary_package(package="busybox-static")
    if pkgs:
        print(f"The repository provides busybox-static version {pkgs[0].Version}.")

        search = ["busybox-static", "zstd"]
        for name in search:
            print(f"Searching {name} 1000 times...")
            res = timeit.timeit(lambda: pool.find_binary_package(package=name), number=1000)
            print("Searching %s took in average %.2f ms" % (name, res * 1000))

    else:
        print("Busybox binary package not found!")

    # Search for the busybox source package
    srcs = pool.find_source_package(package="busybox")
    if srcs:
        print(f"The repository provided the busybox source package version {srcs[0].Version}.")
    else:
        print("Busybox binary package not found!")

    # Get all package versions
    print("The pool provides the following busybox-static versions:")
    for pkg in pool.find_binary_package(package="busybox-static"):
        print(f"{pkg.Package} {pkg.Version}")

    # Generate a apt repository
    pool_dir = local_repo / "pool"
    os.makedirs(pool_dir, exist_ok=True)

    # Download a few packages
    for pkg in pool.find_binary_package(package="busybox-static"):
        deb = pkg.download(downloader=downloader, folder=pool_dir)
        if deb and os.path.isfile(deb):
            print(f"Downloaded deb: {deb}")
        else:
            print(f"Downloaded of package {pkg.Package} ({pkg.Version}) failed!")

    # Download a few sources
    for src in pool.find_source_package(package="busybox"):
        dsc = src.download(downloader=downloader, folder=pool_dir)
        if dsc and os.path.isfile(dsc):
            print(f"Downloaded source: {dsc}")
        else:
            print(f"Downloaded of source {src.Package} ({src.Version}) failed!")

    # Generate the repository metadata
    meta = RepositoryMetadata(suite="local", version="1.0", packages_folder=pool_dir, base_folder=local_repo)
    local_repo_config = generate_repo_metadata(meta, "http://localhost:8124")

    # Serve the local repo.
    proc = run_parallel_http_server()
    # Give the server some time to start.
    time.sleep(1)

    # Create a pool for the local repo
    local_pool = Pool(downloader=downloader)
    local_pool.add_repository(local_repo_config, arch="amd64")
    local_pool.update()

    # Check the available packages
    print("Packages in local pool:")
    for pkg in local_pool.packages:
        print(f"{pkg.Package} ({pkg.Version})")
    print("Sources in local pool:")
    for src in local_pool.sources:
        print(f"{src.Package} ({src.Version})")

    proc.terminate()


if __name__ == "__main__":
    try:
        main(local_repo)
    except Exception as e:
        print(f"Demo failed! {e}")

    # Cleanup local repo
    print("Cleaning local repo...")
    shutil.rmtree(local_repo)
