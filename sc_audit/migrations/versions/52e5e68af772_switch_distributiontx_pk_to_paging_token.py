"""switch DistributionTx PK to paging_token

Revision ID: 52e5e68af772
Revises: 90594e768102
Create Date: 2025-11-10 19:49:34.286846

"""
from typing import Sequence

from alembic import context, op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52e5e68af772'
down_revision: str | None = '90594e768102'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def get_naming_convention():
    # get naming convention from the context
    migration_context = context.get_context()
    target_metadata = migration_context.opts.get("target_metadata")
    assert target_metadata is not None, "Target metadata must be set in the migration context"
    return target_metadata.naming_convention


def upgrade() -> None:
    naming_convention = get_naming_convention()
    dialect_name = context.get_context().dialect.name

    with op.batch_alter_table('distribution_txs', schema=None, naming_convention=naming_convention) as batch_op:
        constraint_name = 'distribution_txs_pkey' if dialect_name == 'postgresql' else None
        batch_op.drop_constraint(constraint_name, type_='primary') # type: ignore
        batch_op.create_primary_key(batch_op.f('pk_distribution_txs'), ['paging_token'])
        batch_op.drop_index(batch_op.f('idx_dtx_toid'))
        batch_op.create_index('idx_dtx_hash', ['hash'], unique=False)

    with op.batch_alter_table('test_distribution_txs', schema=None, naming_convention=naming_convention) as batch_op:
        constraint_name = 'test_distribution_txs_pkey' if dialect_name == 'postgresql' else None
        batch_op.drop_constraint(constraint_name, type_='primary') # type: ignore
        batch_op.create_primary_key(batch_op.f('pk_test_distribution_txs'), ['paging_token'])


def downgrade() -> None:
    """
    Downgrade will fail if there are multiple outflows with the same tx hash.
    """
    naming_convention = get_naming_convention()

    with op.batch_alter_table('distribution_txs', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint(batch_op.f('pk_distribution_txs'), type_='primary')
        batch_op.create_primary_key(None, ['hash'])
        batch_op.drop_index('idx_dtx_hash')
        batch_op.create_index(batch_op.f('idx_dtx_toid'), ['paging_token'], unique=1)

    with op.batch_alter_table('test_distribution_txs', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint(batch_op.f('pk_test_distribution_txs'), type_='primary')
        batch_op.create_primary_key(None, ['hash'])
