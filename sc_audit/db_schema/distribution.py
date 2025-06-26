"""
Declare CARBON distribution DB models.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import datetime as dt

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, MappedAsDataclass

from sc_audit.db_schema.base import ScBase, bigint, hashpk, kgdecimal, strkey


class DistributionTxBase(MappedAsDataclass):

    hash: Mapped[hashpk]
    created_at: Mapped[dt.datetime]
    sender: Mapped[strkey]
    recipient: Mapped[strkey]
    carbon_amount: Mapped[kgdecimal]
    paging_token: Mapped[bigint]


class DistributionTx(DistributionTxBase, ScBase):
    __tablename__ = "distribution_txs"


idx_created_at = Index("idx_dtx_created_at", DistributionTx.created_at.desc())
idx_toid = Index("idx_dtx_toid", DistributionTx.paging_token.desc(), unique=True)
idx_recipient = Index("idx_dtx_recipient", DistributionTx.recipient)
