"""
View Stellarcarbon's current or historical inventory of eco-credits.

The inventory is calculated as: all blocks of credits that have been minted, minus the retirements
that have been taken from these blocks. Historical views reconstruct the inventory on the given
date (end-of-day) by filtering both the blocks and the retirements used in the calculation.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import datetime as dt

import pandas as pd
from sqlalchemy import select

from sc_audit.db_schema.impact_project import VcsProject
from sc_audit.db_schema.mint import MintedBlock
from sc_audit.session_manager import Session


def view_inventory(omit_empty: bool = False, until_date: dt.date | None = None) -> pd.DataFrame:
    credits_remaining_col = MintedBlock.credits_remaining
    if until_date:
        credits_remaining_col = MintedBlock.credits_remaining_on_date(until_date)

    block_columns = [
        MintedBlock.serial_hash,
        MintedBlock.size,
        credits_remaining_col,
        MintedBlock.transaction_hash,
        MintedBlock.created_at,
        MintedBlock.serial_number,
        MintedBlock.sub_account_id,
        MintedBlock.sub_account_name,
        MintedBlock.vintage_start,
        MintedBlock.vintage_end,
    ]
    vcs_project_columns = [
        MintedBlock.vcs_project_id,
        VcsProject.name,
        VcsProject.category,
    ]    
    columns = block_columns + vcs_project_columns
    q_blocks = select(*columns).join(MintedBlock.vcs_project).order_by(MintedBlock.created_at)
    if omit_empty:
        q_blocks = q_blocks.where(credits_remaining_col > 0)

    if until_date:
        until_dt = dt.datetime(until_date.year, until_date.month, until_date.day, 23, 59, 59, 999999)
        q_blocks = q_blocks.where(MintedBlock.created_at <= until_dt)

    with Session.begin() as session:
        mb_rows = session.execute(q_blocks).all()
        mbdf = pd.DataFrame.from_records(mb_rows, columns=(c.key for c in columns))

    return mbdf
