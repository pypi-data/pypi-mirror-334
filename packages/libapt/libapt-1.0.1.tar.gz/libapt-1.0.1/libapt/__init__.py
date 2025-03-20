"""
Libapt provides a cross-platform pure Python interface for interacting with
Debian APT repositories.

Libapt allows parsing the metadata of an apt repository, see:

.. autofunction:: libapt.pool.Pool.update
    :no-index:

When the metadata was downloaded and parsed, you can:

- List all Debian binary and source packages.
- Search for a Debian binary and source packages.
- Download the binary and source packages.
- Extract the metadata form Debian binary packages.
- Extract the content of Debian binary packages.

The primary API is Pool from libapt.pool.

The primary data structure for configuring APT repositories is AptConfig from libapt.apt.
"""

__version__ = "1.0.1"
