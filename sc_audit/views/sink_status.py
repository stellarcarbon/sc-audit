"""
View sinking transactions and their retirement status.

Transactions can be filtered by account, by date, and by their retirement status.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import datetime as dt
from typing import Any, Literal

import pandas as pd
from sqlalchemy import Select, exists, not_, select
from sqlalchemy.orm import contains_eager, selectinload

from sc_audit.db_schema.association import SinkStatus
from sc_audit.db_schema.sink import SinkingTx
from sc_audit.session_manager import Session


def view_sinking_txs(
        for_funder: str | None = None,
        for_recipient: str | None = None, 
        from_date: dt.date | None = None,
        before_date: dt.date | None = None,
        finalized: bool | None = None,
        cursor: int | None = None,
        limit: int | None = None,
        order: Literal['asc', 'desc'] = 'desc',
) -> pd.DataFrame:
    base_query = construct_stx_query(
        for_funder, for_recipient, from_date, before_date, finalized
    ).subquery()
    subq_paging_token = base_query.c.paging_token
    # Determine order and cursor filter
    if order == 'asc':
        subq_order = subq_paging_token.asc()
        stx_order = SinkingTx.paging_token.asc()
        cursor_filter = subq_paging_token > (cursor or 0)
    elif order == 'desc':
        subq_order = subq_paging_token.desc()
        stx_order = SinkingTx.paging_token.desc()
        cursor_filter = subq_paging_token < (cursor or 0)

    with Session.begin() as session:
        # Step 1: Get unique paging_tokens for the page
        token_query = select(subq_paging_token).select_from(base_query)
        if cursor and cursor > 0:
            token_query = token_query.where(cursor_filter)
        
        token_query = token_query.order_by(subq_order).distinct().limit(limit)
        paging_tokens = session.scalars(token_query).all()

        if not paging_tokens:
            return pd.DataFrame()

        # Step 2: Fetch SinkingTxs for those paging_tokens, eager load statuses
        stx_query = (
            select(SinkingTx)
            .outerjoin(SinkStatus)
            .options(contains_eager(SinkingTx.statuses))
            .where(SinkingTx.paging_token.in_(paging_tokens))
            .order_by(stx_order)
        )
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
    # Only build the base query and filters
    q_txs = select(SinkingTx)
    if for_funder:
        q_txs = q_txs.where(SinkingTx.funder == for_funder)
    
    if for_recipient:
        q_txs = q_txs.where(SinkingTx.recipient == for_recipient)
    
    if from_date:
        from_dt = dt.datetime(from_date.year, from_date.month, from_date.day)
        q_txs = q_txs.where(SinkingTx.created_at >= from_dt)
    
    if before_date:
        before_dt = dt.datetime(before_date.year, before_date.month, before_date.day)
        q_txs = q_txs.where(SinkingTx.created_at < before_dt)
    
    if finalized is False:
        # filter on sink txs without any SinkStatus with finalized=True
        # this clause needs to be the perfect negation of `finalized is True`
        q_txs = q_txs.where(
            not_(exists().where(
                SinkStatus.sinking_tx_hash == SinkingTx.hash, SinkStatus.finalized == True
            ).correlate(SinkingTx))
        )
    elif finalized is True:
        # select sink txs that have at least one SinkStatus with finalized=True
        q_txs = q_txs.outerjoin(SinkStatus).where(SinkStatus.finalized == True)
    
    return q_txs


def get_sinking_tx(hash: str) -> dict[str, Any] | None:
    stx_query = (
        select(SinkingTx)
        .options(selectinload(SinkingTx.statuses))
        .where(SinkingTx.hash == hash)
    )
    with Session.begin() as session:
        stx = session.scalar(stx_query)
        stx_data = stx.as_dict() if stx else None

    return stx_data
