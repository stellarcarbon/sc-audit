"""
Load distribution outflows into the DB.

Author: Alex Olieman <https://keybase.io/alioli>
"""

from decimal import Decimal

from sc_audit.config import settings
from sc_audit.db_schema.distribution import DistributionTx
from sc_audit.loader.utils import parse_iso_datetime
from sc_audit.session_manager import Session
from sc_audit.sources.minting_txs import get_carbon_outflows


def load_distribution_txs(cursor: int=settings.FIRST_DIST_CURSOR) -> int:
    """
    Load (all) distribution outflows from Horizon into the DB.

    To catch up with Horizon, specify the cursor parameter to be the incremented paging
    token of the latest record present in the DB.
    """
    number_loaded = 0

    with Session.begin() as session:
        for payment in get_carbon_outflows(cursor):
            session.add(
                DistributionTx(
                    hash=payment['transaction_hash'],
                    created_at=parse_iso_datetime(payment['created_at']),
                    sender=payment['from'],
                    recipient=payment['to'],
                    carbon_amount=Decimal(payment['amount']),
                    paging_token=payment['paging_token'],
                )
            )
        
        number_loaded = len(session.new)

    return number_loaded
