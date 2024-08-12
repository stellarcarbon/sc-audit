"""change paging_token to bigint

Revision ID: 4813b9c06c97
Revises: 19f853853773
Create Date: 2024-08-12 11:54:29.673037

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4813b9c06c97'
down_revision: str | None = '19f853853773'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table('distribution_txs', schema=None) as batch_op:
        batch_op.alter_column('paging_token',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False)

    with op.batch_alter_table('minted_blocks', schema=None) as batch_op:
        batch_op.alter_column('paging_token',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False)

    with op.batch_alter_table('sinking_txs', schema=None) as batch_op:
        batch_op.alter_column('paging_token',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False)

    with op.batch_alter_table('test_distribution_txs', schema=None) as batch_op:
        batch_op.alter_column('paging_token',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False)

    with op.batch_alter_table('test_minted_blocks', schema=None) as batch_op:
        batch_op.alter_column('paging_token',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False)

    with op.batch_alter_table('test_sinking_txs', schema=None) as batch_op:
        batch_op.alter_column('paging_token',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False)


def downgrade() -> None:
    with op.batch_alter_table('test_sinking_txs', schema=None) as batch_op:
        batch_op.alter_column('paging_token',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('test_minted_blocks', schema=None) as batch_op:
        batch_op.alter_column('paging_token',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('test_distribution_txs', schema=None) as batch_op:
        batch_op.alter_column('paging_token',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('sinking_txs', schema=None) as batch_op:
        batch_op.alter_column('paging_token',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('minted_blocks', schema=None) as batch_op:
        batch_op.alter_column('paging_token',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('distribution_txs', schema=None) as batch_op:
        batch_op.alter_column('paging_token',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False)
