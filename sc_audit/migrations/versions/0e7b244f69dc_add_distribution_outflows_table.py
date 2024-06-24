"""add distribution outflows table

Revision ID: 0e7b244f69dc
Revises: b595c6a10724
Create Date: 2024-06-24 17:18:49.287452

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa
from sc_audit.db_schema.base import HexBinary

# revision identifiers, used by Alembic.
revision: str = '0e7b244f69dc'
down_revision: str | None = 'b595c6a10724'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table('distribution_txs',
    sa.Column('hash', HexBinary(length=32), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('sender', sa.String(length=56), nullable=False),
    sa.Column('recipient', sa.String(length=56), nullable=False),
    sa.Column('carbon_amount', sa.DECIMAL(precision=21, scale=3), nullable=False),
    sa.Column('paging_token', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('hash')
    )
    op.create_index('idx_dtx_created_at', 'distribution_txs', [sa.text('created_at DESC')], unique=False)
    op.create_index('idx_dtx_recipient', 'distribution_txs', ['recipient'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_dtx_recipient', table_name='distribution_txs')
    op.drop_index('idx_dtx_created_at', table_name='distribution_txs')
    op.drop_table('distribution_txs')
