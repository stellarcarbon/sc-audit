import datetime as dt
from typing import final

from pandas import Timestamp
import pytest

from sc_audit.loader import minted_blocks, retirement_from_block
from sc_audit.loader import sinking_txs as sink_loader
from sc_audit.loader import sink_status as sink_status_loader
from sc_audit.views import inventory, sink_status as sink_status_view
from tests.data_fixtures.retirements import get_retirements
from tests.db_fixtures import new_session, vcs_project
from tests.test_mint import mock_http as mock_mint_http
from tests.test_sink import mock_http as mock_sink_http


class TestInventoryView:
    def test_inventory_full(self, mock_session_with_associations):
        mbdf = inventory.view_inventory()
        assert len(mbdf) == 9
        assert mbdf['size'].sum() == 202
        assert mbdf['credits_remaining'].sum() == 179
        assert mbdf['vcs_project_id'].min() == 1360
        assert mbdf['vcs_project_id'].max() == 1360

    def test_inventory_nonempty(self, mock_session_with_associations):
        mbdf = inventory.view_inventory(omit_empty=True)
        assert len(mbdf) == 7
        assert mbdf['size'].sum() == 200
        assert mbdf['credits_remaining'].sum() == 179

    def test_inventory_until_2022_01_31(self, mock_session_with_associations):
        mbdf = inventory.view_inventory(until_date=dt.date(2022, 1, 31))
        assert len(mbdf) == 3
        assert mbdf['size'].sum() == 26
        assert mbdf['credits_remaining_on_date'].sum() == 25
        assert mbdf['created_at'].min() == Timestamp('2021-11-20 13:06:51')
        assert mbdf['created_at'].max() == Timestamp('2021-11-21 00:04:23')

    def test_inventory_until_2022_02_01(self, mock_session_with_associations):
        mbdf = inventory.view_inventory(until_date=dt.date(2022, 2, 1))
        assert len(mbdf) == 9
        assert mbdf['size'].sum() == 202
        assert mbdf['credits_remaining_on_date'].sum() == 201
        assert mbdf['created_at'].min() == Timestamp('2021-11-20 13:06:51')
        assert mbdf['created_at'].max() == Timestamp('2022-02-01 00:08:19')

    def test_inventory_until_2024_nonempty(self, mock_session_with_associations):
        mbdf = inventory.view_inventory(omit_empty=True, until_date=dt.date(2024, 1, 1))
        assert len(mbdf) == 7
        assert mbdf['size'].sum() == 200
        assert mbdf['credits_remaining_on_date'].sum() == 179
        assert mbdf['created_at'].min() == Timestamp('2021-11-21 00:04:23')
        assert mbdf['created_at'].max() == Timestamp('2022-02-01 00:08:19')


class TestSinkStatusView:
    def test_construct_query_unfiltered(self):
        stxq = sink_status_view.construct_stx_query(
            for_funder=None,
            for_recipient=None,
            from_date=None,
            before_date=None,
            finalized=None
        )
        assert (
            "FROM sinking_txs LEFT OUTER JOIN sink_status ON sinking_txs.hash = sink_status.sinking_tx_hash"
            in str(stxq)
        )
        assert "WHERE" not in str(stxq)

    def test_construct_query_for_funder(self):
        stxq = sink_status_view.construct_stx_query(
            for_funder="funder-address",
            for_recipient=None,
            from_date=None,
            before_date=None,
            finalized=None
        )
        assert "WHERE sinking_txs.funder" in str(stxq)

    def test_construct_query_for_recipient(self):
        stxq = sink_status_view.construct_stx_query(
            for_funder=None,
            for_recipient="recipient-address",
            from_date=None,
            before_date=None,
            finalized=None
        )
        assert "WHERE sinking_txs.recipient" in str(stxq)

    def test_construct_query_from_date(self):
        stxq = sink_status_view.construct_stx_query(
            for_funder=None,
            for_recipient=None,
            from_date=dt.date(2023, 1, 1),
            before_date=None,
            finalized=None
        )
        assert "WHERE sinking_txs.created_at >=" in str(stxq)

    def test_construct_query_before_date(self):
        stxq = sink_status_view.construct_stx_query(
            for_funder=None,
            for_recipient=None,
            from_date=None,
            before_date=dt.date(2023, 1, 1),
            finalized=None
        )
        assert "WHERE sinking_txs.created_at <" in str(stxq)

    def test_construct_query_finalized(self):
        stxq = sink_status_view.construct_stx_query(
            for_funder=None,
            for_recipient=None,
            from_date=None,
            before_date=None,
            finalized=True
        )
        assert "WHERE sink_status.finalized = true" in str(stxq)

        stxq = sink_status_view.construct_stx_query(
            for_funder=None,
            for_recipient=None,
            from_date=None,
            before_date=None,
            finalized=False
        )
        assert "WHERE sink_status.finalized IS NULL OR sink_status.finalized = false" in str(stxq)


@pytest.fixture
def mock_session(monkeypatch, new_session):
    monkeypatch.setattr(minted_blocks, 'Session', new_session)
    monkeypatch.setattr(retirement_from_block, 'Session', new_session)
    monkeypatch.setattr(sink_loader, 'Session', new_session)
    monkeypatch.setattr(sink_status_loader, 'Session', new_session)
    monkeypatch.setattr(inventory, 'Session', new_session)
    monkeypatch.setattr(sink_status_view, 'Session', new_session)
    return new_session

@pytest.fixture
def mock_session_with_associations(mock_mint_http, mock_sink_http, mock_session, vcs_project):
    with mock_session.begin() as session:
        session.add(vcs_project)
        session.add_all(get_retirements())

    minted_blocks.load_minted_blocks()
    sink_loader.load_sinking_txs(cursor=999)
    retirement_from_block.load_retirement_from_block()
    sink_status_loader.load_sink_statuses()
    return mock_session
