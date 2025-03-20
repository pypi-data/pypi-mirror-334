Download module
===============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. automodule:: libapt.download


The Download interface can be used to bring your own implementation
fitting your infrastructure needs.

.. autoclass:: libapt.download.Downloader
   :members:

If you have no special needs, you can make use of the `DefaultDownloader`.

.. autoclass:: libapt.download.DefaultDownloader
   :members: