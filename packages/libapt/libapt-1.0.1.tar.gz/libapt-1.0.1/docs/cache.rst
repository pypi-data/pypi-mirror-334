Cache module
============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. automodule:: libapt.cache

The Cache interface is used by the `libapt.download.DefaultDownloader`,
and you can bring your own implementation fitting your infrastructure needs.

.. autoclass:: libapt.cache.Cache
   :members:

If you have no special needs, you can make use of the `DefaultCache`.

.. autoclass:: libapt.cache.DefaultCache
   :members:
