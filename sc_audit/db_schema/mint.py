"""
Declare CARBON issuance DB models.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from __future__ import annotations
from dataclasses import dataclass
import datetime as dt
import typing

from sqlalchemy import ForeignKey, Index, SQLColumnExpression, String, func, select
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sc_audit.db_schema.base import HexBinary, ScBase, hashpk
from sc_audit.db_schema.impact_project import VcsProject

if typing.TYPE_CHECKING:
    from sc_audit.db_schema import RetirementFromBlock


VerraSubAccountName = typing.Literal[
    "CARBON Pool | stellarcarbon.io", 
    "CARBON Sink | stellarcarbon.io"
]

@dataclass
class VerraSubAccount:
    id: int
    name: VerraSubAccountName

verra_carbon_pool = VerraSubAccount(11273, "CARBON Pool | stellarcarbon.io")
verra_carbon_sink = VerraSubAccount(11274, "CARBON Sink | stellarcarbon.io")


class MintedBlock(ScBase):
    __tablename__ = "minted_blocks"

    serial_hash: Mapped[hashpk]
    transaction_hash: Mapped[str] = mapped_column(HexBinary(length=32))
    created_at: Mapped[dt.datetime]
    vcs_project_id: Mapped[int] = mapped_column(ForeignKey('vcs_projects.id'))
    vcs_project: Mapped[VcsProject] = relationship(init=False, repr=False, back_populates='minted_blocks')
    serial_number: Mapped[str] = mapped_column(String(128))
    block_start: Mapped[int]
    block_end: Mapped[int]
    sub_account_id: Mapped[int]
    sub_account_name: Mapped[VerraSubAccountName]
    vintage_start: Mapped[dt.date]
    vintage_end: Mapped[dt.date]
    paging_token: Mapped[int]

    consumed_by: Mapped[list[RetirementFromBlock]] = relationship(
        init=False, repr=False, 
        back_populates='block',
        lazy='selectin',
        order_by="asc(RetirementFromBlock.retirement_id)"
    )

    @hybrid_property
    def size(self) -> int:
        return 1 + self.block_end - self.block_start
    
    @hybrid_property
    def credits_remaining(self) -> int:
        credits_consumed = sum(rfb.vcu_amount for rfb in self.consumed_by)
        return self.size - credits_consumed
    
    @credits_remaining.inplace.expression
    @classmethod
    def _credits_remaining_expression(cls) -> SQLColumnExpression[int]:
        from sc_audit.db_schema import RetirementFromBlock
        return (
            select(cls.size - func.coalesce(func.sum(RetirementFromBlock.vcu_amount), 0))
            .where(RetirementFromBlock.block_hash == cls.serial_hash)
            .label("credits_remaining")
        )
    
    @hybrid_method
    def credits_remaining_on_date(self, on_date: dt.date) -> int:
        credits_consumed = sum(
            rfb.vcu_amount
            for rfb in self.consumed_by
            if rfb.retirement.retirement_date <= on_date
        )
        return self.size - credits_consumed
    
    @credits_remaining_on_date.inplace.expression
    @classmethod
    def _credits_remaining_on_date_expression(cls, on_date: dt.date) -> SQLColumnExpression[int]:
        from sc_audit.db_schema import Retirement, RetirementFromBlock
        return (
            select(cls.size - func.coalesce(func.sum(RetirementFromBlock.vcu_amount), 0))
            .where(RetirementFromBlock.block_hash == cls.serial_hash)
            .where(RetirementFromBlock.retirement_id == Retirement.certificate_id)
            .where(Retirement.retirement_date <= on_date)
            .label("credits_remaining_on_date")
        )


idx_created_at = Index("idx_block_created_at", MintedBlock.created_at)
