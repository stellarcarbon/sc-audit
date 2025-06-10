"""
Dump DB tables to newline-delimited json files.

Author: Alex Olieman <https://keybase.io/alioli>
"""
import inspect
from pathlib import Path

import pandas as pd
from sqlalchemy import select, Table

from sc_audit.db_schema.base import ScBase
from sc_audit.session_manager import Session


def dump_table(db_model: type[ScBase] | str, output_path: Path | None = None) -> str | None:
    db_table: Table
    if inspect.isclass(db_model) and issubclass(db_model, ScBase):
        db_table = db_model.__table__ # type: ignore
    else:
        try:
            db_table = ScBase.metadata.tables[db_model]
        except KeyError:
            table_names = get_table_names()
            raise KeyError(f"`db_model` must be one of {table_names}")
        
    ndjson_table = table_to_ndjson(db_table)
    if output_path is not None:
        with output_path.open('w') as ofile:
            ofile.write(ndjson_table + "\n")
    else:
        return ndjson_table


def table_to_ndjson(db_table: Table) -> str:
    dbq = select(db_table)
    columns = db_table.columns
    with Session.begin() as session:
        rows = session.execute(dbq).all()
        tdf = pd.DataFrame.from_records(rows, columns=(c.name for c in columns))

    return tdf.to_json(
        orient='values',
        date_format='iso',
        date_unit='s',
    )[1:-1].replace("],[", "]\n[")


def get_table_names() -> list[str]:
    return [
        table_name
        for table_name in ScBase.metadata.tables.keys()
        if not table_name.startswith("test_")
    ]
