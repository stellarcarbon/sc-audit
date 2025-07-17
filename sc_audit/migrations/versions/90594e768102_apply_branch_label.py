"""apply branch label

Revision ID: 90594e768102
Revises: 713e40249322
Create Date: 2025-07-17 15:45:43.718067

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90594e768102'
down_revision: str | None = '713e40249322'
branch_labels: str | Sequence[str] | None = ('sc-audit',)
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
