
import pytest
from stellar_sdk.client.requests_client import RequestsClient
from stellar_sdk.server import OperationsCallBuilder, PaymentsCallBuilder

from sc_audit.sources import sinking_txs as sink_sources
from sc_audit.sources.sinking_txs import get_sinking_transactions, get_tx_operations
from tests.data_fixtures.sinking_transactions import operations_resp, payments_resp


class MockPaymentsCallBuilder(PaymentsCallBuilder):
     def call(self):
          assert self.params['cursor'] == "999"
          self._check_pageable(payments_resp)
          return payments_resp
     

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
        ops = get_tx_operations("61d4ff5516b7098bbc2219d244e7f29a039c32735e1c16d1c05d66a0739727d9")
        assert len(ops) == 8
