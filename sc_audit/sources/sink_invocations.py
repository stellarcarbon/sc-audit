"""
Fetch sink_carbon invocations from Obsrver Flow.

Author: Alex Olieman <https://keybase.io/alioli>
"""

import datetime as dt
from decimal import Decimal

from pydantic import BaseModel
from sqlalchemy import create_engine, make_url, select, Table, MetaData

from sc_audit.config import settings


UNIT_IN_STROOPS = 10_000_000


class SinkInvocation(BaseModel):
    id: int
    toid: int
    ledger: int
    tx_hash: str
    created_at: dt.datetime
    contract_id: str
    function_name: str
    invoking_account: str
    processed_at: dt.datetime
    schema_name: str
    successful: bool

    funder: str
    recipient: str
    amount: Decimal
    project_id: str
    memo_text: str | None
    email: str | None

    @classmethod
    def from_raw(cls, **data):
        data["amount"] = data["amount"] / UNIT_IN_STROOPS
        data["created_at"] = data["timestamp"]
        return cls(**data)


def get_sink_invocations(cursor: int=settings.FIRST_SINK_CURSOR) -> list[SinkInvocation]:
    if not settings.OBSRVR_FLOW_DB_URI:
        raise ObsrvrError(
             "Skip sink invocations: Obsrvr DB URI is not set in the configuration.",
             dsn_uri=None
        )
    elif settings.MERCURY_KEY:
        raise ObsrvrError(
            "Only one of MERCURY_KEY and OBSRVR_FLOW_DB_URI may be provided.",
            dsn_uri=str(settings.OBSRVR_FLOW_DB_URI)
        )

    db_url = make_url(str(settings.OBSRVR_FLOW_DB_URI))
    engine = create_engine(db_url)
    
    with engine.begin() as conn:
        metadata = MetaData()
        sink_table = Table(
            settings.OBSRVR_FLOW_TABLE,
            metadata,
            autoload_with=conn
        )
        result = conn.execute(
            select(sink_table).where(sink_table.c.toid > cursor)
        )    

    return [SinkInvocation.from_raw(**row._mapping) for row in result]


class ObsrvrError(Exception):
    def __init__(self, msg, dsn_uri: str | None):
        super().__init__(msg, dsn_uri)



if __name__ == "__main__":
    sink_events = get_sink_invocations(cursor=0)
    pass
