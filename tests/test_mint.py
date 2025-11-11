import datetime as dt
from decimal import Decimal

import pytest
from sqlalchemy import select
import sqlalchemy.orm.exc as orm_exc

from sc_audit.db_schema import *
from sc_audit.db_schema.distribution import DistributionTx
from sc_audit.db_schema.impact_project import UnknownVcsProject
from sc_audit.db_schema.mint import verra_carbon_pool
from sc_audit.loader import impact_projects, minted_blocks
from sc_audit.loader import distribution_outflows
from sc_audit.loader.minted_blocks import (
    index_carbon_pool, 
    load_minted_blocks, 
    reconstruct_blocks, 
    serial_matches_hash,
)
from sc_audit.loader.utils import VcsSerialNumber, decode_hash_memo
from sc_audit.sources.minting_txs import filter_distribution_txs, filter_minting_txs
from tests.db_fixtures import connection, new_session
from tests.data_fixtures.carbon_pool import carbon_pool as carbon_pool_fix
from tests.data_fixtures.minting_transactions import distribution_records as outflows_fix
from tests.data_fixtures.minting_transactions import minting_transactions as mint_tx_fix
from tests.data_fixtures.minting_transactions import payment_records as payments_fix
from tests.data_fixtures.retirements import get_retirements_whole_and_round_up


class TestMintDb:
    def test_insert_block(self, session_with_block, first_block: MintedBlock):
        # after commit, the objects are no longer bound to the session
        with pytest.raises(orm_exc.DetachedInstanceError):
            first_block.vcs_project

    def test_get_block(self, session_with_block, first_block_data):
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


class TestMintUtils:
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

    def test_index_carbon_pool(self, monkeypatch):
        # mock carbon pool state
        def mock_carbon_pool():
            return carbon_pool_fix
        
        monkeypatch.setattr(minted_blocks, 'get_carbon_pool_state', mock_carbon_pool)

        carbon_pool = index_carbon_pool()
        assert (
            carbon_pool["a6df717999268d8c021f75830e3a9c3bafe3f3df435879f08968e6b8de069451"] 
            == carbon_pool_fix['credit_batches'][-1]
        )
        assert (
            carbon_pool["1e47dd9c1c536e78cfe46b78f80b8b91a475c13986abb4f8b6d79005edef77be"] 
            == carbon_pool_fix['credit_batches'][0]
        )


class TestMintSources:
    def test_filter_mint_txs(self):
        assert len(payments_fix) == 3
        mint_txs = list(filter_minting_txs(payments_fix))
        assert len(mint_txs) == 1

    def test_filter_dist_txs(self):
        assert len(outflows_fix) == 7
        dist_payments = list(filter_distribution_txs(outflows_fix))
        assert len(dist_payments) == 5


@pytest.fixture
def mock_session(monkeypatch, new_session):
    monkeypatch.setattr(impact_projects, 'Session', new_session)
    monkeypatch.setattr(minted_blocks, 'Session', new_session)
    monkeypatch.setattr(distribution_outflows, 'Session', new_session)
    impact_projects.load_impact_projects()
    return new_session

@pytest.fixture
def mock_http(monkeypatch):
    def mock_carbon_pool():
            return carbon_pool_fix
        
    def mock_mint_txs(cursor):
        return mint_tx_fix
    
    def mock_dist_txs(cursor):
        return list(filter_distribution_txs(outflows_fix))
    
    monkeypatch.setattr(minted_blocks, 'get_carbon_pool_state', mock_carbon_pool)
    monkeypatch.setattr(minted_blocks, 'get_minting_transactions', mock_mint_txs)
    monkeypatch.setattr(distribution_outflows, 'get_carbon_outflows', mock_dist_txs)


class TestMintLoader:
    def test_reconstructed_from_retirement(self):
        blocks = reconstruct_blocks(
            mint_txs=mint_tx_fix[:3], latest_block=None, retirements=get_retirements_whole_and_round_up()[:1]
        )
        assert len(blocks) == 3
        assert blocks[0].serial_hash == decode_hash_memo(mint_tx_fix[0]['transaction']['memo'])
        assert blocks[1].serial_hash == decode_hash_memo(mint_tx_fix[1]['transaction']['memo'])
        assert blocks[2].serial_hash == decode_hash_memo(mint_tx_fix[2]['transaction']['memo'])

    def test_reconstructed_from_latest(self, first_block):
        blocks = reconstruct_blocks(
            mint_txs=mint_tx_fix[1:3], latest_block=first_block, retirements=[]
        )
        assert len(blocks) == 2
        assert blocks[0].serial_hash == decode_hash_memo(mint_tx_fix[1]['transaction']['memo'])
        assert blocks[1].serial_hash == decode_hash_memo(mint_tx_fix[2]['transaction']['memo'])

    def test_load_minted_blocks_vcs_missing(self, mock_session, mock_http, monkeypatch):
        monkeypatch.setattr(minted_blocks, "get_vcs_project", lambda x: None)

        with pytest.raises(UnknownVcsProject):
            load_minted_blocks()
    
    def test_load_minted_blocks_retirements_missing(self, mock_session, mock_http):
        with pytest.raises(ValueError):
            load_minted_blocks()

    def test_load_minted_blocks_verify(self, mock_session, mock_http):
        with mock_session.begin() as session:
            session.add_all(get_retirements_whole_and_round_up())

        load_minted_blocks()

        with mock_session.begin() as session:
            loaded_blocks = session.scalars(
                select(MintedBlock).order_by(MintedBlock.toid.asc())
            ).all()
            assert len(loaded_blocks) == 9
            for block in loaded_blocks:
                serial_number = VcsSerialNumber.from_str(block.serial_number)
                assert serial_matches_hash(serial_number, block.serial_hash)

    def test_load_distribution_outflows(self, mock_session, mock_http):
        distribution_outflows.load_distribution_txs()

        with mock_session.begin() as session:
            loaded_outflows = session.scalars(
                select(DistributionTx).order_by(DistributionTx.toid.asc())
            ).all()
            assert len(loaded_outflows) == 5
            total_outflow = sum(
                (
                    outflow.carbon_amount
                    for outflow in loaded_outflows
                ),
                start=Decimal(),
            )
            assert total_outflow == Decimal("8.616")


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
def first_block(first_block_data) -> MintedBlock:
    serial_number = VcsSerialNumber.from_str(first_block_data['serial_number'])
    return MintedBlock(
        serial_hash=first_block_data['shash'], 
        transaction_hash=first_block_data['txhash'], 
        created_at=first_block_data['mint_timestamp'], 
        vcs_project_id=1360,
        serial_number=serial_number.to_str(),
        block_start=serial_number.block_start,
        block_end=serial_number.block_end,
        sub_account_id=verra_carbon_pool.id,
        sub_account_name=verra_carbon_pool.name, 
        vintage_start=serial_number.vintage_start_date, 
        vintage_end=serial_number.vintage_end_date,
        toid=first_block_data['paging_token']
    )

@pytest.fixture
def session_with_block(monkeypatch, new_session, first_block):
    monkeypatch.setattr(impact_projects, 'Session', new_session)
    impact_projects.load_impact_projects()
    with new_session.begin() as session:
        session.add(first_block)

    yield new_session
