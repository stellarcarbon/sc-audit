"""
Fetch minting transactions from Stellar Horizon.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from stellar_sdk import Server
from stellar_sdk.server import PaymentsCallBuilder

from sc_audit.config import settings

server = Server(horizon_url=str(settings.HORIZON_URL))


def get_minting_transactions(cursor: int=settings.FIRST_MINT_CURSOR):
    query: PaymentsCallBuilder = (
        server.payments()
        .for_account(settings.CARBON_ISSUER_PUB)
        .cursor(cursor)
        .join("transactions")
        .order(desc=False)
        .limit(200)
    )
    resp = query.call()
    yield from filter_minting_txs(resp['_embedded']['records'])
    while next_records := query.next()['_embedded']['records']:
        yield from filter_minting_txs(next_records)

def filter_minting_txs(horizon_records):
    for payment in horizon_records:
        if (
            payment['from'] == settings.CARBON_ISSUER_PUB
            and payment['to'] == settings.CARBON_DISTRIB_PUB
            and payment['asset_code'] == settings.CARBON_ASSET.code
        ):
            yield payment


def get_carbon_outflows(cursor: int=settings.FIRST_DIST_CURSOR):
    query: PaymentsCallBuilder = (
        server.payments()
        .for_account(settings.CARBON_DISTRIB_PUB)
        .cursor(cursor)
        .order(desc=False)
        .limit(200)
    )
    resp = query.call()
    yield from filter_distribution_txs(resp['_embedded']['records'])
    while next_records := query.next()['_embedded']['records']:
        yield from filter_distribution_txs(next_records)

def filter_distribution_txs(horizon_records):
    for payment in horizon_records:
        if (
            payment["type_i"] == 1
            and payment["from"] == settings.CARBON_DISTRIB_PUB
            and payment["asset_code"] == settings.CARBON_ASSET.code
            and payment["asset_issuer"] == settings.CARBON_ASSET.issuer
        ):
            yield payment
