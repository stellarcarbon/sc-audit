"""
Declare carbon sinking DB models.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from __future__ import annotations
import datetime as dt
from  decimal import Decimal
import typing

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sc_audit.db_schema.base import ScBase, hashpk, strkey
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
    carbon_amount: Mapped[Decimal]
    source_asset_code: Mapped[str] = mapped_column(String(12))
    source_asset_issuer: Mapped[strkey | None]
    source_asset_amount: Mapped[Decimal]
    dest_asset_code: Mapped[str] = mapped_column(String(12))
    dest_asset_issuer: Mapped[strkey]
    dest_asset_amount: Mapped[Decimal]
    vcs_project_id: Mapped[int] = mapped_column(ForeignKey("vcs_projects.id"))
    vcs_project: Mapped[VcsProject] = relationship(init=False, repr=False)
    memo_type: Mapped[MemoType]
    memo_value: Mapped[str | None] = mapped_column(String(64))
    paging_token: Mapped[int]

    statuses: Mapped[list[SinkStatus]] = relationship(
        init=False, repr=False, 
        back_populates='sinking_transaction',
        order_by="asc(SinkStatus.certificate_id)"
    )
