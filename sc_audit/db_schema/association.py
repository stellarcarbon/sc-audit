from __future__ import annotations
import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sc_audit.db_schema.base import ScBase, intpk, hashpk

if typing.TYPE_CHECKING:
    from sc_audit.db_schema import MintedBlock, Retirement


class RetirementFromBlock(ScBase):
    __tablename__ = "retirement_from_block"

    retirement_id: Mapped[intpk] = mapped_column(ForeignKey('retirements.certificate_id'))
    block_hash: Mapped[hashpk] = mapped_column(ForeignKey('minted_blocks.serial_hash'))
    vcu_amount: Mapped[int]

    retirement: Mapped[Retirement] = relationship(
        init=False, repr=False,
        back_populates='retired_from'
    )
    block: Mapped[MintedBlock] = relationship(
        init=False, repr=False, 
        back_populates='consumed_by'
    )
