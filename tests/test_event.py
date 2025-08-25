import datetime as dt
from decimal import Decimal

import httpx
from httpx import Client, Response
import pytest
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from sc_audit.db_schema.sink import SinkingTx
from sc_audit.loader import impact_projects, sink_events as event_loader
from sc_audit.loader import sinking_txs as sink_loader
from sc_audit.sources.sink_events import get_sink_events
from tests.data_fixtures.events import query_response
from tests.db_fixtures import new_session
from tests.test_settings import patch_settings
from tests.test_sink import mock_http


class MockClient(Client):
    def __init__(self, headers: dict) -> None:
        assert len(headers['Authorization']) == 32
        assert headers['Content-Type'] == "application/json"
        super().__init__(headers=headers)

    def post(self, url: str, json: dict, **kwargs) -> Response:
        assert "retroshadesv1" in url
        assert "query" in json
        assert "SELECT * FROM sink_event" in json['query']
        assert "WHERE ledger > " in json['query']

        request = self.build_request(
            method="POST",
            url=url,
            json=json,
        )
        
        return Response(status_code=200, text=query_response, request=request)


@pytest.fixture
def mock_client(monkeypatch):
    monkeypatch.setattr(httpx, "Client", MockClient)


@pytest.fixture
def patch_mercury_key(patch_settings):
    patch_settings.OBSRVR_FLOW_DB_URI = None
    if not patch_settings.MERCURY_KEY:
        patch_settings.MERCURY_KEY = "123456789ABCDEFGHJKLMNPQRSTUVWXY"


@pytest.mark.usefixtures("mock_client", "patch_mercury_key")
class TestSinkEventSources:
    def test_events_list_full(self):
        events = get_sink_events(cursor=0)
        assert len(events) == 10
        assert events[0].amount == Decimal("0.2")
        assert events[0].created_at == dt.datetime(2022, 7, 8, 21, 42, 9, tzinfo=dt.UTC)
        assert events[6].amount == Decimal("0.06")
        assert events[6].created_at == dt.datetime(2024, 6, 8, 19, 30, 54, tzinfo=dt.UTC)
        assert events[9].amount == Decimal("0.01")
        assert events[6].created_at == events[9].created_at
        assert events[6].ledger == events[9].ledger


@pytest.fixture
def mock_session(monkeypatch, new_session):
    monkeypatch.setattr(impact_projects, 'Session', new_session)
    monkeypatch.setattr(event_loader, 'Session', new_session)
    monkeypatch.setattr(sink_loader, 'Session', new_session)
    impact_projects.load_impact_projects()
    return new_session


@pytest.mark.usefixtures("mock_client", "patch_mercury_key")
class TestSinkEventLoader:
    def test_load_sink_events(self, mock_session):
        num_loaded = event_loader.load_sink_events(cursor=0)
        assert num_loaded == 10

        with mock_session.begin() as session:
            loaded_events = session.scalars(
                select(SinkingTx).order_by(SinkingTx.paging_token.asc())
                .options(joinedload(SinkingTx.vcs_project))
            ).all()

            assert all(
                tx.contract_id == "CAQWMP2EKO4SQ7VQTIYCNUXASDY7WI5EKEGJXMS7W6AICI6YXPNAB4J5"
                for tx in loaded_events[:2]
            )
            assert all(
                tx.contract_id == "CBW45IZ3W5BBDIKTIXQEAOR3TAHPCFIAVQMD4NO2YPX2FA4LKGLJLWYL"
                for tx in loaded_events[2:]
            )
            assert all(
                tx.carbon_amount == tx.source_asset_amount == tx.dest_asset_amount
                for tx in loaded_events
            )
            assert all(
                "CARBON" == tx.source_asset_code == tx.dest_asset_code
                for tx in loaded_events
            )
            assert all(
                tx.vcs_project and tx.vcs_project_id == 1360
                for tx in loaded_events
            )

            memos = [tx.memo_value for tx in loaded_events]
            assert memos == [
                'donation',
                'offset 2022', 
                None,
                'q2 funding',
                'tree credits',
                'carbon offset',
                'early support',
                'offset tokens',
                'gift',
                'testing'
            ]

    def test_load_sink_txs_and_events(self, mock_http, mock_session):
        sink_loader.load_sinking_txs(cursor=999)
        event_loader.load_sink_events(cursor=999)

        with mock_session.begin() as session:
            loaded_transactions = session.scalars(
                select(SinkingTx).order_by(SinkingTx.paging_token.asc())
            ).all()
            assert len(loaded_transactions) == 30
            
            prev_tx = None
            cumulative_amount = Decimal(0)
            # Events and classic txs are interleaved in the DB
            for tx in loaded_transactions:
                if prev_tx:
                    # is the created_at time in accordance with the paging token?
                    assert tx.created_at >= prev_tx.created_at
                    # is each paging token unique?
                    assert tx.paging_token != prev_tx.paging_token

                prev_tx = tx
                cumulative_amount += tx.carbon_amount

            assert cumulative_amount == Decimal("27.614")
