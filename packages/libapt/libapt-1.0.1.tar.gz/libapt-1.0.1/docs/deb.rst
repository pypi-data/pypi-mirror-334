Deb module
==========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. automodule:: libapt.deb

Provided functions
------------------

.. autofunction:: libapt.deb.load_packages

.. autofunction:: libapt.deb.load_sources

.. autofunction:: libapt.deb.extract_deb

.. autofunction:: libapt.deb.extract_deb_data

.. autofunction:: libapt.deb.extract_deb_meta

Dataclasses
-----------

.. autoclass:: libapt.deb.DebMetadata
   :members:

Debian metadata representation
------------------------------

.. autoclass:: libapt.deb.Package
   :members:

.. autoclass:: libapt.deb.Source
   :members:

.. autoclass:: libapt.deb.Person
   :members:

.. autoclass:: libapt.deb.PackageDependency
   :members:

.. autoclass:: libapt.deb.PackageListEntry
   :members:


Internal support functions
--------------------------

.. autofunction:: libapt.deb._parse_version

.. autofunction:: libapt.deb._parse_dependencies

.. autofunction:: libapt.deb._parse_person

.. autofunction:: libapt.deb._extract_zst

Exceptions
----------

.. autoclass:: libapt.deb.InvalidPackageMetadata
   :members: