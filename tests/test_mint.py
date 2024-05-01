import datetime as dt
from sqlite3 import connect

import pytest
from sqlalchemy import select
import sqlalchemy.orm.exc as orm_exc

from sc_audit.db_schema import *
from sc_audit.db_schema.mint import verra_carbon_pool
from sc_audit.loader.minted_blocks import serial_matches_hash
from sc_audit.loader.utils import VcsSerialNumber
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

    def test_vcs_serial_number_12(self, first_block_data):
        serial_number = VcsSerialNumber.from_str(first_block_data['serial_number'])
        assert serial_number.to_str() == first_block_data['serial_number']
        assert serial_number.project_id == 1360
        assert serial_number.additional_certification is True

    def test_vcs_serial_number_13(self):
        serial_number_str = "9660-115597313-115618057-VCS-VCU-261-VER-US-14-1060-01012019-31122019-0"
        serial_number = VcsSerialNumber.from_str(serial_number_str)
        assert serial_number.to_str() == serial_number_str
        assert serial_number.project_id == 1060
        assert serial_number.additional_certification is False

    def test_serial_matches_hash_true(self, first_block_data):
        serial_number = VcsSerialNumber.from_str(first_block_data['serial_number'])
        test_result = serial_matches_hash(serial_number, first_block_data['shash'])
        assert test_result is True

    def test_serial_matches_hash_false(self, first_block_data):
        serial_number = VcsSerialNumber.from_str(first_block_data['serial_number'])
        test_result = serial_matches_hash(serial_number, first_block_data['txhash'])
        assert test_result is False


@pytest.fixture
def first_block_data():
    return {
        'shash': "016023e64fefb1304a73aeab0877db032d7feceff25e390c00cf15d3fc4cfb79",
        'txhash': "61efb636bd2fb32efbd9a6379cd3ba55a96fb200ef3c523568168374d0aa0980",
        'serial_number': "8040-449402275-449402275-VCU-042-MER-PE-14-1360-01072013-30062014-1",
        'mint_timestamp': dt.datetime(2021, 11, 20, 13, 6, 51, tzinfo=dt.timezone.utc),
        'paging_token': 164806777139924993
    }


@pytest.fixture
def first_block(vcs_project: VcsProject, first_block_data) -> MintedBlock:
    serial_number = VcsSerialNumber.from_str(first_block_data['serial_number'])
    return MintedBlock(
        serial_hash=first_block_data['shash'], 
        transaction_hash=first_block_data['txhash'], 
        created_at=first_block_data['mint_timestamp'], 
        vcs_project_id=vcs_project.id,
        serial_number=serial_number.to_str(),
        block_start=serial_number.block_start,
        block_end=serial_number.block_end,
        sub_account_id=verra_carbon_pool.id,
        sub_account_name=verra_carbon_pool.name, 
        vintage_start=serial_number.vintage_start_date, 
        vintage_end=serial_number.vintage_end_date,
        paging_token=first_block_data['paging_token']
    )

@pytest.fixture
def session_with_block(new_session, vcs_project, first_block):
    with new_session.begin() as session:
        session.add(vcs_project)
        session.add(first_block)

    yield new_session
