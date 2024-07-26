"""
DB connection management.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sc_audit.config import settings
from sc_audit.db_schema.base import create_test_mappers

print(f"Connecting to database {settings.DBAPI_URL}...", file=sys.stderr)
engine = create_engine(settings.DBAPI_URL)
Session = sessionmaker(engine)

# create test mappers after all models have been registered
# TODO: this only needs to happen when running alembic; it would be nice to check
create_test_mappers()
