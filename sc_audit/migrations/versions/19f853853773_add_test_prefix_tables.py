"""add test prefix tables

Revision ID: 19f853853773
Revises: 0e7b244f69dc
Create Date: 2024-07-25 19:00:55.917243

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa
from sc_audit.db_schema.base import HexBinary

# revision identifiers, used by Alembic.
revision: str = '19f853853773'
down_revision: str | None = '0e7b244f69dc'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table('test_distribution_txs',
    sa.Column('hash', HexBinary(length=32), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('sender', sa.String(length=56), nullable=False),
    sa.Column('recipient', sa.String(length=56), nullable=False),
    sa.Column('carbon_amount', sa.DECIMAL(precision=21, scale=3), nullable=False),
    sa.Column('paging_token', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('hash')
    )
    op.create_table('test_vcs_projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('category', sa.Enum('Agriculture Forestry and Other Land Use', native_enum=False), nullable=False),
    sa.Column('protocol', sa.Enum('VM0015', native_enum=False), nullable=False),
    sa.Column('additional_certifications', sa.String(), nullable=True),
    sa.Column('region', sa.Unicode(length=128), nullable=False),
    sa.Column('country', sa.Unicode(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('test_minted_blocks',
    sa.Column('serial_hash', HexBinary(length=32), nullable=False),
    sa.Column('transaction_hash', HexBinary(length=32), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('vcs_project_id', sa.Integer(), nullable=False),
    sa.Column('serial_number', sa.String(length=128), nullable=False),
    sa.Column('block_start', sa.Integer(), nullable=False),
    sa.Column('block_end', sa.Integer(), nullable=False),
    sa.Column('sub_account_id', sa.Integer(), nullable=False),
    sa.Column('sub_account_name', sa.Enum('CARBON Pool | stellarcarbon.io', 'CARBON Sink | stellarcarbon.io', native_enum=False), nullable=False),
    sa.Column('vintage_start', sa.Date(), nullable=False),
    sa.Column('vintage_end', sa.Date(), nullable=False),
    sa.Column('paging_token', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['vcs_project_id'], ['vcs_projects.id'], ),
    sa.PrimaryKeyConstraint('serial_hash')
    )
    op.create_table('test_retirements',
    sa.Column('certificate_id', sa.Integer(), nullable=False),
    sa.Column('vcu_amount', sa.Integer(), nullable=False),
    sa.Column('serial_number', sa.String(length=128), nullable=False),
    sa.Column('retirement_date', sa.Date(), nullable=False),
    sa.Column('retirement_beneficiary', sa.String(length=56), nullable=False),
    sa.Column('retirement_details', sa.String(), nullable=False),
    sa.Column('vcs_project_id', sa.Integer(), nullable=False),
    sa.Column('issuance_date', sa.Date(), nullable=False),
    sa.Column('instrument_type', sa.Enum('VCU', native_enum=False), nullable=False),
    sa.Column('vintage_start', sa.Date(), nullable=False),
    sa.Column('vintage_end', sa.Date(), nullable=False),
    sa.Column('total_vintage_quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['vcs_project_id'], ['vcs_projects.id'], ),
    sa.PrimaryKeyConstraint('certificate_id')
    )
    op.create_table('test_sinking_txs',
    sa.Column('hash', HexBinary(length=32), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('funder', sa.String(length=56), nullable=False),
    sa.Column('recipient', sa.String(length=56), nullable=False),
    sa.Column('carbon_amount', sa.DECIMAL(precision=21, scale=3), nullable=False),
    sa.Column('source_asset_code', sa.String(length=12), nullable=False),
    sa.Column('source_asset_issuer', sa.String(length=56), nullable=True),
    sa.Column('source_asset_amount', sa.DECIMAL(precision=21, scale=7), nullable=False),
    sa.Column('dest_asset_code', sa.String(length=12), nullable=False),
    sa.Column('dest_asset_issuer', sa.String(length=56), nullable=False),
    sa.Column('dest_asset_amount', sa.DECIMAL(precision=21, scale=7), nullable=False),
    sa.Column('vcs_project_id', sa.Integer(), nullable=False),
    sa.Column('memo_type', sa.Enum('text', 'hash', 'none', native_enum=False), nullable=False),
    sa.Column('memo_value', sa.String(length=64), nullable=True),
    sa.Column('paging_token', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['vcs_project_id'], ['vcs_projects.id'], ),
    sa.PrimaryKeyConstraint('hash')
    )
    op.create_table('test_retirement_from_block',
    sa.Column('retirement_id', sa.Integer(), nullable=False),
    sa.Column('block_hash', HexBinary(length=32), nullable=False),
    sa.Column('vcu_amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['block_hash'], ['minted_blocks.serial_hash'], ),
    sa.ForeignKeyConstraint(['retirement_id'], ['retirements.certificate_id'], ),
    sa.PrimaryKeyConstraint('retirement_id', 'block_hash')
    )
    op.create_table('test_sink_status',
    sa.Column('sinking_tx_hash', HexBinary(length=32), nullable=False),
    sa.Column('certificate_id', sa.Integer(), nullable=False),
    sa.Column('amount_filled', sa.DECIMAL(precision=21, scale=3), nullable=False),
    sa.Column('finalized', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['certificate_id'], ['retirements.certificate_id'], ),
    sa.ForeignKeyConstraint(['sinking_tx_hash'], ['sinking_txs.hash'], ),
    sa.PrimaryKeyConstraint('sinking_tx_hash', 'certificate_id')
    )


def downgrade() -> None:
    op.drop_table('test_sink_status')
    op.drop_table('test_retirement_from_block')
    op.drop_table('test_sinking_txs')
    op.drop_table('test_retirements')
    op.drop_table('test_minted_blocks')
    op.drop_table('test_vcs_projects')
    op.drop_table('test_distribution_txs')
