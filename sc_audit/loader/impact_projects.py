"""
Load impact projects into the DB.

Author: Alex Olieman <https://keybase.io/alioli>
"""

from sqlalchemy import select
from sc_audit.db_schema.base import intpk
from sc_audit.db_schema.impact_project import VcsProject, get_vcs_project
from sc_audit.session_manager import Session


def load_impact_projects() -> int:
    """
    Load impact projects from our own data schema into the DB.
    """
    number_loaded = 0

    with Session.begin() as session:
        existing_vcs_projects: set[intpk] = set(session.scalars(select(VcsProject.id)).all())
        if 1360 not in existing_vcs_projects:
            vcs_1360 = get_vcs_project(1360)
            session.add(vcs_1360)
        
        number_loaded = len(session.new)

    return number_loaded
