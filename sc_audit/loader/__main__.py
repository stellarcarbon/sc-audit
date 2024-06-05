"""
Load all database records in the order:
  1. Retirements
  2. Sinking Transactions
  3. Minted Blocks
  4. Retirement from Block
  5. Sink Statuses

Bootstrap the loading process by restoring a DB dump before catching up from live sources.
Do not restore a dump first if a fresh load is requested. This may fail if a Horizon instance
with pruned history is selected. You may select another with the SC_HORIZON_URL env variable.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from sqlalchemy import select

from sc_audit.db_schema.mint import MintedBlock
from sc_audit.db_schema.retirement import Retirement
from sc_audit.db_schema.sink import SinkingTx
from sc_audit.loader.minted_blocks import FIRST_MINT_CURSOR, load_minted_blocks
from sc_audit.loader.retirement_from_block import load_retirement_from_block
from sc_audit.loader.retirements import load_retirements
from sc_audit.loader.sink_status import load_sink_statuses
from sc_audit.loader.sinking_txs import FIRST_SINK_CURSOR, load_sinking_txs
from sc_audit.session_manager import Session


def catch_up_from_sources():
    """
    Ensure that the latest available data is loaded from the original sources.
    Avoid loading duplicate records by filtering on cursor or date where possible.
    """
    with Session.begin() as session:
        latest_retirement_date = session.scalar(
            select(Retirement.retirement_date).order_by(Retirement.retirement_date.desc())
        )
        latest_sink_tx_cursor = session.scalar(
            select(SinkingTx.paging_token).order_by(SinkingTx.created_at.desc())
        )
        latest_mint_tx_cursor = session.scalar(
            select(MintedBlock.paging_token).order_by(MintedBlock.created_at.desc())
        )

    print("Started catch-up from data sources...")
    num_retirements = load_retirements(from_date=latest_retirement_date)
    print(f"Loaded {num_retirements} retirements")
    num_sinking_txs = load_sinking_txs(cursor=latest_sink_tx_cursor or FIRST_SINK_CURSOR)
    print(f"Loaded {num_sinking_txs} sinking transactions")
    num_minting_txs = load_minted_blocks(cursor=latest_mint_tx_cursor or FIRST_MINT_CURSOR)
    print(f"Loaded {num_minting_txs} minted blocks")
    num_retirement_from_block = load_retirement_from_block()
    print(f"Loaded {num_retirement_from_block} retirement-from-block associations")
    num_sink_statuses = load_sink_statuses()
    print(f"Loaded {num_sink_statuses} sink status associations")


if __name__ == "__main__":
    catch_up_from_sources()
