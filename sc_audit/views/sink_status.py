"""
View sinking transactions and their retirement status.

Transactions can be filtered by account, by date, and by their retirement status.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import datetime as dt

import pandas as pd
from sqlalchemy import Select, or_, select
from sqlalchemy.orm import contains_eager

from sc_audit.db_schema.association import SinkStatus
from sc_audit.db_schema.sink import SinkingTx
from sc_audit.session_manager import Session


def view_sinking_txs(
        for_funder: str | None = None,
        for_recipient: str | None = None, 
        from_date: dt.date | None = None,
        before_date: dt.date | None = None,
        finalized: bool | None = None,
) -> pd.DataFrame:
    # TODO: add SQL indexes to aid in filtering
    stx_query = construct_stx_query(for_funder, for_recipient, from_date, before_date, finalized)
    with Session.begin() as session:
        stx_records = session.scalars(stx_query).unique().all()
        txdf = pd.DataFrame.from_records(stx.as_dict() for stx in stx_records)

    return txdf
    
def construct_stx_query(
        for_funder: str | None,
        for_recipient: str | None, 
        from_date: dt.date | None,
        before_date: dt.date | None,
        finalized: bool | None,
) -> Select[tuple[SinkingTx]]:
    q_txs = select(SinkingTx).outerjoin(SinkStatus).options(contains_eager(SinkingTx.statuses))
    if for_funder:
        q_txs = q_txs.where(SinkingTx.funder == for_funder)

    if for_recipient:
        q_txs = q_txs.where(SinkingTx.funder == for_recipient)

    if from_date:
        q_txs = q_txs.where(SinkingTx.created_at >= from_date)

    if before_date:
        q_txs = q_txs.where(SinkingTx.created_at < before_date)

    if finalized is False:
        # not_ and in_ do not work here because NULL and false are treated differently
        q_txs = q_txs.where(or_(SinkStatus.finalized == None, SinkStatus.finalized == False))
    elif finalized is True:
        q_txs = q_txs.where(SinkStatus.finalized == True)

    return q_txs
