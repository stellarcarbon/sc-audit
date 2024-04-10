import datetime as dt
from  decimal import Decimal
import enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sc_audit.db_schema.base import ScBase, hashpk, strkey
from sc_audit.db_schema.impact_project import VcsProject


class MemoType(enum.Enum):
    TEXT = 'text'
    HASH = 'hash'


class SinkingTx(ScBase):
    __tablename__ = "sinking_txs"

    hash: Mapped[hashpk]
    created_at: Mapped[dt.datetime]
    funder: Mapped[strkey]
    recipient: Mapped[strkey]
    carbon_amount: Mapped[Decimal]
    source_asset_code: Mapped[str] = mapped_column(String(12))
    source_asset_issuer: Mapped[strkey]
    source_asset_amount: Mapped[Decimal]
    dest_asset_code: Mapped[str] = mapped_column(String(12))
    dest_asset_issuer: Mapped[strkey]
    dest_asset_amount: Mapped[Decimal]
    vcs_project_id: Mapped[int] = mapped_column(ForeignKey("vcs_projects.id"))
    vcs_project: Mapped[VcsProject] = relationship()
    memo_type: Mapped[MemoType]
    memo_value: Mapped[str] = mapped_column(String(64))
