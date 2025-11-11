
import pytest
from sqlalchemy import select
from stellar_sdk.client.requests_client import RequestsClient
from stellar_sdk.server import OperationsCallBuilder, PaymentsCallBuilder

from sc_audit.db_schema.impact_project import UnknownVcsProject
from sc_audit.db_schema.sink import SinkingTx
from sc_audit.loader import impact_projects, sinking_txs as sink_loader
from sc_audit.loader.sinking_txs import get_payment_data, load_sinking_txs
from sc_audit.sources import sinking_txs as sink_sources
from sc_audit.sources.sinking_txs import get_sinking_transactions, get_tx_operations
from tests.data_fixtures.sinking_transactions import operations_resp, payments_resp
from tests.db_fixtures import new_session


class MockPaymentsCallBuilder(PaymentsCallBuilder):
     def call(self):
        assert self.params['cursor'] == "999"
        self._check_pageable(payments_resp)
        return payments_resp
     
     def next(self):
        assert self.params['cursor'] == "999"
        return {
            '_embedded': {'records': []}
        }


class MockOperationsCallBuilder(OperationsCallBuilder):
     def call(self):
        return operations_resp


@pytest.fixture
def mock_http(monkeypatch):
    def mock_payments():
        return MockPaymentsCallBuilder("", RequestsClient())
        
    def mock_operations():
        return MockOperationsCallBuilder("", RequestsClient())
    
    monkeypatch.setattr(sink_sources.server, 'payments', mock_payments)
    monkeypatch.setattr(sink_sources.server, 'operations', mock_operations)


class TestSinkSources:
    def test_sinking_txs(self, mock_http):
        tx_gen = get_sinking_transactions(cursor=999)
        assert len(list(tx_gen)) == 20

    def test_operations(self, mock_http):
        ops = get_tx_operations("61d4ff...9727d9")
        assert len(ops) == 8


@pytest.fixture
def mock_session(monkeypatch, new_session):
    monkeypatch.setattr(impact_projects, 'Session', new_session)
    monkeypatch.setattr(sink_loader, 'Session', new_session)
    impact_projects.load_impact_projects()
    return new_session


class TestSinkLoader:
    def test_payment_data_missing(self, mock_http):
        ops = get_tx_operations("61d4ff...9727d9")
        with pytest.raises(ValueError):
            get_payment_data(ops[:2])

    def test_payment_data_present(self, mock_http):
        ops = get_tx_operations("61d4ff...9727d9")
        payment_data = get_payment_data(ops)
        assert payment_data['funder'] == "GAVF6ZB7Z7FKCWM5HEY2OV4ENPK3OSSHMFTVR4HHSBFHKW36U3FUH2CB"
        assert payment_data['source_asset_code'] == "AQUA"
        assert payment_data['source_asset_amount'] == "2236.6785284"
        assert payment_data['dest_asset_code'] == "USDC"
        assert payment_data['dest_asset_amount'] == "11.0000000"

    def test_load_sinking_vcs_missing(self, mock_http, mock_session, monkeypatch):
        monkeypatch.setattr(sink_loader, "get_vcs_project", lambda x65: None)

        with pytest.raises(UnknownVcsProject):
            load_sinking_txs(cursor=999)

    def test_load_sinking_transactions(self, mock_http, mock_session):
        load_sinking_txs(cursor=999)

        with mock_session.begin() as session:
            loaded_transactions = session.scalars(
                select(SinkingTx).order_by(SinkingTx.toid.asc())
            ).all()
            assert len(loaded_transactions) == 20

            memos = [tx.memo_value for tx in loaded_transactions]
            assert memos == [
                'Public Node Carbon Offset', 
                'natgas 555 m³', 
                'Business trip', 
                '1 shareholder for 1 month', 
                '9378b8e6075aa70c7a3274c7f72c32e83637d8e0b315509f8a5d26e8c5c7c5f6', 
                '1 shareholder for 1 month', 
                '1 shareholder for 1 month', 
                None, 
                '1 shareholder for 1 month', 
                '✈️ air travel 2013-14', 
                '✈️ air travel 2015-16', 
                '✈️ air travel 2017', 
                '✈️ air travel 2018', 
                '✈️ air travel 2019', 
                '✈️ air travel 2022', 
                '🌎✨🌍💕🌏 care', 
                '🏠 household', 
                '✈️ air travel', 
                '✈️ air travel', 
                '✈️ Meridian 2023'
            ]
