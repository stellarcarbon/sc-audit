"""add contract_id to sinking_txs

Revision ID: 77ea86674a18
Revises: 04d168a1598f
Create Date: 2025-06-10 14:32:14.335259

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77ea86674a18'
down_revision: str | None = '04d168a1598f'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table('sinking_txs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contract_id', sa.String(length=56), nullable=True))

    with op.batch_alter_table('test_sinking_txs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contract_id', sa.String(length=56), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('test_sinking_txs', schema=None) as batch_op:
        batch_op.drop_column('contract_id')

    with op.batch_alter_table('sinking_txs', schema=None) as batch_op:
        batch_op.drop_column('contract_id')
