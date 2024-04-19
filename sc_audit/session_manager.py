"""
DB connection management.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sc_audit.constants import DBAPI_URL
from sc_audit.db_schema.base import ScBase

print(f"Connecting to database {DBAPI_URL}...")
engine = create_engine(DBAPI_URL)
ScBase.metadata.create_all(engine)
Session = sessionmaker(engine)
