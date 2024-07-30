"""
View Stellarcarbon's asset stats. Optionally, filter by recipient.

Author: Alex Olieman <https://keybase.io/alioli>
"""

from decimal import Decimal

from sqlalchemy import func, select, union_all

from sc_audit.db_schema.association import SinkStatus
from sc_audit.db_schema.mint import MintedBlock
from sc_audit.db_schema.sink import SinkingTx
from sc_audit.session_manager import Session


def get_carbon_stats(recipient: str | None = None) -> dict[str, Decimal]:
    sel_sunk = select(func.sum(SinkingTx.carbon_amount))
    sel_retired = select(func.sum(SinkStatus.amount_filled))

    if recipient:
        sel_sunk = sel_sunk.where(SinkingTx.recipient == recipient)
        sel_retired = (
            sel_retired
            .join(SinkStatus.sinking_transaction)
            .where(SinkingTx.recipient == recipient)
        )
        q_stats = union_all(sel_sunk, sel_retired)
    else:
        sel_stored = select(func.sum(MintedBlock.size))
        q_stats = union_all(sel_sunk, sel_retired, sel_stored)

    with Session.begin() as session:
        db_res = (val or Decimal() for val in session.scalars(q_stats).all())

    stats = {
        "carbon_sunk": Decimal(),
        "carbon_retired": Decimal(),
        "carbon_pending": Decimal(),
    }
    if recipient:
        c_sunk, c_retired = db_res
    else:
        c_sunk, c_retired, c_stored = db_res
        stats["carbon_stored"] = c_stored

    stats["carbon_sunk"] = c_sunk
    stats["carbon_retired"] = c_retired
    stats["carbon_pending"] = c_sunk - c_retired

    return stats
