"""
Load minted blocks of CARBON into the DB.

Minted blocks are reconstructed using the relationship between minting transactions and
registry sources. Every carbon credit that is minted is either still in the inventory
or it has already been retired. Blocks that have not yet been used for retirements have a
corresponding serial number hash memo on their minting tx. Serial numbers of any blocks that
have been fully or partly used for retirements are reconstructed on the basis of the serial
numbers of the retired credits.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from hashlib import sha256
from typing import Any, Literal, Sequence

from sqlalchemy import select

from sc_audit.constants import FIRST_MINT_CURSOR
from sc_audit.db_schema.impact_project import UnknownVcsProject, VcsProject
from sc_audit.db_schema.mint import MintedBlock, verra_carbon_pool
from sc_audit.db_schema.retirement import Retirement
from sc_audit.loader.utils import VcsSerialNumber, decode_hash_memo, parse_iso_datetime
from sc_audit.session_manager import Session
from sc_audit.sources.carbon_pool import get_carbon_pool_state
from sc_audit.sources.minting_txs import get_minting_transactions


def load_minted_blocks(cursor: int=FIRST_MINT_CURSOR) -> int:
    """
    Load (all) minting transactions from Horizon into the DB.

    To catch up with Horizon, specify the cursor parameter to be the incremented paging
    token of the latest record present in the DB.
    """
    retired_blocks: list[dict[str, Any]] = []
    pristine_blocks: list[MintedBlock] = []
    carbon_pool = index_carbon_pool()
    with Session.begin() as session:
        existing_vcs_projects: set[int] = set(session.scalars(select(VcsProject.id)).all())
        for mint_tx in get_minting_transactions(cursor):
            # ensure that the related VCS Project exists
            vcs_project_id = get_vcs_project_id(mint_tx)
            if vcs_project_id not in existing_vcs_projects:
                raise UnknownVcsProject(
                    f"VCS project {vcs_project_id} needs to be loaded before related transactions"
                    " can be stored. It may help to catch up on retirements first.",
                    vcs_id=vcs_project_id
                )
            # check whether the block is pristine
            serial_hash = decode_hash_memo(mint_tx['transaction']['memo'])
            if serial_hash in carbon_pool:
                serial_number = VcsSerialNumber.from_str(carbon_pool[serial_hash]['serial_number']) # type: ignore
                block = MintedBlock(
                    serial_hash=serial_hash,
                    transaction_hash=mint_tx['transaction_hash'],
                    created_at=parse_iso_datetime(mint_tx['created_at']),
                    vcs_project_id=vcs_project_id,
                    serial_number=serial_number.to_str(),
                    block_start=serial_number.block_start,
                    block_end=serial_number.block_end,
                    sub_account_id=carbon_pool[serial_hash]['sub_account_id'], # type: ignore
                    sub_account_name=carbon_pool[serial_hash]['sub_account_name'], # type: ignore
                    vintage_start=serial_number.vintage_start_date,
                    vintage_end=serial_number.vintage_end_date,
                    paging_token=mint_tx['paging_token']
                )
                pristine_blocks.append(block)
            else:
                retired_blocks.append(mint_tx)

        if retired_blocks:
            latest_loaded_block: MintedBlock | None = session.scalars(
                select(MintedBlock).order_by(MintedBlock.paging_token.desc())
            ).first()
            # select only retirements without retired_from_block relations
            retirements: Sequence[Retirement] = session.scalars(
                select(Retirement).where(~Retirement.retired_from.any())
            ).all()
            reconstructed_blocks = reconstruct_blocks(
                retired_blocks, latest_loaded_block, retirements
            )
            session.add_all(reconstructed_blocks)

        session.add_all(pristine_blocks)

    return len(retired_blocks) + len(pristine_blocks)
            
            
def get_vcs_project_id(sinking_tx) -> Literal[1360]:
    # TODO: support multiple VCS projects
    return 1360

def index_carbon_pool() -> dict[str, dict[str, str | int]]:
    """
    Index current blocks in the carbon pool by sha256(serial_number).    
    """
    indexed_pool = {}
    carbon_pool = get_carbon_pool_state()
    for block in carbon_pool['credit_batches']:
        serial_number_hash = sha256(block['serial_number'].encode('utf8')).hexdigest()
        indexed_pool[serial_number_hash] = block

    return indexed_pool

def reconstruct_blocks(
        mint_txs: list[dict[str, Any]],
        latest_block: MintedBlock | None,
        retirements: Sequence[Retirement]
    ) -> list[MintedBlock]:
    """
    Attempt to reconstruct blocks by:
    1. checking if the block directly follows the last known block
    2. finding the first retirement done from the block
    """
    reconstructed_blocks: list[MintedBlock] = []
    for mint_tx in mint_txs:
        vcs_project_id = get_vcs_project_id(mint_tx)
        serial_hash = decode_hash_memo(mint_tx['transaction']['memo'])
        block_size = int(float(mint_tx['amount']))
        # check if this block is an extension of the previous block
        if latest_block:
            reconstructed_serial = VcsSerialNumber.from_str(latest_block.serial_number)
            reconstructed_serial.block_start = 1 + reconstructed_serial.block_end
            reconstructed_serial.block_end = (block_size - 1) + reconstructed_serial.block_start
            sub_account_id = latest_block.sub_account_id
            sub_account_name = latest_block.sub_account_name

        # keep looking, unless there is a latest block and the reconstructed serial matches the known hash
        if not (latest_block and serial_matches_hash(reconstructed_serial, serial_hash)):
            for retirement in retirements:
                # find the retirement of the first credit from this block
                reconstructed_serial = VcsSerialNumber.from_str(retirement.serial_number)
                reconstructed_serial.block_end = (block_size - 1) + reconstructed_serial.block_start
                if serial_matches_hash(reconstructed_serial, serial_hash):
                    sub_account_id = verra_carbon_pool.id
                    sub_account_name = verra_carbon_pool.name
                    break
            else:
                raise ValueError(f"No match found for serial hash {serial_hash}.", serial_hash)

        block = MintedBlock(
            serial_hash=serial_hash,
            transaction_hash=mint_tx['transaction_hash'],
            created_at=parse_iso_datetime(mint_tx['created_at']),
            vcs_project_id=vcs_project_id,
            serial_number=reconstructed_serial.to_str(),
            block_start=reconstructed_serial.block_start,
            block_end=reconstructed_serial.block_end,
            sub_account_id=sub_account_id,
            sub_account_name=sub_account_name,
            vintage_start=reconstructed_serial.vintage_start_date,
            vintage_end=reconstructed_serial.vintage_end_date,
            paging_token=mint_tx['paging_token']
        )
        latest_block = block
        reconstructed_blocks.append(block)

    assert len(reconstructed_blocks) == len(mint_txs)
    return reconstructed_blocks

def serial_matches_hash(reconstructed_serial: VcsSerialNumber, serial_hash: str) -> bool:
    """
    Test whether the given serial number corresponds to the known hash.
    """
    reconstructed_serial_hash = sha256(
        reconstructed_serial.to_str().encode('utf8')
    ).hexdigest()
    return serial_hash == reconstructed_serial_hash
