"""
DB connection management.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sc_audit.constants import DBAPI_URL

print(f"Connecting to database {DBAPI_URL}...")
engine = create_engine(DBAPI_URL)
Session = sessionmaker(engine)
