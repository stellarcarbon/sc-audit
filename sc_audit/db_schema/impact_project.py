import enum

from sqlalchemy import Unicode
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sc_audit.db_schema.base import ScBase, intpk


class VcsCategory(enum.Enum):
    AFOLU = "Agriculture Forestry and Other Land Use"


class VcsProtocol(enum.Enum):
    VM0015 = "VM0015"


class VcsProject(ScBase):
    __tablename__ = "vcs_projects"

    id: Mapped[intpk]
    name: Mapped[str]
    category: Mapped[VcsCategory]
    protocol: Mapped[VcsProtocol]
    additional_certifications: Mapped[str | None]
    region: Mapped[str] = mapped_column(Unicode(128))
    country: Mapped[str] = mapped_column(Unicode(128))

    minted_blocks: Mapped[list["MintedBlock"]] = relationship(back_populates="vcs_project") # type: ignore
