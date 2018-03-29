import sqlite3


class Connection(sqlite3.Connection):

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self.enable_spatialite_extension()

    def enable_spatialite_extension(self):
        # requires mod_spatialite.so
        # Ubuntu: $ apt install libsqlite3-mod-spatialite
        self.execute("SELECT load_extension('mod_spatialite')")

    def transaction(self, query, level='DEFERRED'):
        query = "BEGIN %s TRANSACTION; %s; COMMIT TRANSACTION;" % (
            level, query)
        self.executescript(query)

    def initialize_metadata(self):
        """Create and populate SpatiaLite metadata tables."""
        self.transaction('SELECT InitSpatialMetadata()', level='IMMEDIATE')


def connect(*args, **kwargs):
    kwargs['factory'] = Connection
    return sqlite3.connect(*args, **kwargs)
