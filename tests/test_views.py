import datetime as dt
from decimal import Decimal

import pandas as pd
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
        assert mbdf['created_at'].min() == pd.Timestamp('2021-11-20 13:06:51')
        assert mbdf['created_at'].max() == pd.Timestamp('2021-11-21 00:04:23')

    def test_inventory_until_2022_02_01(self, mock_session_with_associations):
        mbdf = inventory.view_inventory(until_date=dt.date(2022, 2, 1))
        assert len(mbdf) == 9
        assert mbdf['size'].sum() == 202
        assert mbdf['credits_remaining_on_date'].sum() == 201
        assert mbdf['created_at'].min() == pd.Timestamp('2021-11-20 13:06:51')
        assert mbdf['created_at'].max() == pd.Timestamp('2022-02-01 00:08:19')

    def test_inventory_until_2024_nonempty(self, mock_session_with_associations):
        mbdf = inventory.view_inventory(omit_empty=True, until_date=dt.date(2024, 1, 1))
        assert len(mbdf) == 7
        assert mbdf['size'].sum() == 200
        assert mbdf['credits_remaining_on_date'].sum() == 179
        assert mbdf['created_at'].min() == pd.Timestamp('2021-11-21 00:04:23')
        assert mbdf['created_at'].max() == pd.Timestamp('2022-02-01 00:08:19')


class TestConstructStxQuery:
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


class TestSinkStatusView:
    def test_sink_status_full(self, mock_session_with_associations):
        txdf = sink_status_view.view_sinking_txs()
        assert len(txdf) == 20
        assert txdf.carbon_amount.sum() == Decimal('26.298')
        assert txdf.vcs_project_id.min() == 1360
        assert txdf.vcs_project_id.max() == 1360

    def test_sink_status_for_recipient(self, mock_session_with_associations):
        txdf = sink_status_view.view_sinking_txs(
            for_recipient="GBIH7Z3SMZUX62JPLLDTHA3QEVMRCGUCUQVCFFRJTEGCKB4MV4NGU7BE",
            order='asc',
        )
        assert len(txdf) == 2
        assert txdf.carbon_amount.sum() == 2
        assert (
            list(txdf.hash.unique()) == [
                'c2f0ed42774091e1249f11af93d56be53af1aa24bc397d36f2fcbb0907475fb4', 
                '2827d90abd658986345f4c20cb68f1f29af128bccaa0d8743ce0248732a2b4fc'
            ]
        )

    def test_sink_status_from_date(self, mock_session_with_associations):
        txdf = sink_status_view.view_sinking_txs(
            for_recipient="GC53JCXZHW3SVNRE4CT6XFP46WX4ACFQU32P4PR3CU43OB7AKKMFXZ6Y",
            from_date=dt.date(2023, 5, 7)
        )
        assert len(txdf) == 4
        assert txdf.carbon_amount.sum() == Decimal('3.028')

    def test_sink_status_before_date(self, mock_session_with_associations):
        txdf = sink_status_view.view_sinking_txs(
            for_recipient="GC53JCXZHW3SVNRE4CT6XFP46WX4ACFQU32P4PR3CU43OB7AKKMFXZ6Y",
            before_date=dt.date(2023, 5, 7)
        )
        assert len(txdf) == 4
        assert txdf.carbon_amount.sum() == Decimal('6.972')

    def test_sink_status_finalized_true(self, mock_session_with_associations):
        txdf = sink_status_view.view_sinking_txs(finalized=True)
        assert len(txdf) == 18
        assert txdf.carbon_amount.sum() == 23
        assert all(txdf.statuses.astype(bool))

    def test_sink_status_finalized_false(self, mock_session_with_associations):
        txdf = sink_status_view.view_sinking_txs(finalized=False)
        assert len(txdf) == 2
        assert txdf.carbon_amount.sum() == Decimal('3.298')
        assert not any(txdf.statuses.astype(bool))

    def test_sink_status_pagination_asc(self, mock_session_with_associations):
        txdf = sink_status_view.view_sinking_txs(limit=2, order='asc')
        assert len(txdf) == 2
        pages = [txdf]
        while len(txdf) == 2:
            cursor = int(txdf.paging_token.iloc[-1])
            txdf = sink_status_view.view_sinking_txs(cursor=cursor, limit=2, order='asc')
            pages.append(txdf)

        combined_pages = pd.concat(pages)
        assert combined_pages.hash.is_unique
        assert len(combined_pages) == 20

    def test_sink_status_pagination_desc(self, mock_session_with_associations):
        txdf = sink_status_view.view_sinking_txs(limit=3, order='desc')
        assert len(txdf) == 3
        pages = [txdf]
        while len(txdf) == 3:
            cursor = int(txdf.paging_token.iloc[-1])
            txdf = sink_status_view.view_sinking_txs(cursor=cursor, limit=3, order='desc')
            pages.append(txdf)

        combined_pages = pd.concat(pages)
        assert combined_pages.hash.is_unique
        assert len(combined_pages) == 20


class TestGetByPk:
    def test_get_sinking_tx(self, mock_session_with_associations):
        stx = sink_status_view.get_sinking_tx(
            "61d4ff5516b7098bbc2219d244e7f29a039c32735e1c16d1c05d66a0739727d9"
        )
        assert stx and stx['paging_token'] == 164821723627237383


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
