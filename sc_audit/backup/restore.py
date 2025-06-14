"""
Restore DB tables from newline-delimited json files.

Author: Alex Olieman <https://keybase.io/alioli>
"""
from io import StringIO
from pathlib import Path
import sys

import pandas as pd
from sqlalchemy import delete, func, select, types

from sc_audit.db_schema import (
    ScBase, DistributionTx, MintedBlock, Retirement, RetirementFromBlock, SinkingTx, SinkStatus, VcsProject
)
from sc_audit.session_manager import Session


TABLE_LOADING_ORDER = (
    VcsProject,
    DistributionTx,
    Retirement,
    SinkingTx,
    MintedBlock,
    RetirementFromBlock,
    SinkStatus,
)

def restore_all_tables(input_dir: Path, replace: bool = False):
    for db_model in TABLE_LOADING_ORDER:
        table_name = db_model.__table__.name # type: ignore
        dump_file = input_dir / f"{table_name}.ndjson"
        if dump_file.exists():
            restore_table(dump_file, replace=replace)
        else:
            print(f"Couldn't find {dump_file}", file=sys.stderr)


def restore_table(json_path: Path, replace: bool = False):
    table_name = json_path.stem
    db_table = ScBase.metadata.tables[table_name]
    tdf = df_from_ndjson(json_path)

    with Session.begin() as session:
        if replace:
            # delete existing rows
            dbres = session.execute(delete(db_table))
            print(f"Deleted {dbres.rowcount} existing rows from {table_name}")
        else:
            # exit early if there are existing rows
            num_rows = session.scalar(select(func.count()).select_from(db_table))
            if num_rows:
                print(f"Leaving {num_rows} rows from {table_name} intact")
                return
            
        # insert the dataframe records into the table
        column_dtypes = {c.name: c.type for c in db_table.columns}
        num_rows = tdf.to_sql(
            name=table_name,
            con=session.connection(),
            if_exists='append',
            index=False,
            chunksize=200,
            dtype=column_dtypes, # type: ignore
        )
        print(f"Restored {num_rows} rows into {table_name}")


def df_from_ndjson(json_path: Path) -> pd.DataFrame:
    table_name = json_path.stem
    db_table = ScBase.metadata.tables[table_name]
    with open(json_path, 'r') as infile:
        ndjson = infile.read().rstrip("\n")

    # turn json lines into a valid array
    json_array = "[" + ndjson.replace("\n", ",") + "]"
    table_df = pd.read_json(
        StringIO(json_array),
        orient='values',
    )
    column_dtypes = {c.name: c.type for c in db_table.columns}
    table_df.columns = list(column_dtypes.keys())

    # parse date(time) strings
    for col_name, col_type in column_dtypes.items():
        if isinstance(col_type, (types.Date, types.DateTime)):
            table_df[col_name] = pd.to_datetime(table_df[col_name], format='ISO8601')

    return table_df


def get_table_row_counts() -> dict[str, int]:
    row_counts: dict[str, int] = {}
    with Session.begin() as session:
        for table_name, table in ScBase.metadata.tables.items():
            num_rows = session.scalar(select(func.count()).select_from(table))
            row_counts[table_name] = num_rows or 0

    return row_counts
