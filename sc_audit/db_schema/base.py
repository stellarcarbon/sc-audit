"""
SQLAlchemy Declarative Dataclass setup.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from dataclasses import fields
from decimal import Decimal
from typing import Annotated, Type

from sqlalchemy import Dialect, MetaData, String
import sqlalchemy.types as types
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from sc_audit.config import settings


class HexBinary(types.TypeDecorator):
    """
    Converts between fixed-length bytes and their hexadecimal string representations.
    """
    impl = types.LargeBinary
    cache_ok = True

    def process_bind_param(self, value: str, dialect: Dialect) -> bytes:
        return bytes.fromhex(value)
    
    def process_result_value(self, value: bytes, dialect: Dialect) -> str:
        if value is None:
            # this can happen during joins or eager loading
            return ""
        
        return value.hex()


intpk = Annotated[int, mapped_column(primary_key=True)]
hashpk = Annotated[str, mapped_column(HexBinary(length=32), primary_key=True)]
strkey = Annotated[str, mapped_column(String(56))]
kgdecimal = Annotated[Decimal, mapped_column(types.DECIMAL(precision=21, scale=3))]
stroopdecimal = Annotated[Decimal, mapped_column(types.DECIMAL(precision=21, scale=7))]
bigint = Annotated[int, mapped_column(types.BigInteger())]


class ScBase(MappedAsDataclass, DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "idx_%(column_0_name)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "%(table_name)s_%(column_0_name)s_fkey",
        "pk": "pk_%(table_name)s"
    })

    def __init_subclass__(cls) -> None:
        prefix_tables_and_foreign_keys(cls)
        super().__init_subclass__()


def prefix_tables_and_foreign_keys(subclass: Type[DeclarativeBase]):
    if settings.TABLE_PREFIX:
        assert issubclass(subclass, MappedAsDataclass)
        # Check if the prefix has already been applied
        # unless the class is a test mapper class
        if (
            subclass.__name__.startswith('Test') 
            or not subclass.__tablename__.startswith(settings.TABLE_PREFIX)
        ):
            # Prefix the table name
            subclass.__tablename__ = f"{settings.TABLE_PREFIX}_{subclass.__tablename__}"

            for dfield in fields(subclass):
                field = getattr(subclass, dfield.name, None)
                if field and hasattr(field, 'foreign_keys'):
                    # Prefix all foreign key column references
                    for fk in field.foreign_keys:
                        if not fk._colspec.startswith(settings.TABLE_PREFIX):
                            fk._colspec = f"{settings.TABLE_PREFIX}_{fk._colspec}"
                        if fk.name and not fk.name.startswith(settings.TABLE_PREFIX):
                            fk.name = f"{settings.TABLE_PREFIX}_{fk.name}"


def create_test_mappers(base_class: Type[DeclarativeBase]):
    """
    Create testnet versions of all registered models.
    These mappers are not needed at runtime, but they must exist when generating migrations.
    """
    models = [
        mapper.class_
        for mapper in base_class.registry.mappers
    ]
    # TODO: generate indexes for test tables
    settings.TABLE_PREFIX = "test"
    for model in models:
        type(
            f'Test{model.__name__}', 
            model.__bases__, 
            {"__tablename__": model.__tablename__}
        )
