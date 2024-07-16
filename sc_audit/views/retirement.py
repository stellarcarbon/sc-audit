"""
View retirements and their details.

Retirements can be filtered by beneficiary, by retirement date, and by impact project.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import datetime as dt
from typing import Any, Literal

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from sc_audit.db_schema.retirement import Retirement
from sc_audit.session_manager import Session


def view_retirements(
        for_beneficiary: str | None = None, 
        from_date: dt.date | None = None,
        before_date: dt.date | None = None,
        project: int | None = None,
        cursor: int | None = None,
        limit: int | None = None,
        order: Literal['asc', 'desc'] = 'desc',
) -> pd.DataFrame:
    rt_query = construct_retirement_query(for_beneficiary, from_date, before_date, project)

    if order == 'asc':
        rt_query = rt_query.order_by(Retirement.certificate_id.asc())
        if cursor:
            rt_query = rt_query.where(Retirement.certificate_id > cursor)
    if order == 'desc':
        rt_query = rt_query.order_by(Retirement.certificate_id.desc())
        if cursor:
            rt_query = rt_query.where(Retirement.certificate_id < cursor)

    if limit:
        rt_query = rt_query.limit(limit)

    with Session.begin() as session:
        rt_records = session.scalars(rt_query).all()
        rtdf = pd.DataFrame.from_records(ret.as_dict() for ret in rt_records)

    return rtdf


def construct_retirement_query(
        for_beneficiary: str | None, 
        from_date: dt.date | None,
        before_date: dt.date | None,
        project: int | None,
):
    q_rets = select(Retirement)
    if for_beneficiary:
        q_rets = q_rets.where(Retirement.retirement_beneficiary.startswith(for_beneficiary))

    if from_date:
        q_rets = q_rets.where(Retirement.retirement_date >= from_date)

    if before_date:
        q_rets = q_rets.where(Retirement.retirement_date < before_date)

    if project:
        q_rets = q_rets.where(Retirement.vcs_project_id == project)

    return q_rets


def get_retirement(certificate_id: int) -> dict[str, Any] | None:
    rt_query = (
        select(Retirement)
        .options(
            selectinload(Retirement.retired_from), 
            selectinload(Retirement.sink_statuses),
            selectinload(Retirement.vcs_project)
        )
        .where(Retirement.certificate_id == certificate_id)
    )
    with Session.begin() as session:
        ret = session.scalar(rt_query)
        ret_data = ret.as_dict(related=True) if ret else None

    return ret_data
