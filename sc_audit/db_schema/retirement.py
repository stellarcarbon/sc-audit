"""
Declare credit retirement DB models.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from __future__ import annotations
import datetime as dt
import typing

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sc_audit.db_schema.base import ScBase, intpk, strkey
from sc_audit.db_schema.impact_project import VcsProject

if typing.TYPE_CHECKING:
    from sc_audit.db_schema import RetirementFromBlock, SinkStatus


InstrumentType = typing.Literal['VCU']


class Retirement(ScBase):
    __tablename__ = "retirements"

    certificate_id: Mapped[intpk]
    vcu_amount: Mapped[int]
    serial_number: Mapped[str] = mapped_column(String(128))
    retirement_date: Mapped[dt.date]
    retirement_beneficiary: Mapped[strkey]
    retirement_details: Mapped[str]
    vcs_project_id: Mapped[int] = mapped_column(ForeignKey("vcs_projects.id"))
    vcs_project: Mapped[VcsProject] = relationship(init=False, repr=False)
    issuance_date: Mapped[dt.date]
    instrument_type: Mapped[InstrumentType]
    vintage_start: Mapped[dt.date]
    vintage_end: Mapped[dt.date]
    total_vintage_quantity: Mapped[int]

    retired_from: Mapped[list[RetirementFromBlock]] = relationship(
        init=False, repr=False, 
        back_populates='retirement',
    )
    sink_statuses: Mapped[list[SinkStatus]] = relationship(
        init=False, repr=False, 
        back_populates='retirement',
    )

    @property
    def tx_hashes_from_details(self) -> list[str]:
        tag, *tx_hashes = self.retirement_details.split()
        assert tag.startswith("stellarcarbon")
        return tx_hashes


idx_retirement_date = Index("idx_retirement_date", Retirement.retirement_date.desc())
idx_retirement_beneficiary = Index("idx_retirement_beneficiary", Retirement.retirement_beneficiary)
