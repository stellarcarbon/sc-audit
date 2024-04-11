import datetime as dt
import typing

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sc_audit.db_schema.base import ScBase, intpk, strkey
from sc_audit.db_schema.impact_project import VcsProject


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
    vcs_project: Mapped[VcsProject] = relationship(init=False)
    issuance_date: Mapped[dt.date]
    instrument_type: Mapped[InstrumentType]
    vintage_start: Mapped[dt.date]
    vintage_end: Mapped[dt.date]
    total_vintage_quantity: Mapped[int]
