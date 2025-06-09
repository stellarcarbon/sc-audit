import datetime as dt
from decimal import Decimal

import httpx
from httpx import Client, Response
import pytest

from sc_audit.sources.sink_events import get_sink_events
from tests.data_fixtures.events import query_response


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


class TestSinkEventSources:
    def test_events_list_full(self, mock_client):
        events = get_sink_events(cursor=0)
        assert len(events) == 10
        assert events[0].amount == Decimal("0.2")
        assert events[0].created_at == dt.datetime(2024, 6, 8, 18, 40, 2, tzinfo=dt.UTC)
        assert events[6].amount == Decimal("0.06")
        assert events[6].created_at == dt.datetime(2024, 6, 8, 19, 40, 0, tzinfo=dt.UTC)
        assert events[9].amount == Decimal("0.01")
        assert events[6].created_at == events[9].created_at
        assert events[6].ledger == events[9].ledger
