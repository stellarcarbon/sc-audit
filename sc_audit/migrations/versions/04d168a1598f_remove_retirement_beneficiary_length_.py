"""remove retirement_beneficiary length constraint

Revision ID: 04d168a1598f
Revises: 4813b9c06c97
Create Date: 2024-08-12 12:32:56.638424

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04d168a1598f'
down_revision: str | None = '4813b9c06c97'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table('retirements', schema=None) as batch_op:
        batch_op.alter_column('retirement_beneficiary',
               existing_type=sa.VARCHAR(length=56),
               type_=sa.String(),
               existing_nullable=False)

    with op.batch_alter_table('test_retirements', schema=None) as batch_op:
        batch_op.alter_column('retirement_beneficiary',
               existing_type=sa.VARCHAR(length=56),
               type_=sa.String(),
               existing_nullable=False)


def downgrade() -> None:
    with op.batch_alter_table('test_retirements', schema=None) as batch_op:
        batch_op.alter_column('retirement_beneficiary',
               existing_type=sa.String(),
               type_=sa.VARCHAR(length=56),
               existing_nullable=False)

    with op.batch_alter_table('retirements', schema=None) as batch_op:
        batch_op.alter_column('retirement_beneficiary',
               existing_type=sa.String(),
               type_=sa.VARCHAR(length=56),
               existing_nullable=False)
