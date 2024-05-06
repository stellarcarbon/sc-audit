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


def load_sink_statuses():
    """
    Load the retirement—sinking_tx associations to make the retirement status of sinking
    transactions explicit.
    """
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


def create_sink_statuses(session, for_retirement: Retirement) -> list[SinkStatus]:
    retirement = for_retirement
    existing_status_txs = {ss.sinking_tx_hash for ss in retirement.sink_statuses}
    existing_status_amount: Decimal = sum(
        (ss.amount_filled for ss in retirement.sink_statuses), start=Decimal()
    )
    new_sink_statuses: list[SinkStatus] = []
    for tx_hash in retirement.tx_hashes_from_details:
        if tx_hash in existing_status_txs:
            continue

        sink_tx = session.get_one(SinkingTx, tx_hash)
        retirement_remaining = retirement.vcu_amount - existing_status_amount
        sink_remaining = sink_tx.carbon_amount - sink_tx.total_filled
        amount_filled = min(sink_remaining, retirement_remaining)
        sink_status = SinkStatus(
            sinking_tx_hash=sink_tx.hash,
            certificate_id=retirement.certificate_id,
            amount_filled=amount_filled,
            finalized=((sink_tx.total_filled + amount_filled) == sink_tx.carbon_amount)
        )
        existing_status_amount += amount_filled
        sink_tx.statuses.append(sink_status)
        new_sink_statuses.append(sink_status)

    return new_sink_statuses



if __name__ == "__main__":
    load_sink_statuses()