"""
Fetch sink events from Mercury Retroshades.

Author: Alex Olieman <https://keybase.io/alioli>
"""

import datetime as dt
from decimal import Decimal

import httpx
from pydantic import BaseModel
from stellar_sdk.sep.toid import TOID

from sc_audit.config import settings

UNIT_IN_STROOPS = 10_000_000


class SinkEvent(BaseModel):
    transaction: str
    created_at: dt.datetime
    contract_id: str
    funder: str
    recipient: str
    amount: Decimal
    project_id: str
    memo_text: str | None
    email: str | None
    ledger: int

    @classmethod
    def from_raw(cls, **data):
        data["amount"] = data["amount"] / UNIT_IN_STROOPS
        data["created_at"] = dt.datetime.fromtimestamp(data["timestamp"], dt.UTC)
        return cls(**data)


def get_sink_events(cursor: int=settings.FIRST_SINK_CURSOR) -> list[SinkEvent]:
    headers = {
        "Authorization": settings.MERCURY_KEY,
        "Content-Type": "application/json",
    }
    ledger_from_toid = TOID.from_int64(cursor).ledger_sequence
    with httpx.Client(headers=headers) as client:
        payload = {
            "query": f"""
                SELECT * FROM sink_event{settings.RETROSHADES_MD5}
                WHERE ledger > {ledger_from_toid}
            """
        }
        resp: httpx.Response = client.post(
            url=str(settings.RETROSHADES_URL),
            json=payload,
        )
        resp.raise_for_status()
        events = resp.json()

    return [SinkEvent.from_raw(**event) for event in events]


if __name__ == "__main__":
    sink_events = get_sink_events(cursor=0)
    pass
