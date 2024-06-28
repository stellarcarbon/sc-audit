"""
Load all database records in the order:
  1. Retirements
  2. Sinking Transactions
  3. Minted Blocks
  4. Retirement from Block
  5. Sink Statuses

Loading from scratch may fail if a Horizon instance with pruned history is selected.
You may select another instance with the SC_HORIZON_URL env variable.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import datetime as dt

from sc_audit.loader.distribution_outflows import load_distribution_txs
from sc_audit.loader.get_latest import get_latest_attr
from sc_audit.loader.minted_blocks import load_minted_blocks
from sc_audit.loader.retirement_from_block import load_retirement_from_block
from sc_audit.loader.retirements import load_retirements
from sc_audit.loader.sink_status import load_sink_statuses
from sc_audit.loader.sinking_txs import load_sinking_txs


def catch_up_from_sources():
    """
    Ensure that the latest available data is loaded from the original sources.
    Avoid loading duplicate records by filtering on cursor or date where possible.
    """
    retirement_date: dt.date
    sink_cursor: int
    mint_cursor: int
    dist_cursor: int
    retirement_date, sink_cursor, mint_cursor, dist_cursor = get_latest_attr(
        'retirement', 
        'sink_tx', 
        'mint_tx',
        'dist_tx'
    ) # type: ignore

    print("Started catch-up from data sources...")
    num_distribution_txs = load_distribution_txs(cursor=dist_cursor)
    print(f"Loaded {num_distribution_txs} distribution outflows")
    num_retirements = load_retirements(from_date=retirement_date)
    print(f"Loaded {num_retirements} retirements")
    num_sinking_txs = load_sinking_txs(cursor=sink_cursor)
    print(f"Loaded {num_sinking_txs} sinking transactions")
    num_minting_txs = load_minted_blocks(cursor=mint_cursor)
    print(f"Loaded {num_minting_txs} minted blocks")
    num_retirement_from_block = load_retirement_from_block()
    print(f"Loaded {num_retirement_from_block} retirement-from-block associations")
    num_sink_statuses = load_sink_statuses()
    print(f"Loaded {num_sink_statuses} sink status associations")


if __name__ == "__main__":
    catch_up_from_sources()
