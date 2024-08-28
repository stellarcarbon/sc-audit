"""
Declare impact project DB models.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from __future__ import annotations
import typing

from sqlalchemy import Unicode
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship

from sc_audit.db_schema.base import ScBase, intpk

if typing.TYPE_CHECKING:
    from sc_audit.db_schema import MintedBlock


VcsCategory = typing.Literal["Agriculture Forestry and Other Land Use"]
VcsProtocol = typing.Literal["VM0015"]


class VcsProjectBase(MappedAsDataclass):

    id: Mapped[intpk]
    name: Mapped[str]
    category: Mapped[VcsCategory]
    protocol: Mapped[VcsProtocol]
    additional_certifications: Mapped[str | None]
    region: Mapped[str] = mapped_column(Unicode(128))
    country: Mapped[str] = mapped_column(Unicode(128))


class VcsProject(VcsProjectBase, ScBase):
    __tablename__ = "vcs_projects"

    minted_blocks: Mapped[list[MintedBlock]] = relationship(
        init=False, repr=False, 
        back_populates="vcs_project", 
        order_by="asc(MintedBlock.block_start)"
    )

    def as_dict(self):
        return {
            col: getattr(self, col)
            for col in self.__table__.columns.keys()
        }


class UnknownVcsProject(Exception):
    def __init__(self, msg, vcs_id: int):
        super().__init__(msg, vcs_id)


def get_vcs_project(vcs_project_id: int) -> VcsProject | None:
    vcs_projects = {
        1360: VcsProject(
            id=1360, 
            name="Forest Management to reduce deforestation and degradation in Shipibo Conibo and Cacataibo Indigenous communities of Ucayali region", 
            category="Agriculture Forestry and Other Land Use", 
            protocol="VM0015", 
            additional_certifications="CCB-Gold", 
            region="Latin America", 
            country="Peru"
        ),
    }
    return vcs_projects.get(vcs_project_id)
