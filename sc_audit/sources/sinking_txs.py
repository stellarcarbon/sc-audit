"""
Fetch sinking transactions from Stellar Horizon.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from stellar_sdk import Server

from sc_audit.constants import FIRST_SINK_CURSOR, HORIZON_URL, SINK_ASSET, SINK_ISSUER_PUB


server = Server(horizon_url=HORIZON_URL)


def get_sinking_transactions(cursor: int=FIRST_SINK_CURSOR):
    query = (
        server.payments()
        .for_account(SINK_ISSUER_PUB)
        .cursor(cursor)
        .join("transactions")
        .order(desc=False)
        .limit(5)  # TODO: 200
    )
    resp = query.call()
    yield from filter_sinking_txs(resp['_embedded']['records'])
    while next_records := query.next()['_embedded']['records']:
        yield from filter_sinking_txs(next_records)


def filter_sinking_txs(horizon_records):
    for payment in horizon_records:
        if (
            payment['from'] == SINK_ISSUER_PUB
            and payment['asset_code'] == SINK_ASSET.code
        ):
            yield payment
