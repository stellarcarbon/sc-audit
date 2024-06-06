"""
DB connection management.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sc_audit.constants import DBAPI_URL

print(f"Connecting to database {DBAPI_URL}...", file=sys.stderr)
engine = create_engine(DBAPI_URL)
Session = sessionmaker(engine)
