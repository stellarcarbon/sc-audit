"""
SQLAlchemy Declarative Dataclass setup.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from decimal import Decimal
from typing import Annotated

from sqlalchemy import Dialect, String
import sqlalchemy.types as types
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


class HexBinary(types.TypeDecorator):
    """
    Converts between fixed-length bytes and their hexadecimal string representations.
    """
    impl = types.BINARY
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


class ScBase(MappedAsDataclass, DeclarativeBase):
    pass
