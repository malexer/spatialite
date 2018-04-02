from .connection import Connection, connect, get_spatialite_version
from .version import __version__


__all__ = (
    'connect',
    'Connection',
)


version = __version__
spatialite_version = get_spatialite_version()
