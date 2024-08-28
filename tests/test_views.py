import datetime as dt
from decimal import Decimal

import pandas as pd
import pytest

from sc_audit.loader import minted_blocks, retirement_from_block
from sc_audit.loader import sinking_txs as sink_loader
from sc_audit.loader import sink_status as sink_status_loader
from sc_audit.views import inventory, retirement, sink_status as sink_status_view, stats
from tests.data_fixtures.retirements import get_retirements
from tests.db_fixtures import new_session
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

    def test_get_retirement(self, mock_session_with_associations):
        ret = retirement.get_retirement(143471)
        assert (
            ret and ret['serial_number'] == 
            "8040-449402275-449402275-VCU-042-MER-PE-14-1360-01072013-30062014-1"
        )
        assert ret['vcs_project']['id'] == 1360


class TestConstructRetQuery:
    def test_construct_query_unfiltered(self):
        retq = retirement.construct_retirement_query(
            for_beneficiary=None,
            from_date=None,
            before_date=None,
            project=None
        )
        assert "FROM retirements" in str(retq)
        assert "WHERE" not in str(retq)

    def test_construct_query_for_beneficiary(self):
        retq = retirement.construct_retirement_query(
            for_beneficiary="beneficiary-address",
            from_date=None,
            before_date=None,
            project=None
        )
        assert "WHERE (retirements.retirement_beneficiary LIKE" in str(retq)

    def test_construct_query_from_date(self):
        retq = retirement.construct_retirement_query(
            for_beneficiary=None,
            from_date=dt.date(2023, 1, 1),
            before_date=None,
            project=None
        )
        assert "WHERE retirements.retirement_date >=" in str(retq)

    def test_construct_query_before_date(self) -> None:
        retq = retirement.construct_retirement_query(
            for_beneficiary=None,
            from_date=None,
            before_date=dt.date(2023, 1, 1),
            project=None
        )
        assert "WHERE retirements.retirement_date <" in str(retq)

    def test_construct_query_project(self):
        retq = retirement.construct_retirement_query(
            for_beneficiary=None,
            from_date=None,
            before_date=None,
            project=999
        )
        assert "WHERE retirements.vcs_project_id" in str(retq)


class TestRetirementView:
    def test_retirements_full(self, mock_session_with_associations):
        rtdf = retirement.view_retirements()
        assert len(rtdf) == 11
        assert rtdf.vcu_amount.sum() == 23
        assert rtdf.vcs_project_id.min() == 1360
        assert rtdf.vcs_project_id.max() == 1360

    def test_retirements_for_beneficiary(self, mock_session_with_associations):
        rtdf = retirement.view_retirements(
            for_beneficiary="GBIH7Z3SMZUX62JPLLDTHA3QEVMRCGUCUQVCFFRJTEGCKB4MV4NGU7BE",
            order='asc',
        )
        assert len(rtdf) == 2
        assert rtdf.vcu_amount.sum() == 2
        assert list(rtdf.certificate_id.unique()) == [187117, 187118]

    def test_retirements_from_date(self, mock_session_with_associations):
        rtdf = retirement.view_retirements(
            for_beneficiary="GC53JCXZHW3SVNRE4CT6XFP46WX4ACFQU32P4PR3CU43OB7AKKMFXZ6Y",
            from_date=dt.date(2023, 5, 7)
        )
        assert len(rtdf) == 1
        assert rtdf.certificate_id.item() == 188439

    def test_retirements_before_date(self, mock_session_with_associations):
        rtdf = retirement.view_retirements(
            for_beneficiary="GC53JCXZHW3SVNRE4CT6XFP46WX4ACFQU32P4PR3CU43OB7AKKMFXZ6Y",
            before_date=dt.date(2023, 5, 7)
        )
        assert len(rtdf) == 1
        assert rtdf.certificate_id.item() == 152309

    def test_retirements_of_project(self, mock_session_with_associations):
        rtdf = retirement.view_retirements(project=67)
        assert len(rtdf) == 0

    def test_retirements_pagination_asc(self, mock_session_with_associations):
        rtdf = retirement.view_retirements(limit=2, order='asc')
        assert len(rtdf) == 2
        pages = [rtdf]
        while len(rtdf) == 2:
            cursor = int(rtdf.certificate_id.iloc[-1])
            rtdf = retirement.view_retirements(cursor=cursor, limit=2, order='asc')
            pages.append(rtdf)

        combined_pages = pd.concat(pages)
        assert combined_pages.certificate_id.is_unique
        assert len(combined_pages) == 11

    def test_retirements_pagination_desc(self, mock_session_with_associations):
        rtdf = retirement.view_retirements(limit=3, order='desc')
        assert len(rtdf) == 3
        pages = [rtdf]
        while len(rtdf) == 3:
            cursor = int(rtdf.certificate_id.iloc[-1])
            rtdf = retirement.view_retirements(cursor=cursor, limit=3, order='desc')
            pages.append(rtdf)

        combined_pages = pd.concat(pages)
        assert combined_pages.certificate_id.is_unique
        assert len(combined_pages) == 11


class TestStatsView:
    def test_stats_global(self, mock_session_with_associations):
        carbon_stats = stats.get_carbon_stats()
        assert carbon_stats["carbon_sunk"] == Decimal('26.298')
        assert carbon_stats["carbon_retired"] == Decimal('23.000')
        assert carbon_stats["carbon_pending"] == Decimal('3.298')
        assert carbon_stats["carbon_stored"] == Decimal('202.000')

    def test_stats_recipient(self, mock_session_with_associations):
        r1_stats = stats.get_carbon_stats(
            recipient="GAXLLGNPEMRUMSLHO3QLYDWZCNPQMBDCWYNLVDPR32ABYWDWQO6YXHSL"
        )
        assert r1_stats["carbon_sunk"] == Decimal('3.015')
        assert r1_stats["carbon_retired"] == Decimal('0')
        assert r1_stats["carbon_pending"] == Decimal('3.015')
        assert "carbon_stored" not in r1_stats

        r2_stats = stats.get_carbon_stats(
            recipient="GC53JCXZHW3SVNRE4CT6XFP46WX4ACFQU32P4PR3CU43OB7AKKMFXZ6Y"
        )
        assert r2_stats["carbon_sunk"] == Decimal('10')
        assert r2_stats["carbon_retired"] == Decimal('10')
        assert r2_stats["carbon_pending"] == Decimal('0')
        assert "carbon_stored" not in r2_stats


@pytest.fixture
def mock_session(monkeypatch, new_session):
    monkeypatch.setattr(minted_blocks, 'Session', new_session)
    monkeypatch.setattr(retirement_from_block, 'Session', new_session)
    monkeypatch.setattr(sink_loader, 'Session', new_session)
    monkeypatch.setattr(sink_status_loader, 'Session', new_session)
    monkeypatch.setattr(inventory, 'Session', new_session)
    monkeypatch.setattr(sink_status_view, 'Session', new_session)
    monkeypatch.setattr(retirement, 'Session', new_session)
    monkeypatch.setattr(stats, 'Session', new_session)
    return new_session

@pytest.fixture
def mock_session_with_associations(mock_mint_http, mock_sink_http, mock_session):
    with mock_session.begin() as session:
        session.add_all(get_retirements())

    minted_blocks.load_minted_blocks()
    sink_loader.load_sinking_txs(cursor=999)
    retirement_from_block.load_retirement_from_block()
    sink_status_loader.load_sink_statuses()
    return mock_session
