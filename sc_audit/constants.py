import os
from pathlib import Path

from stellar_sdk import Asset

def get_default_db_path(db_name="sc-audit.sqlite3") -> Path:
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
        if work_dir.name == "sc_audit":
            return work_dir.parent / db_name
        
        return work_dir / db_name
    else:
        db_dir = home_dir / "sc-audit"
        db_dir.mkdir(exist_ok=True)
        return db_dir / db_name


DBAPI_URL: str = os.environ.get('SC_DBAPI_URL', f"sqlite+pysqlite:///{get_default_db_path()}")

VERRA_ASSET_SEARCH_URL = "https://registry.verra.org/uiapi/asset/asset/search"
VERRA_ASSET_SEARCH_TIMEOUT = 8  # seconds
VERRA_REPORT_URL = "https://registry.verra.org/mymodule/rpt/myRpt.asp"

HORIZON_URL: str = os.environ.get('SC_HORIZON_URL',"https://horizon.stellar.org")
CARBON_ISSUER_PUB = "GCBOATLWKXACOWKRRWORARDI2HFDSYPALMTS23YBZKHOB6XLW6CARBON"
CARBON_DISTRIB_PUB = "GABXJLJDNWRIGCVQPPC2FJ2NORUJBGLNOBYXKW7WQD3CUZS6YTFCS4ZP"
SINK_ISSUER_PUB = "GC7CDWMCWNCY7JYUW5UBEOLNBSTNDKKZSFTHKGZNPPSOXLFYFX3CSINK"
CARBON_ASSET = Asset("CARBON", CARBON_ISSUER_PUB)
SINK_ASSET = Asset("CarbonSINK", SINK_ISSUER_PUB)
FIRST_SINK_CURSOR = 164821723627237376
FIRST_MINT_CURSOR = 164806777139924992
