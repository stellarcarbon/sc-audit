"""
Declare credit retirement DB models.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from __future__ import annotations
import datetime as dt
import typing

from sqlalchemy import ForeignKey, Index, String, event
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from sc_audit.db_schema.base import ScBase, intpk
from sc_audit.db_schema.impact_project import VcsProject
from sc_audit.loader.utils import VcsSerialNumber

if typing.TYPE_CHECKING:
    from sc_audit.db_schema import RetirementFromBlock, SinkStatus


InstrumentType = typing.Literal['VCU']


class RetirementBase(MappedAsDataclass, kw_only=True):
    __tablename__ = "retirements"

    certificate_id: Mapped[intpk]
    vcu_amount: Mapped[int]
    serial_number: Mapped[str] = mapped_column(String(128))
    retirement_date: Mapped[dt.date]
    retirement_beneficiary: Mapped[str]
    retirement_details: Mapped[str]
    vcs_project_id: Mapped[int] = mapped_column(ForeignKey("vcs_projects.id"))
    issuance_date: Mapped[dt.date]
    instrument_type: Mapped[InstrumentType]
    vintage_start: Mapped[dt.date]
    vintage_end: Mapped[dt.date]
    total_vintage_quantity: Mapped[int]


class Retirement(RetirementBase, ScBase):
    __tablename__ = "retirements"

    vcs_project: Mapped[VcsProject] = relationship(init=False, repr=False)
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
    
    def validate_serial_number(self):
        value = self.serial_number
        if not value:
            raise ValueError("Serial number cannot be empty")
        
        serial_number = VcsSerialNumber.from_str(value)
        vcu_amount = 1 + serial_number.block_end - serial_number.block_start
        if serial_number.project_id != self.vcs_project_id:
            raise ValueError(
                f"Serial number {value} does not match VCS project ID {self.vcs_project_id}"
            )
        elif vcu_amount != self.vcu_amount:
            raise ValueError(
                f"Serial number {value} implies a VCU amount of {vcu_amount},"
                f" but got vcu_amount={self.vcu_amount}"
            )
    
    def as_dict(self, related: bool = False):
        data = {
            col: getattr(self, col)
            for col in self.__table__.columns.keys()
        }
        if related:
            del data['vcs_project_id']
            data['vcs_project'] = self.vcs_project.as_dict()
            data['retired_from'] = [
                rfb.as_dict() for rfb in self.retired_from
                if rfb.retirement_id
            ]
            data['sink_statuses'] = [
                status.as_dict() for status in self.sink_statuses
                if status.certificate_id
            ]
        
        return data


idx_retirement_date = Index("idx_retirement_date", Retirement.retirement_date.desc())
idx_retirement_beneficiary = Index("idx_retirement_beneficiary", Retirement.retirement_beneficiary)

@event.listens_for(Retirement, "before_insert")
def validate_retirement(mapper, connection, target: Retirement):
    target.validate_serial_number()
