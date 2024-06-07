"""
Declare carbon sinking DB models.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from __future__ import annotations
import datetime as dt
from  decimal import Decimal
import typing

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sc_audit.db_schema.base import ScBase, hashpk, kgdecimal, strkey, stroopdecimal
from sc_audit.db_schema.impact_project import VcsProject

if typing.TYPE_CHECKING:
    from sc_audit.db_schema import SinkStatus


MemoType = typing.Literal['text', 'hash', 'none']


class SinkingTx(ScBase):
    __tablename__ = "sinking_txs"

    hash: Mapped[hashpk]
    created_at: Mapped[dt.datetime]
    funder: Mapped[strkey]
    recipient: Mapped[strkey]
    carbon_amount: Mapped[kgdecimal]
    source_asset_code: Mapped[str] = mapped_column(String(12))
    source_asset_issuer: Mapped[strkey | None]
    source_asset_amount: Mapped[stroopdecimal]
    dest_asset_code: Mapped[str] = mapped_column(String(12))
    dest_asset_issuer: Mapped[strkey]
    dest_asset_amount: Mapped[stroopdecimal]
    vcs_project_id: Mapped[int] = mapped_column(ForeignKey("vcs_projects.id"))
    vcs_project: Mapped[VcsProject] = relationship(init=False, repr=False)
    memo_type: Mapped[MemoType]
    memo_value: Mapped[str | None] = mapped_column(String(64))
    paging_token: Mapped[int]

    statuses: Mapped[list[SinkStatus]] = relationship(
        init=False, repr=False, 
        back_populates='sinking_transaction',
        lazy='selectin',
        order_by="asc(SinkStatus.certificate_id)"
    )

    @hybrid_property
    def total_filled(self) -> Decimal:
        return sum(
            (ss.amount_filled for ss in self.statuses),
            start=Decimal()
        )
    
    def as_dict(self):
        data = {
            col: getattr(self, col)
            for col in self.__table__.columns.keys()
        }
        data['statuses'] = [status.as_dict() for status in self.statuses]
        return data
    

idx_created_at = Index("idx_stx_created_at", SinkingTx.created_at.desc())
idx_funder = Index("idx_stx_funder", SinkingTx.funder)
idx_recipient = Index("idx_stx_recipient", SinkingTx.recipient)
