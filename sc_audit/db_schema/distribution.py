"""
Declare CARBON distribution DB models.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import datetime as dt

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, MappedAsDataclass

from sc_audit.db_schema.base import ScBase, bigintpk, kgdecimal, strkey, txhash


class DistributionTxBase(MappedAsDataclass):

    hash: Mapped[txhash]
    created_at: Mapped[dt.datetime]
    sender: Mapped[strkey]
    recipient: Mapped[strkey]
    carbon_amount: Mapped[kgdecimal]
    toid: Mapped[bigintpk]


class DistributionTx(DistributionTxBase, ScBase):
    __tablename__ = "distribution_txs"


idx_hash = Index("idx_dtx_hash", DistributionTx.hash)
idx_created_at = Index("idx_dtx_created_at", DistributionTx.created_at.desc())
idx_recipient = Index("idx_dtx_recipient", DistributionTx.recipient)
