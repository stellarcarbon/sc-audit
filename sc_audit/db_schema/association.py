"""
Declare associative models that produce many-to-many tables.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from __future__ import annotations
import typing

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from sc_audit.db_schema.base import ScBase, intpk, hashpk, kgdecimal

if typing.TYPE_CHECKING:
    from sc_audit.db_schema import MintedBlock, Retirement, SinkingTx


class RetirementFromBlockBase(MappedAsDataclass, kw_only=True):

    retirement_id: Mapped[intpk] = mapped_column(ForeignKey('retirements.certificate_id'))
    block_hash: Mapped[hashpk] = mapped_column(ForeignKey('minted_blocks.serial_hash'))
    vcu_amount: Mapped[int]


class RetirementFromBlock(RetirementFromBlockBase, ScBase):
    __tablename__ = "retirement_from_block"

    retirement: Mapped[Retirement] = relationship(
        init=False, repr=False,
        back_populates='retired_from'
    )
    block: Mapped[MintedBlock] = relationship(
        init=False, repr=False, 
        back_populates='consumed_by'
    )

    def as_dict(self):
        return {
            col: getattr(self, col)
            for col in self.__table__.columns.keys()
        }


class SinkStatusBase(MappedAsDataclass, kw_only=True):

    sinking_tx_hash: Mapped[hashpk] = mapped_column(ForeignKey('sinking_txs.hash'))
    certificate_id: Mapped[intpk] = mapped_column(ForeignKey('retirements.certificate_id'))
    amount_filled: Mapped[kgdecimal]
    finalized: Mapped[bool]


class SinkStatus(SinkStatusBase, ScBase):
    __tablename__ = "sink_status"

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
    

idx_finalized = Index("idx_finalized", SinkStatus.finalized)
