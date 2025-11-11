"""rename paging_token columns to TOID

Revision ID: 371cdad348d3
Revises: 52e5e68af772
Create Date: 2025-11-11 12:18:35.680184

"""
from typing import Sequence

from alembic import context, op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '371cdad348d3'
down_revision: str | None = '52e5e68af772'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # turn off FK constraints for SQLite to allow table recreation
    dialect_name = context.get_context().dialect.name
    if dialect_name == 'sqlite':
        op.execute("PRAGMA foreign_keys=OFF")

    with op.batch_alter_table('distribution_txs', schema=None) as batch_op:
        batch_op.alter_column('paging_token', new_column_name='toid')

    with op.batch_alter_table('minted_blocks', schema=None) as batch_op:
        batch_op.alter_column('paging_token', new_column_name='toid')
        batch_op.drop_index(batch_op.f('idx_block_toid'))
        
    op.create_index('idx_block_toid', 'minted_blocks', [sa.literal_column('toid DESC')], unique=True)

    with op.batch_alter_table('sinking_txs', schema=None) as batch_op:
        batch_op.alter_column('paging_token', new_column_name='toid')
        batch_op.drop_index(batch_op.f('idx_stx_toid'))
        
    op.create_index('idx_stx_toid', 'sinking_txs', [sa.literal_column('toid DESC')], unique=True)

    with op.batch_alter_table('test_distribution_txs', schema=None) as batch_op:
        batch_op.alter_column('paging_token', new_column_name='toid')

    with op.batch_alter_table('test_minted_blocks', schema=None) as batch_op:
        batch_op.alter_column('paging_token', new_column_name='toid')

    with op.batch_alter_table('test_sinking_txs', schema=None) as batch_op:
        batch_op.alter_column('paging_token', new_column_name='toid')

    if dialect_name == 'sqlite':
        op.execute("PRAGMA foreign_keys=ON")


def downgrade() -> None:
    dialect_name = context.get_context().dialect.name
    if dialect_name == 'sqlite':
        op.execute("PRAGMA foreign_keys=OFF")

    with op.batch_alter_table('test_sinking_txs', schema=None) as batch_op:
        batch_op.alter_column('toid', new_column_name='paging_token')

    with op.batch_alter_table('test_minted_blocks', schema=None) as batch_op:
        batch_op.alter_column('toid', new_column_name='paging_token')

    with op.batch_alter_table('test_distribution_txs', schema=None) as batch_op:
        batch_op.alter_column('toid', new_column_name='paging_token')

    with op.batch_alter_table('sinking_txs', schema=None) as batch_op:
        batch_op.alter_column('toid', new_column_name='paging_token')
        batch_op.drop_index('idx_stx_toid')
        
    op.create_index(op.f('idx_stx_toid'), 'sinking_txs', [sa.literal_column('paging_token DESC')], unique=True)

    with op.batch_alter_table('minted_blocks', schema=None) as batch_op:
        batch_op.alter_column('toid', new_column_name='paging_token')
        batch_op.drop_index('idx_block_toid')
        
    op.create_index(op.f('idx_block_toid'), 'minted_blocks', [sa.literal_column('paging_token DESC')], unique=True)

    with op.batch_alter_table('distribution_txs', schema=None) as batch_op:
        batch_op.alter_column('toid', new_column_name='paging_token')

    if dialect_name == 'sqlite':
        op.execute("PRAGMA foreign_keys=ON")
