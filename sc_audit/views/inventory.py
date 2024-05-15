"""
View Stellarcarbon's current or historical inventory of eco-credits.

The inventory is calculated as: all blocks of credits that have been minted, minus the retirements
that have been taken from these blocks.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import datetime as dt

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import InstrumentedAttribute, QueryableAttribute

from sc_audit.db_schema.impact_project import VcsProject
from sc_audit.db_schema.mint import MintedBlock
from sc_audit.session_manager import Session


def view_inventory(omit_empty: bool = False, until_date: dt.date | None = None) -> pd.DataFrame:
    columns = (
        MintedBlock.serial_hash,
        MintedBlock.transaction_hash,
        MintedBlock.created_at,
        MintedBlock.serial_number,
        MintedBlock.sub_account_id,
        MintedBlock.sub_account_name,
        MintedBlock.vintage_start,
        MintedBlock.vintage_end,
        MintedBlock.vcs_project_id,
        VcsProject.name,
        VcsProject.category,
        MintedBlock.size,
        MintedBlock.credits_remaining,
    )
    # TODO: implement filters
    q_blocks = select(*columns).join(MintedBlock.vcs_project).order_by(MintedBlock.created_at)
    with Session.begin() as session:
        mb_rows = session.execute(q_blocks).all()
        mbdf = pd.DataFrame.from_records(mb_rows, columns=(c.key for c in columns))

    return mbdf


if __name__ == "__main__":
    view_inventory()
