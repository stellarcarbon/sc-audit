from pathlib import Path
from typing import Literal

from pydantic import HttpUrl, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
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
    

DbTablePrefix = Literal["test"] | None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='SC_', env_file=".env")

    DBAPI_URL: str = f"sqlite+pysqlite:///{get_default_db_path()}"
    TABLE_PREFIX: DbTablePrefix = None

    VERRA_ASSET_SEARCH_URL: HttpUrl = HttpUrl("https://registry.verra.org/uiapi/asset/asset/search")
    VERRA_ASSET_SEARCH_TIMEOUT: int = 8  # seconds
    VERRA_REPORT_URL: HttpUrl = HttpUrl("https://registry.verra.org/mymodule/rpt/myRpt.asp")

    HORIZON_URL: HttpUrl = HttpUrl("https://horizon.stellar.org")
    CARBON_ISSUER_PUB: str = "GCBOATLWKXACOWKRRWORARDI2HFDSYPALMTS23YBZKHOB6XLW6CARBON"
    CARBON_DISTRIB_PUB: str = "GABXJLJDNWRIGCVQPPC2FJ2NORUJBGLNOBYXKW7WQD3CUZS6YTFCS4ZP"
    SINK_ISSUER_PUB: str = "GC7CDWMCWNCY7JYUW5UBEOLNBSTNDKKZSFTHKGZNPPSOXLFYFX3CSINK"
    FIRST_SINK_CURSOR: int = 164821723627237376
    FIRST_MINT_CURSOR: int = 164806777139924992
    FIRST_DIST_CURSOR: int = 164810659791396865

    RETROSHADES_URL: HttpUrl = HttpUrl("https://api.mercurydata.app/retroshadesv1")
    RETROSHADES_MD5: str = "3dd6e7b71adb9fda05a5b45a154611f3"
    MERCURY_KEY: str = ""

    @computed_field
    @property
    def CARBON_ASSET(self) -> Asset:
        return Asset("CARBON", self.CARBON_ISSUER_PUB)

    @computed_field
    @property
    def SINK_ASSET(self) -> Asset:
        return Asset("CarbonSINK", self.SINK_ISSUER_PUB)


settings = Settings()
