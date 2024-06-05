"""
Load the relationships between retirements and minted blocks into the DB.

These relationships are implicit in the source data. Both minted blocks and retirements
are associated with serial numbers that specify a range of individual credits. This loader
module iterates over retirement records and finds the minted blocks that match their serial
numbers, storing the explicit relationships.

Author: Alex Olieman <https://keybase.io/alioli>
"""

from sqlalchemy import and_, func, or_, select

from sc_audit.db_schema.association import RetirementFromBlock
from sc_audit.db_schema.mint import MintedBlock
from sc_audit.db_schema.retirement import Retirement
from sc_audit.loader.utils import VcsSerialNumber
from sc_audit.session_manager import Session


def load_retirement_from_block() -> int:
    """
    Load the retirement—block associations to ensure that all retirements are explicitly covered
    by their originating blocks.
    """
    number_loaded = 0

    with Session.begin() as session:
        # select the retirements that are not fully related to minted blocks
        query = (
            select(Retirement)
            .outerjoin(Retirement.retired_from)
            .group_by(Retirement.certificate_id)
            .having(func.total(RetirementFromBlock.vcu_amount) < Retirement.vcu_amount)
        )
        uncovered_retirements = session.scalars(query).unique().all()
        for retirement in uncovered_retirements:
            from_blocks = cover_retirement(session, retirement)
            session.add_all(from_blocks)
            number_loaded += len(from_blocks)

    return number_loaded

def cover_retirement(session, retirement: Retirement) -> list[RetirementFromBlock]:
    serial_number = VcsSerialNumber.from_str(retirement.serial_number)
    q_matching_blocks = (
        select(MintedBlock).where(
            or_(
                # MintedBlock.block_start <= serial_number.block_start <= MintedBlock.block_end
                and_(
                    MintedBlock.block_start <= serial_number.block_start,
                    serial_number.block_start <= MintedBlock.block_end
                ),
                # MintedBlock.block_start <= serial_number.block_end <= MintedBlock.block_end
                and_(
                    MintedBlock.block_start <= serial_number.block_end,
                    serial_number.block_end <= MintedBlock.block_end
                ),
                # serial_number.block_start <= MintedBlock.block_start <= serial_number.block_end
                # serial_number.block_start <= MintedBlock.block_end <= serial_number.block_end
                and_(
                    MintedBlock.block_start.between(serial_number.block_start, serial_number.block_end),
                    MintedBlock.block_end.between(serial_number.block_start, serial_number.block_end)
                )
            )
        )
    )
    matching_blocks = session.scalars(q_matching_blocks).all()
    retirement_from_blocks = []
    for block in matching_blocks:
        rfb = RetirementFromBlock(
            retirement_id=retirement.certificate_id,
            block_hash=block.serial_hash,
            vcu_amount=overlap_size(serial_number, block)
        )
        raise_if_overspent(block, rfb)
        retirement_from_blocks.append(rfb)

    raise_if_uncovered(retirement, retirement_from_blocks)
    return retirement_from_blocks

def overlap_size(serial_number: VcsSerialNumber, block: MintedBlock) -> int:
    return max(
        0, (
            1 + min(serial_number.block_end, block.block_end) 
            - max(serial_number.block_start, block.block_start)
        )
    )


class BlockOverspent(Exception):
    def __init__(self, msg, block_hash: str, certificate_id: int):
        super().__init__(msg, block_hash, certificate_id)

def raise_if_overspent(block: MintedBlock, retirement_from_block: RetirementFromBlock):
    if retirement_from_block.vcu_amount > block.credits_remaining:
        raise BlockOverspent(
            f"Retiring {retirement_from_block.retirement_id} from block {block.serial_hash}"
            " would cause it to be overspent.",
            block_hash=block.serial_hash,
            certificate_id=retirement_from_block.retirement_id
        )
    

class CoveringBlockMissing(Exception):
    def __init__(self, msg, retirement: Retirement, new_blocks: list[RetirementFromBlock]):
        super().__init__(msg, retirement, new_blocks)

def raise_if_uncovered(retirement: Retirement, new_blocks: list[RetirementFromBlock]):
    new_coverage: int = sum(rfb.vcu_amount for rfb in new_blocks)
    if retirement.vcu_amount > new_coverage:
        raise CoveringBlockMissing(
            f"Retirement {retirement.certificate_id} is not fully covered by known blocks.",
            retirement=retirement,
            new_blocks=new_blocks
        )
