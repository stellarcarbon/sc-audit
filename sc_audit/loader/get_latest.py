"""
Helper functions to load only new records from data sources.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import datetime as dt
from typing import Literal, Union

from sqlalchemy import select
from stellar_sdk.sep.toid import TOID

from sc_audit.constants import FIRST_MINT_CURSOR, FIRST_SINK_CURSOR
from sc_audit.db_schema.mint import MintedBlock
from sc_audit.db_schema.retirement import Retirement
from sc_audit.db_schema.sink import SinkingTx
from sc_audit.session_manager import Session


CoreModelName = Literal['mint_tx', 'retirement', 'sink_tx']
LatestAttr = Union[dt.date, int, None]

def get_latest_attr(*models: CoreModelName) -> LatestAttr | list[LatestAttr]:
    latest_attrs: list[LatestAttr] = [None] * len(models)
    with Session.begin() as session:
        for i, model in enumerate(models):
            if model == 'retirement':
                latest_retirement_date = session.scalar(
                    select(Retirement.retirement_date).order_by(Retirement.retirement_date.desc())
                )
                latest_attrs[i] = latest_retirement_date
            elif model == 'sink_tx':
                latest_sink_tx_cursor = session.scalar(
                    select(SinkingTx.paging_token).order_by(SinkingTx.created_at.desc())
                )
                latest_attrs[i] = increment_paging_token(latest_sink_tx_cursor) or FIRST_SINK_CURSOR
            elif model == 'mint_tx':
                latest_mint_tx_cursor = session.scalar(
                    select(MintedBlock.paging_token).order_by(MintedBlock.created_at.desc())
                )
                latest_attrs[i] = increment_paging_token(latest_mint_tx_cursor) or FIRST_MINT_CURSOR

    if len(latest_attrs) == 1:
        return latest_attrs[0]
    else:
        return latest_attrs


def increment_paging_token(cursor: int | None) -> int | None:
    if cursor:
        toid = TOID.from_int64(cursor)
        toid.increment_operation_order()
        cursor = toid.to_int64()

    return cursor
