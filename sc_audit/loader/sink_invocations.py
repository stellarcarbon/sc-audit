"""
Load sink invocations from sorocarbon into the DB as SinkingTx records.

Author: Alex Olieman <https://keybase.io/alioli>
"""

from sc_audit.config import settings
from sc_audit.db_schema.sink import SinkingTx
from sc_audit.loader.sink_events import try_project_id
from sc_audit.session_manager import Session
from sc_audit.sources.sink_invocations import InvocationSource


def load_sink_invocations(cursor: int=settings.FIRST_SINK_CURSOR) -> int:
    """
    Load (all) sink invocations from Obsrvr Flow into the DB.

    To catch up with Flow, specify the cursor parameter to be the paging token
    of the latest sink invocation record present in the SinkingTx table.
    """
    number_loaded = 0

    with Session.begin() as session:
        for sink_invoke in InvocationSource.get_sink_invocations(cursor):
            vcs_project_id = try_project_id(sink_invoke.project_id)
            memo = sink_invoke.memo_text or None
            session.add(
                SinkingTx(
                    hash=sink_invoke.tx_hash,
                    created_at=sink_invoke.timestamp,
                    contract_id=sink_invoke.contract_id,
                    funder=sink_invoke.funder,
                    recipient=sink_invoke.recipient,
                    carbon_amount=sink_invoke.ton_amount,
                    source_asset_code=settings.CARBON_ASSET.code,
                    source_asset_issuer=settings.CARBON_ISSUER_PUB,
                    source_asset_amount=sink_invoke.ton_amount,
                    dest_asset_code=settings.CARBON_ASSET.code,
                    dest_asset_issuer=settings.CARBON_ISSUER_PUB,
                    dest_asset_amount=sink_invoke.ton_amount,
                    vcs_project_id=vcs_project_id,
                    memo_type='text' if memo else 'none',
                    memo_value=memo,
                    paging_token=sink_invoke.toid,
                )
            )
        
        number_loaded = len(session.new)

    return number_loaded
