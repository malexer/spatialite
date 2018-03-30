import sqlite3


class LoadExtensionError(sqlite3.Error):
    pass


class Connection(sqlite3.Connection):

    EXT_NAMES = (
        'mod_spatialite',
        'mod_spatialite.dylib',  # macOS
    )

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self.enable_spatialite_extension()

    def enable_load_extension(self, enabled):
        try:
            super(Connection, self).enable_load_extension(enabled)
        except AttributeError:
            pass

    def enable_spatialite_extension(self):
        # requires mod_spatialite.so
        # Ubuntu: $ apt-get install libsqlite3-mod-spatialite
        # macOS: $ brew install libspatialite
        self.enable_load_extension(True)
        error = None

        for ext_name in self.EXT_NAMES:
            try:
                self.execute("SELECT load_extension('%s')" % ext_name)
                return
            except sqlite3.OperationalError as e:
                error = e

        msg = (
            'Failed to load SpatiaLite extension. '
            'Verify that your sqlite3 has load_extension support and '
            'check that libspatialite is installed. '
            'Tried extension names: %s' % ', '.join(self.EXT_NAMES)
        )
        raise LoadExtensionError(msg) from error

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
