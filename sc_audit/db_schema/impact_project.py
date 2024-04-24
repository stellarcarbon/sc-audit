"""
Declare impact project DB models.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import typing

from sqlalchemy import Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sc_audit.db_schema.base import ScBase, intpk


VcsCategory = typing.Literal["Agriculture Forestry and Other Land Use"]
VcsProtocol = typing.Literal["VM0015"]


class VcsProject(ScBase):
    __tablename__ = "vcs_projects"

    id: Mapped[intpk]
    name: Mapped[str]
    category: Mapped[VcsCategory]
    protocol: Mapped[VcsProtocol]
    additional_certifications: Mapped[str | None]
    region: Mapped[str] = mapped_column(Unicode(128))
    country: Mapped[str] = mapped_column(Unicode(128))

    minted_blocks: Mapped[list['MintedBlock']] = relationship(init=False, back_populates="vcs_project") # type: ignore


class UnknownVcsProject(Exception):
    def __init__(self, msg, vcs_id: int):
        super().__init__(msg, vcs_id)
