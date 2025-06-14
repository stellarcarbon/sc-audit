"""
DB connection management.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import sys

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import sessionmaker

from sc_audit.config import settings

print(f"Connecting to database {settings.DBAPI_URL}...", file=sys.stderr)

db_url = make_url(settings.DBAPI_URL)
connect_args = {}

if db_url.get_backend_name() == "sqlite":
    connect_args["check_same_thread"] = False

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

engine = create_engine(settings.DBAPI_URL, connect_args=connect_args)
Session = sessionmaker(engine)
