"""
Load sink events from sorocarbon into the DB as SinkingTx records.

Author: Alex Olieman <https://keybase.io/alioli>
"""

from functools import lru_cache

from stellar_sdk.sep.toid import TOID

from sc_audit.config import settings
from sc_audit.db_schema.impact_project import get_vcs_project
from sc_audit.db_schema.sink import SinkingTx
from sc_audit.session_manager import Session
from sc_audit.sources.sink_events import get_sink_events


def load_sink_events(cursor: int=settings.FIRST_SINK_CURSOR) -> tuple[int, list[tuple[str, str]]]:
    """
    Load (all) sink events from Mercury Retroshades into the DB.

    To catch up with Retroshades, specify the cursor parameter to be the incremented
    paging token of the latest record present in the DB. Always get the latest cursor
    once, and then load both sinking transactions and sink events using that cursor.

    There is a real risk of desync and missing SinkingTxs if the cursor is refreshed
    between loading sinking transactions and sink events. The only reason to not load
    from both SinkingTx sources in unison is when you want to analyze one of them
    separately.
    """
    number_loaded = 0
    recipient_emails: dict[str, str] = {}

    with Session.begin() as session:
        last_ledger = 0
        # For each new ledger, reset tx_order to 2^16 to avoid collisions with SinkingTxs.
        # This is a pragmatic choice; ideally, the order should come from Retroshades.
        tx_order = first_tx_index = 2**16
        for sink_event in get_sink_events(cursor):
            if sink_event.email:
                recipient_emails[sink_event.recipient] = sink_event.email

            vcs_project_id = try_project_id(sink_event.project_id)

            # FIXME: the TOID should come from Retroshades if possible
            if sink_event.ledger == last_ledger:
                tx_order += 1
            else:
                tx_order = first_tx_index

            event_toid = TOID(sink_event.ledger, tx_order, 0)
            last_ledger = sink_event.ledger
            # TODO: support multiple events per transaction
            # We can support >1 event per tx by abandoning tx hash as PK, replacing it
            # with the TOID (paging_token). Not done yet, because it requires a data migration.

            memo = sink_event.memo_text or None
            session.add(
                SinkingTx(
                    hash=sink_event.transaction,
                    created_at=sink_event.created_at,
                    contract_id=sink_event.contract_id,
                    funder=sink_event.funder,
                    recipient=sink_event.recipient,
                    carbon_amount=sink_event.amount,
                    source_asset_code=settings.CARBON_ASSET.code,
                    source_asset_issuer=settings.CARBON_ISSUER_PUB,
                    source_asset_amount=sink_event.amount,
                    dest_asset_code=settings.CARBON_ASSET.code,
                    dest_asset_issuer=settings.CARBON_ISSUER_PUB,
                    dest_asset_amount=sink_event.amount,
                    vcs_project_id=vcs_project_id,
                    memo_type='text' if memo else 'none',
                    memo_value=memo,
                    paging_token=event_toid.to_int64(),
                )
            )
        
        number_loaded = len(session.new)

    return number_loaded, list(recipient_emails.items())


@lru_cache(maxsize=32)
def try_project_id(project_id: str) -> int:
    """
    Try to parse the project_id into a VCS project ID.
    If it fails, return 1360 for the default VCS project.

    TODO: replace fallback with AnyProject so we can be more flexible with retirements.
    """
    if project_id.startswith("VCS"):
        try:
            vcs_id = int(project_id[3:])
            vcs_project = get_vcs_project(vcs_id)
            if vcs_project:
                return vcs_project.id
        except ValueError:
            pass

    return 1360  # Default VCS project ID
