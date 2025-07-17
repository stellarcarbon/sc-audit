"""fix test table foreign keys

Revision ID: 0c2f50c4d517
Revises: 77ea86674a18
Create Date: 2025-06-18 12:10:02.734143

"""
from typing import Sequence

from alembic import context, op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c2f50c4d517'
down_revision: str | None = '77ea86674a18'
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

    with op.batch_alter_table('test_minted_blocks', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint('test_minted_blocks_vcs_project_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('test_minted_blocks_vcs_project_id_fkey'), 'test_vcs_projects', ['vcs_project_id'], ['id'])

    with op.batch_alter_table('test_retirement_from_block', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint('test_retirement_from_block_retirement_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('test_retirement_from_block_block_hash_fkey', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('test_retirement_from_block_retirement_id_fkey'), 'test_retirements', ['retirement_id'], ['certificate_id'])
        batch_op.create_foreign_key(batch_op.f('test_retirement_from_block_block_hash_fkey'), 'test_minted_blocks', ['block_hash'], ['serial_hash'])

    with op.batch_alter_table('test_retirements', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint('test_retirements_vcs_project_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('test_retirements_vcs_project_id_fkey'), 'test_vcs_projects', ['vcs_project_id'], ['id'])

    with op.batch_alter_table('test_sink_status', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint('test_sink_status_certificate_id_fkey', type_='foreignkey')
        batch_op.drop_constraint('test_sink_status_sinking_tx_hash_fkey', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('test_sink_status_certificate_id_fkey'), 'test_retirements', ['certificate_id'], ['certificate_id'])
        batch_op.create_foreign_key(batch_op.f('test_sink_status_sinking_tx_hash_fkey'), 'test_sinking_txs', ['sinking_tx_hash'], ['hash'])

    with op.batch_alter_table('test_sinking_txs', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint('test_sinking_txs_vcs_project_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('test_sinking_txs_vcs_project_id_fkey'), 'test_vcs_projects', ['vcs_project_id'], ['id'])


def downgrade() -> None:
    naming_convention = get_naming_convention()

    with op.batch_alter_table('test_sinking_txs', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint(batch_op.f('test_sinking_txs_vcs_project_id_fkey'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'vcs_projects', ['vcs_project_id'], ['id'])

    with op.batch_alter_table('test_sink_status', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint(batch_op.f('test_sink_status_sinking_tx_hash_fkey'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('test_sink_status_certificate_id_fkey'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'sinking_txs', ['sinking_tx_hash'], ['hash'])
        batch_op.create_foreign_key(None, 'retirements', ['certificate_id'], ['certificate_id'])

    with op.batch_alter_table('test_retirements', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint(batch_op.f('test_retirements_vcs_project_id_fkey'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'vcs_projects', ['vcs_project_id'], ['id'])

    with op.batch_alter_table('test_retirement_from_block', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint(batch_op.f('test_retirement_from_block_block_hash_fkey'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('test_retirement_from_block_retirement_id_fkey'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'retirements', ['retirement_id'], ['certificate_id'])
        batch_op.create_foreign_key(None, 'minted_blocks', ['block_hash'], ['serial_hash'])

    with op.batch_alter_table('test_minted_blocks', schema=None, naming_convention=naming_convention) as batch_op:
        batch_op.drop_constraint(batch_op.f('test_minted_blocks_vcs_project_id_fkey'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'vcs_projects', ['vcs_project_id'], ['id'])
