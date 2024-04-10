import datetime as dt
import enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sc_audit.db_schema.base import HexBinary, ScBase, hashpk
from sc_audit.db_schema.impact_project import VcsProject


class VerraSubAccount(enum.Enum):
    CPOOL = "CARBON Pool | stellarcarbon.io"
    CSINK = "CARBON Sink | stellarcarbon.io"


class MintedBlock(ScBase):
    __tablename__ = "minted_blocks"

    serial_hash: Mapped[hashpk]
    transaction_hash: Mapped[bytes] = mapped_column(HexBinary(length=32))
    created_at: Mapped[dt.datetime]
    vcs_project_id: Mapped[int] = mapped_column(ForeignKey("vcs_projects.id"))
    vcs_project: Mapped[VcsProject] = relationship(back_populates="minted_blocks")
    serial_number: Mapped[str] = mapped_column(String(128))
    block_size: Mapped[int]
    sub_account_id: Mapped[int]
    sub_account_name: Mapped[VerraSubAccount]
    vintage_start: Mapped[dt.date]
    vintage_end: Mapped[dt.date]
