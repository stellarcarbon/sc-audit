"""add paging_token indexes

Revision ID: 713e40249322
Revises: 0c2f50c4d517
Create Date: 2025-06-26 14:13:08.992641

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '713e40249322'
down_revision: str | None = '0c2f50c4d517'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table('distribution_txs', schema=None) as batch_op:
        batch_op.create_index('idx_dtx_toid', [sa.literal_column('paging_token DESC')], unique=True)  # type: ignore[arg-type]

    with op.batch_alter_table('minted_blocks', schema=None) as batch_op:
        batch_op.create_index('idx_block_toid', [sa.literal_column('paging_token DESC')], unique=True)  # type: ignore[arg-type]

    with op.batch_alter_table('sinking_txs', schema=None) as batch_op:
        batch_op.create_index('idx_stx_toid', [sa.literal_column('paging_token DESC')], unique=True)  # type: ignore[arg-type]


def downgrade() -> None:
    with op.batch_alter_table('sinking_txs', schema=None) as batch_op:
        batch_op.drop_index('idx_stx_toid')

    with op.batch_alter_table('minted_blocks', schema=None) as batch_op:
        batch_op.drop_index('idx_block_toid')

    with op.batch_alter_table('distribution_txs', schema=None) as batch_op:
        batch_op.drop_index('idx_dtx_toid')
