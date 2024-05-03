"""
Load the relationships between retirements and minted blocks into the DB.

These relationships are implicit in the source data. Both minted blocks and retirements
are associated with serial numbers that specify a range of individual credits. This loader
module iterates over retirement records and finds the minted blocks that match their serial
numbers, storing the explicit relationships.

Author: Alex Olieman <https://keybase.io/alioli>
"""

from sqlalchemy import func, select
from sqlalchemy.orm import contains_eager

from sc_audit.db_schema.association import RetirementFromBlock
from sc_audit.db_schema.retirement import Retirement
from sc_audit.session_manager import Session


def load_retirement_from_block():
    """
    Load the retirement—block associations to ensure that all retirements are explicitly covered
    by their originating blocks.
    """
    with Session.begin() as session:
        # select the retirements that are not fully related to minted blocks
        query = (
            select(Retirement)
            .outerjoin(Retirement.retired_from)
            .group_by(Retirement.certificate_id)
            .having(func.total(RetirementFromBlock.vcu_amount) < Retirement.vcu_amount)
            .options(contains_eager(Retirement.retired_from))
        )
        uncovered_retirements = session.scalars(query).unique().all()


if __name__ == "__main__":
    load_retirement_from_block()
