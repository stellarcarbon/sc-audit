"""
Fetch minting transactions from Stellar Horizon.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from stellar_sdk import Server
from stellar_sdk.server import PaymentsCallBuilder

from sc_audit.constants import (
    CARBON_ASSET,
    CARBON_DISTRIB_PUB, 
    CARBON_ISSUER_PUB, 
    FIRST_DIST_CURSOR,
    FIRST_MINT_CURSOR, 
    HORIZON_URL,
)

server = Server(horizon_url=HORIZON_URL)


def get_minting_transactions(cursor: int=FIRST_MINT_CURSOR):
    query: PaymentsCallBuilder = (
        server.payments()
        .for_account(CARBON_ISSUER_PUB)
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
            payment['from'] == CARBON_ISSUER_PUB
            and payment['to'] == CARBON_DISTRIB_PUB
            and payment['asset_code'] == CARBON_ASSET.code
        ):
            yield payment


def get_carbon_outflows(cursor: int=FIRST_DIST_CURSOR):
    query: PaymentsCallBuilder = (
        server.payments()
        .for_account(CARBON_DISTRIB_PUB)
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
            and payment["from"] == CARBON_DISTRIB_PUB
            and payment["asset_code"] == CARBON_ASSET.code
            and payment["asset_issuer"] == CARBON_ASSET.issuer
        ):
            yield payment
