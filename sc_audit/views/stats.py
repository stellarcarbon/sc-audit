"""
View Stellarcarbon's asset stats. Optionally, filter by recipient.
Compute year-over-year metrics based on historical sinking transactions.

Author: Alex Olieman <https://keybase.io/alioli>
"""

from decimal import Decimal

import numpy as np
import pandas as pd
from sqlalchemy import func, select, union_all

from sc_audit.db_schema.association import SinkStatus
from sc_audit.db_schema.mint import MintedBlock
from sc_audit.db_schema.sink import SinkingTx
from sc_audit.session_manager import Session
from sc_audit.views.sink_status import view_sinking_txs


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


def view_yoy_analytics() -> pd.DataFrame:
    df = view_sinking_txs(order='asc')
    if df.empty:
        return pd.DataFrame()
    
    # Compute price for USDC transactions
    df['price'] = np.where(
        df['dest_asset_code'] == 'USDC', 
        df['dest_asset_amount'].astype(float) / df['carbon_amount'].astype(float),
        np.nan
    )
    
    # Interpolate prices linearly, then extrapolate using forward fill for trailing CARBON transactions
    df['price'] = df['price'].interpolate(method='linear').ffill()
    
    # Convert CARBON denominated amounts to USD using the interpolated price
    mask = df['dest_asset_code'] == 'CARBON'
    df.loc[mask, 'dest_asset_amount'] = df.loc[mask, 'price'] * df.loc[mask, 'carbon_amount'].astype(float)
    
    # Ensure all dest_asset_amount are float for consistent summing
    df['dest_asset_amount'] = df['dest_asset_amount'].astype(float)
    
    # Add year and month columns for binning
    df['year'] = df['created_at'].dt.year
    df['month'] = df['created_at'].dt.month
    
    # Calculate monthly active users (distinct recipients per month)
    mau_df = df.groupby(['year', 'month'])['recipient'].nunique().reset_index()
    mau_yearly = (
        mau_df.groupby('year')['recipient']
        .mean()
        .reset_index()
        .rename(columns={'recipient': 'mau'})
    )
    mau_yearly['mau'] = mau_yearly['mau'].astype(float).round(2)
    
    # Calculate yearly aggregates
    yearly = df.groupby('year').agg(
        num_tx=('hash', 'count'),
        volume_usd=('dest_asset_amount', 'sum'),
        carbon_sunk=('carbon_amount', 'sum')
    ).reset_index()
    yearly['volume_usd'] = yearly['volume_usd'].astype(float).round(2)
    
    # Merge MAU with yearly data
    result = yearly.merge(mau_yearly, on='year', how='left')
    
    # Sort by year
    result = result.sort_values('year')
    
    # Calculate year-over-year percentage changes
    for col in ['mau', 'num_tx', 'volume_usd', 'carbon_sunk']:
        result[f'yoy_{col}'] = (result[col].astype(float).pct_change() * 100).round(2)
    
    # Reorder columns: year, then each core column followed by its yoy column
    result = result[[
        'year', 'mau', 'yoy_mau', 'num_tx', 'yoy_num_tx', 
        'volume_usd', 'yoy_volume_usd', 'carbon_sunk', 'yoy_carbon_sunk',
    ]]
    
    return result
