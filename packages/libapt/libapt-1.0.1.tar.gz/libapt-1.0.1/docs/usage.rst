Usage
=====

Libapt allows interacting with Debian APT repositories.

First you need to specify the APT repository to use.
This can be done by using libyamlconf for loading a yaml file, as done in the example,
or in code, by creating an AptConfig object:

.. autoclass:: libapt.apt.AptConfig
    :no-index:

The `apt_repo` is the base url of the APT repository, e.g. http://ports.ubuntu.com/ubuntu-ports.
If the signature of the repository shall be verified, a the public key needs to be provided as `key`.
The `key` can be a file path or an URL.
In case of a flat repo this information is already enough.
For proper Debian APT repository, the `distro` needs to be provided. This can be e.g. jammy.
The components are a list of component names to parse, e.g. ["main", "universe"].
If multiple repositories are given, the primary repo flag can be used to mark the repository
which shall be used for `debootstrap`.


.. highlight:: python
.. code-block:: python

    from libapt.apt import AptConfig

    config = AptConfig(
        apt_repo="http://ports.ubuntu.com/ubuntu-ports",
        distro="jammy",
        components={"main"},
        key="/etc/apt/trusted.gpg.d/ubuntu-keyring-2018-archive.gpg"
    )

Using this config, we can create a `Pool`, which is the main API if libapt:

.. autoclass:: libapt.pool.Pool
    :no-index:

The pool requires a download, and the downloader can optionally make use of a cache:


.. autoclass:: libapt.download.Downloader
    :no-index:

.. autoclass:: libapt.cache.Cache
    :no-index:

The Downloader and the Cache are abstract base classes.
You can bring your own implementations for the Downloader and the Cache,
or you make use of the provided default implementations:

.. autoclass:: libapt.download.DefaultDownloader
    :no-index:

.. autoclass:: libapt.cache.DefaultCache
    :no-index:

Let's use the provided defaults:

.. highlight:: python
.. code-block:: python

    from libapt.cache import DefaultCache
    from libapt.download import DefaultDownloader
    from libapt.pool import Pool

    downloader = DefaultDownloader(cache=DefaultCache())
    pool = Pool(downloader=downloader)
    pool.add_repository(config=config, arch="arm64")

Now, we can load and parse the metadata:

.. highlight:: python
.. code-block:: python

    pool.update()

All found packages are now available as `pool.packages`,
and all found sources are now available as `pool.sources`.

We can also search for packages and sources using:

.. autofunction:: libapt.pool.Pool.find_binary_package
    :no-index:

.. autofunction:: libapt.pool.Pool.find_source_package
    :no-index:

We can also download Debian binary and source packages using the `download`
methods of `Package` and `Source`.

.. autoclass:: libapt.deb.Package
    :no-index:

.. autofunction:: libapt.deb.Package.download
    :no-index:

.. autoclass:: libapt.deb.Source
    :no-index:

.. autofunction:: libapt.deb.Source.download
    :no-index:

Let's download all versions of the `busybox-static` package
and the corresponding source packages:

.. highlight:: python
.. code-block:: python

    import os
    from pathlib import Path

    # Create a temporary folder
    local_repo = Path(tempfile.mkdtemp())
    pool_dir = local_repo / "pool"
    os.makedirs(pool_dir, exist_ok=True)

    # Download all versions of the busybox-static package
    for pkg in pool.find_binary_package(package="busybox-static"):
        deb = pkg.download(downloader=downloader, folder=pool_dir)
        if deb and os.path.isfile(deb):
            print(f"Downloaded deb: {deb}")
        else:
            print(f"Downloaded of package {pkg.Package} ({pkg.Version}) failed!")

    # Download all busybox source packages.
    for src in pool.find_source_package(package="busybox"):
        dsc = src.download(downloader=downloader, folder=pool_dir)
        if dsc and os.path.isfile(dsc):
            print(f"Downloaded source: {dsc}")
        else:
            print(f"Downloaded of source {src.Package} ({src.Version}) failed!")

Using this download packages, we can create our own local Debian APT repository, by using:

.. autofunction:: libapt.generator.generate_repo_metadata
    :no-index:

.. autoclass:: libapt.generator.RepositoryMetadata
    :no-index:


.. highlight:: python
.. code-block:: python

    from libapt.generator import generate_repo_metadata, RepositoryMetadata

    # Generate the repository metadata
    meta = RepositoryMetadata(suite="local", version="1.0", packages_folder=pool_dir, base_folder=local_repo)
    local_repo_config = generate_repo_metadata(meta, "http://localhost:8124")
