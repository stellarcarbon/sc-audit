from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from sc_audit.db_schema.sink import SinkingTx
from sc_audit.loader import impact_projects
from sc_audit.loader import sink_invocations as invocation_loader
from sc_audit.loader import sinking_txs as sink_loader
from sc_audit.sources.sink_invocations import FlowBase, InvocationSource
from tests.db_fixtures import engine, new_session
from tests.data_fixtures import invocations
from tests.test_settings import patch_settings
from tests.test_sink import mock_http


@pytest.fixture
def patch_flow_db_engine(monkeypatch, patch_settings):
    patch_settings.MERCURY_KEY = ""
    patch_settings.OBSRVR_FLOW_DB_URI = engine.url
    monkeypatch.setattr(InvocationSource, 'engine', engine)


@pytest.fixture
def mock_invocations():
    FlowBase.metadata.create_all(engine)

    with Session(engine) as session:
        session.add_all(invocations.get_items())
        session.commit()

    yield

    FlowBase.metadata.drop_all(engine)



@pytest.mark.usefixtures("mock_invocations", "patch_flow_db_engine")
class TestSinkInvocationSource:
    def test_invoke_list_full(self):
        invokes = InvocationSource.get_sink_invocations(cursor=0)
        assert len(invokes) == 3
        one, two, tri = invokes

        assert all(
            inv.contract_id == "CAVS7HEUNFCMOW6DC7EBY7J6HNFJ5JJ7LV4H7RPUC6V5QO5OMS7AQLD5"
            for inv in invokes
        )
        assert all(
            inv.function_name == "sink_carbon"
            for inv in invokes
        )
        assert all(
            inv.invoking_account == "GAN4SL6DHOQO4POKWOUL4PPCIVJBSDX7SVOLL4GVM4CC27S6WCV7FQZL"
            for inv in invokes
        )
        assert all(
            inv.funder == "GAN4SL6DHOQO4POKWOUL4PPCIVJBSDX7SVOLL4GVM4CC27S6WCV7FQZL"
            for inv in invokes
        )
        assert all(
            inv.recipient == "GC53JCXZHW3SVNRE4CT6XFP46WX4ACFQU32P4PR3CU43OB7AKKMFXZ6Y"
            for inv in invokes
        )
        assert all(
            inv.project_id == "VCS1360"
            for inv in invokes
        )

        assert one.toid == 188328285796925850
        assert one.tx_hash == "2f55d7e30d801908fc72f5f11cbf44b264fca73f6386117ebc6274f356affa71"
        assert one.amount == 1000000
        assert one.ton_amount == Decimal("0.1")
        assert one.memo_text == "one"

        assert two.toid == 188915296156604069
        assert two.tx_hash == "1b2aed0644c8fab9abff84aee78e7f0b92b09a8cf9bd2c1a17e71964c768a805"
        assert two.amount == 3330000
        assert two.ton_amount == Decimal("0.333")
        assert two.memo_text == "two"

        assert tri.toid == 2209834166299873287
        assert tri.tx_hash == "e7d68ab7c57e38e2e103b81926db97731eb9ca861de5282eaf1bcc97e1605deb"
        assert tri.amount == 4444444
        assert tri.ton_amount == Decimal("0.444")
        assert tri.memo_text == "tri"

    def test_returns_the_same_when_repeated(self):
        res_1 = InvocationSource.get_sink_invocations(cursor=0)
        res_2 = InvocationSource.get_sink_invocations(cursor=0)
        res_3 = InvocationSource.get_sink_invocations(cursor=0)

        assert len(res_1) == len(res_2) == len(res_3) == 3
        assert res_1 == res_2 == res_3



@pytest.fixture
def mock_session(monkeypatch, new_session):
    monkeypatch.setattr(impact_projects, 'Session', new_session)
    monkeypatch.setattr(invocation_loader, 'Session', new_session)
    monkeypatch.setattr(sink_loader, 'Session', new_session)
    impact_projects.load_impact_projects()
    return new_session


@pytest.mark.usefixtures("mock_invocations", "patch_flow_db_engine")
class TestSinkInvocationLoader:
    def test_load_sink_invocations(self, mock_session):
        num_loaded = invocation_loader.load_sink_invocations(cursor=0)
        assert num_loaded == 3

        with mock_session.begin() as session:
            loaded_invocations = session.scalars(
                select(SinkingTx).order_by(SinkingTx.paging_token.asc())
                .options(joinedload(SinkingTx.vcs_project))
            ).all()

            assert all(
                tx.contract_id == "CAVS7HEUNFCMOW6DC7EBY7J6HNFJ5JJ7LV4H7RPUC6V5QO5OMS7AQLD5"
                for tx in loaded_invocations
            )
            assert all(
                tx.carbon_amount == tx.source_asset_amount == tx.dest_asset_amount
                for tx in loaded_invocations
            )
            assert all(
                "CARBON" == tx.source_asset_code == tx.dest_asset_code
                for tx in loaded_invocations
            )
            assert all(
                tx.vcs_project and tx.vcs_project_id == 1360
                for tx in loaded_invocations
            )

            memos = [tx.memo_value for tx in loaded_invocations]
            assert memos == ["one", "two", "tri"]

    def test_load_sink_txs_and_invocations(self, mock_http, mock_session):
        sink_loader.load_sinking_txs(cursor=999)
        invocation_loader.load_sink_invocations(cursor=999)

        with mock_session.begin() as session:
            loaded_transactions = session.scalars(
                select(SinkingTx).order_by(SinkingTx.paging_token.asc())
            ).all()
            assert len(loaded_transactions) == 23
            
            prev_tx = None
            cumulative_amount = Decimal(0)
            # Invocations and classic txs are interleaved in the DB
            for tx in loaded_transactions:
                if prev_tx:
                    # is the created_at time in accordance with the paging token?
                    assert tx.created_at >= prev_tx.created_at
                    # is each paging token unique?
                    assert tx.paging_token != prev_tx.paging_token

                prev_tx = tx
                cumulative_amount += tx.carbon_amount

            assert cumulative_amount == Decimal("27.175")
