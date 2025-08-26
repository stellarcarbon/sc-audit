"""
Fetch sink_carbon invocations from Obsrver Flow.

Author: Alex Olieman <https://keybase.io/alioli>
"""

import datetime as dt
from decimal import ROUND_DOWN, Decimal
from typing import Sequence

from sqlalchemy import URL, Engine, create_engine, make_url, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, Session

from sc_audit.config import settings
from sc_audit.constants import KG, UNIT_IN_STROOPS
from sc_audit.db_schema.base import bigint, intpk


class FlowBase(MappedAsDataclass, DeclarativeBase): ...


class SinkInvocation(FlowBase):
    __tablename__ = settings.OBSRVR_FLOW_TABLE

    id: Mapped[intpk]
    toid: Mapped[bigint]
    ledger: Mapped[int]
    timestamp: Mapped[dt.datetime]
    contract_id: Mapped[str]
    function_name: Mapped[str]
    invoking_account: Mapped[str]
    tx_hash: Mapped[str]

    funder: Mapped[str]
    recipient: Mapped[str]
    amount: Mapped[bigint]
    project_id: Mapped[str]
    memo_text: Mapped[str | None]
    email: Mapped[str | None]

    processed_at: Mapped[dt.datetime]
    schema_name: Mapped[str]
    successful: Mapped[bool]
    created_at: Mapped[dt.datetime]

    @hybrid_property
    def ton_amount(self) -> Decimal:
        return (self.amount / UNIT_IN_STROOPS).quantize(KG, rounding=ROUND_DOWN)
    

class ObsrvrError(Exception):
    def __init__(self, msg, dsn_uri: str | None):
        super().__init__(msg, dsn_uri)
    

class InvocationSource:
    db_url: URL | None
    engine: Engine | None

    if not settings.OBSRVR_FLOW_DB_URI:
        db_url = None
        engine = None
    elif settings.MERCURY_KEY:
        raise ObsrvrError(
            "Only one of MERCURY_KEY and OBSRVR_FLOW_DB_URI may be provided.",
            dsn_uri=str(settings.OBSRVR_FLOW_DB_URI)
        )
    else:
        db_url = make_url(str(settings.OBSRVR_FLOW_DB_URI))
        engine = create_engine(db_url)

    @classmethod
    def get_sink_invocations(cls, cursor: int=settings.FIRST_SINK_CURSOR) -> Sequence[SinkInvocation]:
        if not cls.engine:
            raise ObsrvrError(
                "Skip sink invocations: Obsrvr DB URI is not set in the configuration.",
                dsn_uri=None
            )

        query = select(SinkInvocation).where(SinkInvocation.toid > cursor)
        
        with Session(cls.engine, expire_on_commit=False) as session:
            invokes = session.scalars(query).all()

        return invokes


if __name__ == "__main__":
    sink_events = InvocationSource.get_sink_invocations(cursor=0)
    pass
