from logging.config import fileConfig
from typing import Literal

from alembic import context
import sqlalchemy.types as types

from sc_audit.constants import DBAPI_URL
from sc_audit.db_schema.base import HexBinary, ScBase
from sc_audit import session_manager

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = ScBase.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def render_item(type_, obj, autogen_context) -> str | Literal[False]:
    """Apply custom rendering for selected items."""

    if type_ == 'type' and isinstance(obj, HexBinary):
        # add import for this type
        autogen_context.imports.add("from sc_audit.db_schema.base import HexBinary")
        return f"{obj!r}"

    # default rendering for other objects
    return False


def my_compare_type(context, inspected_column,
            metadata_column, inspected_type, metadata_type) -> None | bool:
    """
    Return False if the metadata_type is the same as the inspected_type or None to allow the 
    default implementation to compare these types. A return value of True means the two types do 
    not match and should result in a type change operation.
    """
    if isinstance(metadata_type, HexBinary):
        if (
            isinstance(inspected_type, types.BINARY) 
            and inspected_type.length == metadata_type.length
        ):
            return False
        elif (
            isinstance(inspected_type, types.NUMERIC) 
            and inspected_type.precision == metadata_type.length
        ):
            return False
        else:
            return True

    return None


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = DBAPI_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_item=render_item,
        compare_type=my_compare_type,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = session_manager.engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata, 
            render_item=render_item,
            compare_type=my_compare_type,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
