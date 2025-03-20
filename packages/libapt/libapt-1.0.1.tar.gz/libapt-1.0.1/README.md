# libapt

Libapt provides a cross-platform pure Python interface for interacting with
Debian APT repositories.

Libapt allows parsing the metadata of an apt repository, see libapt.pool.Pool.update.

When the metadata was downloaded and parsed, you can:

- List all Debian binary and source packages.
- Search for a Debian binary and source packages.
- Download the binary and source packages.
- Extract the metadata form Debian binary packages.
- Extract the content of Debian binary packages.

The primary API is Pool from libapt.pool.

The primary data structure for configuring APT repositories is AptConfig from libapt.apt.

For more details see docs/index.rst or https://elische.github.io/libapt/.

## Example

The folder `example` contains an example app using libapt.

Try the example:

- Setup [uv](https://github.com/astral-sh/uv)
- Run the example: `uv run python example/main.py`

## Contribute

This library makes use of [uv](https://github.com/astral-sh/uv) and [ruff](https://github.com/astral-sh/ruff).

Use the following steps to prepare your development environment:

- Prepare a virtual environment and install development dependencies: `uv sync`
- Activate the virtual environment: `source .venv/bin/activate`

Please test your changes locally before raising and PR using `./test.sh all`
