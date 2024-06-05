"""
Load finalized retirements into the DB.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import datetime as dt
from functools import partial

from sqlalchemy import select

from sc_audit.db_schema.impact_project import VcsProject
from sc_audit.db_schema.retirement import Retirement
from sc_audit.loader.utils import parse_iso_date
from sc_audit.session_manager import Session
from sc_audit.sources.retirements import get_retirements_list


def load_retirements(from_date: dt.date | None = None) -> int:
    """
    Load all retirements from Verra into the DB.
  
    TODO: add pagination (to support more than 2000 results)
    """
    retirement_data = get_retirements_list(from_date)
    number_loaded = 0

    with Session.begin() as session:
        existing_ids: set[int] = set(session.scalars(select(Retirement.certificate_id)).all())
        existing_vcs_projects: set[int] = set(session.scalars(select(VcsProject.id)).all())
        for retirement_item in retirement_data['retirements']:
            # only load new retirements
            certificate_id = int(retirement_item['certificate_id'])
            if certificate_id not in existing_ids:
                # ensure that the related VCS Project exists
                vcs_project_id = int(retirement_item['vcs_id'])
                if vcs_project_id not in existing_vcs_projects:
                    existing_vcs_projects.add(vcs_project_id)
                    session.add(
                        VcsProject(
                            id=vcs_project_id,
                            name=retirement_item['vcs_name'],
                            category=retirement_item['vcs_category'],
                            protocol=retirement_item['vcs_protocol'],
                            additional_certifications=retirement_item['additional_certifications'],
                            region=retirement_item['region'],
                            country=retirement_item['country'],
                        )
                    )

                session.add(
                    Retirement(
                        certificate_id=certificate_id,
                        vcu_amount=retirement_item['vcu_amount'],
                        serial_number=retirement_item['serial_numbers'],
                        retirement_date=parse_iso_date(retirement_item['retirement_date']),
                        retirement_beneficiary=retirement_item['retirement_beneficiary'],
                        retirement_details=retirement_item['retirement_details'],
                        vcs_project_id=vcs_project_id,
                        issuance_date=parse_iso_date(retirement_item['issuance_date']),
                        instrument_type=retirement_item['instrument_type'],
                        vintage_start=parse_iso_date(retirement_item['vintage_start']),
                        vintage_end=parse_iso_date(retirement_item['vintage_end']),
                        total_vintage_quantity=retirement_item['total_vintage_quantity'],
                    )
                )
                number_loaded += 1

    return number_loaded
