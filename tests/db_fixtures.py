import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, close_all_sessions

from sc_audit.db_schema.base import ScBase
from sc_audit.db_schema.impact_project import VcsProject

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

@pytest.fixture
def vcs_project() -> VcsProject:
    return VcsProject(
        id=1360, 
        name="Forest Management to reduce deforestation and degradation in Shipibo Conibo and Cacataibo Indigenous communities of Ucayali region", 
        category="Agriculture Forestry and Other Land Use", 
        protocol="VM0015", 
        additional_certifications="CCB-Gold", 
        region="Latin America", 
        country="Peru"
    )
