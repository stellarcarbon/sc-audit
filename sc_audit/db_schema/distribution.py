"""
Declare CARBON distribution DB models.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import datetime as dt

from sqlalchemy import Index
from sqlalchemy.orm import Mapped

from sc_audit.db_schema.base import ScBase, hashpk, kgdecimal, strkey


class DistributionTx(ScBase):
    __tablename__ = "distribution_txs"

    hash: Mapped[hashpk]
    created_at: Mapped[dt.datetime]
    sender: Mapped[strkey]
    recipient: Mapped[strkey]
    carbon_amount: Mapped[kgdecimal]
    paging_token: Mapped[int]


idx_created_at = Index("idx_dtx_created_at", DistributionTx.created_at.desc())
idx_recipient = Index("idx_dtx_recipient", DistributionTx.recipient)
