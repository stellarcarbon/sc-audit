from typing import Annotated

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


intpk = Annotated[int, mapped_column(primary_key=True)]
hashpk = Annotated[bytes, mapped_column(primary_key=True)]


class ScBase(MappedAsDataclass, DeclarativeBase):
    pass
