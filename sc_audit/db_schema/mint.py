"""
Declare CARBON issuance DB models.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from dataclasses import dataclass
import datetime as dt
import typing

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sc_audit.db_schema.base import HexBinary, ScBase, hashpk
from sc_audit.db_schema.impact_project import VcsProject


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
    vcs_project_id: Mapped[int] = mapped_column(ForeignKey("vcs_projects.id"))
    vcs_project: Mapped[VcsProject] = relationship(init=False, back_populates="minted_blocks")
    serial_number: Mapped[str] = mapped_column(String(128))
    block_start: Mapped[int]
    block_end: Mapped[int]
    sub_account_id: Mapped[int]
    sub_account_name: Mapped[VerraSubAccountName]
    vintage_start: Mapped[dt.date]
    vintage_end: Mapped[dt.date]
    paging_token: Mapped[int]
