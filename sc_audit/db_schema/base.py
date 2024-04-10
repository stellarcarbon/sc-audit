from typing import Annotated, Any

from sqlalchemy import Dialect
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
        return value.hex()


intpk = Annotated[int, mapped_column(primary_key=True)]
hashpk = Annotated[bytes, mapped_column(HexBinary(length=32), primary_key=True)]


class ScBase(MappedAsDataclass, DeclarativeBase):
    pass
