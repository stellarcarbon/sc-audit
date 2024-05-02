import datetime
import json as jsonlib

import httpx
from httpx import Client, Response
import pytest

from sc_audit.sources.retirements import format_verra_retirements, get_retirements_list
from tests.data_fixtures.retirements import search_response, retirements as retirements_fix


class MockClient(Client):
    def __init__(self, headers: dict) -> None:
        assert "user-agent" in headers
        super().__init__(headers=headers)

    def post(self, url: str, headers: dict, params: dict, json: dict, timeout: int) -> Response:
        assert "search" in url
        assert headers['accept'] == "application/json"
        assert "stellarcarbon" in params['$filter']

        result_str = search_response
        if "retireOrCancelDate" in params['$filter']:
            result_data = jsonlib.loads(result_str)
            result_data['totalCount'] = 3
            result_data['value'] = result_data['value'][8:]
            result_str = jsonlib.dumps(result_data)
        
        return Response(status_code=200, text=result_str)


@pytest.fixture
def mock_client(monkeypatch):
    monkeypatch.setattr(httpx, "Client", MockClient)


class TestRetirementSources:
    def test_format_retirements(self):
        retirements_data = format_verra_retirements(search_response)
        assert retirements_data['total_count'] == 11
        for i, retirement in enumerate(retirements_data['retirements']):
            assert int(retirement['certificate_id']) == retirements_fix[i].certificate_id

    def test_retirements_list_full(self, mock_client):
        retirements_data = get_retirements_list()
        assert retirements_data['total_count'] == 11
        assert len(retirements_data['retirements']) == 11

    def test_retirements_list_date(self, mock_client):
        date_filter = datetime.date(2023, 1, 1)
        retirements_data = get_retirements_list(from_date=date_filter)
        assert retirements_data['total_count'] == 3
        assert len(retirements_data['retirements']) == 3
        for retirement in retirements_data['retirements']:
            assert "2023" in retirement['retirement_date']


        
