import datetime as dt
from sqlite3 import connect

import pytest
from sqlalchemy import select
import sqlalchemy.orm.exc as orm_exc

from sc_audit.db_schema import *
from tests.db_fixtures import connection, new_session, vcs_project


class TestMint:
    def test_insert_block(self, session_with_block, first_block: MintedBlock):
        # after commit, the objects are no longer bound to the session
        with pytest.raises(orm_exc.DetachedInstanceError):
            first_block.vcs_project

    def test_get_block(self, session_with_block, first_block_data, vcs_project: VcsProject):
        with session_with_block.begin() as session:
            found_block = session.get_one(MintedBlock, first_block_data['shash'])
            assert found_block.transaction_hash == first_block_data['txhash']

    def test_hashes_stored_as_bytes(self, session_with_block, connection, first_block_data):
        # get a cursor from the underlying sqlite3 connection
        cursor = connection.connection.driver_connection.cursor()
        raw_row = cursor.execute(
            str(select(MintedBlock.serial_hash, MintedBlock.transaction_hash))
        ).fetchone()
        assert isinstance(raw_row[0], bytes)
        assert isinstance(raw_row[1], bytes)


@pytest.fixture
def first_block_data():
    return {
        'shash': "016023e64fefb1304a73aeab0877db032d7feceff25e390c00cf15d3fc4cfb79",
        'txhash': "61efb636bd2fb32efbd9a6379cd3ba55a96fb200ef3c523568168374d0aa0980",
        'serial_number': "8040-449402275-449402275-VCU-042-MER-PE-14-1360-01072013-30062014-1",
        'mint_timestamp': dt.datetime(2021, 11, 20, 13, 6, 51, tzinfo=dt.timezone.utc),
    }


@pytest.fixture
def first_block(vcs_project: VcsProject, first_block_data) -> MintedBlock:
    return MintedBlock(
        serial_hash=first_block_data['shash'], 
        transaction_hash=first_block_data['txhash'], 
        created_at=first_block_data['mint_timestamp'], 
        vcs_project_id=vcs_project.id,
        serial_number=first_block_data['serial_number'], 
        block_size=1, 
        sub_account_id=11273,
        sub_account_name="CARBON Pool | stellarcarbon.io", 
        vintage_start=dt.date(2011, 1, 1), 
        vintage_end=dt.date(2014, 1, 1)
    )

@pytest.fixture
def session_with_block(new_session, vcs_project, first_block):
    with new_session.begin() as session:
        session.add(vcs_project)
        session.add(first_block)

    yield new_session
