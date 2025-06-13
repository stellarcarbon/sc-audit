import pytest
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import sessionmaker, close_all_sessions

from sc_audit.db_schema.base import ScBase

connect_args = {"check_same_thread": False}
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, connect_args=connect_args)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture
def new_session():
    ScBase.metadata.create_all(engine)
    Session = sessionmaker(engine)

    yield Session

    close_all_sessions()
    ScBase.metadata.drop_all(engine)


@pytest.fixture
def connection():
    ScBase.metadata.create_all(engine)

    with engine.connect() as conn:
        yield conn

    ScBase.metadata.drop_all(engine)
