from itertools import chain
import sqlite3


class LoadExtensionError(sqlite3.Error):
    pass


class SpatialMetadata(object):

    TABLES = (
        'ElementaryGeometries',
        'SpatialIndex',
        'geometry_columns',
        'geometry_columns_auth',
        'geometry_columns_field_infos',
        'geometry_columns_statistics',
        'geometry_columns_time',
        'spatial_ref_sys',
        'spatial_ref_sys_aux',
        'spatialite_history',
        'sql_statements_log',
        'views_geometry_columns',
        'views_geometry_columns_auth',
        'views_geometry_columns_field_infos',
        'views_geometry_columns_statistics',
        'virts_geometry_columns',
        'virts_geometry_columns_auth',
        'virts_geometry_columns_field_infos',
        'virts_geometry_columns_statistics',
    )

    VIEWS = (
        'geom_cols_ref_sys',
        'spatial_ref_sys_all',
        'vector_layers',
        'vector_layers_auth',
        'vector_layers_field_infos',
        'vector_layers_statistics',
    )

    def __init__(self, connection):
        self.db = connection

    def initialize(self):
        """Create and populate SpatiaLite metadata tables."""
        self.db.transaction('SELECT InitSpatialMetadata()', level='EXCLUSIVE')

    def drop(self, auto_vacuum=True):
        self.db.transaction(
            '; '.join(chain(
                ('DROP VIEW IF EXISTS %s' % t for t in self.VIEWS),
                ('DROP TABLE IF EXISTS %s' % t for t in self.TABLES),
            )),
            level='EXCLUSIVE',
        )
        if auto_vacuum:
            self.db.execute('VACUUM;')

    def recover(self, table, column):
        query = (
            "SELECT InitSpatialMetadata();"
            "SELECT RecoverGeometryColumn('%s', '%s', 4326, 'POINT');"
        )
        query %= (table, column)
        self.db.transaction(query, level='EXCLUSIVE')


class Connection(sqlite3.Connection):

    EXT_NAMES = (
        'mod_spatialite',  # Ubuntu
        'mod_spatialite.so',  # Ubuntu
        'mod_spatialite.dylib',  # macOS
    )

    def __init__(self, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)
        self.enable_spatialite_extension()
        self._metadata = SpatialMetadata(self)

    def enable_spatialite_extension(self):
        # requires mod_spatialite
        # Ubuntu: $ apt-get install libsqlite3-mod-spatialite
        # macOS: $ brew install libspatialite
        try:
            self.enable_load_extension(True)
        except AttributeError:
            pass

        error = None

        for ext_name in self.EXT_NAMES:
            try:
                self.execute("SELECT load_extension('%s')" % ext_name)
                return
            except sqlite3.OperationalError as e:
                error = e

        msg = (
            'Failed to load SpatiaLite extension. '
            'Verify that your python module sqlite3 has load_extension '
            'support and check that libspatialite is installed. '
            'Tried extension names: %s' % ', '.join(self.EXT_NAMES)
        )
        raise LoadExtensionError(msg) from error

    def transaction(self, query, level='DEFERRED'):
        query = "BEGIN %s TRANSACTION; %s; COMMIT TRANSACTION;" % (
            level, query)
        self.executescript(query)

    def initialize_metadata(self):
        """Create and populate SpatiaLite metadata tables."""
        self._metadata.initialize()


def connect(*args, **kwargs):
    kwargs['factory'] = Connection
    return sqlite3.connect(*args, **kwargs)


def get_spatialite_version():
    with connect(':memory:') as db:
        return db.execute('SELECT spatialite_version()').fetchone()[0]
