import enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

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
    additional_certifications: Mapped[str]
    region: Mapped[str] = mapped_column(String(128))
    country: Mapped[str] = mapped_column(String(128))
