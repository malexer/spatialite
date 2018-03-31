spatialite
==========

Wrapper for standard Python module `sqlite3` which adds SpatiaLite support.


Requirement: mod_spatialite
---------------------------

This module will try to load SpatiaLite extension in SQLite and thus requires
"mod_spatialite" being present.

Ubuntu::

    $ apt-get install libsqlite3-mod-spatialite

macOS::

    $ brew install libspatialite


Install
-------

Using pip::

    $ pip install spatialite

Usage
-----

.. code-block:: python

    import spatialite


    with spatialite.connect('sl_temp.db') as db:
        print(db.execute('SELECT spatialite_version()').fetchone()[0])
