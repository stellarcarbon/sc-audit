import importlib
import sys
from typing import Iterator

import pytest

from sc_audit.config import Settings, settings


class TestSettings:
    def test_default_settings(self):
        assert settings.DBAPI_URL.startswith("sqlite+pysqlite://")
        assert settings.DBAPI_URL.endswith("sc-audit.sqlite3")
        assert settings.TABLE_PREFIX is None
        assert str(settings.HORIZON_URL) == "https://horizon.stellar.org/"

    def test_table_default(self):
        base_module = "sc_audit.db_schema.base"
        if base_module in sys.modules:
            del sys.modules[base_module]

        bmod = importlib.import_module(base_module)

        for table_name, table in bmod.ScBase.metadata.tables.items():
            assert not table_name.startswith("test_")
            assert table_name == table.name

        del sys.modules[base_module]

    def test_table_prefix(self, patch_settings: Settings):
        patch_settings.TABLE_PREFIX = "test"
        base_module = "sc_audit.db_schema.base"
        if base_module in sys.modules:
            del sys.modules[base_module]
            
        bmod = importlib.import_module(base_module)

        for table_name, table in bmod.ScBase.metadata.tables.items():
            assert table_name.startswith("test_")
            assert table_name == table.name

        del sys.modules[base_module]


@pytest.fixture
def patch_settings() -> Iterator[Settings]:
    original_settings = settings.model_copy()

    yield settings

    # Restore the original settings
    settings.__dict__.update(original_settings.__dict__)
