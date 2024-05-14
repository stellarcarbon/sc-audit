from __future__ import annotations
from decimal import Decimal
import typing

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sc_audit.db_schema.base import ScBase, intpk, hashpk

if typing.TYPE_CHECKING:
    from sc_audit.db_schema import MintedBlock, Retirement, SinkingTx


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


class SinkStatus(ScBase):
    __tablename__ = "sink_status"

    sinking_tx_hash: Mapped[hashpk] = mapped_column(ForeignKey('sinking_txs.hash'))
    certificate_id: Mapped[intpk] = mapped_column(ForeignKey('retirements.certificate_id'))
    amount_filled: Mapped[Decimal]
    finalized: Mapped[bool]

    sinking_transaction: Mapped[SinkingTx] = relationship(
        init=False, repr=False, 
        back_populates='statuses'
    )
    retirement: Mapped[Retirement] = relationship(
        init=False, repr=False,
        back_populates='sink_statuses'
    )

    def as_dict(self):
        return {
            col: getattr(self, col)
            for col in self.__table__.columns.keys()
        }
