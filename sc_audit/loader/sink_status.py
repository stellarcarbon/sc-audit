"""
Load the relationships between sinking transactions and retirements into the DB.

These relationships are implicit in the source data. Retirement details include a string
representation of the included transaction hashes. This loader module iterates over retirement
records and stores the sink statuses of the corresponding transactions.

Author: Alex Olieman <https://keybase.io/alioli>
"""

from decimal import Decimal
from sqlalchemy import func, select

from sc_audit.db_schema.association import SinkStatus
from sc_audit.db_schema.retirement import Retirement
from sc_audit.db_schema.sink import SinkingTx
from sc_audit.session_manager import Session


def load_sink_statuses() -> int:
    """
    Load the retirement—sinking_tx associations to make the retirement status of sinking
    transactions explicit.
    """
    number_loaded = 0

    with Session.begin() as session:
        # select the retirements that have filled less than their VCU amount
        query = (
            select(Retirement)
            .outerjoin(Retirement.sink_statuses)
            .group_by(Retirement.certificate_id)
            .having(func.total(SinkStatus.amount_filled) < Retirement.vcu_amount)
        )
        open_retirements = session.scalars(query).unique().all()
        for retirement in open_retirements:
            sink_statuses = create_sink_statuses(session, for_retirement=retirement)
            session.add_all(sink_statuses)
            number_loaded += len(sink_statuses)

    return number_loaded


def create_sink_statuses(session, for_retirement: Retirement) -> list[SinkStatus]:
    """
    For the given retirement, find which tx hashes do not yet have corresponding sink statuses.
    Keep track of the carbon amount remaining on the retirement while new statuses are created.
    """
    retirement = for_retirement
    existing_status_txs = {ss.sinking_tx_hash for ss in retirement.sink_statuses}
    existing_status_amount: Decimal = sum(
        (ss.amount_filled for ss in retirement.sink_statuses), start=Decimal()
    )
    new_sink_statuses: list[SinkStatus] = []
    for tx_hash in retirement.tx_hashes_from_details:
        if tx_hash in existing_status_txs:
            # only create new sink statuses
            continue

        sink_tx = session.get_one(SinkingTx, tx_hash)
        retirement_remaining = retirement.vcu_amount - existing_status_amount
        sink_remaining = sink_tx.carbon_amount - sink_tx.total_filled
        # status amount is the sink amount up to the remaining retirement amount
        amount_filled = min(sink_remaining, retirement_remaining)
        sink_status = SinkStatus(
            sinking_tx_hash=sink_tx.hash,
            certificate_id=retirement.certificate_id,
            amount_filled=amount_filled,
            finalized=((sink_tx.total_filled + amount_filled) == sink_tx.carbon_amount)
        )
        # indirect update of retirement_remaining and sink_tx.total_filled
        existing_status_amount += amount_filled
        sink_tx.statuses.append(sink_status)
        new_sink_statuses.append(sink_status)

    return new_sink_statuses
