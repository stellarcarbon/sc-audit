"""
Load sinking transactions into the DB.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from decimal import Decimal
from typing import Any, Literal
from sqlalchemy import select

from sc_audit.constants import FIRST_SINK_CURSOR
from sc_audit.db_schema.base import intpk
from sc_audit.db_schema.impact_project import UnknownVcsProject, VcsProject
from sc_audit.db_schema.sink import SinkingTx
from sc_audit.loader.utils import decode_hash_memo, parse_iso_datetime
from sc_audit.session_manager import Session
from sc_audit.sources.sinking_txs import get_sinking_transactions, get_tx_operations


def load_sinking_txs(cursor: int=FIRST_SINK_CURSOR) -> int:
    """
    Load (all) sinking transactions from Horizon into the DB.

    To catch up with Horizon, specify the cursor parameter to be the incremented paging
    token of the latest record present in the DB.
    """
    number_loaded = 0

    with Session.begin() as session:
        existing_vcs_projects: set[intpk] = set(session.scalars(select(VcsProject.id)).all())
        for sink_tx in get_sinking_transactions(cursor):
            # ensure that the related VCS Project exists
            vcs_project_id = get_vcs_project_id(sink_tx)
            if vcs_project_id not in existing_vcs_projects:
                raise UnknownVcsProject(
                    f"VCS project {vcs_project_id} needs to be loaded before related transactions"
                    " can be stored. It may help to catch up on retirements first.",
                    vcs_id=vcs_project_id
                )
            
            tx_operations = get_tx_operations(sink_tx['transaction_hash'])
            payment_data = get_payment_data(tx_operations)
            memo_type = sink_tx['transaction']['memo_type']
            memo_value=sink_tx['transaction'].get('memo')
            if memo_type == 'hash':
                memo_value = decode_hash_memo(memo_value)

            session.add(
                SinkingTx(
                    hash=sink_tx['transaction_hash'],
                    created_at=parse_iso_datetime(sink_tx['created_at']),
                    funder=payment_data['funder'],
                    recipient=sink_tx['to'],
                    carbon_amount=Decimal(sink_tx['amount']),
                    source_asset_code=payment_data['source_asset_code'],
                    source_asset_issuer=payment_data['source_asset_issuer'],
                    source_asset_amount=Decimal(payment_data['source_asset_amount']),
                    dest_asset_code=payment_data['dest_asset_code'],
                    dest_asset_issuer=payment_data['dest_asset_issuer'],
                    dest_asset_amount=Decimal(payment_data['dest_asset_amount']),
                    vcs_project_id=vcs_project_id,
                    memo_type=memo_type,
                    memo_value=memo_value,
                    paging_token=sink_tx['paging_token'],
                )
            )
        
        number_loaded = len(session.new)

    return number_loaded


def get_vcs_project_id(sinking_tx) -> Literal[1360]:
    # TODO: support multiple VCS projects
    return 1360

def get_payment_data(transaction_operations: list[dict[str, Any]]) -> dict[str, Any]:
    for op in transaction_operations:
        # select the first payment operation
        if op['type_i'] in (1, 2, 13):
            source_asset_code = op.get('source_asset_code', op['asset_code'])
            source_asset_issuer = op.get('source_asset_issuer', op['asset_issuer'])
            if op.get('source_asset_type') == "native":
                source_asset_code = "XLM"
                source_asset_issuer = None

            return {
                'funder': op['from'],
                'source_asset_code': source_asset_code,
                'source_asset_issuer': source_asset_issuer,
                'source_asset_amount': op.get('source_amount', op['amount']),
                'dest_asset_code': op['asset_code'],
                'dest_asset_issuer': op['asset_issuer'],
                'dest_asset_amount': op['amount'],
            }
    else:
        raise ValueError("No payment operation found", transaction_operations)
