"""
SQLAlchemy Declarative Dataclass setup.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from dataclasses import fields
from decimal import Decimal
from typing import Annotated

from sqlalchemy import Dialect, String
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

    def __init_subclass__(cls) -> None:
        if settings.TABLE_PREFIX:
            # Check if the prefix has already been applied
            if not cls.__tablename__.startswith(settings.TABLE_PREFIX):
                # Prefix the table name
                cls.__tablename__ = f"{settings.TABLE_PREFIX}_{cls.__tablename__}"

                for dfield in fields(cls):
                    field = getattr(cls, dfield.name, None)
                    if field and hasattr(field, 'foreign_keys'):
                        # Prefix all foreign key column references
                        for fk in field.foreign_keys:
                            if not fk._colspec.startswith(settings.TABLE_PREFIX):
                                fk._colspec = f"{settings.TABLE_PREFIX}_{fk._colspec}"

        super().__init_subclass__()


def create_test_mappers():
    """
    Create testnet versions of all registered models.
    These mappers are not needed at runtime, but they must exist when generating migrations.
    """
    models = [
        mapper.class_
        for mapper in ScBase.registry.mappers
    ]
    for model in models:
        type(
            f'Test{model.__name__}', 
            model.__bases__, 
            {"__tablename__": f"test_{model.__tablename__}"}
        )
