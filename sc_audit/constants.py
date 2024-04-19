import os
from pathlib import Path

def get_default_db_path(db_name="sc-audit.db") -> Path:
    """
    Return the default location of the SQLite DB, as determined by:

    if the current working dir is a descendent of the home dir:
        use the current working dir
    else:
        use a subdir of the home dir and ensure it exists
    """
    home_dir = Path.home()
    work_dir = Path.cwd()

    if home_dir in work_dir.resolve().parents:
        return work_dir / db_name
    else:
        db_dir = home_dir / "sc-audit"
        db_dir.mkdir(exist_ok=True)
        return db_dir / db_name


DBAPI_URL: str = os.environ.get('SC_DBAPI_URL', f"sqlite+pysqlite://{get_default_db_path()}")

VERRA_ASSET_SEARCH_URL = "https://registry.verra.org/uiapi/asset/asset/search"
VERRA_REPORT_URL = "https://registry.verra.org/mymodule/rpt/myRpt.asp"
VERRA_ASSET_SEARCH_TIMEOUT = 8  # seconds
