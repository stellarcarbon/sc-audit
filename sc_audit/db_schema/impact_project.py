"""
Declare impact project DB models.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from __future__ import annotations
import typing

from sqlalchemy import Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sc_audit.db_schema.base import ScBase, intpk

if typing.TYPE_CHECKING:
    from sc_audit.db_schema import MintedBlock


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

    minted_blocks: Mapped[list[MintedBlock]] = relationship(
        init=False, repr=False, 
        back_populates="vcs_project", 
        order_by="asc(MintedBlock.block_start)"
    )


class UnknownVcsProject(Exception):
    def __init__(self, msg, vcs_id: int):
        super().__init__(msg, vcs_id)
