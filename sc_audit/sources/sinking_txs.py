"""
Fetch sinking transactions from Stellar Horizon.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from stellar_sdk import Server
from stellar_sdk.server import OperationsCallBuilder, PaymentsCallBuilder

from sc_audit.config import settings


server = Server(horizon_url=str(settings.HORIZON_URL))


def get_sinking_transactions(cursor: int=settings.FIRST_SINK_CURSOR):
    query: PaymentsCallBuilder = (
        server.payments()
        .for_account(settings.SINK_ISSUER_PUB)
        .cursor(cursor)
        .join("transactions")
        .order(desc=False)
        .limit(200)
    )
    resp = query.call()
    yield from filter_sinking_txs(resp['_embedded']['records'])
    while next_records := query.next()['_embedded']['records']:
        yield from filter_sinking_txs(next_records)

def filter_sinking_txs(horizon_records):
    for payment in horizon_records:
        if (
            payment["type_i"] == 1
            and payment['from'] == settings.SINK_ISSUER_PUB
            and payment['asset_code'] == settings.SINK_ASSET.code
        ):
            yield payment

def get_tx_operations(tx_hash: str) -> list[dict]:
    query: OperationsCallBuilder = server.operations().for_transaction(tx_hash)
    resp = query.call()
    return resp['_embedded']['records']
