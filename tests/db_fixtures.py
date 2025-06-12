import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, close_all_sessions

from sc_audit.db_schema.base import ScBase

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)


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
