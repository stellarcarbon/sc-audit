"""
Load the relationships between retirements and minted blocks into the DB.

These relationships are implicit in the source data. Both minted blocks and retirements
are associated with serial numbers that specify a range of individual credits. This loader
module iterates over retirement records and finds the minted blocks that match their serial
numbers, storing the explicit relationships.

Author: Alex Olieman <https://keybase.io/alioli>
"""

from sqlalchemy import func, select
from sqlalchemy.orm import contains_eager

from sc_audit.db_schema.association import RetirementFromBlock
from sc_audit.db_schema.mint import MintedBlock
from sc_audit.db_schema.retirement import Retirement
from sc_audit.loader.utils import VcsSerialNumber
from sc_audit.session_manager import Session


def load_retirement_from_block():
    """
    Load the retirement—block associations to ensure that all retirements are explicitly covered
    by their originating blocks.
    """
    retirement_from_blocks = []
    with Session.begin() as session:
        # select the retirements that are not fully related to minted blocks
        query = (
            select(Retirement)
            .outerjoin(Retirement.retired_from)
            .group_by(Retirement.certificate_id)
            .having(func.total(RetirementFromBlock.vcu_amount) < Retirement.vcu_amount)
            .options(contains_eager(Retirement.retired_from))
        )
        uncovered_retirements = session.scalars(query).unique().all()
        for retirement in uncovered_retirements:
            from_blocks = cover_retirement(session, retirement)
            retirement_from_blocks += from_blocks

        session.add_all(retirement_from_blocks)

def cover_retirement(session, retirement: Retirement) -> list[RetirementFromBlock]:
    serial_number = VcsSerialNumber.from_str(retirement.serial_number)
    q_matching_blocks = (
        select(MintedBlock)
        # MintedBlock.block_start <= serial_number.block_start <= MintedBlock.block_end
        .where(MintedBlock.block_start <= serial_number.block_start)
        .where(serial_number.block_start <= MintedBlock.block_end)
        # MintedBlock.block_start <= serial_number.block_end <= MintedBlock.block_end
        .where(MintedBlock.block_start <= serial_number.block_end)
        .where(serial_number.block_end <= MintedBlock.block_end)
    )
    matching_blocks = session.scalars(q_matching_blocks).all()
    retirement_from_blocks = []
    for block in matching_blocks:
        rfb = RetirementFromBlock(
            retirement_id=retirement.certificate_id,
            block_hash=block.serial_hash,
            vcu_amount=overlap_size(serial_number, block)
        )
        # TODO: assert that the block isn't over-spent
        retirement_from_blocks.append(rfb)

    # TODO: assert that the retirement is completely covered
    return retirement_from_blocks

def overlap_size(serial_number: VcsSerialNumber, block: MintedBlock) -> int:
    return max(
        0, (
            1 + min(serial_number.block_end, block.block_end) 
            - max(serial_number.block_start, block.block_start)
        )
    )
