__all__ = ('celery_app',)

import sys

# Override sqlite3 with pysqlite3 to support newer Django versions on older systems
try:
    import pysqlite3
    sys.modules["sqlite3"] = pysqlite3
except ImportError:
    pass
