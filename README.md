# spatialite

Wrapper for standard Python module `sqlite3` which adds SpatiaLite support.


## Requirement: mod_spatialite

This module will try to load SpatiaLite extension in SQLite and thus requires
"mod_spatialite" being present.

For Ubuntu:

    $ apt-get install libsqlite3-mod-spatialite


## Install

    $ pip install spatialite


## Usage

```python
import spatialite


with spatialite.connect('sl_temp.db') as db:
    print(db.execute('SELECT spatialite_version()').fetchone()[0])
```
